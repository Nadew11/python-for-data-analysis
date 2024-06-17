#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:13:27 2024

@author: naodasfaw
Questions
- How many Sales have they made with amounts more than 100
- How many Sales  have they made that belong to the category "Tops" and have Quantity of 3
- The Total sales by Catagory
- Average Amount by Catagory and Status
- Total Sales by Fulfilment and Status
"""

import pandas as pd
# extract the data from excel file and load it to a data frame
sales_data = pd.read_excel("/Users/naodasfaw/Desktop/data projects/Amazon Sales Project/Sales_data.Xlsx")

#==============================================================
#Exploring the data
#==============================================================
#get summery information about the data
sales_data.info()
sales_data.describe()

#looking at the columns
print(sales_data.columns)

#looking at the first few rows
print(sales_data.head())

#check data types of the column
print(sales_data.dtypes)

#==============================================================================
# cleaning the data
#==============================================================================

#check for missing values
print(sales_data.isnull().sum())

#drop all missing values
sales_data_dropped = sales_data.dropna()

#drop rows with missing amounts
sales_data_cleaned = sales_data.dropna(subset = ['Amount'])

#check for missing values cleaned
print(sales_data_cleaned.isnull().sum())

#X=============================================================================
#x slicing and catagorising the data
#x=============================================================================

#catagory with the Top Value
catagory_data = sales_data[sales_data['Category'] == 'Top']
print(catagory_data)

#catagory of the amount greater than 1000
high_amount_data = sales_data[sales_data['Amount'] > 1000]
print(high_amount_data)

#select a subset of data based on the top and quantity greater than 3
filtered_data = sales_data[(sales_data['Category'] == 'Top') & (sales_data['Qty'] == 3)]

# =============================================================================
# Aggregating data
# =============================================================================

#Total sales by catagory
category_total = sales_data_cleaned.groupby('Category')['Amount'].sum()
category_total = sales_data_cleaned.groupby('Category', as_index = False)['Amount'].sum()
#category_total = category_total.sort('Amount',ascending = False)
category_total = category_total.sort_values("Amount",ascending = False)

#calculate the average amount  by Catagorty and fulfiment 
Fulfilment_average = sales_data.groupby(['Category','Fulfilment'], as_index= False)['Amount'].mean()
Fulfilment_average = Fulfilment_average.sort_values('Amount',ascending = False)

#calculate the average by category and status
status_average = sales_data.groupby(['Category','Status'],as_index = False)['Amount'].mean()
status_average = status_average.sort_values('Amount',ascending = False)

# Total sales by shipment and fulfilment
total_shipment = sales_data.groupby(['Courier Status','Fulfilment'],as_index = False)['Amount'].mean()
total_shipment = total_shipment.sort_values('Amount',ascending = False)
total_shipment.rename(columns = {'Courier Status' : 'Shipment'}, inplace  = True)

# =============================================================================
# Exporting the data
# =============================================================================
status_average.to_excel("average_sales_by_category_and_status.xlsx", index=False)
total_shipment.to_excel('total_sales_by_shipment_and_fulfilment.xlsx', index=False)






