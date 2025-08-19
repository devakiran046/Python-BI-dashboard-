import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("Python BI dahboard by DEVA")

# Step 1: Upload CSV
st.header("Step 1: Upload a CSV File")
uploaded_csv = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_csv:
    df_csv = pd.read_csv(uploaded_csv)
    st.subheader("Preview of Uploaded CSV")
    st.dataframe(df_csv)

    # Step 2: Store CSV into in-memory SQLite DB
    conn = sqlite3.connect(":memory:")
    df_csv.to_sql("data", conn, index=False, if_exists="replace")

    # Step 3: SQL Query Interface
    st.header("Step 2: Run SQL Query on Your Data")
    query = st.text_area("Enter SQL query below", "SELECT * FROM data")

    if st.button("Run SQL Query"):
        try:
            df_query = pd.read_sql_query(query, conn)
            st.success("Query executed successfully!")
            st.dataframe(df_query)

            # Step 4: Optional Chart
            if not df_query.empty:
                st.header("Step 3: Visualize the Result")
                chart_type = st.selectbox("Select Chart Type", ["None", "Bar", "Line", "Pie"])
                if chart_type != "None":
                    x_axis = st.selectbox("X-Axis", df_query.columns)
                    y_axis = st.selectbox("Y-Axis", df_query.columns)
                    if chart_type == "Bar":
                        fig = px.bar(df_query, x=x_axis, y=y_axis)
                    elif chart_type == "Line":
                        fig = px.line(df_query, x=x_axis, y=y_axis)
                    elif chart_type == "Pie":
                        fig = px.pie(df_query, names=x_axis, values=y_axis)
                    st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please upload a CSV file to get started.")