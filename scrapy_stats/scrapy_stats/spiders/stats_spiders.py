# @Time    :2019/3/8 10:30
# @Author  :lvjunjie

import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy_stats.items import ScrapyStatsItem
import copy
import time


class StatsSpider(scrapy.Spider):
    count = 0
    # scrapy runspider scrapy_stats/spiders/stats_spiders.py -s LOG_FILE=all.log -o StatsSpider.csv
    name = 'stats_scrapy'
    # start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html']
    allowed_domains = ['www.stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/index.html']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    cookies = {
        "SF_cookie_1": "37059734",
        "_trs_uv": "knx19n12_6_ggt8",
        "_trs_ua_s_1": "knx2pr7r_6_3nat",
        "wzws_cid": "9fa7aa4f9b5e18a398116a49bb3ed75fe29d60c298156cf723dcc4dd39c6233fadce644c3dc6e7eb12350cf92992e3c85145d3cccb1cc1aa95efe20c0490805fa9bfb36dd31021544d334dda0eb5e75f"
    }

    def parse(self, response):
        province_list =response.xpath('//*[@class="provincetr"]/td')
        for item in province_list:
            stats = {}
            # stats = {}
            stats['省份'] = item.xpath('a/text()').extract()[0]

            city_list_url = response.urljoin(item.xpath('a/@href').extract()[0])
            # print(city_list_url)
            yield scrapy.Request(url=city_list_url, meta={"stats": stats}, callback=self.parse_city, dont_filter=True,
                                 headers=StatsSpider.headers, cookies=StatsSpider.cookies)

    def parse_city(self, response):
        stats = response.meta['stats']
        city_list = response.xpath('//*[@class="citytr"]')
        print(city_list)
        for item in city_list:

            stats['城市'] = item.xpath('td[2]/a/text()').extract()[0]
            stats['城市代码'] = item.xpath('td[1]/a/text()').extract()[0]
            county_url = response.urljoin(item.xpath('td[1]/a/@href').extract()[0])
            # yield stats
            yield scrapy.Request(url=county_url, meta={"stats": copy.deepcopy(stats)}, callback=self.parse_county, headers=StatsSpider.headers, cookies=StatsSpider.cookies)

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
                                     dont_filter=True, headers=StatsSpider.headers, cookies=StatsSpider.cookies)

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
                                 dont_filter=True, headers=StatsSpider.headers, cookies=StatsSpider.cookies)

    def parse_villagetr(self, response):
        stats = response.meta['stats']
        villagetr_list = response.xpath('//*[@class="villagetr"]')
        # print('villagetr_list = ')
        # print(villagetr_list)

        for item in villagetr_list:
            stats['社区'] = item.xpath('td[3]/text()').extract()[0]
            stats['社区代码'] = item.xpath('td[1]/text()').extract()[0]
            print(stats)
            StatsSpider.count += StatsSpider.count
            print(StatsSpider.count)
            time.sleep(0.01)
            yield stats


