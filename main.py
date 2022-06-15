import csv
import pandas as pd

class Item:
    def __init__(self, name, class_code, pur_year, pur_price, ammo_rate):
        self.name = name
        self.class_code = class_code
        self.pur_year = int(pur_year)
        self.pur_price = float(pur_price)
        self.ammo_rate = float(ammo_rate)

with open("input_data.csv") as file_name:
    file_read = csv.reader(file_name)
    lines = list(file_read)[1::]
    items = list()
    for line in lines:
        # print(line)
        item = Item(line[0], line[1], line[2], line[3], line[4])
        items.append(item)

# Find the min pur_year
min_pur_year = 9999
for item in items:
    if item.pur_year < min_pur_year:
        min_pur_year = item.pur_year

# generate rows for Table A (ammo values) and Table B (remaining values)
table_A = []
table_B = []
title_row = ["item_name", "class_code", "purchase_year", "purchase_price", "ammo_rate"]

end_year = 2022

for year in range(min_pur_year, end_year+1):
    title_row.append(year)
table_A.append(title_row)
table_B.append(title_row)

for item in items:
    row_A = []
    row_B = []
    remaining_value = item.pur_price
    row_A.append(item.name)
    row_A.append(item.class_code)
    row_A.append(item.pur_year)
    row_A.append(item.pur_price)
    row_A.append(item.ammo_rate)

    row_B.append(item.name)
    row_B.append(item.class_code)
    row_B.append(item.pur_year)
    row_B.append(item.pur_price)
    row_B.append(item.ammo_rate)

    for year in title_row[5::]:
        if year == item.pur_year:
            ammo = item.pur_price * 0.5 * item.ammo_rate
            ammo = round(ammo, 2)
            row_A.append(ammo)
            remaining_value = item.pur_price - ammo
            remaining_value = round(remaining_value, 2)
            row_B.append(remaining_value)
        elif year > item.pur_year:
            ammo = remaining_value * item.ammo_rate
            ammo = round(ammo, 2)
            row_A.append(ammo)
            remaining_value = remaining_value - ammo
            remaining_value = round(remaining_value, 2)
            row_B.append(remaining_value)
        else:
            ammo = ''
            row_A.append(ammo)
            remaining_value = ''
            row_B.append(remaining_value)
    table_A.append(row_A)
    table_B.append(row_B)

# print(table_A)
# print(table_B)

# Output to files
with open("ammo_values_items.csv", "w", newline='') as file_name:
    writer = csv.writer(file_name)
    writer.writerow(table_A[0])
    writer.writerows(table_A[1::])

with open("remaining_values_items.csv", "w", newline='') as file_name:
    writer = csv.writer(file_name)
    writer.writerow(table_B[0])
    writer.writerows(table_B[1::])

# Sort by class_code, then item_code
df = pd.read_csv('ammo_values_items.csv')
df1 = df.sort_values(by=['class_code', 'item_name'])
# print(df1)
df1.to_csv ('ammo_values_items.csv', index = False, header=True)

df = pd.read_csv('remaining_values_items.csv')
df1 = df.sort_values(by=['class_code', 'item_name'])
# print(df1)
df1.to_csv ('remaining_values_items.csv', index = False, header=True)

# Group by class_code
df = pd.read_csv('ammo_values_items.csv')
df1 = df.iloc[:,1]
df2 = df.iloc[:,5:]
df3 = pd.concat([df1, df2], axis=1)
# print(df1)
# print(df2)
# print(df3)
df4 = df3.groupby(['class_code']).sum()
# print(df4)
df4.to_csv ('ammo_values_classes.csv', index = True, header=True)

df = pd.read_csv('remaining_values_items.csv')
df1 = df.iloc[:,1]
df2 = df.iloc[:,5:]
df3 = pd.concat([df1, df2], axis=1)
# print(df1)
# print(df2)
# print(df3)
df4 = df3.groupby(['class_code']).sum()
# print(df4)
df4.to_csv ('remaining_values_classes.csv', index = True, header=True)






