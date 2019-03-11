# @Time    :2019/3/8 10:30
# @Author  :lvjunjie

import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy_stats.items import ScrapyStatsItem
import copy

class StatsSpider(scrapy.Spider):
    # scrapy runspider scrapy_stats/spiders/stats_spiders.py -o 1.csv
    name = 'stats_scrapy'
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']

    def parse(self, response):
        province_list =response.xpath('//*[@class="provincetr"]/td')
        for item in province_list:
            stats ={}
            # stats = {}
            stats['省份'] = item.xpath('a/text()').extract()[0]

            city_list_url = response.urljoin(item.xpath('a/@href').extract()[0])
            yield scrapy.Request(url=city_list_url, meta={"stats": stats}, callback=self.parse_city, dont_filter=True)

    def parse_city(self, response):
        city_list = response.xpath('//*[@class="citytr"]')
        for item in city_list:
            stats = response.meta['stats']
            stats['城市'] = item.xpath('td[2]/a/text()').extract()[0]
            stats['城市代码'] = item.xpath('td[1]/a/text()').extract()[0]
            county_url = response.urljoin(item.xpath('td[1]/a/@href').extract()[0])
            # yield stats
            yield scrapy.Request(url=county_url, meta={"stats": copy.deepcopy(stats)}, callback=self.parse_county)

    def parse_county(self, response):
        county_list = response.xpath('//*[@class="countytr"]')
        stats = response.meta['stats']
        for item in county_list:
            towntr_url = item.xpath('td[1]/a/@href')
            if towntr_url:
                stats['市辖区县'] = item.xpath('td[2]/a/text()').extract()[0]
                stats['市辖区县代码'] = item.xpath('td[1]/a/text()').extract()[0]
            else:
                stats['市辖区县'] = item.xpath('td[2]/text()').extract()[0]
                stats['市辖区县代码'] = item.xpath('td[1]/text()').extract()[0]
            if towntr_url:
                towntr_url = response.urljoin(towntr_url.extract()[0])
                # yield stats
                yield scrapy.Request(url=towntr_url, meta={"stats":  copy.deepcopy(stats)}, callback=self.parse_towntr,
                                     dont_filter=True)

    def parse_towntr(self, response):
        stats = response.meta['stats']
        towntr_list = response.xpath('//*[@class="towntr"]')
        # print('towntr_list = ')
        for item in towntr_list:
            stats['城镇'] = item.xpath('td[2]/a/text()').extract()[0]
            stats['城镇代码'] = item.xpath('td[1]/a/text()').extract()[0]
            county_url = response.urljoin(item.xpath('td[1]/a/@href').extract()[0])
            # yield stats
            yield scrapy.Request(url=county_url, meta={"stats": copy.deepcopy(stats)}, callback=self.parse_villagetr,
                                 dont_filter=True)

    def parse_villagetr(self, response):
        stats = response.meta['stats']
        villagetr_list = response.xpath('//*[@class="villagetr"]')
        # print('villagetr_list = ')
        # print(villagetr_list)
        for item in villagetr_list:
            stats['社区'] = item.xpath('td[3]/text()').extract()[0]
            stats['社区代码'] = item.xpath('td[1]/text()').extract()[0]
            yield stats

