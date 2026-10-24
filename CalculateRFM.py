import pandas as pd
import datetime as dt

# 1. Load the cleaned dataset
df = pd.read_csv('cleaned_online_retail.csv')

# Ensure InvoiceDate is parsed as datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 2. Define a Reference Date for Recency calculation
# (Set to 1 day after the latest transaction date in the dataset)
snapshot_date = df['InvoiceDate'].max() + dt.timedelta(days=1)
print(f"Snapshot Date for Recency calculation: {snapshot_date}")

# 3. Group by CustomerID and calculate R, F, and M
rfm_df = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency: Days since last purchase
    'InvoiceNo': 'nunique',                                  # Frequency: Total number of unique orders
    'TotalPrice': 'sum'                                      # Monetary: Total money spent
})

# 4. Rename the columns for clarity
rfm_df.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
}, inplace=True)

# 5. View the first few rows of the RFM table
print("\nSample RFM Table:")
print(rfm_df.head())

# 6. Save the aggregated table for the next step
rfm_df.to_csv('rfm_table.csv')
print("\nSuccess! RFM table saved as 'rfm_table.csv'.")