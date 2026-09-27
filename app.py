import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path




st.set_page_config(
    page_title="Customer Churn Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)




@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parent

    file_path = (
        project_root
        / "Output Data"
        / "Customer_clustered_result.xlsx"
    )

    return pd.read_excel(file_path)


data = load_data()




data["CHURN"] = data["CHURN"].astype(str).str.upper()

if "CHURN_PREDICTION" in data.columns:
    data["CHURN_PREDICTION"] = (
        data["CHURN_PREDICTION"]
        .astype(str)
        .str.upper()
    )

if "PREDICTED_CHURN_PROBABILITY" in data.columns:
    data["PREDICTED_CHURN_PROBABILITY"] = pd.to_numeric(
        data["PREDICTED_CHURN_PROBABILITY"],
        errors="coerce",
    )

if (
    "CUSTOMER_SEGMENT" in data.columns
    and pd.api.types.is_numeric_dtype(data["CUSTOMER_SEGMENT"])
):
    data["CUSTOMER_SEGMENT"] = data["CUSTOMER_SEGMENT"].map(
        {
            0: "Low-Service Customers",
            1: "High-Service Customers",
        }
    )



st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .small {
            color: #9ca3af;
            font-size: 0.85rem;
        }

        [data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 8px;
            padding: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



def style_chart(fig):
    """Apply a consistent dark Plotly theme."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        margin=dict(
            l=30,
            r=20,
            t=55,
            b=35,
        ),
        legend_title_text="",
    )

    return fig


def churn_rate_by(df, column):
    """Return churn rate grouped by a selected column."""
    return (
        df.groupby(column)["CHURN"]
        .apply(lambda x: x.eq("YES").mean() * 100)
        .reset_index(name="CHURN_RATE")
    )




def overview():
    st.title("Customer Churn Analytics")

    st.caption(
        "Overall customer, churn, revenue and risk overview"
    )

  
    # KPI CALCULATIONS
  

    total_customers = len(data)

    churned_customers = data["CHURN"].eq("YES").sum()

    churn_rate = (
        churned_customers / total_customers * 100
    )

    average_probability = (
        data["PREDICTED_CHURN_PROBABILITY"].mean() * 100
    )

    total_revenue = data["MONTHLY_CHARGES($)"].sum()

    revenue_at_risk = (
        data["MONTHLY_CHARGES($)"]
        * data["PREDICTED_CHURN_PROBABILITY"]
    ).sum()

    high_risk_customers = data[
        data["RISK_TIER"]
        .astype(str)
        .str.lower()
        .isin(["high", "very high"])
    ].shape[0]

  
    # KPI CARDS
  

    kpis = [
        ("Total Customers", f"{total_customers:,}"),
        ("Churned Customers", f"{churned_customers:,}"),
        ("Churn Rate", f"{churn_rate:.1f}%"),
        ("Avg. Churn Probability", f"{average_probability:.1f}%"),
        ("High Risk Customers", f"{high_risk_customers:,}"),
        ("Revenue at Risk", f"${revenue_at_risk:,.0f}"),
    ]

    columns = st.columns(6)

    for column, (label, value) in zip(columns, kpis):
        column.metric(label, value)

    st.divider()

  
    # CHURN + RISK
  

    left, right = st.columns(2)

    with left:
        churn_distribution = (
            data["CHURN"]
            .value_counts()
            .reset_index()
        )

        churn_distribution.columns = [
            "CHURN",
            "CUSTOMERS",
        ]

        figure = px.pie(
            churn_distribution,
            names="CHURN",
            values="CUSTOMERS",
            hole=0.5,
            title="Actual Churn Distribution",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        risk_distribution = (
            data["RISK_TIER"]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = [
            "RISK_TIER",
            "CUSTOMERS",
        ]

        figure = px.bar(
            risk_distribution,
            x="RISK_TIER",
            y="CUSTOMERS",
            title="Customer Risk Distribution",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

  
    # CONTRACT + INTERNET
  

    left, right = st.columns(2)

    with left:
        result = churn_rate_by(data, "CONTRACT")

        figure = px.bar(
            result,
            x="CONTRACT",
            y="CHURN_RATE",
            title="Churn Rate by Contract",
            text_auto=".1f",
            labels={"CHURN_RATE": "Churn Rate (%)"},
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        result = churn_rate_by(data, "INTERNET_SERVICE")

        figure = px.bar(
            result,
            x="INTERNET_SERVICE",
            y="CHURN_RATE",
            title="Churn Rate by Internet Service",
            text_auto=".1f",
            labels={"CHURN_RATE": "Churn Rate (%)"},
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

  
    # PAYMENT + SERVICES
  

    left, right = st.columns(2)

    with left:
        result = churn_rate_by(data, "PAYMENT_METHOD")

        figure = px.bar(
            result,
            x="PAYMENT_METHOD",
            y="CHURN_RATE",
            title="Churn Rate by Payment Method",
            text_auto=".1f",
            labels={"CHURN_RATE": "Churn Rate (%)"},
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        result = churn_rate_by(data, "NO_OF_SERVICES")

        figure = px.bar(
            result,
            x="NO_OF_SERVICES",
            y="CHURN_RATE",
            title="Churn Rate by Number of Services",
            text_auto=".1f",
            labels={
                "NO_OF_SERVICES": "Number of Services",
                "CHURN_RATE": "Churn Rate (%)",
            },
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )


# ============================================================
# PAGE: CHURN ANALYSIS
# ============================================================

def churn_analysis():
    st.title("Churn Analysis")

    st.caption(
        "Explore observed churn across customer and subscription characteristics"
    )

    # Contract + payment
    left, right = st.columns(2)

    with left:
        result = churn_rate_by(data, "CONTRACT")

        figure = px.bar(
            result,
            x="CONTRACT",
            y="CHURN_RATE",
            title="Churn Rate by Contract",
            text_auto=".1f",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        result = churn_rate_by(data, "PAYMENT_METHOD")

        figure = px.bar(
            result,
            x="PAYMENT_METHOD",
            y="CHURN_RATE",
            title="Churn Rate by Payment Method",
            text_auto=".1f",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    # Internet + gender
    left, right = st.columns(2)

    with left:
        result = churn_rate_by(data, "INTERNET_SERVICE")

        figure = px.bar(
            result,
            x="INTERNET_SERVICE",
            y="CHURN_RATE",
            title="Churn Rate by Internet Service",
            text_auto=".1f",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        result = churn_rate_by(data, "GENDER")

        figure = px.bar(
            result,
            x="GENDER",
            y="CHURN_RATE",
            title="Churn Rate by Gender",
            text_auto=".1f",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    # Number of services
    result = churn_rate_by(data, "NO_OF_SERVICES")

    figure = px.bar(
        result,
        x="NO_OF_SERVICES",
        y="CHURN_RATE",
        title="Churn Rate by Number of Services",
        text_auto=".1f",
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )

    # Tenure groups
    tenure_data = data.copy()

    tenure_data["TENURE_GROUP"] = pd.cut(
        tenure_data["TENURE_MONTHS"],
        bins=[
            0,
            12,
            24,
            36,
            48,
            60,
            float("inf"),
        ],
        labels=[
            "0-12 months",
            "13-24 months",
            "25-36 months",
            "37-48 months",
            "49-60 months",
            "60+ months",
        ],
    )

    tenure_churn = (
        tenure_data.groupby(
            "TENURE_GROUP",
            observed=False,
        )["CHURN"]
        .apply(lambda x: x.eq("YES").mean() * 100)
        .reset_index(name="CHURN_RATE")
    )

    figure = px.bar(
        tenure_churn,
        x="TENURE_GROUP",
        y="CHURN_RATE",
        title="Churn Rate by Tenure",
        text_auto=".1f",
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )

    # Probability distribution
    figure = px.histogram(
        data,
        x="PREDICTED_CHURN_PROBABILITY",
        nbins=30,
        title="Predicted Churn Probability Distribution",
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )


# ============================================================
# PAGE: CUSTOMER SEGMENTATION
# ============================================================

def customer_segmentation():
    st.title("Customer Segmentation")

    st.caption(
        "K-Means based customer segments and their business characteristics"
    )

    profile = (
        data.groupby("CUSTOMER_SEGMENT")
        .agg(
            Customers=("CUSTOMER_ID", "count"),
            Avg_Tenure=("TENURE_MONTHS", "mean"),
            Avg_Services=("NO_OF_SERVICES", "mean"),
            Avg_Monthly_Charges=(
                "MONTHLY_CHARGES($)",
                "mean",
            ),
            Monthly_Revenue=(
                "MONTHLY_CHARGES($)",
                "sum",
            ),
            Churn_Rate=(
                "CHURN",
                lambda x: x.eq("YES").mean() * 100,
            ),
            Avg_Churn_Probability=(
                "PREDICTED_CHURN_PROBABILITY",
                "mean",
            ),
        )
        .reset_index()
    )

    profile["Avg_Churn_Probability"] *= 100

  
    # SEGMENT DISTRIBUTION + PROFILE
  

    left, right = st.columns(2)

    with left:
        figure = px.pie(
            profile,
            names="CUSTOMER_SEGMENT",
            values="Customers",
            hole=0.5,
            title="Customer Segment Distribution",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        st.dataframe(
            profile.round(2),
            use_container_width=True,
            hide_index=True,
        )

  
    # CHURN + CHARGES
  

    left, right = st.columns(2)

    with left:
        figure = px.bar(
            profile,
            x="CUSTOMER_SEGMENT",
            y="Churn_Rate",
            title="Churn Rate by Segment",
            text_auto=".1f",
            labels={"Churn_Rate": "Churn Rate (%)"},
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        figure = px.bar(
            profile,
            x="CUSTOMER_SEGMENT",
            y="Avg_Monthly_Charges",
            title="Average Monthly Charges by Segment",
            text_auto=".2f",
            labels={
                "Avg_Monthly_Charges":
                "Average Monthly Charges ($)"
            },
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

  
    # SERVICES VS CHARGES
  

    figure = px.scatter(
        data,
        x="NO_OF_SERVICES",
        y="MONTHLY_CHARGES($)",
        color="CUSTOMER_SEGMENT",
        opacity=0.55,
        title="Services vs Monthly Charges",
        hover_data=[
            "CUSTOMER_ID",
            "CONTRACT",
            "INTERNET_SERVICE",
        ],
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )

  
    # SEGMENT PROBABILITY
  

    figure = px.bar(
        profile,
        x="CUSTOMER_SEGMENT",
        y="Avg_Churn_Probability",
        title="Average Predicted Churn Probability by Segment",
        text_auto=".1f",
        labels={
            "Avg_Churn_Probability":
            "Average Predicted Probability (%)"
        },
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )


# ============================================================
# PAGE: RISK ANALYSIS
# ============================================================

def risk_analysis():
    st.title("Risk Analysis")

    st.caption(
        "Churn risk distribution, probability and customers requiring attention"
    )

  
    # RISK DISTRIBUTION
  

    risk_counts = (
        data["RISK_TIER"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "RISK_TIER",
        "CUSTOMERS",
    ]

    left, right = st.columns(2)

    with left:
        figure = px.bar(
            risk_counts,
            x="RISK_TIER",
            y="CUSTOMERS",
            title="Customers by Risk Tier",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

    with right:
        figure = px.pie(
            risk_counts,
            names="RISK_TIER",
            values="CUSTOMERS",
            hole=0.5,
            title="Risk Tier Distribution",
        )

        st.plotly_chart(
            style_chart(figure),
            use_container_width=True,
        )

  
    # PROBABILITY VS CHARGES
  

    figure = px.scatter(
        data,
        x="PREDICTED_CHURN_PROBABILITY",
        y="MONTHLY_CHARGES($)",
        color="RISK_TIER",
        opacity=0.55,
        title="Predicted Churn Probability vs Monthly Charges",
        hover_data=[
            "CUSTOMER_ID",
            "CONTRACT",
            "CUSTOMER_SEGMENT",
        ],
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )

  
    # RISK BY CONTRACT
  

    risk_by_contract = (
        pd.crosstab(
            data["CONTRACT"],
            data["RISK_TIER"],
            normalize="index",
        )
        * 100
    )

    figure = px.bar(
        risk_by_contract,
        barmode="stack",
        title="Risk Tier Composition by Contract",
        labels={"value": "Percentage (%)"},
    )

    st.plotly_chart(
        style_chart(figure),
        use_container_width=True,
    )

  
    # HIGHEST RISK CUSTOMERS
  

    st.subheader("Highest-Risk Customers")

    columns = [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "CONTRACT",
        "INTERNET_SERVICE",
        "NO_OF_SERVICES",
        "MONTHLY_CHARGES($)",
        "PREDICTED_CHURN_PROBABILITY",
        "RISK_TIER",
        "CUSTOMER_SEGMENT",
    ]

    columns = [
        column
        for column in columns
        if column in data.columns
    ]

    highest_risk = (
        data.sort_values(
            "PREDICTED_CHURN_PROBABILITY",
            ascending=False,
        )
        .head(25)
    )

    st.dataframe(
        highest_risk[columns],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE: CUSTOMER EXPLORER
# ============================================================

def customer_explorer():
    st.title("Customer Explorer")

    st.write(
        "Search and inspect individual customer information, "
        "subscription details and churn predictions."
    )

  
    # CUSTOMER SELECTION
  

    customer_ids = (
        data["CUSTOMER_ID"]
        .dropna()
        .astype(str)
        .tolist()
    )

    selected_id = st.selectbox(
        "Customer ID",
        customer_ids,
    )

    customer = data[
        data["CUSTOMER_ID"].astype(str) == selected_id
    ].iloc[0]

  
    # CUSTOMER HEADER
  

    st.header(
        f"{customer.get('FIRST_NAME', '')} "
        f"{customer.get('LAST_NAME', '')}"
    )

    st.caption(
        f"Customer ID: {customer['CUSTOMER_ID']}"
    )

  
    # KEY METRICS
  

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Actual Churn",
        customer.get("CHURN", "N/A"),
    )

    probability = customer.get(
        "PREDICTED_CHURN_PROBABILITY",
        None,
    )

    c2.metric(
        "Churn Probability",
        (
            f"{float(probability) * 100:.1f}%"
            if pd.notna(probability)
            else "N/A"
        ),
    )

    c3.metric(
        "Risk Tier",
        customer.get("RISK_TIER", "N/A"),
    )

    charges = customer.get(
        "MONTHLY_CHARGES($)",
        None,
    )

    c4.metric(
        "Monthly Charges",
        (
            f"${float(charges):,.2f}"
            if pd.notna(charges)
            else "N/A"
        ),
    )

    services = customer.get(
        "NO_OF_SERVICES",
        None,
    )

    c5.metric(
        "Services",
        (
            int(services)
            if pd.notna(services)
            else "N/A"
        ),
    )

    st.divider()

  
    # PERSONAL + SUBSCRIPTION
  

    left, right = st.columns(2)

    with left:
        st.subheader("Personal Information")

        personal = pd.DataFrame(
            {
                "Attribute": [
                    "Gender",
                    "Age",
                    "Marital Status",
                    "Occupation",
                    "Dependents",
                    "City",
                    "State",
                    "ZIP",
                    "Tenure",
                ],
                "Value": [
                    customer.get("GENDER", "N/A"),
                    customer.get("AGE", "N/A"),
                    customer.get("MARITAL_STATUS", "N/A"),
                    customer.get("OCCUPATION", "N/A"),
                    customer.get("DEPENDENTS", "N/A"),
                    customer.get("CITY", "N/A"),
                    customer.get("STATE", "N/A"),
                    customer.get("ZIP", "N/A"),
                    customer.get("TENURE_MONTHS", "N/A"),
                ],
            }
        )

        st.dataframe(
            personal,
            use_container_width=True,
            hide_index=True,
        )

    with right:
        st.subheader("Subscription Information")

        subscription = pd.DataFrame(
            {
                "Attribute": [
                    "Contract",
                    "Internet Service",
                    "Payment Method",
                    "Phone Service",
                    "Multiple Lines",
                    "Paperless Billing",
                    "Number of Services",
                    "Monthly Charges",
                    "Total Charges",
                    "Customer Segment",
                ],
                "Value": [
                    customer.get("CONTRACT", "N/A"),
                    customer.get("INTERNET_SERVICE", "N/A"),
                    customer.get("PAYMENT_METHOD", "N/A"),
                    customer.get("PHONE_SERVICE", "N/A"),
                    customer.get("MULTIPLE_LINES", "N/A"),
                    customer.get("PAPERLESS_BILLING", "N/A"),
                    customer.get("NO_OF_SERVICES", "N/A"),
                    customer.get("MONTHLY_CHARGES($)", "N/A"),
                    customer.get("TOTAL_CHARGES($)", "N/A"),
                    customer.get("CUSTOMER_SEGMENT", "N/A"),
                ],
            }
        )

        st.dataframe(
            subscription,
            use_container_width=True,
            hide_index=True,
        )

  
    # SERVICE INFORMATION
  

    st.subheader("Service Information")

    services = pd.DataFrame(
        {
            "Service": [
                "Online Security",
                "Online Backup",
                "Device Protection",
                "Tech Support",
                "TV Streaming",
                "Movie Streaming",
            ],
            "Status": [
                customer.get("ONLINE_SECURITY", "N/A"),
                customer.get("ONLINE_BACKUP", "N/A"),
                customer.get("DEVICE_PROTECTION", "N/A"),
                customer.get("TECH_SUPPORT", "N/A"),
                customer.get("TV_STREAMING", "N/A"),
                customer.get("MOVIE_STREAMING", "N/A"),
            ],
        }
    )

    st.dataframe(
        services,
        use_container_width=True,
        hide_index=True,
    )

  
    # MODEL RESULTS
  

    st.subheader("Model Results")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Actual Churn",
        customer.get("CHURN", "N/A"),
    )

    c2.metric(
        "Model Prediction",
        customer.get("CHURN_PREDICTION", "N/A"),
    )

    c3.metric(
        "Risk Tier",
        customer.get("RISK_TIER", "N/A"),
    )


# ============================================================
# PAGE: DATA EXPLORER
# ============================================================

def data_explorer():
    st.title("Data Explorer")

    st.write(
        "Explore, filter and download the customer dataset."
    )

  
    # FILTERS
  

    filtered = data.copy()

    st.subheader("Filters")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        contract = st.multiselect(
            "Contract",
            sorted(
                data["CONTRACT"]
                .dropna()
                .astype(str)
                .unique()
            ),
        )

        if contract:
            filtered = filtered[
                filtered["CONTRACT"]
                .astype(str)
                .isin(contract)
            ]

    with c2:
        internet = st.multiselect(
            "Internet Service",
            sorted(
                data["INTERNET_SERVICE"]
                .dropna()
                .astype(str)
                .unique()
            ),
        )

        if internet:
            filtered = filtered[
                filtered["INTERNET_SERVICE"]
                .astype(str)
                .isin(internet)
            ]

    with c3:
        risk = st.multiselect(
            "Risk Tier",
            sorted(
                data["RISK_TIER"]
                .dropna()
                .astype(str)
                .unique()
            ),
        )

        if risk:
            filtered = filtered[
                filtered["RISK_TIER"]
                .astype(str)
                .isin(risk)
            ]

    with c4:
        churn = st.multiselect(
            "Churn",
            sorted(
                data["CHURN"]
                .dropna()
                .astype(str)
                .unique()
            ),
        )

        if churn:
            filtered = filtered[
                filtered["CHURN"]
                .astype(str)
                .isin(churn)
            ]

  
    # RESULTS
  

    st.divider()

    st.write(
        f"Showing **{len(filtered):,}** customers"
    )

    columns = [
        "CUSTOMER_ID",
        "FIRST_NAME",
        "LAST_NAME",
        "GENDER",
        "AGE",
        "CITY",
        "STATE",
        "TENURE_MONTHS",
        "CONTRACT",
        "INTERNET_SERVICE",
        "PAYMENT_METHOD",
        "NO_OF_SERVICES",
        "MONTHLY_CHARGES($)",
        "TOTAL_CHARGES($)",
        "CHURN",
        "CHURN_PREDICTION",
        "PREDICTED_CHURN_PROBABILITY",
        "RISK_TIER",
        "CUSTOMER_SEGMENT",
    ]

    columns = [
        column
        for column in columns
        if column in filtered.columns
    ]

    st.dataframe(
        filtered[columns],
        use_container_width=True,
        height=600,
        hide_index=True,
    )

  
    # DOWNLOAD
  

    st.divider()

    csv = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_customer_data.csv",
        mime="text/csv",
    )



# SIDEBAR NAVIGATION

with st.sidebar:
    st.markdown("### Customer Churn")
    st.caption("Analytics Dashboard")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Churn Analysis",
            "Customer Segmentation",
            "Risk Analysis",
            "Customer Explorer",
            "Data Explorer",
        ],
    )

    st.divider()

    st.caption(
        f"Dataset: {len(data):,} customers"
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

if page == "Overview":
    overview()

elif page == "Churn Analysis":
    churn_analysis()

elif page == "Customer Segmentation":
    customer_segmentation()

elif page == "Risk Analysis":
    risk_analysis()

elif page == "Customer Explorer":
    customer_explorer()

elif page == "Data Explorer":
    data_explorer()
