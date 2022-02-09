# 视频爬虫脚本使用方法

*author: Chenzy* 2021.12.09

文档内容基本源于Github issue和Stackoverflow相关问题, 请严格遵循以下的配置进行操作，每一步均有设置方式的注释, 保姆级教程了属于是。

## 脚本运行环境

Python 3.8.8 Windows10

最好遵循这个环境配置，开发过程中尝试过用Python 3.10的版本, 出现各种问题

Windows下的IDE: PyCharm

## PyCharm破解安装

安装文件和破解插件已经准备好

![](.\img\1.png)

安装破解方法去公众号(名字：程序员的一天)，照着教程一步一步装

## Git安装

对着安装包一顿装就完事

完事后win+R打开运行输入cmd, 键入git有如图所示的东西就行了

![](.\img\3.png)

## Python 3.8.8安装

对着安装包安装就完事，注意勾选加到系统环境的这个选项

图示的是python 3.10.0，是因为我懒得卸掉重装，python 3.8.8是一样的

![](.\img\4.png)

完事后win+R打开运行输入cmd, 键入python有如图所示的东西就行了

![](.\img\5.png)

## 打开项目代码

打开pycharm，open找到项目代码所在文件夹，打开

先检查python的解析器是否正确

![](.\img\6.png)

正确的解析器界面：

![](.\img\7.png)

## 安装python包

在pycharm界面alt + F12

![](.\img\8.png)

键入以下python库

- `pip install xlrd==1.2.0`
- `pip install xlutils`
- `pip install xlwt`
- `pip install yapi`
- `pip install urllib3==1.25.11`
- `pip install requests`

拉取TikTokAPI开源项目

```bash
git clone https://github.com/avilash/TikTokAPI-Python.git
cd TikTokAPI-Python
python setup.py install
```

至此环境基本是搞定了

## youtubeAPI的googleAuth配置

项目使用了谷歌提供的免费API YouTube V3，使用前需要在谷歌云平台获取一个凭据，可以在[这里](https://console.cloud.google.com/apis/api/youtube/overview)注册自己的项目。

如下图所示搜索youtube Data V3, 启用API

![](.\img\9.png)

回到上图所示界面，找到凭据码

![](.\img\10.png)

粘贴在cookies.json的googleAuth字段中

![](.\img\11.png)

## tiktokAPI的cookies配置

首先打开谷歌浏览器，打开[tiktok官网](https://www.tiktok.com/)

![](.\img\12.png)

找到图中的cookies并单击

![](.\img\13.png)

在tiktok.com/Cookie表项下找到ttwid的内容，复制出来

![](.\img\14.png)

同样在www.tiktok.com/Cookie表项下找到s_v_web_id，复制出来

![](.\img\15.png)

![](.\img\16.png)

粘贴在cookies.json配置文件的对应位置

![](.\img\17.png)

## 输入文件和输出文件配置

在cookies.json配置文件对应位置处进行修改，如果要放在别的位置，要输入绝对路径

如果跟我一样这样输入的话，文件的位置应该置于项目文件夹的位置，可以理解为跟main.py文件在同个地方

![](.\img\18.png)

## 爬虫脚本注意事项

- 出现“截取Id失败”相关的bug，反馈给我，连带着url一起
- 出现“重定向失败”的报错，是正常的，有些链接确实是连不上
- 出现“网络问题无法访问”的报错，也是正常的，虽然重定向成功了，但是使用api获取视频信息时需要考虑到超时时间，超时时间内未返回结果则抛出此报错（绝大部分都是tiktok的报错，属实垃圾）
- 出现“远程主机强迫关掉连接”的报错，这也是正常的，应该是不会影响到脚本继续跑，爬虫脚本被视为攻击脚本，所以访问的服务器自我保护关掉连接，这个是我解决不了的问题
- 上述的问题都会导致那条视频链接被放弃，不要问我为什么你输入多少条，输出少了
- 建议xls_input最好是用xls格式，xlrd库对xlsx库的支持有限
- 输出文件及时拿走，我没试过留在那里会怎么样，应该是会被覆盖掉