# -*- coding:utf-8 -*-
# author:臧海彬
# function:验证码识别主函数

import logging
import os
import datetime
from config.logger import logger
from config.config import dir_vcodes
from config.config import dir_logs
from config.config import dir_cache
from PIL import Image
import copy
# import tesserocr
import pytesseract
import re

####################################################
# function: 初始化日志对象
####################################################
def initLogger():
    if not os.path.exists(dir_logs):
        os.mkdir(dir_logs)
    handler1 = logging.FileHandler(dir_logs + "/" + "main." + str(datetime.date.today()) + ".log",mode = "a",encoding = "utf8")
    handler2 = logging.StreamHandler()
    formatter1 = logging.Formatter(fmt="%(asctime)s [%(levelname)s] [%(lineno)d] >> %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    formatter2 = logging.Formatter(fmt = "[%(levelname)s] >> %(message)s")
    handler1.setFormatter(formatter1)
    handler2.setFormatter(formatter2)
    logger.setLevel(logging.INFO)
    handler1.setLevel(logging.INFO)
    handler2.setLevel(logging.INFO)
    logger.addHandler(handler1)
    logger.addHandler(handler2)

####################################################
# function: 对im进行预处理的函数
# im: PIL.Image对象
# length,min_gray_value,min_total: 各项参数
####################################################
def imagePreDeal(im,length,min_gray_value,min_total):
    size = im.size
    matrix = [[0 for y in range(size[1])] for x in range(size[0])]
    pixels = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if pixels[i,j] <= min_gray_value:
                for x in range(i - length,i + length + 1):
                    for y in range(j - length,j + length + 1):
                        if x > 0 and x < size[0] and y > 0 and y < size[1]:
                            matrix[x][y]+=1
                            
    for i in range(size[0]):
        for j in range(size[1]):
            if matrix[i][j] >= min_total and pixels[i,j] <= min_gray_value:
                pixels[i,j] = 0
            else:
                pixels[i,j] = 255

####################################################
# function: 对im进行预处理的函数
# im: PIL.Image对象
####################################################
def imagePreDeal1(im):
    size = im.size
    pixels = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if pixels[i,j] > 0:
                pixels[i,j] = 255

####################################################
# function: 对im验证码进行预处理，并将处理后的图片保存
# im: PIL.Image对象
# vcode: 验证码名称
# preDealFunction: 指定预处理函数
# cacheDir: 预处理后图片存储位置
# preDealArgs: 传给preDealFunction函数的参数
# return: 保存图片的路径
####################################################
def imagePreDealProcess(im,vcode,preDealFunction,cacheDir,*preDealArgs):
    logger.info("{} 开始预处理，preDealFunction = {} preDealArgs = {}".format(vcode,[x.__name__ for x in preDealFunction],preDealArgs))

    # 对图片进行预处理，可以通过多个预处理方式进行处理，也可单独一个
    if type(preDealFunction) == list:
        # 每次处理后都保存处理后的图片
        for i in range(len(preDealFunction)):
            preDealFunction[i](im,*preDealArgs[i])
            dir_tem_pre = cacheDir + "/" + preDealFunction[i].__name__ + str(preDealArgs[i])
            if not os.path.exists(dir_tem_pre):
                os.mkdir(dir_tem_pre)
            im.save(dir_tem_pre + "/" + vcode)
            cacheDir = dir_tem_pre
    else:
        preDealFunction(im,*preDealArgs)
        dir_tem_pre = cacheDir + "/" + preDealFunction.__name__ + str(preDealArgs)
        if not os.path.exists(dir_tem_pre):
            os.mkdir(dir_tem_pre)
        im.save(dir_tem_pre + "/" + vcode)

    im.save(dir_tem_pre + "/" + vcode)
    logger.info("{} 预处理完成，处理结果保存在 {}".format(vcode,dir_tem_pre + "/" + vcode))
    return dir_tem_pre

####################################################
# function: 对指定文件夹下的图片验证码进行识别
# listDir: 验证码文件图片列表
# sourceDir: 验证码图片所在的文件夹
# cacheDir: 预处理图片存放的文件夹
# preDealFunction: 预处理方法
# preDealArgs: 传给preDealFunction函数的参数
# return: 识别正确率
####################################################
def imageRecognition(sourceDir,cacheDir,preDealFunction,*preDealArgs):
    listDir = os.listdir(sourceDir)
    count_correct = 0
    for vcode in listDir:
        # 打开图片并转为灰度图片
        im = Image.open(sourceDir + "/" + vcode)
        im = im.convert("L")

        resultDir = imagePreDealProcess(im,vcode,preDealFunction,cacheDir,*preDealArgs)
        result = pytesseract.image_to_string(im,"eng")
        # 往resultDir中写入识别结果
        if "f" not in locals() and "f" not in globals():
            f = open(resultDir + "/result.txt",mode = "a")

        # 判断结果正确性
        trueAnswer = vcode.split(".")[0]
        regular = re.compile("""\s""")
        result = regular.sub("",result,0)
        if trueAnswer == result:
            logger.info("{} 识别结果：{}  |正确".format(vcode,result))
            f.write(trueAnswer + " " + result + " 1\n")
            count_correct += 1
        else:
            logger.error("{} 识别结果：{}  |错误".format(vcode,result))
            f.write(trueAnswer + " " + result + " 0\n")


    # 关闭文件句柄
    if "f" in locals() or "f" in globals():
        f.close()

    return len(listDir),count_correct

if __name__ == "__main__":
    initLogger()
    logger.info("----顺丰快递验证码识别程序启动----")

    # 指定预处理方法
    preDealFunction = [imagePreDeal,imagePreDeal]
    preDealArgs = [(2,150,18),(1,10,5)]

    # 通过指定预处理方法进行识别
    result = imageRecognition(dir_vcodes,dir_cache,preDealFunction,*preDealArgs)
    logger.info("验证码总数：{} 正确识别数：{} 识别正确率：{}".format(result[0],result[1],result[1]/result[0]))
    logger.info("----顺丰快递验证码识别程序结束----")