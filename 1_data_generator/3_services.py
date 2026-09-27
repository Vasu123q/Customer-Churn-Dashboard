import pandas as pd
import numpy as np
import random
import math
from pathlib import Path

#path
Project_root=Path(__file__).resolve().parent.parent
input_file=Project_root/'1_data_generator'/'Customer_Data_With_Locations.xlsx'
output_file=Project_root/'Input Data'/'Customer_Data.xlsx'

customer_df = pd.read_excel(input_file)


BASE_CHURN_RATE = 0.5

CONTRACT_MULT = {
    "Month-to-Month": 2.5,
    "One Year": 0.40,
    "Two Year": 0.10,
}

INTERNET_MULT = {
    "Fiber Optic": 2.0,
    "DSL": 0.6,
    "Cable": 1.10,   
    "NO": 0.40,
}

PAYMENT_MULT = {
    "Electronic Check": 2.0,
    "Mailed Check": 0.75,
    "Bank Transfer": 0.5,
    "Credit Card": 0.5,
    "Debit Card": 0.5,
}

SECURITY_MULT = {
    "Yes": 0.85,
    "No": 2.0,
}

EXTRA_SERVICE_LOG_ODDS_EACH = -0.15
AFFORDABILITY_SLOPE = 6.5
AFFORDABILITY_CENTER = 0.05  

TENURE_DECAY_STRENGTH = 1.5
TENURE_DECAY_CAP_MONTHS = 60

HIGH_RISK_INTERACTION_LOG_ODDS = 0.45
LOYALTY_BONUS_LOG_ODDS=0.4


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def compute_churn_probability(
    contract,
    internet,
    payment_method,
    online_security,
    extra_service_yes_count,   
    tenure,
    monthly,
    income,
    
):
    log_odds = math.log(BASE_CHURN_RATE / (1 - BASE_CHURN_RATE))

    log_odds += math.log(CONTRACT_MULT[contract])
    log_odds += math.log(INTERNET_MULT[internet])
    log_odds += math.log(PAYMENT_MULT[payment_method])

    if internet != "NO":
        log_odds += math.log(SECURITY_MULT[online_security])

    log_odds += EXTRA_SERVICE_LOG_ODDS_EACH * extra_service_yes_count



    if income > 0:
        charge_ratio = monthly / income
    else:
        charge_ratio = 0.05   
    log_odds += (charge_ratio - AFFORDABILITY_CENTER) * AFFORDABILITY_SLOPE

    log_odds += -TENURE_DECAY_STRENGTH * math.log1p(
        min(tenure, TENURE_DECAY_CAP_MONTHS)
    ) / math.log1p(TENURE_DECAY_CAP_MONTHS)

    total_services = extra_service_yes_count + (1 if online_security == "Yes" else 0)
    if (
        contract == "Month-to-Month"
        and tenure < 12
        and total_services <= 1
        and charge_ratio >= AFFORDABILITY_CENTER
    ):
        log_odds += HIGH_RISK_INTERACTION_LOG_ODDS

    if tenure>36 and total_services>=4:
        log_odds-=LOYALTY_BONUS_LOG_ODDS

    probability = sigmoid(log_odds)
    probability = max(0.02, min(probability, 0.95))  # soft safety bounds only
    return probability


phone_service = []
multiple_lines = []
internet_service = []
online_security = []
online_backup = []
device_protection = []
tech_support = []
streaming_tv = []
streaming_movies = []
contract = []
paperless_billing = []
payment_method = []
monthly_charges = []
total_charges = []
churn_probability = []
no_of_services = []
churn=[]

for tenure, income in zip(
    customer_df["Tenure_Months"], customer_df["Monthly_Income($)"]
):
    charge = 0

    phone = random.choices(["Yes", "No"], weights=[90, 10], k=1)[0]
    phone_service.append(phone)

    if phone == "No":
        multi = "No Phone Service"
    else:
        multi = random.choices(["Yes", "No"], weights=[40, 60], k=1)[0]
        charge += 25
        if multi == "Yes":
            charge += 10
    multiple_lines.append(multi)

    internet = random.choices(
        ["Fiber Optic", "DSL", "Cable", "NO"], weights=[45, 20, 25, 10], k=1
    )[0]
    internet_service.append(internet)

    if internet == "NO":
        sec = back = protect = support = tv = movies = "No Internet Service"
    else:
        if internet == "Fiber Optic":
            charge += 60
        elif internet == "Cable":
            charge += 50
        else:
            charge += 40

        sec = random.choice(["Yes", "No"])
        back = random.choice(["Yes", "No"])
        protect = random.choice(["Yes", "No"])
        support = random.choice(["Yes", "No"])
        tv = random.choice(["Yes", "No"])
        movies = random.choice(["Yes", "No"])

        if sec == "Yes":
            charge += 8
        if back == "Yes":
            charge += 6
        if protect == "Yes":
            charge += 7
        if support == "Yes":
            charge += 8
        if tv == "Yes":
            charge += 10
        if movies == "Yes":
            charge += 10

    online_security.append(sec)
    online_backup.append(back)
    device_protection.append(protect)
    tech_support.append(support)
    streaming_tv.append(tv)
    streaming_movies.append(movies)

    cont = random.choices(
        ["Month-to-Month", "One Year", "Two Year"], weights=[60, 25, 15], k=1
    )[0]
    contract.append(cont)

    if cont == "One Year":
        charge -= 7
    elif cont == "Two Year":
        charge -= 12

    paper = random.choices(["Yes", "No"], weights=[75, 25], k=1)[0]
    paperless_billing.append(paper)

    payment = random.choice(
        ["Credit Card", "Debit Card", "Bank Transfer", "Electronic Check", "Mailed Check"]
    )
    payment_method.append(payment)

    monthly = round(charge + random.uniform(-3, 3), 2)
    if monthly < 20:
        monthly = 20
    monthly_charges.append(monthly)

    total = round(monthly * tenure + random.uniform(-20, 20), 2)
    if total < 0:
        total = 0
    total_charges.append(total)

    services = 0
    if phone == "Yes":
        services += 1
    if multi == "Yes":
        services += 1
    if internet != "NO":
        services += 1
    if sec == "Yes":
        services += 1
    if back == "Yes":
        services += 1
    if protect == "Yes":
        services += 1
    if support == "Yes":
        services += 1
    if tv == "Yes":
        services += 1
    if movies == "Yes":
        services += 1
    no_of_services.append(services)

    extra_service_yes_count = sum(
        1 for v in [back, protect, support, tv, movies] if v == "Yes"
    )

    probability = compute_churn_probability(
        contract=cont,
        internet=internet,
        payment_method=payment,
        online_security=sec if internet != "NO" else "Yes",  # neutral if no internet
        extra_service_yes_count=extra_service_yes_count,
        tenure=tenure,
        monthly=monthly,
        income=income,
    )
    churn_probability.append(probability)
    churn.append("Yes" if random.random() < probability else "No")



customer_df["Phone_Service"] = phone_service
customer_df["Multiple_Lines"] = multiple_lines
customer_df["Internet_Service"] = internet_service
customer_df["Online_Security"] = online_security
customer_df["Online_Backup"] = online_backup
customer_df["Device_Protection"] = device_protection
customer_df["Tech_Support"] = tech_support
customer_df["Streaming_TV"] = streaming_tv
customer_df["Streaming_Movies"] = streaming_movies
customer_df["Contract"] = contract
customer_df["Paperless_Billing"] = paperless_billing
customer_df["Payment_Method"] = payment_method
customer_df["No_of_Services"] = no_of_services
customer_df["Monthly_Charges"] = monthly_charges
customer_df["Total_Charges"] = total_charges
customer_df["Churn_Probability"] = churn_probability
customer_df['Churn']= churn


customer_df.to_excel( output_file,index=False,)