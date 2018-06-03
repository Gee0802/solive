from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pymysql
import datetime

try:
    from live_crawler import spiders
except:
    from .live_crawler import spiders


def crawl_videos():
    settings = get_project_settings()
    settings.update({'LOG_LEVEL': 'ERROR'})
    p = CrawlerProcess(settings)
    for spider_name in spiders.all_name:
        p.crawl(spider_name)
    p.crawl('lives_num')
    p.start()
    # conn = pymysql.connect(host=settings['MYSQL_HOST'], port=settings['MYSQL_PORT'],
    #                user=settings['MYSQL_USER'], password=settings['MYSQL_PASSWORD'], db=settings['MYSQL_DB'])
    # cursor = conn.cursor()
    # cursor.execute('DELETE FROM videos WHERE SUBDATE(NOW(), INTERVAL 5 MINUTE) > 4;')
    # cursor.close()
    # conn.close()


if __name__ == '__main__':
    crawl_videos()