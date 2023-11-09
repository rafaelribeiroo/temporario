from configparser import ConfigParser
# from utils import remove_emoji
# import urllib.parse
from scrapy import Spider

config = ConfigParser(allow_no_value=False)
config.read('config.ini')

class Facebook(Spider):
    name = 'facebook'
    custom_settings = {'FEED_EXPORT_ENCODING': 'utf-8'}

    def __init__(self, config, strictmode, city_id, **kwargs):

        # build the URL
        keywords = '%20'.join(config["DEFAULT"]["Keywords"].split(' '))
        exclusions = config['DEFAULT']['Exclusions'].split(',')
        SP_code = config['FACEBOOK']['city_id_sp']
        RS_code = config['FACEBOOK']['city_id_rs']

        self.keywords = config["DEFAULT"]["Keywords"].split(' ')
        self.exclusions = exclusions
        self.strictmode = strictmode
        self.start_urls = [f"https://www.facebook.com/marketplace/{SP_code}/"
                           f"search?query={keywords}&daysSinceListed=1"
                           f"&sortBy=creation_time_descend",
                           f"https://www.facebook.com/marketplace/{RS_code}/"
                           f"search?query={keywords}&daysSinceListed=1"
                           f"&sortBy=creation_time_descend",
                           ]
        super().__init__(**kwargs)

    def parse(self, response):
        # each flex item box (each ad)

        for ads in response.xpath(
            '//div[@style="max-width:1872px"]/div[2]/div'
        ):
            try:
                # check for any exclusion is in the title, ignore if so
                # if any(exclusions.lower() in title.lower() for exclusions in self.exclusions):
                #     continue

                # import pdb; pdb.set_trace()
                if len(ads.css('span::text').getall()) == 3:
                    yield {
                        'city': ads.css('span::text').getall()[2],
                        'title': ads.css('span::text').getall()[1].title(),
                        'price': ads.css('span::text').getall()[0],
                        'pic_url': ads.css('img::attr(src)').extract()[0],
                        'link': 'https://www.facebook.com' + ads.css('a::attr(href)').extract()[0]
                    }

                elif len(ads.css('span::text').getall()) == 4:
                    yield {
                        'previous_price': ads.css('span::text').getall()[1],
                        'price': ads.css('span::text').getall()[0],
                        'city': ads.css('span::text').getall()[3],
                        'title': ads.css('span::text').getall()[2].title(),
                        'pic_url': ads.css('img::attr(src)').extract()[0],
                        'link': 'https://www.facebook.com' + ads.css('a::attr(href)').extract()[0],
                    }

                # # check if title has a keyword, in future this can be an option in the config (strictmode)
                # # if self.strictmode and not any(keywords.lower() in title.lower() for keywords in self.keywords):
                # #     continue

            except:
                ṕrint('Nao foi possível')
                pass
