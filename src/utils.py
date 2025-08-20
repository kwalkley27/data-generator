import os
import platform
import time 
from pathlib import Path

def get_default_download_folder() -> Path:
    system = platform.system()  # 'Windows', 'Linux', 'Darwin'
    
    if system == "Windows":
        return Path(os.path.join(os.environ.get("USERPROFILE", ""), "Downloads"))
    elif system == "Darwin":  # macOS
        return Path(os.path.join(os.environ.get("HOME", ""), "Downloads"))
    elif system == "Linux":
        return Path(os.path.join(os.environ.get("HOME", ""), "Downloads"))
    else:
        raise RuntimeError(f"Unsupported OS: {system}")
    
def write_string_to_file(download_path:Path, contents:str):
    file_path = f'{download_path}/sample_{str(int(time.time()))}'
    with open(file_path, 'w') as f:
        f.write(contents)

def write_string_to_downloads(contents:str):
    write_string_to_file(get_default_download_folder(), contents)