import Mapping_function as mp
import pandas as pd
from datetime import datetime  
from pathlib import Path

#path
project_root=Path(__file__).resolve().parent.parent
input_file=project_root/'Input Data'/'Customer_Data.xlsx'
output_file=project_root/'mapped_data'/'MAPPED_CHURN_DATA.xlsx'

data=pd.read_excel(input_file)


data.columns=(data.columns.str.strip().str.upper())
data.rename(columns=mp.title,inplace=True)

GENDER={k.upper().strip():v for k,v in mp.gender.items()}
MARTIAL_STATUS={k.upper().strip():v for k,v in mp.marital_status.items()}
PHONE_SERVICE={k.upper().strip():v for k,v in mp.Phone_service.items()}
MULTIPLE_LINES={k.upper().strip():v for k,v in mp.multiple_lines.items()}
INTERNET_SERVICE={k.upper().strip():v for k,v in mp.internet_service.items()}
ONLINE_SECURITY={k.upper().strip():v for k,v in mp.online_services.items()}
CONTRACT={k.upper().strip():v for k,v in mp.contract.items()}
PAYMENT_METHOD={k.upper().strip():v for k,v in mp.payment_method.items()}
CHURN={k.upper().strip():v for k,v in mp.churn.items()}

cols_non_num=['GENDER','MARITAL_STATUS','PHONE_SERVICE','MULTIPLE_LINES','INTERNET_SERVICE','ONLINE_SECURITY','ONLINE_BACKUP','DEVICE_PROTECTION','TECH_SUPPORT','TV_STREAMING','MOVIE_STREAMING','CONTRACT','PAYMENT_METHOD','CHURN']
for col in cols_non_num:
    data[col]=data[col].astype(str).str.upper().str.strip()

data['GENDER']=data['GENDER'].map(GENDER).fillna(data['GENDER'])
data['MARITAL_STATUS']=data['MARITAL_STATUS'].map(MARTIAL_STATUS).fillna(data['MARITAL_STATUS'])
data['PHONE_SERVICE']=data['PHONE_SERVICE'].map(PHONE_SERVICE).fillna(data['PHONE_SERVICE'])
data['MULTIPLE_LINES']=data['MULTIPLE_LINES'].map(MULTIPLE_LINES).fillna(data['MULTIPLE_LINES'])
data['INTERNET_SERVICE']=data['INTERNET_SERVICE'].map(INTERNET_SERVICE).fillna(data['INTERNET_SERVICE'])

cols_x=['ONLINE_SECURITY','ONLINE_BACKUP','DEVICE_PROTECTION','TECH_SUPPORT','TV_STREAMING','MOVIE_STREAMING']

for col in cols_x:
    data[col]=data[col].map(ONLINE_SECURITY).fillna(data[col])

data['CONTRACT']=data['CONTRACT'].map(CONTRACT).fillna(data['CONTRACT'])
data['PAYMENT_METHOD']=data['PAYMENT_METHOD'].map(PAYMENT_METHOD).fillna(data['PAYMENT_METHOD'])
data['CHURN']=data['CHURN'].map(CHURN).fillna(data['CHURN'])


cols_num=['AGE','DEPENDENTS','MONTHLY_INCOME($)','ZIP','TENURE_MONTHS','MONTHLY_CHARGES($)','TOTAL_CHARGES($)', 'NO_OF_SERVICES','CHURN_PROBABILITY']
for col in cols_num:
    data[col]=pd.to_numeric(data[col],errors='coerce')

data['JOIN_DATE']=pd.to_datetime(data['JOIN_DATE'],errors='coerce')

current = pd.Timestamp.now()
data["TENURE_MONTHS"] = (
    (current.year - data["JOIN_DATE"].dt.year) * 12 +
    (current.month - data["JOIN_DATE"].dt.month)
)

data['TOTAL_CHARGES($)'] = data['MONTHLY_CHARGES($)'] * data['TENURE_MONTHS']
print('Data Cleaning and Mapping Done')

data.to_excel(output_file,index=False)
print('Mapped Data Saved to mapped_data.xlsx')