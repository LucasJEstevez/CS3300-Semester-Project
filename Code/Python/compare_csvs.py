import csv

def compare_and_merge_csv(file1, file2, match_columns, additional_column, output_file):
    file2_data = {}
    with open(file2, mode='r') as f2:
        reader2 = csv.reader(f2)
        headers2 = next(reader2)
        
        for row in reader2:
            key = tuple(row[i] for i in match_columns)
            file2_data[key] = row[additional_column]

    with open(file1, mode='r') as f1, open(output_file, mode='w', newline='') as out_file:
        reader1 = csv.reader(f1)
        writer = csv.writer(out_file)

        headers1 = next(reader1)
        writer.writerow(headers1 + ("Last" + [headers2[additional_column]]))

        for row in reader1:
            key = tuple(row[i] for i in match_columns)
            additional_value = file2_data.get(key, '')
            writer.writerow(row + [additional_value])