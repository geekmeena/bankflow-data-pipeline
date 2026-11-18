
import os

import pandas as pd
import streamlit as st
import psycopg2


st.set_page_config(
    page_title="BankFlow Dashboard",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 BankFlow — Transaction Analytics")
st.write("Banking transaction analysis using PostgreSQL.")


@st.cache_data(ttl=60)
def load_data():
    with psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="bankflow_db",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    ) as conn:
        return pd.read_sql_query(
            """
            SELECT customer_id, total_spending
            FROM dbt_dev.customer_spending
            ORDER BY total_spending DESC
            """,
            conn,
        )


try:
    df = load_data()

    st.metric("Total Customer Spending", f"{df['total_spending'].sum():,.2f}")

    st.subheader("Spending by Customer")
    st.bar_chart(df.set_index("customer_id")["total_spending"])

    st.subheader("Customer Spending Data")
    st.dataframe(df, use_container_width=True)

except Exception:
    st.error(
        "Unable to load PostgreSQL data. "
        "Check your database and DB_USER/DB_PASSWORD settings."
    )
