import os

from dotenv import load_dotenv


load_dotenv()


def get_command_prefix():
    prefix = os.getenv('DEV_CMD')
    if prefix:
        return prefix
    else:
        return "'"
