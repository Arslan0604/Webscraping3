import scrapy


class Bookspider9Spider(scrapy.Spider):
    name = "bookspider9"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        pass
