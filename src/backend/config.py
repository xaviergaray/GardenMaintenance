# Load environment variables
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Environment Variables for Configuration
DB_FILEPATH = Path(os.getenv('DB_FILEPATH', '../out'))