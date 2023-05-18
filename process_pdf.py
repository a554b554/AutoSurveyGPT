import requests
import io
from PyPDF2 import PdfReader
import openai
import config
import prompt
import gpt_config
import json
import logging
from logging_config import setup_logging

def download_pdf(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a valid response
    return io.BytesIO(response.content)

def extract_first_n_words(pdf_stream, n):
    pdf = PdfReader(pdf_stream)
    text = ''
    for page in range(len(pdf.pages)):
        content = pdf.pages[page].extract_text()
        text += ' ' + content
    words = text.split()
    ans = ' '.join(words[:n])
    return str(ans.encode('utf-8', errors='ignore'))


def extract_sections(pdf_text):
    logging.info('extracting sections using openai')
    openai.api_key = config.openai_api_key
    res = openai.ChatCompletion.create(
        model=gpt_config.pdf_extraction_model,
        messages=prompt.pdf_section_extraction_prompt(pdf_text)
    )

    ans = res['choices'][0]['message']['content']
    logging.info('openai raw ans: '+ans)
    ans = json.loads(ans, strict=False)

    return ans


def main():
    setup_logging()
    url = 'https://dl.acm.org/doi/pdf/10.1145/3544548.3580991'
    

    pdf_stream = download_pdf(url)
    first_n_words = extract_first_n_words(pdf_stream, n=5000)
    logging.info('first n words extracted: '+first_n_words)
    ans = extract_sections(first_n_words)
    # logging.info('extracted output: '+str(ans)) 
    json_object = json.dumps(ans, indent=4)
    with open("output/pdf_extract_sample.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    main()
