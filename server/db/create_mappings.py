import pandas as pd
from db.database import engine
from sqlalchemy import text

# Mappings:
# Some tables have a case_id column, which is our source of truth for mapping
# Other tables have patient_id and timestamp columns, which we can use to infer the case
