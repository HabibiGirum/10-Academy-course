import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
def load_data():
    df = pd.read_csv('solar_measurements_benin_malanville_qc_year2.csv', encoding='latin1')
    # Ensure 'GHI' column is numeric, coercing errors to NaN
    df['GHI'] = pd.to_numeric(df['GHI'], errors='coerce')
    return df



df = load_data()

# Title of the dashboard
st.title("Data Insights Dashboard")

# Display data information
st.write("### Data Overview")
st.write(df.head())

# Sidebar for interactive elements
st.sidebar.title("Interactive Controls")
slider_value = st.sidebar.slider("Select a Range for GHI", min_value=float(df['GHI'].min()), max_value=float(df['GHI'].max()), value=(float(df['GHI'].min()), float(df['GHI'].max())))
filtered_df = df[(df['GHI'] >= slider_value[0]) & (df['GHI'] <= slider_value[1])]

# Display filtered data based on slider
st.write(f"### Filtered Data (GHI between {slider_value[0]} and {slider_value[1]})")
st.write(filtered_df)

# Create a plot based on the filtered data
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=filtered_df['Timestamp'], y=filtered_df['GHI'], ax=ax)
ax.set_title("GHI Over Time (Filtered by Range)")
plt.xticks(rotation=45)
st.pyplot(fig)

# Allow users to choose a column for correlation plot
column_choice = st.selectbox("Select a column for correlation plot", options=df.columns)
st.write(f"Correlation of {column_choice} with GHI:")
st.write(df[column_choice].corr(df['GHI']))
