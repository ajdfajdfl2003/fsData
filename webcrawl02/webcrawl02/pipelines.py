# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from models import Deals, db_connect, create_deals_table
import logging, sys

class QueryExists(object):
    def go(self, deal, session):
        mapper = class_mapper(Deals)
        db = session.query(mapper).filter(Deals.timestamp==deal.timestamp,\
             Deals.category==deal.category, Deals.type==deal.type,\
             Deals.address==deal.address).first()
        return db

class fsDataPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        deal = Deals(**item)
        try:
            exists = QueryExists().go(deal, session)
            if exists is None:
                logging.warning(deal.timestamp+" | "+deal.category+" | "+deal.type+" | "+deal.address+" | "+deal.assignUnit)
            else:
                logging.debug("exists")
            session.merge(deal)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
