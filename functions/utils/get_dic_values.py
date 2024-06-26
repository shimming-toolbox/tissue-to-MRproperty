# This function is a util as it will be used to create CSV files from the dictionaries from both label and Volume
import csv
# From Volume class we will create a CSV file of susceptibility with corresponding ID and name
# From Label we will create a CSV file with relaxation times

def to_csv_sus(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ["Label ID", "Name", "Susceptibility"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

def to_csv_relax():
    # Future implementation
    pass
