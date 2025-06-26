import requests
import pandas as pd
from datetime import datetime, timedelta
import os

def fetch_currency_timeseries(api_key: str):
    # Set date range: last 30 days
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=30)

    # Set URL and parameters
    url = "https://api.exchangerate.host/timeseries"
    params = {
        "access_key": api_key,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "base": "USD",
        "symbols": "IDR,EUR,GBP,JPY"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        print("Raw response:", data)  # Debug (you can remove this after successful run)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Check response validity
    if not data.get("success"):
        print("❌ Failed to retrieve data from API.")
        return

    # Parse into DataFrame
    rates = data.get("rates", {})
    df = pd.DataFrame(rates).T  # Transpose: dates become rows
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().reset_index()
    df.rename(columns={"index": "Date"}, inplace=True)

    # Save to CSV
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "currency_rates.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Data successfully saved to: {output_path}")

if __name__ == "__main__":
    # Replace with your actual API key here
    YOUR_API_KEY = "WRITE_YOUR_API_KEY_HERE"
    fetch_currency_timeseries(YOUR_API_KEY)