# -*- coding: utf-8 -*-
import scrapy
import requests
import json
import math
from ximalaya.items import XimalayaItem
class VipSpider(scrapy.Spider):
    name = 'vip'
    #allowed_domains = ['https://www.ximalaya.com']
    xm_name = input("请输入要下载的音频名：")
    #start_urls = ['https://www.ximalaya.com/youshengshu/mr132t2721/']
    start_urls = ["https://www.ximalaya.com/search/{}/".format(xm_name)]
    base_url = "https://www.ximalaya.com"
    base_api = 'https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort=0&pageSize=30'
    time_api = 'https://www.ximalaya.com/revision/time'
    pay_api = 'https://www.ximalaya.com/revision/album?albumId={}'
    pay_api_2 =  'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId={}&pageNum={}'
    pay_api_allinfo = 'http://180.153.255.6/mobile-album/album/page/ts-1569206246849?ac=WIFI&albumId={}' \
                               '&device=android&isAsc=true&isQueryInvitationBrand=true&isVideoAsc=true&pageId=1' \
                               '&pageSize={}'
    pay_api_single = 'http://mobile.ximalaya.com/mobile/redirect/free/play/{}/2'
    header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
    
    s = requests.session()
    
    # def get_pay_fm(self, xm_fm_id):
    #     # 根据有声书ID构造url
    #     fm_url = self.pay_api.format(xm_fm_id)
    #     print(fm_url)
    #     r_fm_url = self.s.get(fm_url, headers=self.header)
    #     r_json = r_fm_url.json()
    #     fm_title = r_json['data']['mainInfo']['albumTitle']
    #     # 取最大页数
    #     max_tracks = r_json['data']['tracksInfo']['trackTotalCount']
    #     max_page = math.ceil(int(r_json['data']['tracksInfo']['trackTotalCount'])/30)
    #     print('书名：' + fm_title)
    #     # 新建有声书ID的文件夹
    #     fm_path = self.make_dir(xm_fm_id)
    #     if max_tracks:
    #         r_album_alltracks = self.s.get(self.pay_api_allinfo.format(xm_fm_id, max_tracks), headers=self.header)
    #         raa_json = json.loads(r_album_alltracks.text)
    #         tracks = raa_json['data']['tracks']['list']
    #         for track in tracks:
    #             audio_id = track['trackId']
    #             audio_title = str(track['title']).replace(' ', '')
    #             audio_src = self.pay_api_single.format(audio_id)
    #             print(audio_title, audio_src)
    #             #self.get_detail(audio_title, audio_src, fm_path)
    #             # 每爬取1页，30个音频，休眠1~3秒
    #             #time.sleep(random.randint(1, 3))
    #     else:
    #         print(os.error)

    def parse(self, response):
        # xm_fm_id_list = response.xpath("//div[@class='content']/ul//a[@class='album-title line-1 lg bold _bkf']/@href").re("\d+")
        # for xm_fm_id in xm_fm_id_list:
        #     yield scrapy.Request(self.pay_api.format(xm_fm_id),headers=self.header,meta={"xm_fm_id":xm_fm_id},callback=self.get_list)
        # #下一页
        # page_next_list = response.xpath("//a[@class='page-link _bfuk']/@href").extract()
        # for page_next in range(2,35):
        #     yield scrapy.Request("https://www.ximalaya.com/youshengshu/mr132t2721/p{}/".format(page_next),callback=self.parse,headers=self.header)
        xm_fm_id_list = response.xpath("//div[@class='_Tt']//div/a[@class='xm-album-title ellipsis-2']")
        for xm_fm_id in xm_fm_id_list:
            print("%s-%s"%(xm_fm_id.xpath("./@title").extract_first(),xm_fm_id.xpath("./@href").re("\d+")[0]))
        xm_fm_id = input("请选择要下载的声音，输入声音id：")
        yield scrapy.Request(self.pay_api.format(xm_fm_id),headers=self.header,meta={"xm_fm_id":xm_fm_id},callback=self.get_list)
    def get_list(self,response):
        
        r_fm_url=json.loads(response.text)
        r_json = r_fm_url
        fm_title = r_json['data']['mainInfo']['albumTitle']
        # 取最大页数
        max_tracks = r_json['data']['tracksInfo']['trackTotalCount']
        max_page = math.ceil(int(r_json['data']['tracksInfo']['trackTotalCount'])/30)
        xm_fm_id = response.meta['xm_fm_id']
        print('书名：' + fm_title)

        if max_tracks:
            yield scrapy.Request(self.pay_api_allinfo.format(xm_fm_id, max_tracks),headers=self.header,meta={"fm_title":fm_title},callback=self.get_detail)
            

    def get_detail(self,response):
        try:
            fm_title = response.meta['fm_title']   
            raa_json = json.loads(response.text)
            tracks = raa_json['data']['tracks']['list']
            item = XimalayaItem() 
            
            for track in tracks:
                audio_id = track['trackId']
                audio_title = str(track['title']).replace(' ', '')
                audio_src = self.pay_api_single.format(audio_id)
                # audio_src = self.s.get(audio_src,allow_redirects=False,headers=self.header)
                # audio_src = audio_src.headers.get("Location")
                item['audio_id'] = audio_id
                item['audio_title'] = audio_title
                item['audio_detail'] = track
                item['audio_fm_title'] = fm_title
                item['audio_src'] = audio_src
                yield item
        except Exception as e:
            print("没有数据，跳过")

   
   