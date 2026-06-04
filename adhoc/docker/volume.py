from pathlib import Path 
from datetime import datetime
import os

Path("/data/cleaned_data").mkdir(parents=True, exist_ok=True)

out = Path("/data/cleaned_data/hello.txt")

with out.open("a") as f:
    f.write(f"Hello docker volume: {datetime.now()}")