# Job Fetcher Application

This repository contains a Python application and a GitHub Actions workflow to fetch job listings from the City Football Group careers page and email the list if there are new job postings.

## GitHub Secrets Setup

To run this application, you need to set up the following GitHub secrets in your repository:

- `EMAIL_ADDRESS`: The email address to send the job listings from and to.
- `EMAIL_USER`: The email account username.
- `EMAIL_PASSWORD`: The email account password.

## Running the Script Locally

To run the script locally, follow these steps:

1. Create a virtual environment in the local `.venv` directory:
    ```sh
    python -m venv .venv
    ```

2. Activate the virtual environment:
    - On Windows:
        ```sh
        .venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install Playwright:
    ```sh
    playwright install
    ```

5. Set the required environment variables:
    ```sh
    export EMAIL_ADDRESS='your_email@example.com'
    export EMAIL_USER='your_email_username'
    export EMAIL_PASSWORD='your_email_password'
    ```

6. Run the script:
    ```sh
    python main.py
    ```
