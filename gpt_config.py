import os

gen_query_model = "gpt-3.5-turbo"
html_parse_model = "gpt-4"
abstract_parse_model = "gpt-3.5-turbo"
pdf_extraction_model = "gpt-3.5-turbo"

def get_driver_path():
    if os.name == 'nt':
        return 'driver/chromedriver.exe'
    else:
        return 'driver/chromedriver'