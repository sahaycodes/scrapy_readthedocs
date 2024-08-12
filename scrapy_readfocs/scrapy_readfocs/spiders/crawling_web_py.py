import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

class CrawlingSpider(CrawlSpider):
    name = "webcrawler"
    allowed_domains = ["hyperledger-fabric.readthedocs.io"]
    start_urls = ["https://hyperledger-fabric.readthedocs.io/en/latest/"]

    rules = (
        Rule(LinkExtractor(allow=("")), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(CrawlingSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse_item(self, response):
        page_title = response.css('title::text').get()
        url = response.url
        print(f'Scraping URL: {url}')
        print(f'Page title: {page_title}')
        headings = response.css('h1::text, h2::text, h3::text, h4::text, h5::text, h6::text').getall()
        paragraphs = response.css('p::text').getall()
        links = response.css('a::attr(href)').getall()
        full_links = [response.urljoin(link) for link in links]

        item = {
            'url': url,
            'title': page_title,
            'headings': headings,
            'content': paragraphs,
            'links': full_links,
        }

        self.items.append(item)  # Collect items

        yield item

    def closed(self, reason):
        # Write collected items to the JSON file with proper formatting
        with open('output.json', 'w') as f:
            json.dump(self.items, f, indent=4)
