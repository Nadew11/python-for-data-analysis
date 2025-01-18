#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:17:38 2024

@author: naodasfaw
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working directory
os.chdir('/Users/naodasfaw/Desktop/data projects/Ecommerce Orders Project')

# Check the working directory
print(os.getcwd())

# =============================================================================
# Loading files
# =============================================================================

# Load the orders data
orders_data = pd.read_excel('orders.xlsx')

# Load payment data
payment_data = pd.read_excel('order_payment.xlsx')

# Load customers data
customers_data = pd.read_excel('customers.xlsx')

# ================================================== ===========================
# Describing the data
# =============================================================================
print(orders_data.info())
print(payment_data.info())
print(customers_data.info())

# Handling missing data
print(orders_data.isnull().sum())
print(payment_data.isnull().sum())
print(customers_data.isnull().sum())

# Filling missing values in the orders data
orders_data = orders_data.fillna("N/A")

# Drop rows with missing values in the payment data
payment_data = payment_data.dropna()

# =============================================================================
# Remove duplicates
# =============================================================================

# Remove duplicates from orders data
orders_data = orders_data.drop_duplicates()

# Remove duplicates from payment data
payment_data = payment_data.drop_duplicates()

# =============================================================================
# Filtering the data
# =============================================================================

# Select a subset of the orders data based on the order status
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']

# Reset index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)

# Select a subset of the payments data where payment type = credit card and payment value > 1000
credit_card_payment_data = payment_data[(payment_data['payment_type'] == 'credit_card') & (payment_data['payment_value'] > 1000)]

# Select a subset of customers based on customer state = SP
customers_state_data = customers_data[customers_data['customer_state'] == 'SP']

# =============================================================================
# Merge and join DataFrames
# =============================================================================

merged_data = pd.merge(orders_data, payment_data, on='order_id')

# Join the merged data with customer data on the customer_id column
joined_data = pd.merge(merged_data, customers_data, on='customer_id')

# =============================================================================
# Data visualization
# =============================================================================

# Ensure the 'order_purchase_timestamp' column is in datetime format
joined_data['order_purchase_timestamp'] = pd.to_datetime(joined_data['order_purchase_timestamp'])

# Create fields for month-year, week-year, and year
joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M').astype(str)
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W').astype(str)
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y').astype(str)

# Group by month_year and sum payment values
grouped_data = joined_data.groupby('month_year')['payment_value'].sum().reset_index()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(grouped_data['month_year'], grouped_data['payment_value'])
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.xticks(rotation=90)
plt.yticks(fontsize=8)
plt.title('Monthly Payment Value Over Time')
plt.show()

# Scatter plot
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value': 'sum', 'payment_installments': 'sum'}).reset_index()

plt.figure(figsize=(10, 6))
plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs. Payment Installments')
plt.show()

# Use seaborn for the scatterplot
sns.set_theme(style='darkgrid')

sns.scatterplot(data=scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs. Payment Installments')
plt.show()
plt.tight_layout()

# Bar displays of the data
bar_df = joined_data.groupby(['payment_type', 'month_year'])['payment_value'].sum().reset_index()

pivot_data = bar_df.pivot(index='month_year', columns='payment_type', values='payment_value')

pivot_data.plot(kind='bar', stacked=True)
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per Payment Type by Month')
plt.show()

# Create a box plot
payment_value = joined_data['payment_value']
payment_type = joined_data['payment_type']

#create a separate box plot per payment
plt.boxplot([ payment_value[payment_type == 'credit_card'],
              payment_value[payment_type == 'boleto'],
              payment_value[payment_type == 'voucher'],
              payment_value[payment_type == 'debit_card']],
            
              labels = ['Credirt Card','Boleto','Voucher','Debit Card']
            )

#set the labels and titles
plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.title('Box Plot showing payment value ranges by Payment Type')
plt.show()

# creating a subplot(3 plot in one)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

#ax as the box plot
ax1.boxplot([ payment_value[payment_type == 'credit_card'],
              payment_value[payment_type == 'boleto'],
              payment_value[payment_type == 'voucher'],
              payment_value[payment_type == 'debit_card']],
            
              labels = ['Credirt Card','Boleto','Voucher','Debit Card']
            )
ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Payment Value')
ax1.set_title('Box Plot showing payment value ranges by Payment Type')

#ax2 stacked bar chart
pivot_data.plot(kind='bar', stacked=True, ax = ax2)

ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per Payment Type by Month')

# ax3 as scatter plot
ax3.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value vs. Payment Installments')

fig.tight_layout()

plt.savefig('my_plot.png')




