# -*- coding: utf-8 -*-
import sys
import json
import scrapy
from scrapy.http import Request, FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import fsData

class firestation(scrapy.Spider):
    name = "fire"
    allowed_domains = ["web.chfd.gov.tw"]
    start_urls = [
        "http://web.chfd.gov.tw/current_case.php"
    ]

    def parse(self, response):
        request = Request(response.url, callback = self.parse_fireLog)
        yield request

    def parse_fireLog(self, response):
        sel = Selector(response)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        _table = sel.css('table')
        _rows = _table.css('tr')

        itemResult = []
        noData = '本縣目前無任何災害案件'

        for i, _cell in enumerate(_rows):
            _contents = _cell.css('td')
            _tmp = []
            for j, _datas in enumerate(_contents):
                _d = _datas.css('font').xpath('text()').extract()
                if(len(_d)):
                    _tmp.append(_d[0].strip())
                ## Deal with not <font></font> tag
                else:
                    _d = _datas.xpath('text()').extract()
                    _tmp.append(_d[0].strip())
            if(len(_tmp) and _tmp[0] != noData):
                item = fsData()
                item['timestamp']   = _tmp[1].strip()
                item['category']    = _tmp[2].strip()
                item['type']        = _tmp[3].strip()
                item['address']     = _tmp[4].strip()
                item['assignUnit']  = _tmp[5].strip()
                item['status']      = _tmp[6].strip()
                item['allData']     = dict(item)
                itemResult.append(item)
                #print json.dumps(item['all_data'], ensure_ascii=False)
                #print _data[4].strip().strip('&nbsp;').strip('\r\n').strip(' ').strip('\n')
        return itemResult
