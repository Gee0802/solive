from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import roomItem


class longzhuSpider(CrawlSpider):
    name = 'longzhu'
    start_urls = ['https://www.longzhu.com/games']
    rules = (
        Rule(LinkExtractor(allow=('/channels/\w+',)), callback='parse_cate'),
    )

    def parse_cate(self, response):
        room_items = response.xpath('//*[@id="list-con"]/a')
        for room in room_items:
            item = roomItem()
            item['source'] = self.name
            item['room'] = room.xpath('./@href').extract_first()
            item['nickname'] = room.xpath('./span[1]/strong/text()').extract_first()
            item['title'] = room.xpath('./h3/text()').extract_first()
            item['cover'] = room.xpath('./img/@src').extract_first()
            item['cate'] = (room.xpath('./ul/li[2]/span[2]/text()') or
                            response.xpath('//*[@id="list-head"]/h2/text()')).extract_first().strip()
            viewers_num = room.xpath('./ul/li[1]/span[2]/text()').extract_first()
            try:
                item['viewers_num'] = str(float(viewers_num[:-1]) * 10000) if '万' in viewers_num else viewers_num
            except TypeError:
                item['viewers_num'] = '0'
            yield item