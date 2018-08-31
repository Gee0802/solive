from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem

from ..items import roomItem


class pandaSpider(CrawlSpider):
    name = 'panda'
    start_urls = ['https://www.panda.tv/cate']
    rules = (
        Rule(LinkExtractor(allow=('/cate/\w+',)), callback='parse_cate'),
    )

    def parse_cate(self, response):
        room_items = response.xpath('//ul[@id="sortdetail-container"]/li')
        for room in room_items[1:]:
            item = roomItem()
            item['source'] = self.name
            item['room'] = 'https://www.panda.tv' + room.xpath('./a/@href').extract_first()
            item['nickname'] = room.xpath('./a/div[2]/span[2]/@title').extract_first()
            item['title'] = room.xpath('./a/div[2]/span[1]/@title').extract_first()
            item['cover'] = room.xpath('./a/div[1]/img/@data-original').extract_first()
            item['cate'] = (room.xpath('./div/div/a[1]/text()').extract_first() or '').strip()
            viewers_num = room.xpath('./a/div[2]/span[3]/text()').extract_first()
            try:
                item['viewers_num'] = str(float(viewers_num[:-1]) * 10000) if '万' in viewers_num else viewers_num
            except TypeError:
                item['viewers_num'] = '0'
            yield item