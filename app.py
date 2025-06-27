import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.forecast import forecast_rate

# Load data
df = pd.read_csv("data/dummy_currency_rates.csv")
df["Date"] = pd.to_datetime(df["Date"])

# List of currencies
currencies = [col for col in df.columns if col != "Date"]

# Sidebar: currency selection
st.sidebar.title("Currency Dashboard")
selected_currency = st.sidebar.selectbox("Select a currency:", currencies)

# Page title
st.title(f"💱 Exchange Rate Trend: USD to {selected_currency}")

# Select & forecast data
df_selected = df[["Date", selected_currency]].rename(columns={selected_currency: "Rate"})
df_forecasted = forecast_rate(df_selected)

# Get only real data for metrics
df_real = df_forecasted[df_forecasted["Is_Prediction"] == False]
avg_rate = df_real["Rate"].mean()
max_rate = df_real["Rate"].max()
min_rate = df_real["Rate"].min()

# Display metrics
st.metric("Average Rate", f"{avg_rate:.2f}")
st.metric("Highest Rate", f"{max_rate:.2f}")
st.metric("Lowest Rate", f"{min_rate:.2f}")

# Trend chart
fig, ax = plt.subplots()

# Real data
ax.plot(df_real["Date"], df_real["Rate"], marker="o", linestyle="-", label="Real", color="blue")

# Forecast data
df_pred = df_forecasted[df_forecasted["Is_Prediction"] == True]
ax.plot(df_pred["Date"], df_pred["Rate"], marker="x", linestyle="-", label="Forecast", color="orange")

ax.set_xlabel("Date")
ax.set_ylabel("Rate")
ax.set_title(f"USD to {selected_currency} - 30 Days + Forecast")
ax.grid(True)
ax.legend()
fig.autofmt_xdate()

st.pyplot(fig)

# Download CSV button
st.subheader("📥 Download Forecast Data")
csv = df_forecasted.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"forecast_{selected_currency}.csv",
    mime="text/csv"
)
