# Context-Aware Concurrent Data Collection

This module collects search results from multiple search engines (Google, Bing) under various simulated user contexts to study the impact of user context on search engine behavior and potential biases.

## Overview

The Context-Aware Concurrent Data Collection module is designed to systematically gather search results across different search engines while simulating various user contexts such as language preferences, geographic regions, browser environments, and search histories. This enables comprehensive analysis of how search engines adapt their results based on user context.

## Architecture

```
Context-Aware Concurrent Data Collection/
├── 1_central_manager.py           # Central management and scheduling system
├── 2_url_to_content.py            # Full content extraction from URLs
├── Serverless_Functions/          # AWS Lambda functions for HTTP requests
├── aws_functions.json             # AWS configuration information
├── search_history.csv             # Search history data
├── bing_news/                     # Bing news search module
├── google_news/                   # Google news search module
```

Each search engine module contains identical structure:

```
{engine}_{type}/
├── accept_language.json       # Language settings
├── cookies.json               # Cookie configurations
├── create_acceptlanguage.py   # Language-based data collection
├── create_region.py           # Region-based data collection
├── create_searchhistory.py    # Search history-based data collection
├── create_useragent.py        # User agent-based data collection
├── headers.json               # HTTP headers information
└── user_agent.json            # User agent strings
```

## Context Methods

The system simulates four different user contexts:

1. **Accept-Language**: Simulates different language preference settings
   - Supported languages: "en-US", "ja-JP", "ko-KR", "fr-FR", "en-GB", "zh-CN"
   - Uses specialized HTTP headers for each language
   - Saves results to `/dataset/{created_date}/{engine}/accept_language/`

2. **Region**: Simulates different geographic locations
   - Supported regions: 'us-west-1', 'us-east-2', 'ap-northeast-2', 'ap-northeast-1', 'eu-west-2', 'eu-west-3'
   - Uses region-specific AWS Lambda functions
   - Saves results to `/dataset/{created_date}/{engine}/region/`

3. **User-Agent**: Simulates different browser/OS environments
   - Uses various user agent strings
   - Applies user agent-specific HTTP headers
   - Saves results to `/dataset/{created_date}/{engine}/user_agent/`

4. **Search History**: Simulates previous search context
   - Uses different search history patterns from `search_history.csv`
   - Patterns include: direct_support, direct_neutral, direct_oppose, indirect_support, indirect_neutral, indirect_oppose
   - Saves results to `/dataset/{created_date}/{engine}/search_history/`

## URL Content Extraction

The URL content extraction system (`2_url_to_content.py`) processes the URLs collected from search results to extract detailed content:

- **Full Content Retrieval**: Extracts complete article text, images, and metadata from each URL
- **Content Parsing**: Uses specialized parsers for different news sources and content types
- **Error Handling**: Manages connection issues, paywalls, and anti-scraping measures
- **Data Enrichment**: Enhances search result data with full article content
- **Output Format**: Saves detailed content to `/dataset/{created_date}/{engine}/{method}/detailed/{topic}_{context}.csv`

## Serverless Architecture

Data collection is performed through AWS Lambda serverless functions:

- `lambda_function.py`: Core function for handling HTTP requests
- `aws_update.py`: Lambda function updater
- `aws_functions.json`: AWS Lambda function configuration

## Central Management System

The central management system (`1_central_manager.py`) integrates and schedules various search engine modules and context methods:

- Creates data collection tasks for each service (bing_news, google_news)
- Uses thread-based execution for concurrency management
- Implements daily scheduling (runs at 14:18 every day)
- Includes comprehensive logging system

## Data Collection Process

1. Load topic data (from `topic.csv`)
2. For each combination of search engine and context method:
   - Select appropriate AWS Lambda function
   - Set request parameters, headers, cookies
   - Perform search request via Lambda function
   - Parse response HTML to extract relevant data
   - Handle pagination (up to 50 results or 5 pages)
   - Save results to CSV file
3. Update Lambda function and retry in case of errors
4. Process search results through `2_url_to_content.py` to retrieve full content from each URL
5. Save and log all results after collection completes

## Concurrency and Performance Management

- Parallel data collection using ThreadPoolExecutor (max 60 threads)
- Round-robin allocation for load balancing between Lambda functions
- Random delays (60-90 seconds) between requests
- Exponential backoff retry strategy for AWS Lambda functions
- Automatic Lambda function update mechanism

## Search Engine Implementation Differences

While all search engines follow the same structure, they have specific implementations:

### Google News vs Bing News:
- **HTML Parsing Differences**:
  - Bing News: `news-card newsitem cardcommon` class
  - Google News: `SoaBEf` class
- **Parameter Differences**:
  - Bing News: `q`, `first`, `FORM=HDRSC7` 
  - Google News: `q`, `tbm=nws`, `start`
- **Cookie Management**:
  - Google News: Additional random cookie selection
- **Pagination Method Differences**

### Search vs News:
- **Parsing Pattern Differences**: General search and news search have different HTML structures
- **Header and Cookie Configuration**: Optimized per search type
- **Result Format Differences**: News includes source information, while general search includes different metadata

## Usage

1. **Setup AWS Configuration**:
   - Configure AWS Lambda functions in `aws_functions.json`
   - Ensure proper IAM permissions are set

2. **Configure Search Topics**:
   - Edit `topic.csv` with your search queries

3. **Run Data Collection**:
   ```
   python 1_central_manager.py
   ```

4. **Scheduled Operation**:
   - The system is configured to run automatically at 14:18 daily
   - Modify the schedule in `1_central_manager.py` if needed

5. **For Full Content Extraction**:
   ```
   python 2_url_to_content.py
   ```

6. **Output Data**:
   - Search results are saved to `/dataset/{created_date}/{engine}/{method}/{topic}_{context}.csv`
   - Each search CSV contains columns: page, rank, source, title, content, url
   - Full content extraction results are saved to `/dataset/{created_date}/{engine}/{method}/detailed/{topic}_{context}.csv`
   - Detailed content includes full article text, additional metadata, and content analysis

## Requirements

- Python 3.7+
- Required packages:
  - requests
  - pandas
  - beautifulsoup4
  - boto3
  - schedule
  - browser_cookie3
  - concurrent.futures

## Notes

- The system implements random delays and user agent rotation to avoid detection/blocking
- AWS Lambda functions are automatically updated when errors occur
- Data collection is limited to 50 results per context to manage resource consumption
- Cookie management varies between search engines to match their specific requirements
- Content extraction respects robots.txt and implements appropriate rate limiting