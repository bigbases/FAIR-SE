# Prompt Collection for LLM and Search Analysis

This repository contains a set of structured prompts designed for the annotation, summary, and analysis of search results using LLM (Large Language Models). The files aim to facilitate tasks such as political leaning, stance detection, subjectivity classification, bias measurement, sentiment analysis, and filter bubble investigation. Below is a description of each file and its purpose.

## Files Overview

### 1. **search_history_prompt.txt**

- **Description:**
    
    This prompt defines guidelines for creating search history queries reflecting different user perspectives (supportive, neutral, opposing) for a given topic. The objective is to simulate diverse viewpoints to study search result behaviors.
    
- **Key Elements:**
    - Definition of perspectives (Support, Neutral, Oppose)
    - Examples for topics like *Climate Change* and *Healthcare Reform*
    - Instructions for generating 50 search history terms per perspective


### 2. **prompt_role_supportive_left.txt**

- **Description:**
    
    This prompt defines the persona of a user who supports left-leaning perspectives. Annotators label articles based on criteria such as political leanings, sentiment, subjectivity, and bias while reflecting this persona.
    
- **Key Elements:**
    - Labeling guidelines for four criteria (Political, Stance, Subjectivity, Bias)
    - Output in JSON format
    - Examples for topics like *Biden*, *Trump*, and *Immigration*

### 3. **prompt_role_supportive_right.txt**

- **Description:**
    
    This prompt defines the persona of a user who supports right-leaning perspectives. Annotators label articles based on criteria such as political leanings, sentiment, subjectivity, and bias while reflecting this persona.
    
- **Key Elements:**
    - Labeling guidelines for four criteria (Political, Stance, Subjectivity, Bias)
    - Output in JSON format
    - Examples for topics like *Biden*, *Trump*, and *Immigration*

### 4. **prompt_role_opposed_left.txt**

- **Description:**
    
    This prompt defines the persona of a user who opposes left-leaning perspectives. Annotators label articles based on criteria such as political leanings, sentiment, subjectivity, and bias while reflecting this persona.
    
- **Key Elements:**
    - Labeling guidelines for four criteria (Political, Stance, Subjectivity, Bias)
    - Output in JSON format
    - Examples for topics like *Biden*, *Trump*, and *Immigration*

### 5. **prompt_role_opposed_right.txt**

- **Description:**
    
    This prompt defines the persona of a user who opposes right-leaning perspectives. Annotators label articles based on criteria such as political leanings, sentiment, subjectivity, and bias while reflecting this persona.
    
- **Key Elements:**
    - Labeling guidelines for four criteria (Political, Stance, Subjectivity, Bias)
    - Output in JSON format
    - Examples for topics like *Biden*, *Trump*, and *Immigration*

## Usage

### 1. **Search History Simulation**

Use `search_history_prompt.txt` to create hypothetical search queries reflecting multiple viewpoints on topics of interest. These can help study the influence of search engine algorithms on results based on user perspectives.

### 2. **LLM-Based Summary and Analysis**

Utilize `llm_summary_prompt.txt` for summarizing datasets by categorizing user behaviors, analyzing political and sentiment-based trends, and investigating filter bubble formation.

### 3. **Annotation Tasks**

- Refer to `prompt_role_supportive_left.txt`, `prompt_role_supportive_right.txt`, `prompt_role_opposed_left.txt`, and `prompt_role_opposed_right.txt` to annotate news articles based on the defined personas.
- These prompts provide tailored instructions for consistent and nuanced labeling, enabling analysis of diverse perspectives.
