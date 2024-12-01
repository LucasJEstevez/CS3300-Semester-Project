import csv

#Compare the available cars and sold cars csv to find any matches of year, make, and model to display a recently sold price.
def compare_and_merge_csv(file1, file2, match_columns, additional_column, output_file):
    file2_data = {}
    #Parse the sold cars file to get the columns passed (should be year, make, and model)
    with open(file2, mode='r') as f2:
        reader2 = csv.reader(f2)
        headers2 = next(reader2)
        
        for row in reader2:
            key = tuple(row[i] for i in match_columns)
            file2_data[key] = row[additional_column]

    #Parse the available cars csv for year, make, and model then check for matches and add a price into the recently sold column if a match is found
    with open(file1, mode='r') as f1, open(output_file, mode='w', newline='') as out_file:
        reader1 = csv.reader(f1)
        writer = csv.writer(out_file)

        headers1 = next(reader1)
        writer.writerow(headers1 + [headers2[additional_column]])

        for row in reader1:
            key = tuple(row[i] for i in match_columns)
            additional_value = file2_data.get(key, '')
            writer.writerow(row + [additional_value])