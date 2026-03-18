
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu


# ---------------- MENU ----------------
selected = option_menu(
    menu_title=None,
    options=["Home", "SQL Query Runner", "EDA Visualizations", "Country Profile Page"],
    orientation="horizontal"
)


# ---------------- HOME PAGE ----------------
if selected == "Home":

    st.title("🌍 Global Education & Economy Dashboard")

    st.markdown("""
This dashboard analyzes:

• Literacy rates
• Illiteracy trends
• GDP per capita
• Average years of schooling

Use the **navigation menu above** to explore the dashboard.
""")


# ---------------- SQL QUERY PAGE ----------------
elif selected == "SQL Query Runner":

    st.title("SQL Query Runner")

    conn = sqlite3.connect("merged.db")

    queries = {

"Top 10 GDP but low schooling (2020)": """
SELECT country, GDP_per_capita_PPP, avg_years_of_schooling
FROM merged_data
WHERE year = 2020
AND avg_years_of_schooling < 6
ORDER BY GDP_per_capita_PPP DESC
LIMIT 10
""",

"Countries with literacy rate below 70%": """
SELECT country, year, literacy_rate
FROM merged_data
WHERE literacy_rate < 70
ORDER BY literacy_rate
""",

"Top 10 countries by literacy rate (2020)": """
SELECT country, literacy_rate
FROM merged_data
WHERE year = 2020
ORDER BY literacy_rate DESC
LIMIT 10
""",

"Countries with highest illiteracy percentage": """
SELECT country, year, Illiteracy_percent
FROM merged_data
ORDER BY Illiteracy_percent DESC
LIMIT 10
""",

"Top GDP per capita countries (2020)": """
SELECT country, GDP_per_capita_PPP
FROM merged_data
WHERE year = 2020
ORDER BY GDP_per_capita_PPP DESC
LIMIT 10
"""
}

    selected_query = st.selectbox("Select SQL Query", list(queries.keys()))

    st.code(queries[selected_query], language="sql")

    if st.button("Run Query"):

        df = pd.read_sql_query(queries[selected_query], conn)

        st.dataframe(df)


# ---------------- EDA PAGE ----------------
elif selected == "EDA Visualizations":

    st.title("📊 Data Visualizations")

    conn = sqlite3.connect("merged.db")
    df = pd.read_sql("SELECT * FROM merged_data", conn)

    chart = st.selectbox(
        "Choose Visualization",
        [
            "Literacy Rate Distribution",
            "GDP Distribution",
            "Schooling Years Boxplot",
            "GDP vs Schooling Scatter",
            "GDP Correlation Heatmap",
            "Literacy Trend Over Time"
        ]
    )


    if chart == "Literacy Rate Distribution":

        fig, ax = plt.subplots()
        ax.hist(df["literacy_rate"].dropna(), bins=20)
        ax.set_title("Literacy Rate Distribution")

        st.pyplot(fig)


    elif chart == "GDP Distribution":

        fig, ax = plt.subplots()
        ax.hist(df["GDP_per_capita_PPP"].dropna(), bins=20)
        ax.set_title("GDP Distribution")

        st.pyplot(fig)


    elif chart == "Schooling Years Boxplot":

        fig, ax = plt.subplots()
        sns.boxplot(x=df["avg_years_of_schooling"], ax=ax)
        ax.set_title("Schooling Years")

        st.pyplot(fig)


    elif chart == "GDP vs Schooling Scatter":

        fig, ax = plt.subplots()

        ax.scatter(
            df["avg_years_of_schooling"],
            df["GDP_per_capita_PPP"]
        )

        ax.set_xlabel("Schooling")
        ax.set_ylabel("GDP")

        st.pyplot(fig)


    elif chart == "GDP Correlation Heatmap":

        numeric_df = df[
            [
                "avg_years_of_schooling",
                "GDP_per_capita_PPP",
                "GDP_per_Schooling_Year",
                "Education_Index"
            ]
        ]

        corr = numeric_df.corr()

        fig, ax = plt.subplots()

        sns.heatmap(corr, annot=True, ax=ax)

        st.pyplot(fig)


    elif chart == "Literacy Trend Over Time":

        fig, ax = plt.subplots()

        sns.lineplot(
            x="year",
            y="adult_literacy",
            data=df
        )

        ax.set_title("Literacy Trend")

        st.pyplot(fig)


# ---------------- COUNTRY PROFILE PAGE ----------------
elif selected == "Country Profile Page":

    st.title("🌍 Country Profile")

    conn = sqlite3.connect("merged.db")
    df = pd.read_sql("SELECT * FROM merged_data", conn)

    country = st.selectbox(
        "Select Country",
        sorted(df["country"].dropna().unique())
    )

    df_country = df[df["country"] == country].sort_values("year")

    st.dataframe(df_country)


    st.subheader("📈 Literacy Trend")

    fig, ax = plt.subplots()

    ax.plot(df_country["year"], df_country["literacy_rate"])

    st.pyplot(fig)


    st.subheader("💰 GDP Trend")

    fig, ax = plt.subplots()

    ax.plot(df_country["year"], df_country["GDP_per_capita_PPP"])

    st.pyplot(fig)


    st.subheader("🎓 Schooling Trend")

    fig, ax = plt.subplots()

    ax.plot(df_country["year"], df_country["avg_years_of_schooling"])

    st.pyplot(fig)


    st.subheader("📉 Illiteracy Trend")

    fig, ax = plt.subplots()

    ax.plot(df_country["year"], df_country["Illiteracy_percent"])

    st.pyplot(fig)
