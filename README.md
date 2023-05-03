# ELEN6889_Final_Project
- A streaming processing project about NBA games based on [Twitter API](https://developer.twitter.com/en).
- Mainly focus on sentiment analysis by location and time.

## How to Run

1. Install all dependencies
  - ```pip install -r requirements.txt```
2. Run flask only
  - ```cd webpage/flask```
  - ```python3 __init__.py```
3. Note that for Big Query: (if you find errors about Big Query)
  - in local you should connect your CLI to your google account 
  - or in gcp you should give your account IAM permission and export like this:
  - ```export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key-file.json"```

  
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

## About Screenshot

![ce063309ccb94acaa15b5416bfcec53](https://user-images.githubusercontent.com/42087697/235928047-dc6e0532-0183-4403-afeb-830e9b9e0336.png)

![56f8d63c832f2ff9c0b285c90d500d8](https://user-images.githubusercontent.com/42087697/235927643-abb20d31-9891-4464-a532-fbfaf33feacc.png)

![4f0af2d8b70892293674bdeafc4224f](https://user-images.githubusercontent.com/42087697/235927824-4d430ee6-0cc4-46b1-8ea7-d34096ef8812.png)

![image](https://user-images.githubusercontent.com/42087697/235928633-652e2449-e05d-47af-a1dc-01a2c2bc5a7a.png)

![image](https://user-images.githubusercontent.com/42087697/235928479-50727c4d-829d-48f2-b272-8093c8da1a93.png)

![e03052096b11c5c68c8a89ae8702c87](https://user-images.githubusercontent.com/42087697/235927880-cdb651e9-1c15-4042-b60d-8016da48ae89.png)

![6814876c822c360846dcd1bcf7e273f](https://user-images.githubusercontent.com/42087697/235927733-43fc3f4e-8eb3-44e7-a39d-5ec0c1fa04a7.png)
