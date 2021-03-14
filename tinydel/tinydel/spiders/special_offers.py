# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    # start_urls = [
    #     'https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']
    # start_requests 를 지정해 주는 경우 , start_urls 불필요

    def start_requests(self):
        yield scrapy.Request(url='https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html', callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield {
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                # urljoin 필요 (http://제외된 경우)
                'url': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                # .//span[@class='productSpecialPrice fl']/text()
                'discounted_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'original_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent': response.request.headers['User-Agent']
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
