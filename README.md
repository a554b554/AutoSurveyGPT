# AutoSurveyGPT

AutoSurveyGPT is an open-source program for parsing Google Scholar and finding related work using GPT-3.5 Turbo (default)/GPT-4. It searches for relevant papers based on a user-provided idea description and generates a report containing a list of related papers and their relevance scores.

## Features

- Parse Google Scholar search results
- Extract information (title, authors, venue, abstract) from individual papers
- Analyze abstracts using OpenAI GPT (Analyze PDF in development)
- Generate relevance scores for each paper based on a user-provided topic
- Search for cited and related papers and analyze them recursively
- Generate a JSON report containing a list of relevant papers and their scores

### Features under Development
- Parsing PDFs: Extract the introduction section for comparison with the provided description, and the related work section for identifying other relevant studies.
- Pause and resume paper hunting at any time.

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

```python
{
  "search_query": "deep learning for novel view synthesis ", #The input keywords that will be used on your google scholar search
  "my_topic": "We present a method for novel view synthesis from input images that are freely distributed around a scene. Our method does not rely on a regular arrangement of input views, can synthesize images for free camera movement through the scene, and works for general scenes with unconstrained geometric layouts. We calibrate the input images via SfM and erect a coarse geometric scaffold via MVS. This scaffold is used to create a proxy depth map for a novel view of the scene. Based on this depth map, a recurrent encoder-decoder network processes reprojected features from nearby views and synthesizes the new view. Our network does not need to be optimized for a given scene. After training on a dataset, it works in previously unseen environments with no fine-tuning or per-scene optimization. We evaluate the presented approach on challenging real-world datasets, including Tanks and Temples, where we demonstrate successful view synthesis for the first time and substantially outperform prior and concurrent work.", #Try to describ your idea as detail as possible, like a paper abstract. This will be used to compare with existing papers found online.
  "search_breadth": 10, # how many paper to search in a single round
  "search_depth_cited": 2, # how many round of search for paper in cited by 
  "search_depth_related": 2, # how many round of search for paper in related
  "relevance_threshold": 3, # The relevance score that will determine whether a paper should be search for its cited by paper and related paper.
  "max_papers": 50, #maximum number of paper to analyze
  "output_file": "output/report.ndjson"
}
```

2. Run the `main.py` script with the input JSON file:

```bash
python main.py -i path/to/your/input.ndjson
```

3. The program will generate a JSON report in the specified output file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

Please be aware that:

1. When using the OpenAI API, you are responsible for managing your own costs. Be mindful of the usage and potential expenses associated with the API calls. On average, analyzing one paper takes around 2,000 tokens. Setting search_breadth and depth too large can result in a significant increase in API call costs. Adjust these parameters carefully.

2. Scraping Google Scholar or other website may violate its terms of service. By using this tool, you acknowledge that you understand and accept any potential risks and consequences associated with scraping. Please use this feature responsibly and in compliance with applicable policies.