import scrapy
from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess
from scrapy.pipelines.images import ImagesPipeline


class LogoItem(scrapy.Item):
    source = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    cate = scrapy.Field()
    cate_en = scrapy.Field()


class LogoSpider(Spider):
    name = 'logo'
    start_urls = ['https://www.quanmin.tv/category',
                  'https://www.panda.tv/cate',
                  'http://longzhu.com/games',
                  'https://www.huya.com/g',
                  'https://www.douyu.com/directory']

    def parse(self, response):
        url = response.url
        if 'quanmin' in url:
            yield from self.parse_quanmin(response)
        elif 'panda' in url:
            yield from self.parse_panda(response)
        elif 'longzhu' in url:
            yield from self.parse_longzhu(response)
        elif 'huya' in url:
            yield from self.parse_huya(response)
        elif 'douyu' in url:
            yield from self.parse_douyu(response)

    def parse_quanmin(self, response):
        for cate in response.xpath('//div[@class="list_p-category"]/div[1]/a'):
            item = LogoItem()
            item['source'] = 'quanmin'
            item['image_urls'] = [cate.xpath('./img/@src').extract_first()]
            item['cate'] = cate.xpath('./p/text()').extract_first()
            item['cate_en'] = cate.xpath('./@href').re_first(r'/game/(\w+)')
            yield item

    def parse_panda(self, response):
        for cate in response.xpath('//div[@class="sort-container"]/ul/li'):
            item = LogoItem()
            item['source'] = 'panda'
            item['image_urls'] = [cate.xpath('./a/div/img/@src').extract_first()]
            item['cate'] = cate.xpath('./a/div/img/@alt').extract_first().replace(':','：')
            item['cate_en'] = cate.xpath('./a/@href').re_first(r'/cate/(\w+)')
            yield item

    def parse_longzhu(self, response):
        for cate in response.xpath('//div[@id="list-one"]/div'):
            item = LogoItem()
            item['source'] = 'longzhu'
            item['image_urls'] = [cate.xpath('./div/a/img/@src').extract_first()]
            item['cate'] = cate.xpath('./h2/a/text()').extract_first()
            item['cate_en'] = cate.xpath('./div/a/@href').re_first(r'/channels/(\w+)')
            yield item

    def parse_huya(self, response):
        for cate in response.xpath('//ul[@id="js-game-list"]/li'):
            item = LogoItem()
            item['source'] = 'huya'
            item['image_urls'] = ['http:' + cate.xpath('./a/img/@data-original').extract_first()]
            item['cate'] = cate.xpath('./a/h3/text()').extract_first().replace(':', '：')
            item['cate_en'] = cate.xpath('./a/@href').re_first(r'/g/(\w+)')
            yield item

    def parse_douyu(self, response):
        for cate in response.xpath('//ul[@id="live-list-contentbox"]/li'):
            item = LogoItem()
            item['source'] = 'douyu'
            item['image_urls'] = [cate.xpath('./a/img/@data-original').extract_first()]
            item['cate'] = cate.xpath('./a/p/text()').extract_first().replace(':', '：')
            item['cate_en'] = cate.xpath('./a/@href').re_first(r'/game/(\w+)')
            yield item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'item': item}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        return 'full/%s/%s.jpg' % (item['source'], item['cate'])



settings = dict(
    ROBOTSTXT_OBEY = False,
    FEED_URI = 'cate.json',
    ITEM_PIPELINES = {'crawl_cate_logo.MyImagesPipeline': 300,
                      },
    IMAGES_STORE = 'pic'
)


if __name__ == '__main__':
    p = CrawlerProcess(settings)
    p.crawl(LogoSpider)
    p.start()

