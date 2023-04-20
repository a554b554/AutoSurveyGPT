# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT


import scholar_parser
import urllib.parse
from logging_config import setup_logging
import logging
import json
from website_parser import GenericWebsiteParser
import os


class QueryProcessor:
    def __init__(self, query:dict) -> None:
        self.initial_query = query
        self.gsparse = scholar_parser.GScholarParser()
        self.task_queue = [] #queue of GSEntry
        self.reported_task_id = 0
        self.current_task_id = 0
        self.website_parser = GenericWebsiteParser()
        self.rel_thre =self.initial_query['relevance_threshold']

    def initiate_search(self):
        keywords = self.initial_query['search_query']
        initial_url = QueryProcessor.gen_gs_search(keywords)
        # self.task_queue += self.gsparse.visit_url(initial_url)

        # while len(self.task_queue)<self.initial_query['search_breadth']:
        #     logging.info('parsed papers: '+str(len(self.task_queue))+' '+str(self.task_queue[-1]))
        #     if self.task_queue[-1].metadata['next_page_url'] == "":
        #         break
        #     self.task_queue += self.gsparse.visit_url(self.task_queue[-1].metadata['next_page_url'])
        
        # if self.task_queue > self.initial_query['search_breadth']:
        #     self.task_queue = self.task_queue[:self.initial_query['search_breadth']]

        # logging.info('total parsed papers: '+str(len(self.task_queue)))

        self.gs_search(initial_url, depth=1)
        print('initial parsing done')
        
        while self.validate_search():
            self.perform()
        self.write_report()

    def validate_search(self):
        if self.reported_task_id<self.initial_query['max_papers'] and self.current_task_id<len(self.task_queue):
            return True
        elif self.reported_task_id>=self.initial_query['max_papers']:
            logging.info('Searching ended due to reached maximum number of paper.')
            print('Searching ended due to reached maximum number of paper.')
            return False
        elif self.current_task_id>=len(self.task_queue):
            logging.info('Searching ended due to no task added. Try to use different keywords and search again.')
            print('Searching ended due to no task added. Try to use different keywords and search again.')
            return False
        else:
            print('Searching ended due to unknown reason.')
            return False


    def gs_search(self, url, depth=1, repeat_flag=False):

        len_before = len(self.task_queue)

        if repeat_flag:
            self.task_queue += self.gsparse.visit_url(url, depth)[1:]
        else:
            self.task_queue += self.gsparse.visit_url(url, depth)

        
        while len(self.task_queue)-len_before<self.initial_query['search_breadth']:
            logging.info('parsed papers: '+str(len(self.task_queue)-len_before)+' last paper: '+str(self.task_queue[-1]))
            if self.task_queue[-1].metadata['next_page_url'] == "":
                break
            self.task_queue += self.gsparse.visit_url(self.task_queue[-1].metadata['next_page_url'], depth)

        
        if len(self.task_queue)-len_before > self.initial_query['search_breadth']:
            self.task_queue = self.task_queue[:len_before+self.initial_query['search_breadth']]

        logging.info('total parsed papers: '+str(len(self.task_queue)-len_before)+' at depth: '+str(depth))
        

    def perform(self):
        logging.debug("current id:"+str(self.current_task_id)+" done id:"+str(self.reported_task_id))
        logging.debug('grand total paper in list:'+str(len(self.task_queue)))
        current_task = self.task_queue[self.current_task_id]
        
        if current_task.metadata['pub_url'] is not None:
            parsing_results = self.website_parser.visit_url_and_parse(current_task.metadata['pub_url'])
        
        if parsing_results is None:
            current_task.process_status = 1
        else:
            current_task.process_status = 2
            current_task.fetch_parsing_results(parsing_results)
            current_task.notes = GenericWebsiteParser.read_abstract_by_gpt(current_task.abstract, self.initial_query['my_topic'])


            #update queue
            if int(current_task.notes['Score']) >= self.rel_thre and len(self.task_queue)<self.initial_query['max_papers']:
                self.update_queue_by_cited(current_task)
                self.update_queue_by_related(current_task)


        self.current_task_id += 1

        if self.current_task_id % 5 == 0:
            self.write_report()


    def update_queue_by_cited(self, task):
        if task.depth >= self.initial_query['search_depth_cited']:
            return
        elif task.metadata['cited_by_url'] == "":
            return
        else:
            self.gs_search(task.metadata['cited_by_url'], depth=task.depth+1)

    def update_queue_by_related(self, task):
        if task.depth >= self.initial_query['search_depth_related']:
            return
        elif task.metadata['related_url'] == "":
            return
        else:
            self.gs_search(task.metadata['related_url'], depth=task.depth+1, repeat_flag=True)
        

    def write_report(self):
        output_path = self.initial_query['output_file']
        while self.reported_task_id < self.current_task_id:
            task = self.task_queue[self.reported_task_id]
            report = {}
            report['title'] = task.metadata['title']
            report['authors'] = task.authors
            report['venue'] = task.venue
            report['depth'] = task.depth
            if task.process_status != 2:
                report['notes'] = "Parsing failed. Please read paper manually."
            else:
                report['notes'] = task.notes
            json_string = json.dumps(report, indent=4)


            # Check if the file exists and is not empty
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                # If the file exists and is not empty, append a newline character
                with open(output_path, "a") as file:
                    file.write("\n")

            # Append the JSON string to the file
            with open(output_path, "a") as file:
                file.write(json_string)

            self.reported_task_id += 1
        return
        


    @staticmethod
    def gen_gs_search(keywords:str):
        base_url = "https://scholar.google.com/scholar?q="
        encoded_query = urllib.parse.quote(keywords)
        google_scholar_url = base_url + encoded_query
        return google_scholar_url
    

def test_url():
    setup_logging()
    a = QueryProcessor.gen_gs_search("deep learning augmented reality")
    print(a)

    pass


def test_query():
    setup_logging()
    with open('query1.json', 'r') as file:
        data = json.load(file)
    qp = QueryProcessor(data)
    qp.initiate_search()

if __name__ == "__main__":
    test_query()