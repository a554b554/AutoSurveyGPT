# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT
# This function will attempt to find a pdf link given a paper title

from query_processor import QueryProcessor
from bs4 import BeautifulSoup
from selenium import webdriver
from gpt_config import get_driver_path
import logging
import time
import random
from logging_config import setup_logging

class PDFFinder:
    def __init__(self, title:str) -> None:
        self.browser = webdriver.Chrome(executable_path=get_driver_path())
        self.browser.implicitly_wait(5)
        self.logger = logging.getLogger(__name__)
        self.gs_url = QueryProcessor.gen_gs_search(title)
        

    def findPDFURL(self):
        '''find PDF url given a paper title, return None if no pdf url found.'''
        
        #timeout set for preventing anti-bot trigger
        # time.sleep(random.randint(6, 30))
        self.browser.get(self.gs_url)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})
        if len(res)==0:
            logging.debug('no gs record found.')
            self.browser.quit()
            return None
        
        div_html  = res[0]
        #extract all url
        soup = BeautifulSoup(str(div_html), 'html.parser')
        urls = soup.find_all('a')

        # print(urls)

        #check if contains pdf link
        for url in urls:
            link = url.get('href')
            if 'pdf' in link:
                logging.debug('pdf link found in direct gs entry: '+link)
                self.browser.quit()
                return link
        

        #no pdf link found, go to all version link
        for url in urls:
            link = url.get('href')
            if '/scholar?cluster' in link:
                logging.debug('pdf link not found, go to all versions')
                ans = self.parse_cluster(link)
                self.browser.quit()
                return ans

        return None

    def parse_cluster(self, cluster_url):
        self.browser.get("https://scholar.google.com"+cluster_url)
        html = self.browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        urls = soup.find_all('a')

        #if contains pdf
        for url in urls:
            link = url.get('href')
            if 'pdf' in link:
                logging.debug('pdf link found in version: '+link)
                return link

        #if contains arxiv
        for url in urls:
            link = url.get('href')
            if 'arxiv.org' in link:
                a = link.replace('abs', 'pdf')
                logging.debug('pdf link found in arxiv: '+a)
                return a


        #otherwise nothing found
        return None



def unit_test():
    setup_logging()
    engine = PDFFinder("")
    url = engine.findPDFURL()
    print(url)

    pass

if __name__ == "__main__":
    unit_test()

