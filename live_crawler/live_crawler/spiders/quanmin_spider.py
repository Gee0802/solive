from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import roomItem


class quanminSpider(CrawlSpider):
    name = 'quanmin'
    start_urls = ['https://www.quanmin.tv/category']
    rules = (
        Rule(LinkExtractor(allow=('/game/\w+',)), callback='parse_cate'),
    )

    def parse_cate(self, response):
        room_items = response.xpath('//ul[@class="list_w-videos_video-list"]/li')
        for room in room_items:
            item = roomItem()
            item['source'] = self.name
            item['room'] = 'https:' + room.xpath('./div/div/a[1]/@href').extract_first()
            item['nickname'] = room.xpath('./div/div/a[1]/div[3]/div/div/span[1]/text()').extract_first()
            item['title'] = room.xpath('./div/div/a[1]/div[3]/div/p/text()').extract_first()
            item['cover'] = room.xpath('./div/div/a[1]/div[1]/picture//img/@src').extract_first()
            item['viewers_num'] = room.xpath('./div/div/a[1]/div[3]/div/div/span[2]/text()').extract_first()
            item['cate'] = room.xpath('./div/div/a[2]/text()').extract_first()
            yield item