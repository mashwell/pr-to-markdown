# GitHub PR to Markdown Converter

## Overview

This application fetches details from a GitHub Pull Request (PR) and converts them into a comprehensive Markdown summary. This allows for easy offline viewing, sharing, or archiving of PR information.

## Features

The generated Markdown summary includes:

- PR Title
- Link to the original GitHub Repository
- PR Author
- PR Creation Date
- PR Status (Open, Closed, Merged)
- PR Description
- Issue Comments
- Inline Review Comments
- Overall Review Summaries (Approved, Changes Requested, Commented)
- File Changes:
  - Full source code diffs for each changed file.
  - Option to list only filenames without the diffs.

### Input Options

- **GitHub PR URL**: The URL of the pull request you want to process.
- **GitHub Token (Optional)**: Your GitHub Personal Access Token. Providing a token is recommended to avoid API rate limits, especially for frequent use or when accessing private repositories.
- **Include full source code diff**: A checkbox (ticked by default) that controls whether the full diff for each changed file is included in the output. If unticked, only the names of the changed files will be listed.

## Dependencies

- **Python**: Python 3.10 is recommended.
  - *Note for Windows users*: Transitive dependencies (like `aiohttp`, which may be pulled in by one of the primary dependencies) can have compilation issues with newer Python versions on Windows. Using Python 3.10 is strongly advised to avoid these problems.
- **Libraries**:
  - `streamlit`
  - `PyGithub`

You can install these dependencies using the provided `requirements.txt` file.

## How to Run

1. **Clone the repository (if you haven't already):**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    This will open the application in your web browser.
