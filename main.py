import logging
import os
import datetime
from config.logger import logger
from config.config import dir_vcodes
from config.config import dir_logs
from config.config import dir_tem
from PIL import Image
import copy
import tesserocr
import re

def initLogger():
    if not os.path.exists(dir_logs):
        os.mkdir(dir_logs)
    handler1 = logging.FileHandler(dir_logs + "/" + str(datetime.date.today()) + ".log",mode = "a",encoding = "utf8")
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

def imagePreDeal1(im):
    size = im.size
    pixels = im.load()
    for i in range(size[0]):
        for j in range(size[1]):
            if pixels[i,j] > 0:
                pixels[i,j] = 255

def imagePreDealTest(im,vcode,length,min_gray_value,min_total):
    logger.info("{} 开始预处理，length = {} min_gray_value = {} min_total = {}".format(vcode,length,min_gray_value,min_total))
    imagePreDeal(im,length,min_gray_value,min_total)
    # imagePreDeal1(im)

    dir_tem_pre = dir_tem + "/" + str(length) + "_" + str(min_gray_value) + "_" + str(min_total)
    if not os.path.exists(dir_tem_pre):
        os.mkdir(dir_tem_pre)
    im.save(dir_tem_pre + "/" + vcode)
    logger.info("{} 预处理完成，处理结果保存在 {}".format(vcode,dir_tem_pre + "/" + vcode))

if __name__ == "__main__":
    initLogger()
    logger.info("----顺丰快递验证码识别程序启动----")
    listdir = os.listdir(dir_vcodes)
    count_correct = 0
    for vcode in listdir:
        im = Image.open(dir_vcodes + "/" + vcode)
        im = im.convert("L")

        # length = 2
        # min_gray_value = 10
        # min_total = 19
        # for length in range(1,5):
        #     for min_total in range((2 * length + 1) ** 2 // 2,(2 * length + 1) ** 2):
        #         im_copy = copy.deepcopy(im)
        #         imagePreDealTest(im_copy,vcode,length,min_gray_value,min_total)

        length = 2
        min_gray_value = 70
        min_total = 19
        imagePreDealTest(im,vcode,length,min_gray_value,min_total)
        result = tesserocr.image_to_text(im)

        trueAnswer = vcode.split(".")[0]
        regular = re.compile("""\s""")
        result = regular.sub("",result,0)
        if trueAnswer == result:
            logger.info("{} 识别结果：{}  |正确".format(vcode,result))
            count_correct += 1
        else:
            logger.error("{} 识别结果：{}  |错误".format(vcode,result))
    logger.info("length = {} min_gray_value = {} min_total = {} 总数：{} 正确数：{} 正确率：{}".format(length,min_gray_value,min_total,len(listdir),count_correct,count_correct/len(listdir)))
    logger.info("----顺丰快递验证码识别程序结束----")