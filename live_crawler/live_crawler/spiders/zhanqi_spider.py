from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import roomItem


class zhanqiSpider(CrawlSpider):
    name = 'zhanqi'
    start_urls = ['https://www.zhanqi.tv/games']
    rules = (
        Rule(LinkExtractor(allow=('/games/\w+',)), callback='parse_first'),
    )

    def parse_first(self, response):
        """
        Get the XMLHttpRequest url for rooms list.
        """
        ajax_url = (response.xpath('//div[@id="js-live-list-panel"]/div[2]/@data-url') or
                    response.xpath('//div[@id="js-live-list-panel"]/div[2]/div/@data-url') or
                    response.xpath('//div[@id="js-live-list-panel"]/div[3]/@data-url')).extract_first()
        ajax_url = response.urljoin(ajax_url.replace('${size}', '30').replace('${page}', '1'))
        yield Request(ajax_url, callback=self.parse_cate)

    def parse_cate(self, response):
        """
        Parse the response json.
        """
        import json
        ajax_result = json.loads(response.text)
        room_items = ajax_result['data']['rooms']
        for room in room_items:
            item = roomItem()
            item['source'] = self.name
            item['room'] = 'https://www.zhanqi.tv' + room['url']
            item['nickname'] = room['nickname']
            item['title'] = room['title']
            item['cover'] = room['bpic']
            item['cate'] = room['gameName']
            viewers_num = room['online']
            try:
                item['viewers_num'] = str(float(viewers_num[:-1]) * 10000) if '万' in viewers_num else viewers_num
            except TypeError:
                item['viewers_num'] = '0'
            yield item

