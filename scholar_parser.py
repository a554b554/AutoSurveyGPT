# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT


from selenium import webdriver
from bs4 import BeautifulSoup
import logging
from logging_config import setup_logging
import re
import time

class GScholarParser:
    def __init__(self, driver_path="driver/chromedriver.exe") -> None:
        self.browser = webdriver.Chrome(executable_path=driver_path)
        self.logger = logging.getLogger(__name__)
        
    def visit_url(self, url, depth=1):
        gsentries = []

        #timeout set for preventing anti-bot trigger
        time.sleep(3)
        self.browser.get(url)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})
        self.logger.info("found "+str(len(res))+" records in url.")

        next_page_html = soup.find(id="gs_n")
        next_page_urls = next_page_html.find_all('a')
        next_page_url = next_page_urls[-1].get('href')
        logging.info('getting next page url:'+str(next_page_url))


        for i in range(len(res)):
            gs = self.register_gsentry(div_html=str(res[i]))
            gs.depth = depth
            if next_page_url is not None:
                gs.set_next_page_url("https://scholar.google.com"+next_page_url)
            gsentries.append(gs)
        
        for i in range(len(gsentries)):
            self.logger.debug('parsed gs entries:'+str(gsentries[i]))

        return gsentries

    def register_gsentry(self, div_html):
        soup = BeautifulSoup(div_html, 'html.parser')
        self.logger.debug('input div html: '+str(div_html))


        title_html = soup.find('h3', attrs={'class': 'gs_rt'})
        
        #remove patterns in title
        title = title_html.text
        pattern = r'\[PDF\]|\[B\]|\[BOOK\]'
        title = re.sub(pattern, '', title).strip()

        pub_url = title_html.find("a").get("href")
        self.logger.debug('title:'+title)
        self.logger.debug('pub_url:'+str(pub_url))



        url_list = soup.find_all('a')
        cited_by_url = ""
        related_url = ""
        version_url = ""
        for url in url_list:
            link = url.get("href")
            if "/scholar?cites" in link:
                cited_by_url = "https://scholar.google.com"+link
                self.logger.debug("cited by: "+cited_by_url)
            elif "/scholar?q=related" in link:
                related_url = "https://scholar.google.com"+link
                self.logger.debug("related: "+related_url)
            elif "/scholar?cluster" in link:
                version_url = link
            else:
                pass
        
        gs = GSEntry(title, pub_url, cited_by_url, related_url, version_url)
        return gs



class GSEntry:
    def __init__(self, title, pub_url, cited_by_url, related_url, version_url) -> None:
        self.metadata = {
            'title': "",
            'pub_url': "",
            'cited_by_url': "",
            'related_url': "",
            "version_url": "",
            'next_page_url': ""
        }
        self.metadata['title'] = title
        self.metadata['pub_url'] = pub_url
        self.metadata['cited_by_url'] = cited_by_url
        self.metadata['related_url'] = related_url
        self.metadata['version_url'] = version_url

        self.title = ""
        self.authors = []
        self.venue = ""
        self.abstract = ""  #extracted abstract from paper
        self.notes = {}      #parsed by gpt on how this paper is related to user's topic

        self.depth = 0
        self.priority = 0
        self.process_status = 0 # 0 unprocessed, 1 process failed, 2 process successful
        pass

    def __str__(self) -> str:
        return str(self.metadata)

    def set_next_page_url(self, url):
        self.metadata['next_page_url'] = url

    def fetch_parsing_results(self, results):
        self.title = results['title']
        self.authors = results['authors']
        self.venue = results['venue']
        self.abstract = results['abstract']
        pass


    

def unit_test():
    setup_logging()
    parser = GScholarParser()
    parser.visit_url('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=augmented+reality&btnG=&oq=augmente')

if __name__ == "__main__":
    unit_test()