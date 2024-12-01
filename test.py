import csv
import ast

arr = "[]"

arr2 = ast.literal_eval(arr)

for elem in arr2:
    print(elem)

print(arr2)

