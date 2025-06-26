import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_rate(df, days=7):
    """
    Forecast future currency rates using linear regression.

    Parameters:
    - df: DataFrame with columns ['Date', 'Rate']
    - days: number of future days to predict

    Returns:
    - DataFrame that combines real and predicted data,
      including a column 'Is_Prediction' to differentiate them
    """

    # Make a copy of the data to avoid modifying the original DataFrame
    df = df.copy()

    # Ensure 'Date' column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert each date into a number (days since the first date)
    df["Day_Num"] = (df["Date"] - df["Date"].min()).dt.days

    # Prepare input (X) and output (y) for regression
    X = df["Day_Num"].values.reshape(-1, 1)  # Features: day numbers (2D array)
    y = df["Rate"].values                    # Target: actual exchange rates

    # Initialize and train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future day numbers for prediction
    last_day = df["Day_Num"].max()
    future_days = np.array([last_day + i for i in range(1, days+1)]).reshape(-1, 1)

    # Generate future actual dates (starting from the next day)
    future_dates = pd.date_range(df["Date"].max() + pd.Timedelta(days=1), periods=days)

    # Predict future exchange rates using the trained model
    predictions = model.predict(future_days)

    # Create a DataFrame for future (predicted) data
    df_future = pd.DataFrame({
        "Date": future_dates,
        "Rate": predictions,
        "Is_Prediction": True
    })

    # Mark the historical data as non-predicted
    df["Is_Prediction"] = False

    # Combine real and predicted data into one DataFrame
    final_df = pd.concat(
        [df[["Date", "Rate", "Is_Prediction"]], df_future],
        ignore_index=True
    )

    return final_df