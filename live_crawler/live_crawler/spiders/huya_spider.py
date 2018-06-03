from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem

from ..items import roomItem


class huyaSpider(CrawlSpider):
    name = 'huya'
    start_urls = ['http://www.huya.com/g']
    rules = (
        Rule(LinkExtractor(allow=('/g/\w+',)), callback='parse_cate'),
    )

    def parse_cate(self, response):
        room_items = response.xpath('//ul[@id="js-live-list"]/li')
        for room in room_items:
            item = roomItem()
            item['source'] = self.name
            item['room'] = room.xpath('./a[1]/@href').extract_first()
            item['nickname'] = room.xpath('./span/span/i/@title').extract_first()
            item['title'] = room.xpath('./a[2]/text()').extract_first()
            item['cover'] = room.xpath('./a[1]/img/@data-original').extract_first()
            item['cate'] = (response.xpath('/html/body/div[2]/div/div[2]/div[2]/h2/a/text()') or
                            response.xpath('/html/body/div[2]/div/div[2]/div[1]/h2/a/text()')).extract_first().strip()
            viewers_num = room.xpath('./span/span[2]/i[2]/text()').extract_first()
            try:
                item['viewers_num'] = str(float(viewers_num[:-1]) * 10000) if '万' in viewers_num else viewers_num
            except TypeError:
                item['viewers_num'] = '0'
            yield item