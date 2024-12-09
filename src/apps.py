import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def load_data():
    # Direct download URL from Google Drive
    url = 'https://drive.google.com/uc?id=1XuCRFXjFs5TqDQh13GHLuxAyQTJmLrFe'
    
    # Read the CSV file directly from the URL
    df = pd.read_csv(url, encoding='latin1')
    
    # Process the data
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')  # Convert Timestamp to datetime
    df['GHI'] = pd.to_numeric(df['GHI'], errors='coerce')  # Ensure GHI is numeric
    df['DNI'] = pd.to_numeric(df['DNI'], errors='coerce')  # Ensure another example column (DNI) is numeric

    # Return the cleaned DataFrame
    return df


df = load_data()
df.dropna(subset=['Timestamp', 'GHI'], inplace=True)  # Drop rows with invalid Timestamp or GHI

# Dashboard Title
st.title("Data Insights Dashboard")

# Sidebar Filter
st.sidebar.title("Filters and Options")
slider_value = st.sidebar.slider(
    "Select a Range for GHI",
    min_value=float(df['GHI'].min()),
    max_value=float(df['GHI'].max()),
    value=(float(df['GHI'].min()), float(df['GHI'].max()))
)
filtered_df = df[(df['GHI'] >= slider_value[0]) & (df['GHI'] <= slider_value[1])]

# Display Filtered Data
st.write(f"### Filtered Data (GHI between {slider_value[0]} and {slider_value[1]})")
st.write(filtered_df)

# Line Plot of GHI Over Time
if st.sidebar.checkbox("Show GHI Over Time Plot"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Timestamp', y='GHI', data=filtered_df, ax=ax)
    ax.set_title("Global Horizontal Irradiance (GHI) Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("GHI (W/m²)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Interactive Data Summary
st.sidebar.subheader("Data Summary")
st.sidebar.write(f"Number of Rows: {df.shape[0]}")
st.sidebar.write(f"Number of Columns: {df.shape[1]}")

# Interactive correlation plot
column_choice = st.selectbox("Select a column for correlation analysis", options=df.columns)
if pd.api.types.is_numeric_dtype(df[column_choice]) and pd.api.types.is_numeric_dtype(df['GHI']):
    correlation = df[column_choice].corr(df['GHI'])
    st.write(f"Correlation between {column_choice} and GHI: {correlation}")
else:
    st.write(f"Selected column '{column_choice}' or GHI contains non-numeric values and cannot be correlated.")

# Deployment
if st.sidebar.button("Deploy App"):
    st.write("App is successfully deployed and ready for public use!")

# Style the app with markdown
st.markdown("<h3 style='text-align: center;'>Interactive Data Dashboard</h3>", unsafe_allow_html=True)
