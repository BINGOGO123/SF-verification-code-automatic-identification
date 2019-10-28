# -*- coding:utf-8 -*-
# author:臧海彬
# function:负责从顺丰快递下载指定参数信息并入库和生成文件

from config.logger import logger
import requests
import time
import datetime
from modules.tools import getName
import os
from PIL import Image

class Downloader:
    # 指定downloader类常量
    __headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    def __code(self):
        return "https://www.sf-express.com/sf-service-owf-web/service/captcha/sms?force=true&time={}".format(int(time.time()*1000))

    # 初始化
    def __init__(self):
        logger.info("初始化Downloader对象")
        self.s = requests.session()
        self.s.headers.update(self.__headers)
        logger.info("初始化Downloader对象结束")
    
    # 下载验证码
    def getVerificationCode(self,path,count):
        logger.info("开始下载验证码，path = {}，count = {}".format(path,count))
        # 验证码认证
        for i in range(count):
            logger.info("-- i = {} count = {} --".format(i + 1,count))
            try:
                r = self.s.get(self.__code())
                r.raise_for_status()
            except:
                logger.exception("获取验证码出现错误，退出")
                return
            # 保存验证码
            if not os.path.exists(path):
                logger.info("{} 目录不存在，创建之".format(path))
                os.mkdir(path)
            verificationCodeName = getName(path + "/" + str(datetime.date.today()) + ".png")
            f = open(verificationCodeName,"wb")
            f.write(r.content)
            f.close()
            logger.info("验证码保存在 {} 中".format(verificationCodeName))
        logger.info("验证码下载完毕，path = {}，count = {}".format(path,count))