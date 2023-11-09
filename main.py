from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from websites.facebook import Facebook
from configparser import ConfigParser
from twisted.internet import reactor


def main():
    config = ConfigParser(allow_no_value=False)
    config.read('config.ini')

    strictmode = config['DEFAULT'].getboolean('StrictMode')
    interval = config['DEFAULT']['Interval']

    if config['FACEBOOK']['Enabled'] == 'True':
        scrape(Facebook, config, interval, strictmode)
    reactor.run()


process = CrawlerRunner(
    settings={"FEEDS": {"hits.json": {"format": "json", "overwrite": False}, }, "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36)'})  # Kijiji has anti scraping method using the user agent


def scrape(spider, config, interval, strictmode, city_id):
    # Facebook behaves differently with another user agent
    process_for_facebook = CrawlerRunner(
        settings={"FEEDS": {"hits.json": {"format": "json", "overwrite": False}}})
    task = LoopingCall(lambda: process_for_facebook.crawl(
        spider, config, strictmode))
    task.start(60 * int(interval))


main()
