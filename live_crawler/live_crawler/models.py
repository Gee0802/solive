from sqlalchemy import Column, String, Integer, DateTime, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    source = Column(String(32))
    nickname = Column(String(32))
    room = Column(String(128), unique=True)
    title = Column(String(128))
    cover = Column(String(256))
    viewers_num = Column(Integer)
    cate = Column(String(32))
    parent_cate_name = Column(String(32), ForeignKey('categories.name'))


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    total_rooms = Column(Integer)
    total_viewers = Column(Integer)
    contains = relationship(Video, backref='parent_cate', lazy='dynamic')


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('mysql://root:123456@localhost/test?charset=utf8mb4')
    session = sessionmaker(bind=engine)()
    # video = session.query(Video).get(1)
    # print(video.nickname)
    video = Video(nickname='💓爱萝莉Lolita💓')
    session.add(video)
    session.commit()