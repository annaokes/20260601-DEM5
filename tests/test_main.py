import pandas as pd
import datetime as dt
from sqlalchemy import create_engine


class TestEnrichDate:
    
    def setUp(self):
        data = {
            'date_col1': []
        }