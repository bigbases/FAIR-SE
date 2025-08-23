import requests
import pandas as pd
import os
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import botocore
import boto3
import random
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Serverless_Functions.aws_update import LambdaUpdater

current_dir = os.path.dirname(os.path.abspath(__file__))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json(file_name):
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        return json.load(file)

def invoke_lambda(client, arn, payload, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = client.invoke(FunctionName=arn, Payload=payload, InvocationType="RequestResponse")
            return json.loads(response['Payload'].read().decode('utf-8'))
        except Exception as e:
            logging.error(f"Error invoking Lambda function ARN: {arn} (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

def search_results_store(num, topic, search_history_type, perspective, aws, created_date):
    arn = aws['arn']
    region = aws['region']
    logging.info(f"Storing search results: topic={topic}, type={search_history_type}, perspective={perspective}, num={num}, ARN={arn}")

    source_list, title_list, content_list, url_list, page_list, rake_list = [], [], [], [], [], []

    session = boto3.session.Session()
    client_config = botocore.config.Config(
        read_timeout=100, 
        connect_timeout=100, 
        retries={"max_attempts": 3}
    )
    client = session.client('lambda',
                            aws_access_key_id="",
                            aws_secret_access_key="",
                            config=client_config,
                            region_name=region)

    start = 0
    while True:
        try:
            import browser_cookie3
            cookie_file = load_json('cookies.json')[perspective]
            cookies = browser_cookie3.chrome(domain_name='google.com', cookie_file=cookie_file['file'])
            cookies = {cookie.name: cookie.value for cookie in cookies}
            headers = load_json('headers.json')[perspective]
            
            topic_params = {
                'q': topic,
                'tbm': 'nws',
                'start': str(start) if start > 0 else None,
            }
            topic_params = {k: v for k, v in topic_params.items() if v is not None}
            
            url = 'https://www.google.com/search'
            payload = json.dumps({
                "url": url,
                "params": topic_params,
                "cookies": cookies,
                "headers": headers
            })
            
            response = invoke_lambda(client, arn, payload)
            if not response:
                logging.warning(f"No response from Lambda function ARN: {arn} for topic={topic}, perspective={perspective}")
                break

            soup = BeautifulSoup(response['body'], 'html.parser')
            results = soup.find_all('div', class_='SoaBEf')

            if not results:
                logging.info(f"No results found: start={start}, perspective={perspective}, ARN={arn}")
                LambdaUpdater().update_lambda_functions(region, arn)

            elif results:
                for result in results:
                    try:
                        source = result.find('div', class_='MgUUmf NUnG9d')
                        source = source.text.strip() if source else ""
                        source_list.append(source)

                        title = result.find('div', class_='n0jPhd ynAwRc MBeuO nDgy9d')
                        title = title.text.replace("\n", "").strip() if title else 'Title Not Found'
                        title_list.append(title)

                        content = result.find('div', class_='GI74Re nDgy9d')
                        content = content.text.replace("\n", "").strip() if content else ""
                        content_list.append(content)

                        url_block = result.find('a', class_='WlydOe')
                        url = url_block['href'] if url_block else ""
                        url_list.append(url)

                        page_list.append(start // 10 + 1)
                        rake_list.append(len(title_list))
                        
                        if len(title_list) > 50 or start > 50:
                            break
                    except Exception as e:
                        logging.error(f"Error processing result for ARN {arn}: {str(e)}")
                        continue
                
                logging.info(f"ARN={arn}, perspective={perspective}, num={num}, page={start//10 + 1}, count={len(title_list)}, title={title[:30]}")
                start += 10
                time.sleep(random.uniform(60, 90))

            if len(title_list) > 50 or start > 50:
                break

        except Exception as e:
            logging.error(f"Error in search_results_store for ARN {arn}: {str(e)}")
            LambdaUpdater().update_lambda_functions(region, arn)
            time.sleep(random.uniform(60, 90))
            continue

    search_results_dir_path = os.path.join(current_dir, f"../../dataset/{created_date}/google_news/search_history")
    os.makedirs(search_results_dir_path, exist_ok=True)
    
    df = pd.DataFrame({
        'page': page_list,
        'rank': rake_list,
        'source': source_list,
        'title': title_list,
        'content': content_list,
        'url': url_list
    })
    
    csv_path = f"{search_results_dir_path}/{topic}_{search_history_type}_{perspective}_{num+1}.csv"
    df.to_csv(csv_path, index=False)
    logging.info(f"Data saved to {csv_path} for ARN {arn}")

def fetch_data(topic, search_history_type, perspective, search_terms, aws, created_date):
    arn = aws['arn']
    region = aws['region']
    logging.info(f"Fetching data: topic={topic}, type={search_history_type}, perspective={perspective}, ARN={arn}")

    session = boto3.session.Session()
    client_config = botocore.config.Config(
        read_timeout=100, 
        connect_timeout=100, 
        retries={"max_attempts": 3}
    )
    client = session.client('lambda',
                            aws_access_key_id="",
                            aws_secret_access_key="",
                            config=client_config,
                            region_name=region)

    for num, term in enumerate(search_terms[:50]):
        try:
            import browser_cookie3
            cookie_file = load_json('cookies.json')[perspective]
            cookies = browser_cookie3.chrome(domain_name='google.com', cookie_file=cookie_file['file'])
            cookies = {cookie.name: cookie.value for cookie in cookies}
            headers = load_json('headers.json')[perspective]

            logging.info(f"Processing term {num}: {term}, ARN={arn}")
            
            search_history_params = {
                'q': term,
            }
            
            url = 'https://www.google.com/search'
            payload = json.dumps({
                "url": url,
                "params": search_history_params,
                "cookies": cookies,
                "headers": headers
            })
            
            response = invoke_lambda(client, arn, payload)
            if not response:
                logging.warning(f"No response from Lambda function ARN: {arn} for term={term}")
                continue

            soup = BeautifulSoup(response['body'], 'html.parser')
            results = soup.find_all('div', class_='MjjYud')

            if not results:
                logging.info(f"No results found for term: {term}, ARN={arn}")
                LambdaUpdater().update_lambda_functions(region, arn)
            else:
                for idx, result in enumerate(results[:5]):
                    try:
                        title = result.find('h3', class_='LC20lb MBeuO DKV0Md')
                        title = title.text.replace("\n", "").strip() if title else 'Title Not Found'
                        
                        url_block = result.select('div.kb0PBd.cvP2Ce.jGGQ5e > div > div > span > a')
                        url_ping = url_block[0].get('ping') if url_block else None
                        
                        if url_ping:
                            redic_url = f"https://www.google.com{url_ping}"
                            
                            interaction_payload = json.dumps({
                                "url": redic_url,
                                "params": None,
                                "cookies": cookies,
                                "headers": headers
                            })
                            invoke_lambda(client, arn, interaction_payload)
                            time.sleep(random.uniform(15, 20))
                            logging.info(f"Interaction {idx} for term {num}: {title[:30]}, ARN={arn}")
                    except Exception as e:
                        logging.error(f"Error processing result {idx} for term {num}, ARN={arn}: {str(e)}")
                        continue

            if num in [9, 29, 49]:
                search_results_store(num, topic, search_history_type, perspective, aws, created_date)
                
        except Exception as e:
            logging.error(f"Error processing term {num}, ARN={arn}: {str(e)}")
            LambdaUpdater().update_lambda_functions(region, arn)
            time.sleep(random.uniform(60, 90))
            continue

    logging.info(f"Completed fetching data for {topic} - {search_history_type} - {perspective}, ARN={arn}")


def process_group(organized_data, aws, created_date):
    with ThreadPoolExecutor(max_workers=60) as executor:
        futures = []
        aws_index = 0

        for topic_type, search_terms_dict in organized_data.items():
            topic, search_history_type = topic_type.split('_', 1)
            for perspective, terms in search_terms_dict.items():
                future = executor.submit(fetch_data, topic, search_history_type, perspective, terms, aws[aws_index], created_date)
                futures.append(future)
                aws_index = (aws_index + 1) % len(aws)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"An error occurred in a thread: {str(e)}")

    logging.info("Completed processing all topics and perspectives")

def start(created_date):
    df = pd.read_csv(os.path.join(current_dir,'../search_history.csv'))

    organized_data = {}
    for column in df.columns:
        topic_type, perspective = column.rsplit('_', 1)
        if topic_type not in organized_data:
            organized_data[topic_type] = {}
        organized_data[topic_type][perspective] = df[column].dropna().tolist()

    with open(os.path.join(current_dir, '../aws_functions.json')) as f:
        aws = json.load(f)
    
    aws_functions = aws['us-west-1']

    process_group(organized_data, aws_functions, created_date)