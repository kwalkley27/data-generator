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
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import get_default_download_folder, write_string_to_file, write_string_to_downloads


class TestGetDefaultDownloadFolder(unittest.TestCase):
    """Test cases for get_default_download_folder function"""

    @patch('pathlib.Path.exists')
    @patch('platform.system')
    def test_macos(self, mock_system, mock_exists):
        """Test on macOS (Darwin)"""
        mock_system.return_value = 'Darwin'
        mock_exists.return_value = True
        with patch.dict(os.environ, {'HOME': '/Users/testuser'}):
            result = get_default_download_folder()
            self.assertEqual(result, Path('/Users/testuser/Downloads'))

    @patch('pathlib.Path.exists')
    @patch('platform.system')
    def test_linux(self, mock_system, mock_exists):
        """Test on Linux"""
        mock_system.return_value = 'Linux'
        mock_exists.return_value = True
        with patch.dict(os.environ, {'HOME': '/home/testuser'}):
            result = get_default_download_folder()
            self.assertEqual(result, Path('/home/testuser/Downloads'))

    @patch('pathlib.Path.exists')
    @patch('platform.system')
    def test_windows(self, mock_system, mock_exists):
        """Test on Windows"""
        mock_system.return_value = 'Windows'
        mock_exists.return_value = True
        with patch.dict(os.environ, {'USERPROFILE': 'C:\\Users\\testuser'}):
            result = get_default_download_folder()
            # Path normalizes separators, so compare strings
            self.assertTrue(str(result).endswith('Downloads'))
            self.assertIn('testuser', str(result))

    @patch('platform.system')
    def test_unsupported_os(self, mock_system):
        """Test with unsupported OS"""
        mock_system.return_value = 'UnsupportedOS'
        with self.assertRaises(RuntimeError) as context:
            get_default_download_folder()
        self.assertIn('Unsupported OS', str(context.exception))


class TestWriteStringToFile(unittest.TestCase):
    """Test cases for write_string_to_file function"""

    def setUp(self):
        """Create a temporary directory for tests"""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Remove the temporary directory after tests"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_successful_write(self):
        """Test successful file write"""
        content = '{"name": "John Doe", "email": "john@example.com"}'
        file_path = write_string_to_file(self.test_dir, content)

        self.assertTrue(Path(file_path).exists())
        with open(file_path, 'r') as f:
            written_content = f.read()
        self.assertEqual(written_content, content)

    def test_empty_content(self):
        """Test with empty content"""
        with self.assertRaises(ValueError) as context:
            write_string_to_file(self.test_dir, "")
        self.assertIn('Cannot write empty content', str(context.exception))

    def test_nonexistent_directory(self):
        """Test with non-existent directory"""
        nonexistent_dir = Path('/nonexistent/directory')
        with self.assertRaises(ValueError) as context:
            write_string_to_file(nonexistent_dir, "test content")
        self.assertIn('does not exist', str(context.exception))

    def test_filename_format(self):
        """Test that filename includes timestamp and .json extension"""
        content = '{"test": "data"}'
        file_path = write_string_to_file(self.test_dir, content)

        filename = Path(file_path).name
        self.assertTrue(filename.startswith('sample_'))
        self.assertTrue(filename.endswith('.json'))


class TestWriteStringToDownloads(unittest.TestCase):
    """Test cases for write_string_to_downloads function"""

    @patch('utils.get_default_download_folder')
    @patch('utils.write_string_to_file')
    def test_successful_write_to_downloads(self, mock_write, mock_get_folder):
        """Test successful write to downloads folder"""
        mock_folder = Path('/Users/test/Downloads')
        mock_get_folder.return_value = mock_folder
        mock_write.return_value = str(mock_folder / 'sample_123.json')

        content = '{"test": "data"}'
        result = write_string_to_downloads(content)

        mock_get_folder.assert_called_once()
        mock_write.assert_called_once_with(mock_folder, content)
        self.assertEqual(result, str(mock_folder / 'sample_123.json'))


if __name__ == '__main__':
    unittest.main()
