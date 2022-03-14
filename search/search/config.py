"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# URL of the index server
INDEX_API_URL = "http://localhost:8001/api/v1/hits/"

# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent
# UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SEARCH_ROOT/'var'/'wikipedia.sqlite3'
