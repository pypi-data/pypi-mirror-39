import csv


def read_csv(file_path, *args, **kwargs):
    with open(file_path, 'r', newline='') as f:
        return list(csv.reader(f, *args, **kwargs))


def write_csv(file_path, data, *args, **kwargs):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, *args, **kwargs)
        writer.writerows(data)
