import pandas as pd

# 1. Load the RFM table
rfm = pd.read_csv('rfm_table.csv')

# 2. Assign scores from 1 to 5 using quantiles
# Recency: Lower days is better, so labels are inverted [5, 4, 3, 2, 1]
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency & Monetary: Higher is better, so labels are [1, 2, 3, 4, 5]
# Using rank(method='first') prevents errors if there are many duplicate values
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Convert scores to integers
rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)

# 3. Combine scores into an overall RFM Score string (e.g., '555')
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# 4. Assign customer segments based on their scores
def segment_customer(df):
    if df['R_Score'] >= 4 and df['F_Score'] >= 4 and df['M_Score'] >= 4:
        return 'Champions'
    elif df['F_Score'] >= 3 and df['M_Score'] >= 3:
        return 'Loyal Customers'
    elif df['R_Score'] >= 4 and df['F_Score'] <= 2:
        return 'Recent Customers'
    elif df['R_Score'] <= 2 and df['F_Score'] >= 3:
        return 'At Risk'
    elif df['R_Score'] <= 2 and df['F_Score'] <= 2:
        return 'Lost'
    else:
        return 'Potential Loyalists'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Print out segment breakdown
print("\nCustomer Segment Breakdown:")
print(rfm['Segment'].value_counts())

# 5. Save the final segmented dataset
rfm.to_csv('segmented_customers.csv', index=False)
print("\nSuccess! Segmented table saved as 'segmented_customers.csv'.")