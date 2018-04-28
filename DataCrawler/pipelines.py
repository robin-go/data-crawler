# -*- coding: utf-8 -*-
import logging

import MySQLdb
from scrapy.exceptions import DropItem


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


class RecipePipeline(object):
    """如果item title为空，丢弃item"""
    def process_item(self, item, spider):
        if item['title']:
            return item
        else:
            raise DropItem('Missing title in %s' % item)


class MysqlPipeline(object):
    """用于不同Mysqlpipeline的继承"""
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '111111', 'spider_db', charset="utf8")
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """当spider关闭时调用"""
        self.cursor.close()
        self.conn.close()


class RecipeMysqlPipeline(MysqlPipeline):
    """把菜谱保存到Mysql"""
    def process_item(self, item, spider):
        insert_sql = "insert into recipe(title, materials, steps, rank, url) values (%s, %s, %s, %s, %s)"

        self.cursor.execute(insert_sql, (item['title'], item['materials'], item['steps'], item['rank'], item['url']))
        self.conn.commit()

        logger.info('MySQL: add %s to mysql' % item['title'])

        return item


class JokeMysqlPipeline(MysqlPipeline):
    """把笑话保存到Mysql"""
    def process_item(self, item, spider):
        insert_sql = "insert into joke(title, content) values (%s, %s)"

        self.cursor.execute(insert_sql, (item['title'], item['content']))
        self.conn.commit()

        logger.info('MySQL: add %s to mysql' % item['title'])

        return item


class CheckPostcodePipeline(object):
    """字段为空则丢弃item"""
    def process_item(self, item, spider):
        if item['address']:
            return item
        else:
            raise DropItem('Missing address or code in %s' % item)


class PostcodeCountyMysqlPipeline(MysqlPipeline):
    """县级邮编pipeline"""
    def process_item(self, item, spider):
        insert_sql = "insert into postcode_county(address, code) values (%s, %s)"

        self.cursor.execute(insert_sql, (item['address'], item['code']))
        self.conn.commit()

        logger.info('MySQL: add %s to mysql' % item['address'])

        return item


class PostcodeDetailMysqlPipeline(MysqlPipeline):
    """社区、村级别邮编pipeline"""
    def process_item(self, item, spider):
        insert_sql = "insert into postcode_detail(address, code) values (%s, %s)"

        self.cursor.execute(insert_sql, (item['address'], item['code']))
        self.conn.commit()

        # logger.info('MySQL: add %s to mysql' % item['address'])

        return item
