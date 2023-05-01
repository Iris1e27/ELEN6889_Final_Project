# ELEN6889_Final_Project
- A streaming processing project about NBA games based on [Twitter API](https://developer.twitter.com/en).
- Mainly focus on sentiment analysis by location and time.

## How to Run

1. Install all dependencies
  - ```pip install -r requirements.txt```
2. Run flask only
  - ```cd webpage/flask```
  - ```python3 __init__.py```
  
## About Requirements

- Data/Input
  - What data sources will you use?
  - Will the data be stored and replayed, or pulled in live?
  - Do you need to create new connectors to access the data?
- Techniques/Application
  - What is the problem you will solve?
  - Is there a set of references that motivate this?
  - Do you need to integrate other tools?
- Results
  - How will you present your results?
  - What will you show as a demo?
- Next Steps
  - Will you use any algorithms from class? 
  - Will you use any optimizations? 

## About Implementation

### Dataset

- We query several [team names](https://github.com/Iris1e27/ELEN6889_Final_Project/blob/master/dataset/teams.txt) as hashtags to get streaming data during 4/13/2023-4/21/2023 (because we have ELEVATED level twitter api so we only can search about recent 7 days), and finally we use [this csv](https://github.com/Iris1e27/ELEN6889_Final_Project/blob/master/dataset/mergedAllWithHeader.csv) for the further analysis.
- Also because there is a limit when using twitter api, if it exceeds the limit, we wait for 15 min and then repeat until all teams done.

### Analysis

- We use Spark streaming, using 30 min as a start time interval and 1 h as a duration to analyze data, as you can see [here](https://github.com/Iris1e27/ELEN6889_Final_Project/blob/master/analysis/6889_streaming_analysis.ipynb)
- Also we try a smaller interval, using 30 min as a start time interval and 30 min as a duration to analyze data, as you can see [here](https://github.com/Iris1e27/ELEN6889_Final_Project/blob/master/analysis/streaming_method_NBA.py)

### Webpage

- We use Flask as our web framework, and some html frontpages written by [Jinjia](https://jinja.palletsprojects.com/en/3.1.x/).
- For the frontend design, we use [this](https://bootstrapmade.com/demo/Reveal/) as our template.
- For plot design, we post info from '/plot', and generate graphs by [this](https://github.com/Iris1e27/ELEN6889_Final_Project/blob/master/webpage/flask/plotBigQuery.py) python script, then show them on the same page.

## About GCP deployment

1. We run cluster (3 masters, 2 workers) on GCP to analyze our streaming data, save the results in Google Cloud Storage (GCS) and combine them into one csv.
2. Then import data to Big Query and save as a table, also write a .py file to query from the result.
3. Run a VM instance to deploy our web app and set up environment. 

## About Results

- Some codes and graphs showing the information we get
- An interactive web app to query streaming data and generate graphs
