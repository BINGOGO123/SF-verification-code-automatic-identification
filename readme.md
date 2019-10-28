## 顺丰快递登录验证码自动识别
> 由于之前顺丰快递信息爬取时登录不能自动识别验证码，依然要眼动输入，所以这里打算解决一下

这里主要解决的是验证码后面有一团黑色像素环绕的问题，如下图：

![image](https://github.com/BINGOGO123/SF-verification-code-automatic-identification/blob/master/vcodes/4px5a.png)

## 解决思路

通过PIL库进行处理，将图片后面的黑色部分抹掉，然后直接用tesserocr进行识别

## 实际效果

这里尝试了多种方式进行预处理，但是都没有达到很好的效果。

最后使用的是判断周围一定范围内色块数目的方式，总量达到一定数量则保留该像素为黑色快，经过不停的参数调整后该方式处理后的图片如下：
> 所有预处理结果图片都在 /tem 目录下

![image](https://github.com/BINGOGO123/SF-verification-code-automatic-identification/blob/master/tem/1_10_8/4px5a.png)

![image](https://github.com/BINGOGO123/SF-verification-code-automatic-identification/blob/master/tem/1_30_9/4px5a.png)

![image](https://github.com/BINGOGO123/SF-verification-code-automatic-identification/blob/master/tem/2_10_19/4px5a.png)

![image](https://github.com/BINGOGO123/SF-verification-code-automatic-identification/blob/master/tem/2_70_19/4px5a.png)

处理后的图片通过人眼观察已经基本去除了后面的黑色色块，但是在数字的边缘部分多出来的黑色块很难判定它是不是数字自身的一部分

最后的识别率也只有64%多一点

## 文件说明
```
home
│   readme.md
│   main.py -- 验证码识别主函数   
│   download.py -- 验证码下载主函数   
│
└───config
│   │   config.py -- 存放各项参数
|   |   logger.py -- 公共日志类
|
└───downloader
|   |   downloader.py -- 爬虫下载验证码类
|
└───modules
|   |   tools.py -- 一些工具函数
|
└───logs
|   │   main.2019-10-25.log -- main日志文件，命名方式为：main.日期.log
|   │   download.2019-10-25.log -- download日志文件，命名方式为：download.日期.log
|
└───vcodes
|   │   4px5a.png -- 验证码图片，名称为其正确内容
|   |   ...
|
└───pre_deal
|   └───imagePreDeal(2, 70, 19) -- 预处理函数，内存有通过该处理方式处理过的验证码图片
|   |   |   result.txt -- 该方式下各个验证码识别结果
|   |   |   4px5a.png
|   |   |   ...
|   |   └───imagePreDeal(1, 10, 4) -- 预处理函数，按照此格式递归下去
|   |   |   |   ...
|   |   |
|   |   └───...
|   |
|   └───...
|
└───unmarked
    |   2019-10-28_1.png -- 未标记的验证码，命名方式：date_num.log
    |   ...
```

## 代码执行
执行验证码自动识别
```python
python main.py
```

从顺丰官网下载验证码
```python
python download.py
```