from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy

class CraigslistItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    price = scrapy.Field()
    maplink = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    url = scrapy.Field()
    image_links = scrapy.Field()
    time = scrapy.Field()


class RoomSpider(CrawlSpider):
    name = "vcrooms"
    allowed_domains = [ "vancouver.craigslist.ca" ]
    start_urls = [ "http://vancouver.craigslist.ca/search/roo" ]
    #start_urls = ["http://vancouver.craigslist.ca/search/roo",
    #          "http://vancouver.craigslist.ca/search/roo/?s=100",
    #          "http://vancouver.craigslist.ca/search/roo/?s=200",
             #]

    rules = (Rule(SgmlLinkExtractor(allow=[r'.*?/.+?/roo/\d+\.html']), callback='parse_roo', follow=False),)

    def parse_roo(self, response):
      url = response.url
      titlebar = response.xpath('//*[@id="pagecontainer"]/section/h2/text()').extract()
      title = ''.join(titlebar)
      price = response.xpath('//*[@class="price"]/text()').extract()
      #price = int(re.search(r'\$(\d+)', price[0]).group(1))
      content = response.xpath('//*[@id="postingbody"]').extract()[0]
      maplink = response.xpath('//*[@id="pagecontainer"]/section/section[2]/div[1]/div/p/small/a[1]').extract()

      longitude = None
      latitude = None
      mapdata = response.xpath('//*[@id="map"]')
      if len(mapdata) != 0:
          longitude = float(mapdata.xpath("@data-longitude").extract()[0])
          latitude = float(mapdata.xpath("@data-latitude").extract()[0])


      image_links = response.xpath('//*[@id="thumbs"]/a/@href').extract()
      time = response.xpath('//*[@id="display-date"]/time/@datetime').extract()[0]

      item = CraigslistItem(url=url,
          price=price,
          title=title,
          content=content,
          maplink=maplink,
          longitude=longitude,
          latitude=latitude,
          image_links=image_links,
          time=time)

      return item