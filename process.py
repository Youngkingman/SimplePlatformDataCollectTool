import time
import xlrd
import xlwt
from xlutils.copy import copy
from PlatFormAPI import PlatFormAPI

class xlsProcess(object):
    def __init__(self, cookies, googleAuth, xls_input, xls_output, try_count, time_out):
        # 类字段初始化
        self.cookies = cookies
        self.googleAuth = googleAuth
        self.xls_input = xls_input
        self.xls_output = xls_output
        self.try_count = try_count
        self.time_out = time_out
        self.api = PlatFormAPI(self.cookies, self.googleAuth, self.try_count, self.time_out)

    def xlsReadProcess(self):
        xls = xlrd.open_workbook(filename=self.xls_input)
        sheet = xls.sheet_by_index(0)

        i = 0
        allVideo = []
        while i < sheet.nrows:
            url = sheet.row(i)[0].value
            print("------------正在解析第", i + 1, "行的数据-----------------")
            code, platform, VideoId, redirect_url = self.api.UrlToPlatformAndVedioId(url)
            if code < 0:
                if code == -1:
                    print("解析失败, 配置为空, 请检查")
                elif code == -2:
                    print("解析失败, 尝试重定向失败, url为", url)
                elif code == -3:
                    print("解析失败, 重定向后配置不合法, url为", redirect_url)
                elif code == -4:
                    print("解析失败, 截取Id失败, url为", redirect_url)
            else:
                print("解析成功", platform, VideoId)
            allVideo.append([url, code, redirect_url, platform, VideoId])
            i += 1
            time.sleep(2)
        print("excel表数据解析完毕")
        # 释放资源
        xls.release_resources()
        del xls
        return allVideo

    def xlsWriteProcess(self):
        # 获取excel文件, 爬虫处理
        allVideos = self.xlsReadProcess()
        # 输出文件初始化
        xls = xlwt.Workbook(encoding='utf-8')
        sheet = xls.add_sheet('视频爬虫')
        sheet.write(0, 0, '原链接')
        sheet.write(0, 1, '重定向后链接')
        sheet.write(0, 2, '播放')
        sheet.write(0, 3, '点赞')
        i = 1
        while i < len(allVideos) + 1:
            url = allVideos[i - 1][0]
            code = allVideos[i - 1][1]
            redirect_url = allVideos[i - 1][2]
            PlatForm = allVideos[i - 1][3]
            VideoId = allVideos[i - 1][4]
            if code == 0:
                print("------------正在爬取第", i + 1, "行的视频信息-----------------")
                try:
                    LikeCount, PlayCount = self.api.getCommonInfo(PlatForm, VideoId)
                    sheet.write(i, 0, url)
                    sheet.write(i, 1, redirect_url)
                    sheet.write(i, 2, PlayCount)
                    sheet.write(i, 3, LikeCount)
                    print("写入成功")
                    time.sleep(2)
                except:
                    print("爬取视频信息失败, url为", redirect_url, "可能是网络问题导致无法访问")
                    sheet.write(i, 0, url)
                    sheet.write(i, 1, redirect_url)
                    time.sleep(2)
            else:
                sheet.write(i, 0, url)
            i += 1
        try:
            xls.save(self.xls_output)
            del xls
        except:
            print("没有获取到输出文件的权限, 检查一下是不是打开了文件")

        print("查询完成")
