import pandas as pd
import numpy as np
import random
from pathlib import Path

#path
PROJECT_ROOT=Path(__file__).resolve().parent.parent

customer_input=PROJECT_ROOT/'1_data_generator'/'CustomerIDs.xlsx'
first_name_input=PROJECT_ROOT/'1_data_generator'/'Clean_FirstNames_2600.xlsx'
last_name_input=PROJECT_ROOT/"1_data_generator"/'Clean_Lastnames_3000.xlsx'
customer_data_output= PROJECT_ROOT/'1_data_generator'/'Customer_Master.xlsx'


#excel_reding
customer_df =pd.read_excel(customer_input)
first_df = pd.read_excel(first_name_input)
last_df = pd.read_excel(last_name_input)


first_names = first_df.to_dict("records")
last_names = last_df.iloc[:, 0].tolist()

generated_first = []
generated_last = []
generated_gender = []

for _ in range(len(customer_df)):

   
    person = random.choice(first_names)

    first_name = person["FirstName"]
    gender = person["Gender"]

    
    if gender == "M":
        gender=random.choice(["Male","male","MALe","Men","man","MEN","MALE","HE","he","mEn","maLe"])
    else:
        gender = "Female"
        gender=random.choice(["Female","female","FEMALE","Women","women","SHE","she","WOMEN","WoMan","wOmen","fEmale"])
    
    last_name = random.choice(last_names)

    generated_first.append(first_name)
    generated_last.append(last_name)
    generated_gender.append(gender)


customer_df["FirstName"] = generated_first
customer_df["LastName"] = generated_last
customer_df["Gender"] = generated_gender

customer_df["Age"] = [
    random.choices(
        [
            random.randint(18, 30),
            random.randint(31, 64),
            random.randint(65, 80)
        ],
        weights=[40, 45, 15],
        k=1
    )[0]
    for _ in range(len(customer_df))
]

marital_status = []

for age in customer_df["Age"]:

    if age <= 22:
        status = random.choices(
            ["Single", "Married"],
            weights=[90, 10],
            k=1
        )[0]

    elif age <= 30:
        status = random.choices(
            ["Single", "Married", "Divorced"],
            weights=[60, 35, 5],
            k=1 
        )[0]

    elif age <= 45:
        status = random.choices(
            ["Single", "Married", "Divorced"],
            weights=[5, 70, 25],
            k=1
        )[0]

    elif age <= 60:
        status = random.choices(
            ["Married", "Divorced", "Widowed", "Single"],
            weights=[65, 20, 10, 5],
            k=1
        )[0]

    else:
        status = random.choices(
            ["Married", "Widowed", "Divorced", "Single"],
            weights=[50, 30, 15, 5],
            k=1
        )[0]

    marital_status.append(status)

customer_df["Marital_Status"] = marital_status
occupation = []

for age in customer_df["Age"]:

    if age <= 22:
        job = random.choices(
            ["Student", "Part-Time Worker", "Retail Associate", "Unemployed"],
            weights=[70, 25, 5, 5],
            k=1
        )[0]

    elif age <= 30:
        job = random.choice([
            "Customer Service Representative",
            "Retail Associate",
            "Teacher",
            "Technician",
            "Software Engineer",
            "Data Analyst",
            "Nurse",
            "Accountant"
        ])

    elif age <= 50:
        job = random.choice([
            "Manager",
            "Accountant",
            "Sales Executive",
            "Software Engineer",
            "Business Owner",
            "Doctor",
            "Lawyer",
            "Data Analyst",
            "Technician"
        ])

    elif  age<= 60:
        job = random.choice([
            "Manager",
            "Business Owner",
            "Teacher",
            "Accountant",
            "Sales Executive",
            "Technician"
        ])

    else:
        job = random.choices(
            ["Retired", "Business Owner", "Part-Time Worker"],
            weights=[80, 15, 5],
            k=1
        )[0]

    occupation.append(job)

customer_df["Occupation"] = occupation

dependents = []

for age, status in zip(customer_df["Age"], customer_df["Marital_Status"]):

    if status == "Single":
        if age <= 25:
            dep = 0
        else:
            dep = random.choices(
                [0, 1, 2],
                weights=[90, 5, 5],
                k=1
            )[0]

    elif status == "Married":
        if age <= 25:
            dep = random.choices(
                [0, 1,2,3],
                weights=[40,35,20,5],
                k=1
            )[0]
        elif age <= 40:
            dep = random.choices(
                [0, 1, 2, 3],
                weights=[20, 35, 30, 15],
                k=1
            )[0]
        else:
            dep = random.choices(
                [0, 1, 2, 3, 4],
                weights=[15, 20, 30, 25, 10],
                k=1
            )[0]

    elif status == "Divorced":
        dep = random.choices(
            [0, 1, 2, 3],
            weights=[40, 30, 20, 10],
            k=1
        )[0]

    else:  # Widowed
        dep = random.choices(
            [0, 1, 2, 3],
            weights=[50, 25, 20, 5],
            k=1
        )[0]

    dependents.append(dep)

customer_df["Dependents"] = dependents


def generate_income(min_salary, max_salary, skew=2.5):
   
    val = np.random.beta(skew, skew * 1.8)  # skewed toward the lower end
    salary = min_salary + (max_salary - min_salary) * val
    return round(salary / 50) * 50


income = []

for job in customer_df["Occupation"]:

    if job == "Student":
        salary = 0

    elif job == "Unemployed":
        salary = 0

    elif job == "Part-Time Worker":
        salary = generate_income(1500, 5500)

    elif job == "Retail Associate":
        salary = generate_income(2500, 8000)

    elif job == "Customer Service Representative":
        salary = generate_income(3000, 10500)

    elif job == "Administrative Assistant":
        salary = generate_income(3000, 10000)

    elif job == "Teacher":
        salary = generate_income(4000, 13000)

    elif job == "Technician":
        salary = generate_income(8000, 20000)

    elif job == "Nurse":
        salary = generate_income(8000, 20000)

    elif job == "Accountant":
        salary = generate_income(10000, 25000)

    elif job == "Sales Executive":
        salary = generate_income(8000, 20000)

    elif job == "Data Analyst":
        salary = generate_income(20000, 40000)

    elif job == "Software Engineer":
        salary = generate_income(30000, 70000)

    elif job == "Manager":
        salary = generate_income(30000, 80000)

    elif job == "Business Owner":
        salary = generate_income(80000, 350000)

    elif job == "Lawyer":
        salary = generate_income(10000, 65000)

    elif job == "Doctor":
        salary = generate_income(30000, 90000)

    else:  # Retired
        salary = generate_income(1500, 5000)

    income.append(salary)

customer_df["Monthly_Income($)"] = income


def income_category(income):
    if income < 8000:
        return "Low"
    elif 8000 <= income < 20000:
        return "Lower-Middle"
    elif 20000 <= income < 40000:
        return "Middle"
    elif 40000 <= income < 100000:
        return "Upper-Middle"
    else:
        return "High"


customer_df["Income_Category"] = customer_df["Monthly_Income($)"].apply(
    income_category
)


customer_df.to_excel(customer_data_output,index=False)

print("Customer file generated successfully!")  