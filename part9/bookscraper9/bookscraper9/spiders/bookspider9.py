from urllib.parse import urlencode
import scrapy


API_KEY = '6cab1526-7898-4397-9aca-6b28d4af0a1b'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class Bookspider9Spider(scrapy.Spider):
    name = "bookspider9"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        'FEEDS' : {
            'databook.json':{'format': 'json', 'overwrite': True},
        }
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield scrapy.Request(url=book_url, callback= self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield scrapy.Request(url=next_page_url, callback= self.parse)

    def parse_book_page(self, response):
        book = response.css("div.product_main")[0]
        table_rows = response.css("table tr")
           
        yield {
            'url' : response.url,
            'title' : response.css('.product_main h1::text').get(),
            'upc'   : table_rows[0].css('td ::text').get(),
            'product_type' : table_rows[1].css('td ::text').get(),
            'price_excluding_tax' : table_rows[2].css('td ::text').get(),
            'price_including_tax' : table_rows[3].css('td ::text').get(),
            'tax' : table_rows[4].css('td ::text').get(),
            'availability' : table_rows[5].css('td ::text').get(),
            'num_reviews' : table_rows[6].css('td ::text').get(),
            'stars' : response.css("p.star-rating").attrib['class'],
            'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price' : response.css('p.price_color::text').get(),
        }

        
