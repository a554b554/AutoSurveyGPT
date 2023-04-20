# Copyright (c) 2023 Chang Xiao
# SPDX-License-Identifier: MIT

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import logging
from logging_config import setup_logging
import re
import config
import openai
import json
import time
from scholar_parser import GScholarParser, GSEntry

class GenericWebsiteParser:
    def __init__(self, driver_path="driver/chromedriver") -> None:
        self.browser = webdriver.Chrome(driver_path)
        self.browser.implicitly_wait(5)
        self.logger = logging.getLogger(__name__)
        
  
    def visit_url_and_parse(self, url):
        """
        This function parse url and return the paper information.

        Parameters:
        url (str): The target url to be parsed.

        Returns:
        dict: A dict contains paper title, authors, venue and abstract.
        """
        if url.endswith('.pdf'):
            return self.parse_pdf(url)


        self.browser.get(url)
        logging.debug('Processing url: '+url)
        html = self.browser.page_source
        txt = self.browser.find_element(By.XPATH, "/html/body").text
        # self.logger.info('extracted text for '+url+': '+txt)

        ans = GenericWebsiteParser.parsing_html_by_gpt(txt)
        return ans

    def parse_pdf(self, url, text_len_limit=10000):
        return None


    @staticmethod
    def parsing_html_by_gpt(html_text, text_len_limit=10000, max_tryout=3):
        openai.api_key = config.openai_api_key
        if len(html_text)>=text_len_limit:
            html_text = html_text[0:text_len_limit]

        tryout = 0
        while tryout<max_tryout:
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are a document parser, I want to you extract information in a text document"},
                        {"role": "user", "content": "This is a text document extracted from a webpage: ["+html_text+"] can you extract paper title, paper author, publication venue, and abstract from the document? Please return the answer in a json format, the keys in json are <title>, <authors>, <venue>, <abstract>. Please make sure to extract the full abstract."},
                    ]
            )
            ans = res['choices'][0]['message']['content']
            try:
                jans = json.loads(ans, strict=False)
                print('gpt ans:'+str(jans))
                logging.info("gpt ans: "+str(jans))
                return jans
            except json.decoder.JSONDecodeError as e:
                logging.debug(str(e))
                logging.debug('information extracted failed. ans:'+str(ans))
                logging.debug('input html text:'+str(html_text))
                tryout += 1
        return None

        

    def parsing_html_by_rule(self, html_text):
        raise NotImplementedError

    @staticmethod
    def read_abstract_by_gpt(abstract:str, prompt:str, max_tryout=3):
        """
        This function parse the abstract based on the prompt.

        Parameters:
        abstract (str): The target abstract to be parsed.
        prompt (str): The instruction on how to parse the abstract.

        Returns:
        str: Parsing results.
        """
        tryout = 0
        while tryout<max_tryout:
            logging.info("tryout: "+str(tryout)+". Analyzing abstract for "+abstract)
            openai.api_key = config.openai_api_key
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are an academic researcher's assistant, I want to you read a paper and tell me whether it is relevant to my idea or not."},
                        {"role": "user", "content": "Here is the abstract of a paper: ["+abstract+"]. Here is the description of my paper:["+prompt+"].  Please read them and answer my question: [Q1: What are the similarities between this paper and my idea? Q2: What are the difference between the paper and my idea? Q3: Please provide a similarity score from 1 to 5, where a higher score indicates greater relevance between two research papers. Use the following calibration for the scores: 1 - Not relevant: Papers from different fields with no shared methodologies or insights, e.g., one paper on natural language processing and the other on computer graphics. 2 - Somewhat relevant: Papers from the same subfield, such as adversarial learning, neural rendering, or tangible input interfaces. 3 - Relevant: Papers addressing similar problems (e.g., increasing the robustness of adversarial learning, tangible input interfaces in AR), or using similar methodologies to solve different problems. Papers with this level of similarity should be considered for citation. 4 - Very relevant: Papers addressing similar problems and using similar techniques. 5 - Mostly relevant: Papers addressing almost identical problems and using similar techniques.] Please provide your answer in .json format, the keys are <Similarity>, <Difference>, <Score>"},
                    ]
            )

            ans = res['choices'][0]['message']['content']
            try:
                ans = json.loads(ans, strict=False)
                # print('gpt ans for similarity:'+str(ans))
                logging.info("gpt ans for similarity: "+str(ans))
                return ans
            except json.decoder.JSONDecodeError as e:
                logging.debug('output parsing failed for input: '+abstract)
                tryout += 1

        return None

def unit_test():
    setup_logging()
    parser= GenericWebsiteParser()
    parser.visit_url_and_parse('https://arxiv.org/abs/2304.08448')



def unit_test_prompt():
    my_topic = "This paper presents a comprehensive survey of ChatGPT and GPT-4, state-of-the-art large language models (LLM) from the GPT series, and their prospective applications across diverse domains. Indeed, key innovations such as large-scale pre-training that captures knowledge across the entire world wide web, instruction fine-tuning and Reinforcement Learning from Human Feedback (RLHF) have played significant roles in enhancing LLMs' adaptability and performance. We performed an in-depth analysis of 194 relevant papers on arXiv, encompassing trend analysis, word cloud representation, and distribution analysis across various application domains. The findings reveal a significant and increasing interest in ChatGPT/GPT-4 research, predominantly centered on direct natural language processing applications, while also demonstrating considerable potential in areas ranging from education and history to mathematics, medicine, and physics. This study endeavors to furnish insights into ChatGPT's capabilities, potential implications, ethical concerns, and offer direction for future advancements in this field."

    abstract = "The digitization of healthcare has facilitated the sharing and re-using of medical data but has also raised concerns about confidentiality and privacy. HIPAA (Health Insurance Portability and Accountability Act) mandates removing re-identifying information before the dissemination of medical records. Thus, effective and efficient solutions for de-identifying medical data, especially those in free-text forms, are highly needed. While various computer-assisted de-identification methods, including both rule-based and learning-based, have been developed and used in prior practice, such solutions still lack generalizability or need to be fine-tuned according to different scenarios, significantly imposing restrictions in wider use. The advancement of large language models (LLM), such as ChatGPT and GPT-4, have shown great potential in processing text data in the medical domain with zero-shot in-context learning, especially in the task of privacy protection, as these models can identify confidential information by their powerful named entity recognition (NER) capability. In this work, we developed a novel GPT4-enabled de-identification framework (\"DeID-GPT\") to automatically identify and remove the identifying information. Compared to existing commonly used medical text data de-identification methods, our developed DeID-GPT showed the highest accuracy and remarkable reliability in masking private information from the unstructured medical text while preserving the original structure and meaning of the text. This study is one of the earliest to utilize ChatGPT and GPT-4 for medical text data processing and de-identification, which provides insights for further research and solution development on the use of LLMs such as ChatGPT/GPT-4 in healthcare. Codes and benchmarking data information are available at this https URL."

    ans = GenericWebsiteParser.read_abstract_by_gpt(abstract, my_topic)
    print(ans)
    pass

if __name__ == "__main__":
    unit_test_prompt()