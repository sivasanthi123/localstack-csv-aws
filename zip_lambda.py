import zipfile

with zipfile.ZipFile('process_csv.zip', 'w') as zipf:
    zipf.write('lambda/process_csv.py', arcname='process_csv.py')
print("Zipped lambda/process_csv.py to process_csv.zip")
