# -*- coding: utf-8 -*-
import scrapy
import logging
#from scrapy.shell import inspect_response
#from scrapy.urils.response import open_in_browser


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = [
        'https://www.worldometers.info/world-population/population-by-country/']
    #country_name = ''

    def parse(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            # self.country_name = name
            link = country.xpath(".//@href").get()

            # absoulute_url = f"https://www.worldometers.info{link}"
            # absoulute_url = response.urljoin(link)

            # yield scrapy.Request(url=absoulute_url)
            # callback 추가 시 , 크롤링 후 callback 실행
            # meta 추가 시, callback에 전달됨.
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        # inspect_response(response, self)  # debugging
        # open_in_brower(response)
        # loggin.warning(response.status)
        name = response.request.meta['country_name']
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                # 'name': self.country_name,
                'country_name': name,
                'year': year,
                'population': population
            }

# DataSet 출력하기
# scrapy crawl countries -o population_dataset.json
# scrapy crawl countries -o population_dataset.csv
