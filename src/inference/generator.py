# Copyright 2025 Kyle Walkley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


def format_user_input(input:list[dict]) -> str:
    '''Takes the streamlit generated list of fields and value descriptions and formats
    it into a dictionary string for easy processing'''
    if not input:
        raise ValueError('ERROR: No fields provided')

    schema = dict()

    for field in input:
        # Validate field structure
        if 'col1' not in field or 'col2' not in field:
            raise ValueError('ERROR: Invalid field structure')

        # Check for empty field names
        if not field['col1'] or not field['col1'].strip():
            raise ValueError('ERROR: Field name cannot be empty')

        # Check for duplicate field names
        if field['col1'] in schema:
            raise ValueError(f'ERROR: Cannot define the same field twice: "{field["col1"]}"')

        schema[field['col1']] = field['col2']

    return str(schema)

def generate_data_sample(num_records:int, input_user_schema:str) -> str:
    '''Submits a formatted prompt and returns the structured model output containing
    the sample data'''
    # Validate API key exists
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GOOGLE_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment variables")
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in your .env file. "
            "Get your API key from: https://makersuite.google.com/app/apikey"
        )

    # Validate inputs
    if num_records < 1 or num_records > 100:
        raise ValueError("Number of records must be between 1 and 100")

    if not input_user_schema or not input_user_schema.strip():
        raise ValueError("Schema cannot be empty")

    try:
        logger.info(f"Generating {num_records} records with schema: {input_user_schema}")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.7,
            google_api_key=GOOGLE_API_KEY,
            response_format={"type": "json_object"}
        )

        response = llm.invoke(f'''Generate {num_records} example records with the following format.

                              Format: {input_user_schema}

                              The output should be formatted as line delimited json only.
                              Respond ONLY with valid JSON. Do not use markdown code blocks or triple backticks.

                              ''')

        logger.info("Successfully generated data sample")
        return response.content

    except Exception as e:
        logger.error(f"Error generating data sample: {str(e)}")
        raise RuntimeError(f"Failed to generate data: {str(e)}")
