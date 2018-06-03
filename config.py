import os


basedir = os.path.abspath(os.path.dirname(__file__))

url_cate_mappings = {
    'lol': '英雄联盟',
    'pubg': '绝地求生',
    'wzry': '王者荣耀',
    'dnf': 'DNF',
    'hearthstone': '炉石传说',
    'dota': 'DOTA',
    'dota2': 'DOTA2',
    'qqfc': 'QQ飞车',
    'qqfcsy': 'QQ飞车手游',
    'qqxw': 'QQ炫舞',
    'qqxwsy': 'QQ炫舞手游',
    'qqxxz': 'QQ仙侠传',
    'qqzyhx': 'QQ自由幻想',
    'qqhx': 'QQ华夏',
    'qqsg': 'QQ三国',
    'qqyx': 'QQ游戏',
    'cfsy': 'CF手游',
    'cf': '穿越火线',
    'csgo': 'CSGO',
    'fortnite': '堡垒之夜',
    'cjzc': '刺激战场',
    'qjcj': '全军出击',
    'fbyx': '风暴英雄',
    'fzscjh': '方舟生存进化',
    'jh': '饥荒',
    'bns': '剑灵',
    'jw3': '剑网3',
    'jtlq': '街头篮球',
    'mxd': '冒险岛',
    'mxd2': '冒险岛2',
    'mhxy': '梦幻西游',
    'mhxysy': '梦幻西游手游',
    'wow': '魔兽世界',
    'mszb': '魔兽争霸',
    'qqdzz': '球球大作战',
    'sgs': '三国杀',
    'swxf': '守望先锋',
    'tymyd': '天涯明月刀',
    'tlbb': '天龙八部',
    'wd': '问道',
    'wdsj': '我的世界',
    'zjyx': '主机游戏',
    '300yx': '300英雄',
    'ahphs3': '暗黑破坏神3',
    'blct': '部落冲突',
    'hszz': '皇室战争',
    'mhzx': '梦幻诛仙',
    'dwrg': '第五人格',
    'hyxd': '荒野行动',
    'hjjd': '怀旧经典',
    'dhxy': '大话西游',
    'ecy': '二次元',
    'ecyyx': '二次元游戏',
    'grsm': '光荣使命',
    'lrs': '狼人杀',
    'hw': '户外',
    'jwt': '劲舞团',
    'jzpaj': '决战平安京',
    'tksj': '坦克世界',
    'yys': '阴阳师',
    'nba': 'NBA',
    'jpfc': '极品飞车',
    'ppkdc': '跑跑卡丁车',
    'yxs': '英雄杀',
    'xjzb': '星际争霸',
    'dzpk': '德州扑克',
    'gwlr': '怪物猎人',
    'hbq': '虎豹骑',
    'fifa': 'FIFA',
    'football': '足球专区',
    'hyrz': '火影忍者',
    'qpyl': '棋牌娱乐',
    'ktp': '昆特牌',
    'cq': '传奇专区',
    'zt': '征途',
    'ppt': '泡泡堂',
    'cs': '反恐',
    'lzg': '龙之谷',
    'gdjh': '孤岛惊魂',
    'gdyx': '格斗游戏',
    'dzzh': '盗贼之海',
    'mssy2': '末世鼠疫2',
    'sljt': '杀戮尖塔',
    'sos': 'SOS终极逃脱',
    'jsyx': '竞速游戏',
    'smzh': '使命召唤',
    'qezb': '企鹅直播',
    'yanzhi': '颜值',
    'qfqxzl': '起凡群雄逐鹿',
    'xingxiu': '星秀',
    'meishi': '美食',
    'ylzt': '御龙在天',
    'nz': '逆战',
    'qnyh': '倩女幽魂',
    'szhj': '神之浩劫',
    'shenwu': '神武',
    'hdlgl': '魂斗罗归来',
    'mlbb': '魔力宝贝',
    'yhzr': '英魂之刃',
    'zzyscc': '战争艺术赤潮',
    'chlh': '彩虹六号',
    'zjz': '终结者',
    'msg': '梦三国',
    'lfzl': '流放之路',
    'byxx': '捕鱼休闲',
    'clx': '楚留香',
    'yzs': '影之诗',
    'kxjs': '科学技术',
    'car': '汽车',
    'junshi': '军事',
    'qhyx': '枪火游侠',
    'jrlc': '金融理财',
    'yyzb': '语音直播',
    'stdp': '视听点评',
    'znl': '正能量',
    'tkx': '脱口秀',
    'music': '音乐',
    'sports': '体育',
    'blizzard': '暴雪专区',
    'xyzq': '新游专区',
    'dm': '动漫',
    'wegame': 'WeGame',
    'jyxx': '教育学习',
    'qtyx': '其他游戏',
    'qtsy': '其他手游',
    'other': '其他',
}

cate_url_mappings = {v: k for k, v in url_cate_mappings.items()}

url_source_mappings = {
    'douyu': '斗鱼',
    'panda': '熊猫',
    'huya': '虎牙',
    'longzhu': '龙珠',
    'quanmin': '全民',
    'zhanqi': '战旗',
    'bilibili': 'bilibili'
}

source_url_mappings = {v: k for k, v in url_source_mappings.items()}

hot_hosts = [
    'https://www.panda.tv/666666',
    'https://www.panda.tv/2009',
    'https://www.panda.tv/10015',
    'https://www.panda.tv/520520',
    'https://www.panda.tv/10091',
    'https://www.panda.tv/10455',
    'https://www.panda.tv/101010',
    'https://www.panda.tv/99999',
    'https://www.panda.tv/11110',
    'https://www.panda.tv/2009',
    'https://www.panda.tv/596605',
    'https://www.panda.tv/66666',
    'https://www.panda.tv/10029',
    'https://www.panda.tv/31131',
    'https://www.panda.tv/575757',
    'https://www.panda.tv/10027',
    'https://www.douyu.com/911',
    'https://www.douyu.com/dongzhu',
    'https://www.douyu.com/lslalala',
    'https://www.douyu.com/606118',
    'https://www.douyu.com/1229',
    'https://www.douyu.com/520',
    'https://www.douyu.com/71017',
    'https://www.douyu.com/78622',
    'https://www.douyu.com/4811710',
    'https://www.douyu.com/290935',
    'https://www.douyu.com/4835718',
    'https://www.douyu.com/9999',
    'https://www.huya.com/sgjsheng',
    'https://www.huya.com/saonan',
    'https://www.huya.com/871001',
    'https://www.huya.com/kuangren',
    'https://www.huya.com/ximen',
    'https://www.huya.com/godv',
    'https://www.huya.com/miss',
    'https://www.huya.com/a16789',
    'https://www.huya.com/xuanmo',
    '//star.longzhu.com/xuxubaobao?from=challcontent',
    '//star.longzhu.com/777777?from=challcontent',
    '//star.longzhu.com/langziyan?from=challcontent',
    '//star.longzhu.com/l666666?from=challcontent',
    'https://www.quanmin.tv/666',
    'https://www.quanmin.tv/2333',
    'https://www.zhanqi.tv/weixiao',
    'https://www.zhanqi.tv/biyouxia',
    'https://www.zhanqi.tv/9527',
    'https://www.zhanqi.tv/edgclearlove'
]

so_labels = {
    'game': ['英雄联盟', '绝地求生', '王者荣耀', '穿越火线', 'DNF', 'DOTA2', '炉石传说'],
    'entertainment': ['户外', '星秀', '星颜', '美食', '音乐', '动漫', '语音直播', '视听点评', '脱口秀'],
    'education': ['教育学习', '科学技术', '金融理财', '军事', '汽车', '正能量']
}


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    ALLOWED_UPLOAD_TYPES = ('.jpg', '.jpeg', '.png')
    GLOBAL_TEMPLATE_ARGS = {
        'recommend': ['英雄联盟', 'DNF', '堡垒之夜'],
        'categories': {
            '热门竞技': ['英雄联盟', '绝地求生', '炉石传说', 'DOTA2'],
            '娱乐联盟': ['户外', '星秀', '美食', '颜值'],
            '网络游戏': ['DNF', 'QQ飞车', '穿越火线', '堡垒之夜'],
            '手游专区': ['王者荣耀', '第五人格', '刺激战场', '球球大作战']
        },
        'cate_url_mappings': cate_url_mappings
    }
    SO_TIME = 6300

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_MIGRATE_REPO = 'migrations/dev_migrations'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_MIGRATE_REPO = 'migrations/test_migrations'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql://root:123456@127.0.0.1:3306/test'
    SQLALCHEMY_MIGRATE_REPO = 'migrations/pro_migrations'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
    }
