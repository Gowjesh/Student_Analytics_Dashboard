
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Analytics Dashboard")
st.caption("📊 Student Performance Analysis System")

df = pd.read_csv("./student_data.csv")

if "Age" in df.columns:
    df["Age"] = df["Age"].fillna(df["Age"].mean()).astype(float).round(2)

if "Marks" in df.columns:
    df["Marks"] = df["Marks"].fillna(df["Marks"].mean()).astype(float).round(2)

if "Attendance" in df.columns:
    df["Attendance"] = df["Attendance"].fillna(df["Attendance"].mean()).astype(float).round(2)

st.sidebar.title("📚 Dashboard Menu")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dataset Preview",
        "Statistics",
        "Visualizations",
        "Top Students",
        "Student Search"
    ]
)

if menu == "Dataset Preview":

    st.header("📋 Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📌 Dataset Information")

    col1, col2 = st.columns(2)

    col1.metric(
        "Rows",
        df.shape[0]
    )

    col2.metric(
        "Columns",
        df.shape[1]
    )

elif menu == "Statistics":

    st.header("📈 Student Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Total Students",
        len(df)
    )

    col2.metric(
        "📝 Average Marks",
        round(df["Marks"].mean(), 2)
    )

    col3.metric(
        "🏆 Highest Marks",
        round(df["Marks"].max(), 2)
    )

    col4.metric(
        "📉 Lowest Marks",
        round(df["Marks"].min(), 2)
    )

    st.subheader("🧮 Numerical Analysis")

    marks = np.array(df["Marks"])

    st.write("Mean :", np.mean(marks).astype(float).round(2))
    st.write("Median :", np.median(marks).astype(float).round(2))
    st.write("Maximum :", np.max(marks).astype(int))
    st.write("Minimum :", np.min(marks).astype(int))
    st.write("Standard Deviation :", np.std(marks).astype(float).round(2))

    st.subheader("🏢 Department Wise Average Marks")

    dept_avg = df.groupby(
        "Department"
    )["Marks"].mean().reset_index()

    st.dataframe(
        dept_avg,
        use_container_width=True
    )

    st.subheader("✅ Pass / Fail Analysis")

    df["Result"] = np.where(
        df["Marks"] >= 50,
        "Pass",
        "Fail"
    )

    st.dataframe(
        df["Result"].value_counts(),
        use_container_width=True
    )

elif menu == "Visualizations":

    st.header("📊 Data Visualizations")

    chart_type = st.selectbox(
        "📊 Select Visualization",
        [
            "📈 Line Chart - Mark Improvement",
            "📊 Bar Chart - Department Average Marks",
            "🥧 Pie Chart - Gender Distribution",
            "📉 Histogram - Marks Distribution",
            "🔵 Scatter Plot - Attendance vs Marks",
            "🔥 Heatmap - Correlation Analysis",
            "📦 Boxplot - Marks Distribution by Department"
        ]
    )

    if chart_type == "📈 Line Chart - Mark Improvement":

        fig, ax = plt.subplots(figsize=(10,3))

        if "StudentID" in df.columns:

            sorted_df = df.sort_values("StudentID")

            ax.plot(
                sorted_df["StudentID"],
                sorted_df["Marks"],
                marker="1"
            )

            ax.set_xlabel("Student ID")
            ax.set_ylabel("Marks")

        else:

            ax.plot(
                df.index,
                df["Marks"],
                marker="o"
            )

        ax.set_title("Marks Trend")

        st.pyplot(fig)

    elif chart_type == "📊 Bar Chart - Department Average Marks":

        dept_marks = df.groupby(
            "Department"
        )["Marks"].mean()

        fig, ax = plt.subplots(figsize=(10,3))

        ax.bar(
            dept_marks.index,
            dept_marks.values
        )

        ax.set_title("Department Average Marks")
        ax.set_xlabel("Department")
        ax.set_ylabel("Average Marks")

        st.pyplot(fig)

    elif chart_type == "🥧 Pie Chart - Gender Distribution":

        gender_count = df["Gender"].value_counts()

        fig, ax = plt.subplots(figsize=(1,1))

        ax.pie(
            gender_count,
            labels=gender_count.index,
            autopct="%1.1f%%",
            textprops={"fontsize":8}
        )

        ax.set_title(
            "Gender Distribution",
            fontsize=10
        )

        st.pyplot(fig)

    elif chart_type == "📉 Histogram - Marks Distribution":

        fig, ax = plt.subplots(figsize=(10,3))

        ax.hist(
            df["Marks"],
            bins=10
        )

        ax.set_title("Marks Distribution")
        ax.set_xlabel("Marks")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    elif chart_type == "🔵 Scatter Plot - Attendance vs Marks":

        fig, ax = plt.subplots(figsize=(10,3))

        ax.scatter(
            df["Attendance"],
            df["Marks"]
        )

        ax.set_title("Attendance vs Marks")
        ax.set_xlabel("Attendance")
        ax.set_ylabel("Marks")

        st.pyplot(fig)

    elif chart_type == "🔥 Heatmap - Correlation Analysis":

        numeric_df = df.select_dtypes(
            include=np.number
        )

        corr_matrix = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(3, 3))

        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        ax.set_title("Correlation Heatmap")

        st.pyplot(fig)

    elif chart_type == "📦 Boxplot - Marks Distribution by Department":

        fig, ax = plt.subplots(figsize=(10, 3))

        sns.boxplot(
            x="Department",
            y="Marks",
            data=df,
            ax=ax
        )

        ax.set_title(
            "Marks Distribution by Department"
        )

        st.pyplot(fig)

elif menu == "Top Students":

    st.header("🥇 Top 10 Students")

    filter_type = st.selectbox(
        "🔽 Select Filter",
        [
            "Overall",
            "Department",
            "Gender",
            "City",
            "Age"
        ]
    )

    filtered_df = df.copy()

    if filter_type == "Department":

        department = st.selectbox(
            "🏢 Select Department",
            sorted(
                df["Department"]
                .dropna()
                .unique()
            )
        )

        filtered_df = df[
            df["Department"] == department
        ]

    elif filter_type == "Gender":

        gender = st.selectbox(
            "🚻 Select Gender",
            sorted(
                df["Gender"]
                .dropna()
                .unique()
            )
        )

        filtered_df = df[
            df["Gender"] == gender
        ]

    elif filter_type == "City":

        city = st.selectbox(
            "🌍 Select City",
            sorted(
                df["City"]
                .dropna()
                .unique()
            )
        )

        filtered_df = df[
            df["City"] == city
        ]

    elif filter_type == "Age":

        age = st.selectbox(
            "🎂 Select Age",
            sorted(
                df["Age"]
                .dropna()
                .astype(int)
                .unique()
            )
        )

        filtered_df = df[
            df["Age"].astype(int) == age
        ]

    top_students = filtered_df.sort_values(
        by="Marks",
        ascending=False
    ).head(10)

    st.dataframe(
        top_students,
        use_container_width=True
    )

elif menu == "Student Search":

    st.header("👨‍🎓 Student Search")

    name = st.text_input(
        "🔍 Enter Student Name"
    )

    if name:

        result = df[
            df["Name"].str.contains(
                name,
                case=False,
                na=False
            )
        ]

        st.dataframe(
            result,
            use_container_width=True
        )

    st.subheader("🏢 Department Filter")

    department = st.selectbox(
        "🏢 Select Department",
        ["All"] + list(
            df["Department"]
            .dropna()
            .unique()
        )
    )

    if department != "All":

        st.dataframe(
            df[
                df["Department"] == department
            ],
            use_container_width=True
        )

    st.subheader("🚻 Gender Filter")

    gender = st.selectbox(
        "🚻 Select Gender",
        ["All"] + list(
            df["Gender"]
            .dropna()
            .unique()
        )
    )

    if gender != "All":

        st.dataframe(
            df[
                df["Gender"] == gender
            ],
            use_container_width=True
        )

    st.subheader("🎂 Age Filter")

    age = st.selectbox(
        "🎂 Select Age",
        ["All"] + sorted(
            list(
                df["Age"]
                .dropna()
                .astype(int)
                .unique()
            )
        )
    )

    if age != "All":

        st.dataframe(
            df[
                df["Age"]
                .astype(int) == age
            ],
            use_container_width=True
        )

    st.subheader("📝 Marks Filter")

    marks = st.selectbox(
        "📝 Select Marks",
        ["All"] + sorted(
            list(
                df["Marks"]
                .dropna()
                .astype(int)
                .unique()
            )
        )
    )

    if marks != "All":

        st.dataframe(
            df[
                df["Marks"]
                .astype(int) == marks
            ],
            use_container_width=True
        )

    st.subheader("🌍 City Filter")

    city = st.selectbox(
        "🌍 Select City",
        ["All"] + list(
            df["City"]
            .dropna()
            .unique()
        )
    )

    if city != "All":

        st.dataframe(
            df[
                df["City"] == city
            ],
            use_container_width=True
        )
