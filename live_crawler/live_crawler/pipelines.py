import pymysql
from scrapy.exceptions import DropItem
from .url_cate_mappings import mappings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Video


class MysqlPipeline(object):
    def __init__(self, host, port, user, password, db):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db,
                                    charset='utf8mb4')
        self.cate_iter = mappings.values()
        self.rooms = set()  # Used for duplication eliminating.
        self.execute_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(host=settings['MYSQL_HOST'], port=settings['MYSQL_PORT'],
                   user=settings['MYSQL_USER'], password=settings['MYSQL_PASSWORD'], db=settings['MYSQL_DB'])

    def open_spider(self, spider):
        self.cur = pymysql.cursors.DictCursor(self.conn)
        # try:
        #     self.cur.execute('CREATE TABLE videos ('
        #                      'id INT(6) NOT NULL AUTO_INCREMENT,'
        #                      'created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
        #                      'source VARCHAR(32) NOT NULL,'
        #                      'nickname VARCHAR(32) NOT NULL,'
        #                      'room VARCHAR(128) NOT NULL,'
        #                      'cate VARCHAR(32) NOT NULL,'
        #                      'title VARCHAR(128) NOT NULL,'
        #                      'viewers_num INT,'
        #                      'cover VARCHAR(256),'
        #                      'PRIMARY KEY(id)'
        #                      ');')
        # except:
        #     pass

    def process_item(self, item, spider):
        if item['room'] in self.rooms:
            raise DropItem('Duplicated item!')
        self.rooms.add(item['room'])
        if item['cate'] in self.cate_iter:
            item['parent_cate_name'] = item['cate']
        else:
            item['parent_cate_name'] = '其他'
        self.cur.execute('INSERT INTO videos '
                         '(source, nickname, room, cate, title, viewers_num, cover, parent_cate_name) VALUES '
                         '(%(source)s, %(nickname)s, %(room)s, %(cate)s, %(title)s, %(viewers_num)s, %(cover)s, '
                         '%(parent_cate_name)s) ON DUPLICATE KEY UPDATE source=%(source)s, nickname=%(nickname)s, '
                         'cate=%(cate)s, title=%(title)s, viewers_num=%(viewers_num)s, cover=%(cover)s, '
                         'parent_cate_name=%(parent_cate_name)s;', dict(item))
        # TODO: Try execute_many.
        # self.cur.execute('REPLACE INTO videos '
        #                  '(source, nickname, room, cate, title, viewers_num, cover, parent_cate_name) VALUES '
        #                  '(%(source)s, %(nickname)s, %(room)s, %(cate)s, %(title)s, %(viewers_num)s, %(cover)s, '
        #                  '%(parent_cate_name)s);', dict(item))
        self.execute_count += 1
        if self.execute_count % 10 == 0:
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


class SqlAlchemyPipeline:
    def __init__(self):
        self.engine = create_engine('mysql://root:123456@localhost/test?charset=utf8mb4')
        self.Session = sessionmaker(bind=self.engine)
        self.cate_iter = mappings.values()

    def process_item(self, item, spider):
        if item['cate'] in self.cate_iter:
            item['parent_cate_name'] = item['cate']
        else:
            item['parent_cate_name'] = '其他'
        session = self.Session()
        video = Video(cate=item['cate'], title=item['title'], nickname=item['nickname'], cover=item['cover'],
                      room=item['room'], viewers_num=item['viewers_num'], parent_cate_name=item['parent_cate_name'])
        session.merge(video)
        session.commit()
        return item
