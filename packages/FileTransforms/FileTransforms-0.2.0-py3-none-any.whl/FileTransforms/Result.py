from typing import List, Dict, Tuple, Union
import collections
import os
import csv
from .FileType import FileType
from .csv_utils import write_csv

try:
    # noinspection PyUnresolvedReferences
    import pandas as pd
except ModuleNotFoundError:
    pass


class BaseOutputFile:

    def __init__(self, filename: str = 'default.csv', file_type: FileType = FileType.CSV) -> None:
        self.filename = filename
        self.file_type = file_type
        self.data = []
        self.headers = None
        self.file_path: str = ''
        self.sheet_name = 'Sheet 1'
        self.output_options: Dict = {
            'delimiter': ',',
            'quotechar': '"',
            'quoting': csv.QUOTE_NONNUMERIC,
        }
        self.write_methods = {
            FileType.CSV: self._write_csv,
            FileType.TEXT: self._write_text,
            FileType.XLSX: self._write_xlsx,
        }

    def add_row(self, r):
        self.data.append(r)

    def _write_csv(self):
        data = self.data
        if self.headers is not None:
            data = [self.headers] + data
        write_csv(self.file_path, data, **self.output_options)

    def _write_text(self):
        with open(self.file_path, 'w') as f:
            for r in self.data:
                f.write(str(r) + '\n')

    def _write_xlsx(self):
        if self.headers is None:
            self.headers = self.data.pop(0)

        df = pd.DataFrame(self.data, columns=self.headers)
        writer = pd.ExcelWriter(self.file_path)
        df.to_excel(writer, index=False, sheet_name=self.sheet_name)
        writer.save()

    def write_to_file(self, folder_path: str = './') -> bool:
        if self.file_path == '':
            self.file_path = os.path.join(folder_path, self.filename)

        if not self.data and not self.headers:
            return False

        if self.file_type in self.write_methods:
            self.write_methods[self.file_type]()
            return True

        return False

    def __repr__(self):  # pragma: no cover
        return 'filename: {}, file_path: {}, file_type: {}, len(data): {}'.format(
            self.filename, self.file_path, self.file_type, len(self.data))

    def __getitem__(self, item: Union[int, Tuple[int, Union[str, int]]]):
        if isinstance(item, tuple):
            row, column = item
            if isinstance(item[1], str):
                if column not in self.headers:
                    return None
                column = self.headers.index(column)
            return self.data[row][column]
        return self.data[item]


class BaseResult:

    def __init__(self):
        self.id = 0
        self.error = None
        self.extra = {}
        self.canceled: bool = False
        self.input_file_paths: List[str] = []
        self.output_files: collections.OrderedDict = collections.OrderedDict()
        self.output_file_class = BaseOutputFile
        self.execution_time = 0.0

    def add_file(self, filename: str = 'default.csv', common_name: str = None, headers: List[str] = None,
                 file_type: FileType = FileType.CSV):
        if common_name is None:
            common_name = filename

        self.output_files[common_name] = self.output_file_class(filename, file_type=file_type)
        self.output_files[common_name].headers = headers
        return self.output_files[common_name]

    def add_text_file(self, *args, **kwargs):
        return self.add_file(*args, **kwargs, file_type=FileType.TEXT)

    def get_file(self, name: str) -> BaseOutputFile:
        return self.output_files[name]

    def write_all(self, folder_path: str = None):
        if not folder_path:
            folder_path = './'
        for k in self.output_files:
            self.output_files[k].write_to_file(folder_path)

    def __repr__(self):  # pragma: no cover
        return 'canceled: {}, output_files: {}'.format(self.canceled, self.output_files)
