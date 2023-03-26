from actual_time import Time
import pandas as pd
import csv
obj=Time()
dataf=obj.total_time()
df = pd.DataFrame(dataf)
with open('my_data.csv', mode='w', newline='') as csv_file:
    # create a writer object
    writer = csv.writer(csv_file)

    # write the header row
    writer.writerow(['Name','Total Time'])

    # write data rows dynamically from the DataFrame
    for row in df.itertuples(index=False):
        writer.writerow(row)
    # table.add_row([])