# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
import json

from ..items import roomItem


class bilibiliSpider(Spider):
    name = 'bilibili'

    def start_requests(self):
        start_url_pattern = 'https://api.vc.bilibili.com/room/v1/area/getList?parent_id={}'
        for parent_id in range(1,5):
            start_url = start_url_pattern.format(parent_id)
            yield Request(start_url, callback=self.parse_start)

    def parse_start(self, response):
        cate_result = json.loads(response.text)
        data = cate_result['data']
        cate_url_pattern = 'https://api.vc.bilibili.com/room/v1/area/getRoomList?area_id={}'
        for cate in data:
            cate_url = cate_url_pattern.format(cate['id'])
            yield Request(cate_url, callback=self.parse_cate, meta={'cate_name': cate['name']})

    def parse_cate(self, response):
        room_result = json.loads(response.text)
        room_items = room_result['data']
        for room in room_items:
            item = roomItem()
            item['source'] = self.name
            item['cate'] = response.meta['cate_name']
            item['room'] = 'https://live.bilibili.com' + room['link']
            item['nickname'] = room['uname']
            item['title'] = room['title']
            item['cover'] = room['system_cover']
            item['viewers_num'] = room['online']
            yield item
