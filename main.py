# MIT License

# Copyright (c) 2023 Chang Xiao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
from logging_config import setup_logging
from query_processor import QueryProcessor
import json




def main():
    parser = argparse.ArgumentParser(description="AutoSurveyGPT Main Program")

    # Add arguments to the parser
    parser.add_argument('-i', '--input', type=str, help="path of input json query", required=True)

    # Parse the arguments
    args = parser.parse_args()

    setup_logging()

    with open(args.input, 'r') as file:
        data = json.load(file)
    qp = QueryProcessor(data)
    qp.initiate_search()


if __name__ == '__main__':
    main()
