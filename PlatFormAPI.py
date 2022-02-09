from platform import platform
import yapi
import requests
import re
from TikTokAPI import TikTokAPI
from urllib.parse import urlparse

class PlatFormAPI(object):
    def __init__(self, cookies, googleAuth, try_count, time_out):
        self.cookies = cookies
        self.googleAuth = googleAuth
        self.try_count = try_count
        self.time_out = time_out
        self.headers = headers = {
            'User-Agent' : 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 96.0.4664.45 Safari / 537.36'
        }
        self.driveConfig = {
            'youtube': self.getYtbLikeAndPlay,
            'tiktok' : self.getTikLikeAndPlay,
        }
        #正则表达式相关初始化
        self.redirec_pattern = re.compile(r'\"(.*)\"')
        self.titok_pattern = re.compile(r'\.(tiktok)\.')
        self.ytb_pattern = re.compile(r'\.(youtube)\.')
        self.titok_video_pattern = re.compile(r'\/video\/(\d+)\/?\?')

    # 开源tiktok api获取视频信息, 返回一个json
    def getTiktokVideoAllInfo(self, VideoId):
        api = TikTokAPI(self.cookies)
        return api.getVideoById(VideoId)

    # Tiktok视频信息处理, 筛选出需要的数据
    def getTikLikeAndPlay(self, VideoId):
        result = self.getTiktokVideoAllInfo(VideoId)
        LikeCount = result['itemInfo']['itemStruct']['stats']['diggCount']
        PlayCount = result['itemInfo']['itemStruct']['stats']['playCount']
        return LikeCount, PlayCount

    # 通过谷歌api获取ytb所有视频信息,返回一个object
    def getYtbVideoAllInfo(self, VideoId):
        api = yapi.YoutubeAPI(self.googleAuth)
        video = api.get_video_info(VideoId)
        return video

    # ytb视频信息处理，筛出需要的数据
    def getYtbLikeAndPlay(self, VideoId):
        video = self.getYtbVideoAllInfo(VideoId)
        LikeCount = video.items[0].statistics.likeCount
        PlayCount = video.items[0].statistics.viewCount
        return LikeCount, PlayCount

    # 通用视频端口,通过platform指向不同的平台调用不同Api获取视频信息
    def getCommonInfo(self, platform, VideoId):
        LikeCount, PlayCount = -1, -1
        try:
            LikeCount, PlayCount = self.driveConfig[platform](VideoId)
        except:
            return
        return int(LikeCount), int(PlayCount)

    # 获取重定向的url
    def get_redirect_url(self, url):
        try_count = 1
        while try_count < self.try_count:
            if try_count > 1:
                print("正在进行第", try_count, "次尝试")
            try:
                response = requests.get(url, headers=self.headers, timeout=self.time_out)
                redirect_url = response.url
                response.close()
                return 0, redirect_url
            except:
                print("第", try_count, "次尝试失败")
                try_count = try_count + 1
        return -1, url

    #处理tiktok链接的VideoId提取
    def get_titok_videoId(self,url):
        videoId = self.titok_video_pattern.findall(url)
        if videoId:
            return videoId[0]
        else:
            response = requests.get(url, headers=self.headers, timeout=self.time_out, allow_redirects=False)
            redirect_url = self.redirec_pattern.findall(response.text)[0]
            videoId = self.titok_video_pattern.findall(redirect_url)
            response.close()
            if videoId:
                return videoId[0]

        return ""

    # 从url解析视频数据，返回平台类型和视频ID
    def UrlToPlatformAndVedioId(self, url):
        PlatForm = "SBpython"
        VideoId  = "SBpython"
        if url == "":
            return -1, PlatForm, VideoId, url

        redirect_url = url

        #只有两个平台先这么写
        if self.titok_pattern.search(url):
            PlatForm = 'tiktok'
        elif self.ytb_pattern.search(url):
            PlatForm = 'youtube'
        else:
            return -3, PlatForm, VideoId, redirect_url

        # # 筛掉不合法链接
        # if code == -1:
        #     return -2, PlatForm, VideoId, url
        # elif len(result.netloc.split('.')) < 2:
        #     return -3, PlatForm, VideoId, redirect_url


        # 根据平台截取重定向后的链接ID
        if PlatForm == 'youtube':
            try:
                code, redirect_url = self.get_redirect_url(url)
                if code == -1:
                    return -2, PlatForm, VideoId, url
                result = urlparse(redirect_url)
                #建议这里也整成正则
                VideoId = result.query.split('=')[1].split('&')[0]
            except:
                return -4, PlatForm, VideoId, redirect_url
        if PlatForm == 'tiktok':
            try:
                VideoId = self.get_titok_videoId(url)
                if VideoId == "":
                    return -4, PlatForm, VideoId, redirect_url
            except:
                return -4, PlatForm, VideoId, redirect_url

        return 0, PlatForm, VideoId, redirect_url
