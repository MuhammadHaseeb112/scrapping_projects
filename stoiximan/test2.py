from datetime import datetime
import pytz
import pandas as pd

# Define the timezone for Greece
greece_timezone = pytz.timezone('Europe/Athens')

# Get the current date and time in Greece
greece_time = datetime.now(greece_timezone)

# Format the date as dd/MM/yyyy
formatted_date = greece_time.strftime('%Y/%m/%d')

# Print the formatted date
print("Current date in Greece (dd/MM/yyyy):", formatted_date)


data_file =  pd.read_excel("excel\example of excel.xlsx")

date = data_file["DATE (dd/MM/yyyy)"]
link = data_file["GAME URL"]
result = data_file["RESULT"]

# price = input("Please enter Price: ")
# print(price)

for index, row in data_file.iterrows():
    print(f"Row {index}:")
    print(row["RESULT"])
    for col_name, cell_value in row.items():
        print(f"  {col_name}: {cell_value}")
    print("-" * 20)  # Separator between rows for clarity
    
    
for index, row in data_file.iterrows():
    date = row["DATE (dd/MM/yyyy)"].strftime('%Y/%m/%d')
    print(f"{date} vs {formatted_date}")
    if date==formatted_date:
        print("date match")
    else:
        print("date not match")

    # print(f"Result: {row["RESULT"]}")
    
    
    print(f"Result: {row['RESULT']}")
    if not pd.isna(row["RESULT"]):
        print("There are NaN values in the 'RESULT' column.")
        
