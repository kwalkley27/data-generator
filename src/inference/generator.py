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
from langchain_google_genai import ChatGoogleGenerativeAI


def format_user_input(input:list[dict]):
    schema = dict()

    for field in input:
        if field['col1'] in schema:
            raise ValueError('ERROR: Cannot define the same field twice')
        else:
            schema[field['col1']] = field['col2']

    return str(schema)

def generate_data_sample(num_records:str, input_user_schema:str):
    
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=GOOGLE_API_KEY,
        response_format={"type": "json_object"}
    )

#    num_records = 5
#
#    input_user_schema = '''
#            {
#                'src': ip,
#                'dst': ip,
#                'src_port': int between 1-65535,
#                'dst_port': int between 1-65535,
#                'protocol': enum either FOO or BAR,
#                'bytes': int
#            }
#
#        '''
    
    response = llm.invoke(f'''Generate {str(num_records)} example records with the following format.
                            
                          Format: {input_user_schema}

                          The output should be formatted as line delimited json only.
                          Respond ONLY with valid JSON. Do not use markdown code blocks or triple backticks.
                          
                          ''')
    
    return response.content
