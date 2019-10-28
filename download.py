# -*- coding:utf-8 -*-
# author:臧海彬
# function:负责从顺丰快递下载验证码

import logging
import os
import datetime
from config.logger import logger
from config.config import dir_logs
from config.config import dir_unmarked
from downloader.downloader import Downloader


def initLogger():
    if not os.path.exists(dir_logs):
        os.mkdir(dir_logs)
    handler1 = logging.FileHandler(dir_logs + "/" + "download." + str(datetime.date.today()) + ".log",mode = "a",encoding = "utf8")
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

if __name__ == "__main__":
    initLogger()
    logger.info("----顺丰快递验证码下载程序启动----")
    downloader = Downloader()
    num = int(input("请输入下载的验证码数量：\n"))
    logger.info("下载验证码数量：{}".format(num))
    downloader.getVerificationCode(dir_unmarked,num)
    logger.info("----顺丰快递验证码下载程序结束----")