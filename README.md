# AutoSurveyGPT

AutoSurveyGPT is an open-source program for parsing Google Scholar and finding related work using GPT-3.5 Turbo/GPT-4. It searches for relevant papers based on a user-provided search query and generates a report containing a list of related papers and their relevance scores.

## Features

- Parse Google Scholar search results
- Extract information (title, authors, venue, abstract) from individual papers
- Analyze abstracts using OpenAI GPT (Analyze PDF in development)
- Generate relevance scores for each paper based on a user-provided topic
- Search for cited and related papers and analyze them recursively
- Generate a JSON report containing a list of relevant papers and their scores

## Prerequisites

- Python 3.7 or later
- `selenium` library
- `beautifulsoup4` library
- `openai` library
- A valid OpenAI API key
- ChromeDriver (for Selenium)

## Setup

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/AutoSurveyGPT.git
cd AutoSurveyGPT
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Place your ChromeDriver executable in the `driver` folder.

4. Set your OpenAI API key in the `config.py` file:

```python
openai_api_key = "your_openai_api_key"
```

## Usage

1. Create a JSON file containing your search query and configuration. Here's an example:

```json
{
  "search_query": "deep learning",
  "my_topic": "Deep learning applied in natural language processing",
  "search_breadth": 10,
  "search_depth_cited": 2,
  "search_depth_related": 2,
  "relevance_threshold": 3,
  "max_papers": 50,
  "output_file": "output/report.json"
}
```

2. Run the `main.py` script with the input JSON file:

```bash
python main.py -i path/to/your/input.json
```

3. The program will generate a JSON report in the specified output file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
