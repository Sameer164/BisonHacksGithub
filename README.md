# Video Demo

[![Watch the video](https://img.youtube.com/vi/kJlVKYKef_o/0.jpg)](https://www.youtube.com/watch?v=kJlVKYKef_o)





# Interactive Notebook System

Inspired by Notebook LM, this Streamlit-based application lets users upload PDFs, extract key content, and generate personalized study plans with minimal manual input. But in addition to the features provided by Notebook LM, we support splitting and distributing content over weeks incorporating spaced repetition, and ensuring that users get to learn what they want as effectively and quickly as possible. We also support various LLMs like OpenAI, Anthropic, Claude, and whisper, so the user can select the LLM best trained/suited for their needs. 

## Features

- **PDF Notebook Creation:**  
  Upload one or more PDFs to automatically create a notebook.

- **Automated Content Transformations:**  
  - **Summaries:** Quick and dense summaries.  
  - **Table of Contents Extraction:** Automatically fetch the document's structure.  
  - **Document Analysis & Reflections:** Generate insights with fixed prompts.  
  - **Interactive Q&A:** Ask questions and receive links to specific PDF sections.

- **Generate Personalized Study Plan:**  
  A three-phase process using user-selected AI models:
  1. **Weekly Breakdown:** Analyze the table of contents for a week-by-week plan.
  2. **Detailed Notes:** Generate comprehensive notes for each week.
  3. **Quizzes:** Create quizzes for spaced repetition learning.

- **Data Storage:**  
  Notebooks, notes, and study plans are stored as `Source` objects (with title and content) in SurrealDB, hosted on a separate Docker container.

## Technology Stack

- **Frontend:** Streamlit  
- **Backend:** Python with integrated AI models  
- **LLM Integration:** Langchain is used to prompt different LLM APIs, currently supporting Google Gemini, OpenAI, Anthropic, and Claude.  
- **Database:** SurrealDB (Dockerized)


## How to use
Head over here: https://985e-138-238-254-99.ngrok-free.app


## How to install

```
poetry install
docker compose --profile db_only up
poetry run streamlit run Auth.py

```
