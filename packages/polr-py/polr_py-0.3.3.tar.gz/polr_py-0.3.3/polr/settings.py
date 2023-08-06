import os
import sys

from .utils import print_error


# Required settings
try:
    POLR_API_KEY = os.environ["POLR_API_KEY"]
    POLR_URL = os.environ["POLR_URL"]
except KeyError as err:
    print_error(f"missing required env var: {err}")
    sys.exit(1)
