from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem

from ..items import roomItem


class douyuSpider(CrawlSpider):
    name = 'douyu'
    start_urls = ['https://www.douyu.com/directory']
    rules = (
        Rule(LinkExtractor(allow=('/g_\w+',)), callback='parse_cate'),
    )

    def parse_cate(self, response):
        room_items = response.xpath('//ul[@id="live-list-contentbox"]/li')
        for room in room_items[:25]:
            item = roomItem()
            item['source'] = self.name
            item['room'] = 'https://www.douyu.com' + room.xpath('./a/@href').extract_first()
            item['nickname'] = room.xpath('./a/div[1]/p/span[1]/text()').extract_first()
            item['title'] = room.xpath('./a/@title').extract_first()
            item['cover'] = room.xpath('./a/span/img/@data-original').extract_first()
            item['cate'] = (room.xpath('./a/div[1]/div/span/text()').extract_first() or '').strip()
            viewers_num = room.xpath('./a/div[1]/p/span[2]/text()').extract_first()
            try:
                item['viewers_num'] = str(float(viewers_num[:-1]) * 10000) if '万' in viewers_num else viewers_num
            except TypeError:
                item['viewers_num'] = '0'
            yield item
