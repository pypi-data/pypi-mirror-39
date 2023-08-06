import csv

try:
    import pandas as pd
except ModuleNotFoundError:
    pass


def read_csv(file_path, *args, **kwargs):
    with open(file_path, 'r', newline='') as f:
        return list(csv.reader(f, *args, **kwargs))


def write_csv(file_path, data, *args, **kwargs):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, *args, **kwargs)
        writer.writerows(data)


def convert_xlsx_to_csv(file_path):
    csv_file_path = file_path + '.csv'
    data_xls = pd.read_excel(file_path, index_col=None)
    data_xls.to_csv(csv_file_path, index=False)
    return csv_file_path
