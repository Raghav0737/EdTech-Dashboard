# Placement Readiness Dashboard

An AI-powered web application designed to help students and professionals evaluate their job readiness. This tool analyzes resumes, simulates an ATS, aggregates coding profiles, and conducts mock interviews to provide comprehensive feedback for job applicants.

## Features

*   **AI-Powered Resume Analysis:** Upload your resume to receive instant, AI-generated feedback on its content, structure, and job readiness.
*   **ATS Score Simulation:** Get an Applicant Tracking System (ATS) score based on how well your resume matches a given job description.
*   **Coding Profile Aggregation:** Fetches and displays your statistics from popular coding platforms like LeetCode, GitHub, and Codeforces.
*   **Certificate Verification:** Automatically verifies the authenticity of your online certificates from platforms like Credly and Unstop.
*   **AI-Powered Mock Interviews:** Generates tailored interview questions based on the job description and evaluates your recorded audio answers using speech-to-text and AI analysis.

## Architecture Overview

The application is built using a monolithic architecture with a Flask backend. It follows a clear separation of concerns between the presentation, application, and service layers.

```
+---------------------------------------------------------------------------------+
|                                  User's Browser                                 |
| (HTML, CSS, JavaScript)                                                         |
+---------------------------------------------------------------------------------+
       | (HTTP Requests: Resume Upload, Form Submissions, API Calls)
       v
+---------------------------------------------------------------------------------+
|                      Application Server (Gunicorn + Flask)                      |
|---------------------------------------------------------------------------------|
|                                    main.py                                      |
| (Routing, Session Management, Request/Response Handling)                        |
|---------------------------------------------------------------------------------|
|                                   Service Layer (`utils/`)                      |
|                                                                                 |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+ |
|  |    llms.py      |  |     ats.py      |  |    stats.py     |  |  answer.py   | |
|  | (LangChain,    |  | (scikit-learn)  |  | (Platform APIs) |  | (AssemblyAI) | |
|  |  Google Gemini) |  |                 |  |                 |  |              | |
|  +-----------------+  +-----------------+  +-----------------+  +--------------+ |
+---------------------------------------------------------------------------------+
       | (API Calls to External Services)
       v
+---------------------------------------------------------------------------------+
|                               External Services                                 |
|---------------------------------------------------------------------------------|
| - Google Gemini API (for AI)                                                    |
| - AssemblyAI API (for Transcription)                                            |
| - LeetCode, GitHub, etc. APIs (for Stats)                                       |
| - Credly, Unstop, etc. (for Verification)                                       |
| - Sentry (for Error Monitoring)                                                 |
+---------------------------------------------------------------------------------+
```

## Project Structure

The project is organized into the following directories:

```
.
├── main.py             # Main Flask application file (routing and orchestration)
├── requirements.txt    # Project dependencies
├── vercel.json         # Configuration for Vercel deployment
├── .env                # (To be created) For storing environment variables
├── static/             # Frontend assets
│   ├── placement.css   # Custom stylesheets
│   └── js/
│       └── placement.js# Custom JavaScript
├── templates/          # Jinja2 HTML templates for the UI
│   ├── index.html      # Landing page
│   ├── dashboard.html  # Main results dashboard
│   └── ...
├── utils/              # Core application logic and services
│   ├── llms.py         # Handles all interactions with the Gemini LLM
│   ├── ats.py          # Calculates the ATS score
│   ├── stats.py        # Fetches data from coding platforms
│   ├── answer.py       # Handles audio transcription via AssemblyAI
│   ├── verification.py # Verifies certificates
│   └── prompt.py       # Stores all LLM prompt templates
└── uploads/            # Default directory for storing uploaded resumes
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the environment file:**
    Create a file named `.env` in the root directory and add the necessary API keys:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    DSN="YOUR_SENTRY_DSN_URL"
    # Add other keys if needed (e.g., for AssemblyAI)
    ```

## Usage

To run the application locally, use the following command:

```bash
flask run
```

Or directly run the main Python file:

```bash
python main.py
```

Navigate to `http://127.0.0.1:5000` in your web browser.

## Key Dependencies

*   **Flask:** Web framework for the backend.
*   **LangChain:** Framework for developing applications powered by language models.
*   **google-generativeai:** Python client for the Google Gemini API.
*   **scikit-learn:** For calculating the TF-IDF based ATS score.
*   **AssemblyAI:** For speech-to-text transcription.
*   **Requests:** For making HTTP requests to external APIs.
*   **Gunicorn:** WSGI HTTP Server for UNIX-like systems.
