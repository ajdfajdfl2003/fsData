# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import Deals, db_connect, create_deals_table

class fsDataPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        deal = Deals(**item)
        try:
            ## Use merge to avoid duplicate key
            session.merge(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
