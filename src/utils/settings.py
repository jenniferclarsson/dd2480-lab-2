import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

test_folder=".."
test_file_pattern="*tests.py"
test_output_file="./tests.log"

repo_dir = Path('/tmp/cloned-repo-to-be-tested/')
repo_dir_src = Path('/tmp/cloned-repo-to-be-tested/src')

GIT_USER = os.getenv('GIT_USER')
GIT_TOKEN = os.getenv('GIT_TOKEN')
GIT_REPO_OWNER = os.getenv('GIT_REPO_OWNER')
GIT_REPO = os.getenv('GIT_REPO')
GIT_SHA = os.getenv('GIT_SHA')
GIT_BROKEN_SHA = os.getenv('GIT_BROKEN_SHA')