import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

#path
project_root=Path(__file__).resolve().parent.parent
customer_input=project_root/'1_data_generator'/'Customer_Master.xlsx'
locations_input=project_root/'1_data_generator'/'Locations_Full_State_Names.xlsx'
output_file=project_root/'1_data_generator'/'Customer_Data_With_Locations.xlsx'


customer_df = pd.read_excel(customer_input)
locations_df = pd.read_excel(locations_input)

random_locations = locations_df.sample(
    n=len(customer_df),   # Same number of rows as customers
    replace=True,         # Allow locations to repeat
    random_state=None     # Different results every run
).reset_index(drop=True)

customer_df["City"] = random_locations["City"]
customer_df["State"] = random_locations["State"]
customer_df["ZIP"] = random_locations["ZIP"]

start_date = datetime(2018, 1, 1)
end_date = datetime(2025, 12, 31)

date_range = (end_date - start_date).days

customer_df["Join_Date"] = [
    start_date + timedelta(days=random.randint(0, date_range))
    for _ in range(len(customer_df))
]


today = datetime.today()


customer_df["Join_Date"] = pd.to_datetime(customer_df["Join_Date"])
customer_df["Tenure_Months"] = (
    (today.year - customer_df["Join_Date"].dt.year) * 12
    + (today.month - customer_df["Join_Date"].dt.month)
)


customer_df.to_excel(output_file, index=False)

print("Locations assigned successfully!")
        