import os
from dotenv import load_dotenv

load_dotenv()

def check_for_src(potential_filename: str) -> str:
    """
    If current working directory ends with 'src', prefix filename with '..' to go up a directory.
    """
    cwd = os.getcwd()
    if cwd.endswith("src"):
        return os.path.join("..", potential_filename)
    return potential_filename

"""
PROTOTYPE FUNCTION CHECK_FOR_SRC
#Make a function to append to file names based on src? To add ..\ if they need to go back up on directory
def check_for_src(potential_filename):
    cwd = os.getcwd()
    if_src = cwd[-3:]
    if(if_src == "src"):
        potential_filename = "..\\" + potential_filename
    return potential_filename
"""

def get_env_var(key: str) -> str:
    """
    Safely get environment variable with fallback to empty string.
    """
    return os.getenv(key, "")
