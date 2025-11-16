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
import platform
import time
import logging
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


def get_default_download_folder() -> Path:
    '''Returns the default Downloads folder path for the current operating system'''
    system = platform.system()  # 'Windows', 'Linux', 'Darwin'

    try:
        if system == "Windows":
            path = Path(os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"))
        elif system == "Darwin":  # macOS
            path = Path(os.path.join(os.environ.get("HOME", ""), "Downloads"))
        elif system == "Linux":
            path = Path(os.path.join(os.environ.get("HOME", ""), "Downloads"))
        else:
            raise RuntimeError(f"Unsupported OS: {system}")

        # Verify the directory exists
        if not path.exists():
            logger.warning(f"Downloads folder does not exist: {path}")
            raise RuntimeError(f"Downloads folder not found: {path}")

        logger.info(f"Using downloads folder: {path}")
        return path

    except Exception as e:
        logger.error(f"Error getting download folder: {str(e)}")
        raise


def write_string_to_file(download_path:Path, contents:str) -> str:
    '''Writes content to a file with a timestamp-based filename'''
    if not contents:
        raise ValueError("Cannot write empty content to file")

    if not download_path.exists():
        raise ValueError(f"Download path does not exist: {download_path}")

    try:
        file_path = download_path / f'sample_{int(time.time())}.json'
        logger.info(f"Writing data to file: {file_path}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(contents)

        logger.info(f"Successfully wrote data to {file_path}")
        return str(file_path)

    except IOError as e:
        logger.error(f"Error writing to file: {str(e)}")
        raise RuntimeError(f"Failed to write file: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error writing file: {str(e)}")
        raise


def write_string_to_downloads(contents:str) -> str:
    '''Writes content to a file in the default Downloads folder'''
    try:
        download_folder = get_default_download_folder()
        return write_string_to_file(download_folder, contents)
    except Exception as e:
        logger.error(f"Error writing to downloads: {str(e)}")
        raise
