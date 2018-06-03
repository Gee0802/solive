from scrapy import Spider, Item, Field

class LiveItem(Item):
    platform = Field()
    lives_num = Field(serializer=int)


class LiveSpider(Spider):
    name = 'lives_num'
    start_urls = ['https://www.panda.tv/all',
                  'https://www.longzhu.com',
                  'https://www.huya.com/l',
                  'https://www.quanmin.tv/game/all',
                  'https://www.zhanqi.tv/lives',
                  'https://api.live.bilibili.com/area/home',
                  'https://www.douyu.com/gapi/rkc/home/list'
                  ]
    custom_settings = {'ITEM_PIPELINES': {}, 'FEED_FORMAT': 'json', 'FEED_URI': 'live.json'}

    def parse(self, response):
        import json

        url = response.url
        item = LiveItem()
        if 'panda' in url:
            item['platform'] = 'panda'
            item['lives_num'] = response.xpath('//*[@id="later-play-list"]/@data-total').extract_first()
        elif 'longzhu' in url:
            item['platform'] = 'longzhu'
            item['lives_num'] = response.xpath('//span[@class="living-tit-info"]/span/text()').extract_first()
        elif 'huya' in url:
            item['platform'] = 'huya'
            item['lives_num'] = int(response.xpath('//*[@id="js-list-page"]/@data-pages').extract_first()) * 120
        elif 'quanmin' in url:
            item['platform'] = 'quanmin'
            item['lives_num'] = int(response.xpath('//span[text()="跳转到:"]/preceding-sibling::a[2]/text()')
                                    .extract_first().strip()) * 60
        elif 'zhanqi' in url:
            item['platform'] = 'zhanqi'
            item['lives_num'] = response.xpath('//*[@id="hotList"]/div[2]/@data-cnt').extract_first()
        elif 'bilibili' in url:
            item['platform'] = 'bilibili'
            item['lives_num'] = json.loads(response.text)['data']['total']
        elif 'douyu' in url:
            item['platform'] = 'douyu'
            item['lives_num'] = json.loads(response.text)['data']['live_num']
        yield item