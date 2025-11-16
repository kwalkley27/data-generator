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

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inference.generator import format_user_input, generate_data_sample


class TestFormatUserInput(unittest.TestCase):
    """Test cases for format_user_input function"""

    def test_valid_input(self):
        """Test with valid field definitions"""
        input_data = [
            {'col1': 'name', 'col2': 'realistic full names'},
            {'col1': 'email', 'col2': 'professional email addresses'}
        ]
        result = format_user_input(input_data)
        self.assertIn('name', result)
        self.assertIn('email', result)
        self.assertIn('realistic full names', result)

    def test_empty_input(self):
        """Test with empty input list"""
        with self.assertRaises(ValueError) as context:
            format_user_input([])
        self.assertIn('No fields provided', str(context.exception))

    def test_duplicate_field_names(self):
        """Test with duplicate field names"""
        input_data = [
            {'col1': 'name', 'col2': 'first description'},
            {'col1': 'name', 'col2': 'second description'}
        ]
        with self.assertRaises(ValueError) as context:
            format_user_input(input_data)
        self.assertIn('Cannot define the same field twice', str(context.exception))

    def test_empty_field_name(self):
        """Test with empty field name"""
        input_data = [
            {'col1': '', 'col2': 'some description'}
        ]
        with self.assertRaises(ValueError) as context:
            format_user_input(input_data)
        self.assertIn('Field name cannot be empty', str(context.exception))

    def test_whitespace_field_name(self):
        """Test with whitespace-only field name"""
        input_data = [
            {'col1': '   ', 'col2': 'some description'}
        ]
        with self.assertRaises(ValueError) as context:
            format_user_input(input_data)
        self.assertIn('Field name cannot be empty', str(context.exception))

    def test_missing_column(self):
        """Test with missing col1 or col2"""
        input_data = [
            {'col1': 'name'}  # Missing col2
        ]
        with self.assertRaises(ValueError) as context:
            format_user_input(input_data)
        self.assertIn('Invalid field structure', str(context.exception))


class TestGenerateDataSample(unittest.TestCase):
    """Test cases for generate_data_sample function"""

    def test_missing_api_key(self):
        """Test when API key is not set"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                generate_data_sample(10, "{'name': 'test'}")
            self.assertIn('GEMINI_API_KEY not found', str(context.exception))

    def test_invalid_num_records_too_low(self):
        """Test with num_records < 1"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with self.assertRaises(ValueError) as context:
                generate_data_sample(0, "{'name': 'test'}")
            self.assertIn('between 1 and 100', str(context.exception))

    def test_invalid_num_records_too_high(self):
        """Test with num_records > 100"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with self.assertRaises(ValueError) as context:
                generate_data_sample(101, "{'name': 'test'}")
            self.assertIn('between 1 and 100', str(context.exception))

    def test_empty_schema(self):
        """Test with empty schema"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with self.assertRaises(ValueError) as context:
                generate_data_sample(10, "")
            self.assertIn('Schema cannot be empty', str(context.exception))

    @patch('inference.generator.ChatGoogleGenerativeAI')
    def test_successful_generation(self, mock_llm_class):
        """Test successful data generation"""
        # Mock the LLM response
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '{"name": "John Doe"}'
        mock_llm.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            result = generate_data_sample(10, "{'name': 'test'}")
            self.assertEqual(result, '{"name": "John Doe"}')
            mock_llm.invoke.assert_called_once()


if __name__ == '__main__':
    unittest.main()
