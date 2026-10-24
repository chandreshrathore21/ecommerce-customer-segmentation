import pandas as pd

# 1. Load the dataset
# Update the filename/path if necessary
df = pd.read_csv('online_retail.csv', encoding='ISO-8859-1')

print(f"Initial row count: {df.shape[0]}")

# 2. Drop rows where CustomerID is missing
# (We can't segment customers if we don't know who they are)
df = df.dropna(subset=['CustomerID'])

# 3. Remove cancelled orders and returns
# Cancellations in this dataset start with 'C' in InvoiceNo, and Quantity is usually negative
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[df['Quantity'] > 0]

# 4. Feature Engineering: Calculate Total Price for each transaction line
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# 5. Convert InvoiceDate to datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Check the cleaned dataframe shape and info
print(f"Cleaned row count: {df.shape[0]}")
print(df.head())

# 6. Save the cleaned dataset for your SQL or Tableau workflow
df.to_csv('cleaned_online_retail.csv', index=False)