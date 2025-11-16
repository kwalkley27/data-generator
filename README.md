# data-generator

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)

An app that allows users to generate sample data by defining fields with natural language.

**Example Use Case:**
Define fields like `name: realistic first and last names` and `email: professional email addresses`, then generate 100 records of synthetic data instantly.

## Features

- Natural language field definitions
- Generate 1-100 records at once
- Download data in JSON format
- Powered by Google's Gemini AI
- Simple, intuitive Streamlit interface

## Installation

**Requirements:** Python 3.9 or higher

1. Clone the repository:
   ```bash
   git clone https://github.com/kwalkley27/data-generator.git
   cd data-generator
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

2. Open the app in your browser (usually http://localhost:8501)

3. Define your data schema:
   - Enter field names (e.g., "name", "email", "age")
   - Describe the values you want (e.g., "realistic full names", "corporate emails", "ages between 25-65")

4. Enter the number of records to generate (1-100)

5. Click "Submit" to generate the data

6. Click "Download" to save the data to your Downloads folder

## Example

See the [examples/](examples/) directory for sample outputs.

## Troubleshooting

**Error: "GEMINI_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**App won't start**
- Verify Python 3.9+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
