import csv


def getCVSData(fileName):
    # Create an empty list to store rows
    rows = []
    # Open the CSV file
    dataFile = open(fileName, 'r')

    # Create a CSV Reader from CSV file
    reader = csv.reader(dataFile)

    # Skip the headers
    next(reader)

    # Add rows from reader list
    for row in reader:
        rows.append(row)
    return rows
