# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import scrapy
import json
import os
import re
from scrapy.exceptions import DropItem
from ximalaya.settings import FILES_STORE
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class XimalayaPipeline(FilesPipeline):
    #fp = open("ximalaya.json",'w',encoding='utf-8')

    def get_media_requests(self, item, info):

        yield scrapy.Request(item['audio_src'],meta={'dont_redirect': False, 'handle_httpstatus_list': [302],"audio_title":item['audio_title'],"audio_fm_title":item['audio_fm_title']})

    def  file_path(self,request,response=None,info=None):
    
        name = request.meta['audio_title'] + '.m4a'
        filename = os.path.join("{0}/{1}".format(re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', request.meta['audio_fm_title']),name))
        print(filename,"保存的文件路径")
        return filename

    def item_completed(self, results, item, info):
        print(results,"保存结果")
        file_paths = [x['path'] for ok,x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        print(file_paths[0],"保存的文件")
        ##os.rename(FILE_STORE+file_paths[0],FILE_STORE+item['audio_fm_title']+"/"+item['audio_title'])
        item['audio_files'] = file_paths[0]
        return item
class XimalayaJsonPipeline(object):

    
    fp = open("ximalaya.json",'w+',encoding='utf-8')

    def process_item(self, item, spider):
        
        item_json = json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(item_json+"\n")
        return item

    def close_spider(self,spider):
        self.fp.close()
        print("爬虫结束了....")


   

    
