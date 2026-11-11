# E-Commerce DashBoard – E-Commerce Customer Intelligence Dashboard

## Description

E-Commerce DashBoard is a Streamlit-based dashboard for exploring e-commerce customer data. It uses Python, Pandas, Seaborn, and Matplotlib to perform exploratory data analysis (EDA), visualize customer behavior, compare app and website engagement, and identify the customers with the highest yearly spending.

Users can upload an e-commerce customer CSV file through the sidebar and explore the data using interactive filters and visualizations.

## 3 Key Findings

1. **Membership and Spending:** Length of Membership has the strongest positive relationship with Yearly Amount Spent, with a correlation of approximately **0.81**.
2. **App vs. Website Engagement:** Time on App has a stronger relationship with yearly spending (correlation approximately **0.499**) than Time on Website (approximately **-0.003**).
3. **Customer Spending:** The average Yearly Amount Spent is approximately **499.31**.

## Technologies Used

- Python
- Streamlit
- Pandas
- Seaborn
- Matplotlib

## Run the Project

Install the required libraries:

```bash
pip install streamlit pandas seaborn matplotlib
```

Start the dashboard:

```bash
streamlit run E-Commerce DashBoard_app.py
```

Upload your e-commerce customer CSV file using the sidebar uploader.
