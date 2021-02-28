# CTGU课表导出

原来查看课程一直是用的是超级课程表，但现在越来越多的广告，一些莫名其妙的功能，实在忍受不了了遂去找一些所谓的的破解版，发现好多都不能使用。也可能是三峡大学名气太小，市场上的一些其他课程表都不支持三峡大学的课表导出。所以原来一直用手机自带的日历手动导入课表，不过手动导入难免会出现错误，并且还挺麻烦的，所以就写了这个程序来偷偷懒​，:laughing:。

## 一、开始使用

```shell
# username为学号，password为教务处密码，shool_year为学年，term为学期1表示春季学期，3表示秋季学期
python3 main.py -u <username> -p <password> -y <shool_year> -t <term>
```

在程序运行完成后会在程序目录出现一个t.ics的文件，把这个文件发送给手机，用手机自带的日历打开即可导入课表信息。在导入之后课表的配色可以手动修改一些，这样看上去可能更好看一些。

苹果可以将ICS文件内容复制到https://www.qrcode-monkey.com/上，生成一个二维码通过自带的相机扫一扫就可以了。

## 二、示例

- Samsung手机导入效果
<img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/img1.jpg">
<img src="https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/img2.jpg">

- Windows10导入效果

  ![image-20210221191624038](https://dongliu-1301367244.cos.ap-shanghai.myqcloud.com/img/image-20210221191624038.png)

## 三、ISC文件格式解析

ICS文件格式可以参考这两篇文章[日历标准格式](https://cloud.tencent.com/developer/article/1655829)，[日历标准格式研究](https://gist.github.com/yulanggong/be953ffee1d42df53a1a),这两篇写的非常详细，我这里就不累述了。

## 四、项目文件结构

- ics.py

  ISC类，用于构建与写入ISC文件。

- jwc_login.py

  用于处理导入教务处的一些操作

- jwc_schedule.py

  用于获取课表消息

- time_calculation.py

  对课表信息进行解析、时间计算。

- main.py

  主程序，用于获取用户输入。

- cookies \

  用于存储cookies

