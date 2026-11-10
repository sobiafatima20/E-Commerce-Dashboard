import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="E-Commerce DashBoard | Customer Analytics",
    page_icon="🛍️",
    layout="wide"
)

NUMERIC_COLS = [
    "Avg. Session Length",
    "Time on App",
    "Time on Website",
    "Length of Membership",
    "Yearly Amount Spent"
]


@st.cache_data
def read_csv_file(file_bytes):
    return pd.read_csv(BytesIO(file_bytes))


def prepare_data(raw):
    missing = [c for c in NUMERIC_COLS if c not in raw.columns]

    if missing:
        raise ValueError(
            "Required columns missing: " + ", ".join(missing)
        )

    df = raw.copy()

    for col in NUMERIC_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=NUMERIC_COLS)

    return df.drop(columns=["Avatar"], errors="ignore")


def style_axes(ax, title, xlabel="", ylabel=""):
    ax.set_title(title, fontsize=14, pad=12, weight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)


def show_fig(fig):
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# Sidebar
st.sidebar.title("🛍️ E-Commerce DashBoard")
st.sidebar.subheader("📂 Upload Customer Data")

uploaded = st.sidebar.file_uploader(
    "Upload E-commerce CSV",
    type=["csv"]
)

# Load Dataset
try:
    if uploaded is not None:
        raw = read_csv_file(uploaded.getvalue())
        source = uploaded.name

    else:
        try:
            with open("ecommerce_customers.csv", "rb") as f:
                raw = read_csv_file(f.read())

            source = "ecommerce_customers.csv"

        except FileNotFoundError:
            with open("Ecommerce Customers.csv", "rb") as f:
                raw = read_csv_file(f.read())

            source = "Ecommerce Customers.csv"

    commerce = prepare_data(raw)

except FileNotFoundError:
    st.title("🛍️ E-Commerce DashBoard")
    st.warning(
        "CSV nahi mili. Sidebar se CSV upload karein "
        "ya app folder mein ecommerce_customers.csv rakhein."
    )
    st.stop()

except Exception as e:
    st.title("E-Commerce DashBoard")
    st.error(f"Data load error: {e}")
    st.stop()


st.sidebar.success(f"Loaded: {source}")
st.sidebar.caption(f"Clean records: {len(commerce):,}")

st.sidebar.divider()
st.sidebar.title("Dashboard Filters")


# Filters
membership_range = st.sidebar.slider(
    "Membership Duration",
    float(commerce["Length of Membership"].min()),
    float(commerce["Length of Membership"].max()),
    (
        float(commerce["Length of Membership"].min()),
        float(commerce["Length of Membership"].max())
    ),
    step=0.1
)

spending_range = st.sidebar.slider(
    "Yearly Spending Range",
    float(commerce["Yearly Amount Spent"].min()),
    float(commerce["Yearly Amount Spent"].max()),
    (
        float(commerce["Yearly Amount Spent"].min()),
        float(commerce["Yearly Amount Spent"].max())
    ),
    step=10.0
)


filtered = commerce[
    commerce["Length of Membership"].between(*membership_range)
    & commerce["Yearly Amount Spent"].between(*spending_range)
].copy()


st.sidebar.metric("Filtered Customers", len(filtered))

if filtered.empty:
    st.warning("No customers found. Please adjust your filters.")
    st.stop()


# Dashboard Header
st.title("🛍️ E-Commerce DashBoard")
st.subheader("E-Commerce Customer Intelligence Dashboard")

st.write(
    "Explore customer behavior, platform engagement "
    "and yearly spending."
)

st.divider()


# Business Overview
st.subheader("Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Customers", f"{len(filtered):,}")

c2.metric(
    "Average Yearly Spend",
    f"${filtered['Yearly Amount Spent'].mean():,.2f}"
)

c3.metric(
    "Average Membership",
    f"{filtered['Length of Membership'].mean():.2f}"
)

c4.metric(
    "Highest Spending",
    f"${filtered['Yearly Amount Spent'].max():,.2f}"
)


# Dataset Overview
with st.expander("Dataset Overview & Data Quality"):

    left, right = st.columns(2)

    with left:
        st.write("Original shape:", raw.shape)
        st.write("Cleaned shape:", commerce.shape)
        st.write("Columns:", commerce.columns.tolist())

        st.write("First 5 rows")
        st.dataframe(commerce.head(), use_container_width=True)

    with right:
        st.write("Missing values")

        st.dataframe(
            commerce.isnull().sum().rename("Missing Values")
        )

        st.write(
            "Duplicate rows:",
            int(commerce.duplicated().sum())
        )

        if "Email" in commerce.columns:
            st.write(
                "Duplicate emails:",
                int(commerce["Email"].duplicated().sum())
            )

        st.write("Descriptive statistics")

        st.dataframe(
            commerce[NUMERIC_COLS].describe(),
            use_container_width=True
        )


# EDA Analysis
st.divider()
st.header("🔍 EDA Question Analysis")

tab1, tab2, tab3, tab4 = st.tabs([
    "Univariate Analysis",
    "Bivariate Analysis",
    "Own Choice Questions",
    "Correlation Heatmap"
])


# Univariate Analysis: Q1-Q3
with tab1:

    questions = [
        (
            "Question 1",
            "What is the distribution of Yearly Amount Spent among customers?",
            "Yearly Amount Spent",
            "Yearly Spending Distribution"
        ),
        (
            "Question 2",
            "How is the Time on App distributed among customers?",
            "Time on App",
            "Time on App Distribution"
        ),
        (
            "Question 3",
            "What is the distribution of Length of Membership?",
            "Length of Membership",
            "Membership Duration Distribution"
        )
    ]

    for heading, question, col, title in questions:

        st.subheader(heading)
        st.markdown(f"**{question}**")

        fig, ax = plt.subplots(figsize=(10, 4))

        sns.histplot(
            data=filtered,
            x=col,
            bins=25,
            kde=True,
            ax=ax
        )

        style_axes(ax, title, col, "Customer Count")

        show_fig(fig)

        st.info(
            f"Average {col}: {filtered[col].mean():.2f}"
        )

        st.divider()


# Bivariate Analysis: Q4-Q6
with tab2:

    pairs = [
        (
            "Question 4",
            "Is there a relationship between Time on App and Yearly Amount Spent?",
            "Time on App"
        ),
        (
            "Question 5",
            "Is there a relationship between Time on Website and Yearly Amount Spent?",
            "Time on Website"
        ),
        (
            "Question 6",
            "Does Length of Membership have a relationship with Yearly Amount Spent?",
            "Length of Membership"
        )
    ]

    for heading, question, xcol in pairs:

        corr = filtered[xcol].corr(
            filtered["Yearly Amount Spent"]
        )

        st.subheader(heading)
        st.markdown(f"**{question}**")

        fig, ax = plt.subplots(figsize=(10, 4))

        sns.regplot(
            data=filtered,
            x=xcol,
            y="Yearly Amount Spent",
            scatter_kws={"alpha": 0.6},
            line_kws={"color": "red"},
            ax=ax
        )

        style_axes(
            ax,
            f"{xcol} vs Yearly Spending",
            xcol,
            "Yearly Amount Spent"
        )

        show_fig(fig)

        st.metric(
            f"{xcol} Correlation",
            f"{corr:.3f}"
        )

        st.info(
            f"Correlation with yearly spending: {corr:.3f}"
        )

        st.divider()


# Correlations
corr_app = filtered["Time on App"].corr(
    filtered["Yearly Amount Spent"]
)

corr_web = filtered["Time on Website"].corr(
    filtered["Yearly Amount Spent"]
)

corr_membership = filtered["Length of Membership"].corr(
    filtered["Yearly Amount Spent"]
)

stronger_platform = (
    "Mobile App"
    if abs(corr_app) > abs(corr_web)
    else "Website"
)


# Own Choice Questions: Q7-Q8
with tab3:

    # Question 7
    st.subheader("Question 7")

    st.markdown(
        "**Which platform, App or Website, has a stronger "
        "relationship with Yearly Amount Spent?**"
    )

    platform_data = pd.DataFrame({
        "Platform": ["Mobile App", "Website"],
        "Correlation": [corr_app, corr_web]
    })

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.barplot(
        data=platform_data,
        x="Platform",
        y="Correlation",
        hue="Platform",
        legend=False,
        ax=ax
    )

    ax.set_ylim(-1, 1)
    ax.axhline(0, linewidth=0.8)

    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.3f",
            padding=4
        )

    style_axes(
        ax,
        "App vs Website Relationship with Spending",
        "Platform",
        "Correlation"
    )

    show_fig(fig)

    st.success(
        f"{stronger_platform} has the stronger absolute "
        "correlation with yearly spending."
    )

    st.divider()

    # Question 8
    st.subheader("Question 8")

    st.markdown(
        "**Who are the top 10 customers with the highest "
        "Yearly Amount Spent?**"
    )

    top10 = filtered.nlargest(
        10,
        "Yearly Amount Spent"
    ).copy()

    if "Email" in top10.columns:

        top10 = top10[
            ["Email", "Yearly Amount Spent"]
        ]

        label_col = "Email"

    else:

        top10 = top10[
            ["Yearly Amount Spent"]
        ].copy()

        top10.insert(
            0,
            "Customer",
            [
                f"Customer {i}"
                for i in range(1, len(top10) + 1)
            ]
        )

        label_col = "Customer"

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=top10,
        x="Yearly Amount Spent",
        y=label_col,
        ax=ax
    )

    style_axes(
        ax,
        "Top 10 Highest Spending Customers",
        "Yearly Amount Spent",
        "Customer"
    )

    show_fig(fig)

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )

    st.success(
        f"Highest spending customer: "
        f"${top10['Yearly Amount Spent'].max():,.2f}"
    )


# Correlation Heatmap
with tab4:

    st.subheader("Customer Behavior Correlation Heatmap")

    corr_matrix = filtered[NUMERIC_COLS].corr()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        linewidths=0.5,
        ax=ax
    )

    ax.set_title(
        "Correlation Between Numeric Variables",
        pad=14
    )

    show_fig(fig)

    st.info(
        "Correlation shows association, not causation."
    )


# Business Findings
st.divider()
st.header("Main Business Findings")

st.markdown(f"""
1. **Customer Spending:** Average yearly spending is ${filtered['Yearly Amount Spent'].mean():,.2f}.

2. **App Engagement:** Correlation with yearly spending is {corr_app:.3f}.

3. **Website Engagement:** Correlation with yearly spending is {corr_web:.3f}.

4. **Membership:** Correlation with yearly spending is {corr_membership:.3f}.

5. **Platform Comparison:** {stronger_platform} has the stronger absolute correlation in this selection.
""")

st.caption(
    "Correlation indicates association, not causation. "
    "Findings update with the selected filters."
)


# Raw Data and CSV Download
st.divider()
st.header("Raw Customer Data")

if st.checkbox("Show Raw Data Table"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

    st.download_button(
        "⬇️ Download Filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="E-Commerce DashBoard_filtered_data.csv",
        mime="text/csv"
    )


# Footer
st.divider()

st.caption(
    "E-Commerce DashBoard | E-Commerce Customer Intelligence Dashboard"
)
