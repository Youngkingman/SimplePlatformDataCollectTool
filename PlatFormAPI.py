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
        self.headers = {
            'User-Agent' : 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 96.0.4664.45 Safari / 537.36'
        }
        self.driveConfig = {
            'youtube': self.getYtbLikeAndPlay,
            'tiktok' : self.getTikLikeAndPlay,
        }
        #正则表达式相关初始化
        self.redirec_pattern = re.compile(r'\"(.*)\"')
        self.titok_pattern = re.compile(r'(tiktok)')
        self.ytb_pattern = re.compile(r'(youtu\.?be)')
        self.tiktok_video_pattern = re.compile(r'\/video\/(\d+)\/?\?')
        self.ytb_video_pattern = re.compile(r'\=(.*)\&')
        self.ytb_video_pattern2 = re.compile(r'\=(.*)')
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

    # videoId提取
    def getVideoId(self, url, PlatForm):
        video_pattern = self.ytb_video_pattern if PlatForm == "youtube" else self.tiktok_video_pattern
        allowRedirects = True if PlatForm == "youtube" else False
        VideoId = video_pattern.findall(url)
        if VideoId:
            return VideoId[0], url
        else:
            try:
                response = requests.get(url, headers=self.headers, timeout=self.time_out, allow_redirects=allowRedirects)
                redirect_url = self.redirec_pattern.findall(response.text)[0] if PlatForm == "tiktok" else response.url
                VideoId = video_pattern.findall(redirect_url)
                response.close()
                if VideoId:
                    return VideoId[0], redirect_url
                elif PlatForm == "youtube":
                    VideoId = self.ytb_video_pattern2.findall(redirect_url)
                    if VideoId:
                        return VideoId[0], redirect_url
            except:
                return "", url
        return "", url

    # 从url解析视频数据，返回平台类型和视频ID
    def urlToPlatformAndVedioId(self, url):
        PlatForm = "SBpython"
        VideoId  = "SBpython"
        if url == "":
            return -1, PlatForm, VideoId, url

        if self.titok_pattern.search(url):
            PlatForm = 'tiktok'
        elif self.ytb_pattern.search(url):
            PlatForm = 'youtube'
        else:
            return -3, PlatForm, VideoId, url

        try_count = 1
        while try_count < self.try_count:
            if try_count > 1:
                print("正在进行第", try_count, "次尝试")

            # 根据平台做对应的处理
            try:
                VideoId, redirect_url = self.getVideoId(url, PlatForm)
                if VideoId != "":
                    return 0, PlatForm, VideoId, redirect_url
                else:
                    try_count = try_count + 1
            except:
                print("第", try_count, "次尝试失败")
                try_count = try_count + 1
        return -4, PlatForm, VideoId, url
