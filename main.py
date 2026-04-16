import csv

import pandas

sales_0 = pandas.read_csv("data/daily_sales_data_0.csv")
sales_1 = pandas.read_csv("data/daily_sales_data_1.csv")
sales_2 = pandas.read_csv("data/daily_sales_data_2.csv")

files = ['data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv']

final_list = []

for file in files:

    data = pandas.read_csv(file)
    # filter out others
    data = data[data["product"] == "pink morsel"]

    #Calculate Sales: price * quantity
    if data['price'].dtype == 'object':
        data['price'] = data['price'].str.replace('$', '').astype(float)

    data['sales'] = data['price'] * data['quantity']

    final_list.append(data)


final_data = pandas.concat(final_list)

final_data.to_csv('data/formatted_data_task1.csv', index=False)
