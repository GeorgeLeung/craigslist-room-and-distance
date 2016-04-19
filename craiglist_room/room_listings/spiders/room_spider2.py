from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import scrapy,simplejson, urllib

class CraigslistItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    drivingtime = scrapy.Field()
    bikingtime = scrapy.Field()
    transittime = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
   

class RoomSpider(CrawlSpider):
    name = "atl_room"
    allowed_domains = [ "atlanta.craigslist.org" ]
    start_urls = [ "http://atlanta.craigslist.org/search/roo" ]
    #start_urls = ["http://atlanta.craigslist.org/search/roo",
    #          "http://atlanta.craigslist.org/search/roo/?s=100",
    #          "http://atlanta.craigslist.org/search/roo/?s=200",
    #          "http://atlanta.craigslist.org/search/roo/?s=300",
    #          "http://atlanta.craigslist.org/search/roo/?s=400",
    #          "http://atlanta.craigslist.org/search/roo/?s=500",
    #          "http://atlanta.craigslist.org/search/roo/?s=600",
    #          "http://atlanta.craigslist.org/search/roo/?s=700",
    #          "http://atlanta.craigslist.org/search/roo/?s=800",
    #          "http://atlanta.craigslist.org/search/roo/?s=900"
    #         ]

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
      drivingtime = None
      bikingtime = None
      transittime = None
      
      #mapdata = response.xpath('//*[@id="map"]')
      #if len(mapdata) != 0:
      #    longitude = float(mapdata.xpath("@data-longitude").extract()[0])
      #    latitude = float(mapdata.xpath("@data-latitude").extract()[0])
          
      mapdata = response.xpath('//*[@id="map"]')
      if len(mapdata) != 0:
          longitude = float(mapdata.xpath("@data-longitude").extract()[0])
          latitude = float(mapdata.xpath("@data-latitude").extract()[0])
          orgtext = map(str, [latitude ,longitude])
          driveurl = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations=201+dowman+drive+atlanta+georgia+30322&mode=driving&departure_time=1460984400&key=AIzaSyD5mEjmwk_nMs_FQKKmFCxai7QLpy4CRpY".format(orgtext[0],orgtext[1])
          result= simplejson.load(urllib.urlopen(driveurl))
          drivingtime = result['rows'][0]['elements'][0]['duration']['value']
          bikeurl = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations=201+dowman+drive+atlanta+georgia+30322&mode=bicycling&departure_time=1460984400&key=AIzaSyD5mEjmwk_nMs_FQKKmFCxai7QLpy4CRpY".format(orgtext[0],orgtext[1])
          result= simplejson.load(urllib.urlopen(bikeurl))
          bikingtime = result['rows'][0]['elements'][0]['duration']['value']
          transiturl = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations=201+dowman+drive+atlanta+georgia+30322&mode=transit&departure_time=1460984400&key=AIzaSyD5mEjmwk_nMs_FQKKmFCxai7QLpy4CRpY".format(orgtext[0],orgtext[1])
          result= simplejson.load(urllib.urlopen(transiturl))
          transittime = result['rows'][0]['elements'][0]['duration']['value']


      #image_links = response.xpath('//*[@id="thumbs"]/a/@href').extract()
      #time = response.xpath('//*[@id="display-date"]/time/@datetime').extract()[0]


      item = CraigslistItem(
          
          price=price,
          title=title,
          drivingtime = drivingtime,
          bikingtime = bikingtime,
          transittime = transittime,
          longitude=longitude,
          latitude=latitude,
          
          )

      return item