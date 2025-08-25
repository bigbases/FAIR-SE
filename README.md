# FAIR-SE: Fairness Analysis in Search Engines

FAIR-SE is a comprehensive framework for analyzing fairness and bias in search engine results across different user contexts, search engines, and topics. This project employs a multi-layered approach to collect, analyze, and statistically verify bias patterns in search results.

## Publication
**Paper Title:** FAIR-SE: Framework for Analyzing Information Disparities in Search Engines with Diverse LLM-Generated Personas 
**Authors:** Jaebeom You, Seung-Kyu Hong, Ling Liu, Kisung Lee, Hyuk-Yoon Kwon  
**Conference:** Proceedings of the 34th ACM International Conference on Information and Knowledge Management  
**Year:** 2025  
**DOI:** ---
**Published:** November 10--14, 2025 
**Link:** --

## Project Overview

Search engines are critical information gatekeepers that shape how users access and perceive information online. However, various user contexts (such as language settings, geographic location, browser environment, and search history) can potentially influence search results, leading to personalization bubbles or systematic biases. FAIR-SE provides a systematic methodology to detect, quantify, and analyze such biases.

## Architecture

The project consists of four main modules, each handling a specific aspect of the fairness analysis:

```
FAIR-SE/
├── Context-Aware Concurrent Data Collection/    # Data collection from search engines
├── LLM Persona-based Data Analyzation/          # Analysis of collected data using LLMs
├── Statistical Significance Verification/        # Statistical testing of bias patterns
├── Prompt/                                      # Prompt templates for LLM analysis
└── datasets/                                     # Storage for collected and processed data
```

## Modules

### 1. Context-Aware Concurrent Data Collection

This module systematically collects search results from multiple search engines (Google, Bing) under various simulated user contexts.

Key features:
- Simulation of different language preferences (`accept_language`)
- Simulation of different geographic regions (`region`)
- Simulation of different browser environments (`user_agent`)
- Simulation of different search histories (`search_history`)
- Serverless architecture using AWS Lambda for distributed collection
- Concurrent data collection with error handling and retry mechanisms

This module creates a comprehensive dataset of search results across different user contexts, which serves as the foundation for subsequent analysis.

### 2. LLM Persona-based Data Analyzation

This module uses Large Language Models (LLMs) like Claude and ChatGPT to analyze the collected search results from multiple political and stance perspectives.

Key features:
- Multi-dimensional analysis (Political, Stance, Subjectivity, Bias)
- Multi-perspective evaluation using four personas:
  - Left-leaning opposed (opp_left)
  - Right-leaning opposed (opp_right)
  - Left-leaning supportive (sup_left)
  - Right-leaning supportive (sup_right)
- Structured JSON output with quantitative scores
- Robust parsing and caching mechanisms
- Handles multiple LLM models (Claude, ChatGPT)

This module transforms raw search results into structured, multi-dimensional data that can be statistically analyzed.

### 3. Statistical Significance Verification

This module applies rigorous statistical methods to verify whether observed differences in search results across user contexts are statistically significant.

Key features:
- Normality and homogeneity testing
- Parametric (ANOVA) and non-parametric (Kruskal-Wallis) testing
- Effect size calculation
- Multiple comparison corrections (Bonferroni, Benjamini-Hochberg)
- Visualization of statistical trends
- Comprehensive error handling and NaN management

This module provides scientific evidence for the presence or absence of search engine bias across different user contexts.

### 4. Prompt

This module provides various prompt templates and guidelines used for LLM analysis.

Key features:
- Persona definitions for diverse political perspectives (left/right, opposed/supportive)
- Structured evaluation guidelines for search result analysis
- Guidelines and examples for search history simulation
- Consistent LLM output format definitions

This module helps LLMs analyze search results in a consistent and systematic manner.

## Data Flow

1. **Collection**: The Context-Aware Concurrent Data Collection module gathers search results from multiple search engines under various user contexts.

2. **Storage**: Results are stored in the `datasets` directory, organized by date, search engine, and context type.

3. **Analysis**: The LLM Persona-based Data Analyzation module processes the collected data, evaluating each search result across multiple dimensions and perspectives.

4. **Statistical Testing**: The Statistical Significance Verification module performs rigorous statistical testing to determine the significance of observed patterns.

5. **Visualization**: Results are visualized to highlight significant bias patterns and trends.

## Research Questions

FAIR-SE addresses the following key research questions:

1. Do search engines deliver different results based on user contexts?
2. Are there systemic political or topical biases in search results?
3. How do these biases vary across different search engines?
4. Which user contexts have the most significant impact on search results?
5. Are these differences statistically significant with meaningful effect sizes?

## Usage

Each module has its own README.md with detailed instructions on setup and usage. In general, the modules should be run in sequence:

1. First, collect data using the Context-Aware Concurrent Data Collection module
2. Then, analyze the collected data using the LLM Persona-based Data Analyzation module
3. Finally, perform statistical verification using the Statistical Significance Verification module

## Requirements

- Python 3.7+
- AWS account (for serverless functions)
- API keys for supported LLMs (Claude, ChatGPT)
- Required Python packages (see individual module READMEs)

## Sample Topics

The project includes analysis for several controversial topics:
- Russia Ukraine
- Trump Harris
- Israel Hamas
- Immigration
- Abortion
- LGBT
- Marijuana

## Future Work

Potential extensions to the FAIR-SE framework include:
- Support for additional search engines
- More granular user context simulations
- Advanced visualization and interactive dashboards
- Longitudinal analysis to track bias patterns over time
- Integration with browser extensions for real-user context analysis

## Note

This project is designed for research purposes to understand potential biases in search engines. The goal is to contribute to more transparent and fair information access systems.
