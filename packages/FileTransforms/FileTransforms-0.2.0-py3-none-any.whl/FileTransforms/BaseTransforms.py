import logging
import os
import time
from typing import List, Dict, Iterable, Callable, Union, Any
from difflib import get_close_matches
from .header_utils import load_headers, generate_header_lookup_dict, enumerate_headers
from .FileType import FileType
from .Result import BaseResult
from .csv_utils import read_csv
from .ColumnMod import ColumnMod
from .FixedWidthTextParser import FixedWidthTextParser
from .Exceptions import ProcessingFunctionReturnError


class BaseTransform:

    def __init__(self, result: BaseResult = None, log_level: int = logging.ERROR) -> None:
        if result is None:
            result = BaseResult()

        self.result: BaseResult = result

        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            h = logging.StreamHandler()
            h.setFormatter(logging.Formatter('%(asctime)s [%(levelname)-5.5s]  %(message)s'))
            self.logger.addHandler(h)

        self.logger.setLevel(log_level)

        self.output_name: str = 'transformed.csv'
        self.output_type: FileType = FileType.CSV

        # these functions are run in sequence to clean up the input data - processing func example:
        '''
        def processing_func(data):
           pass
        return data  # data is passed to next processing func
        '''
        self.pre_processing_funcs: List[Callable[[List], List]] = []
        self.processing_funcs: List[Callable[[Iterable], List]] = []

        self.input_delimiter: str = ','
        self.combine_inputs = False  # Determine if processing functions should be applied to each input or all at once
        self.output_options: Dict = {}

        self.current_file_path: str = None  # Updated every time a new file is read and processing begins

        self.has_headers: bool = True  # (First) input file will have headers to parse
        self.headers: List[str] = None  # Current list of headers
        self.header_map: Dict[str, str] = {}  # Dictionary of header replacements
        self.enumerable_headers: List[str] = []  # Headers that will repeat and need a number suffix
        self.prefixable_headers: List[str] = []  # Headers that need a prefix
        self.column_mods: Dict[int, ColumnMod] = {}
        self.has_parsed_headers = False  # Set this to true as soon as headers are parsed so that they aren't redone
        self.run_parse_headers = True  # Determine if self.parse_headers() should be run on the header list
        self.default_not_found: str = None  # Default replacement if not specified by self.header_map
        self.headers_file_path: str = None  # File path to a JSON file filled with header replacements
        self.header_ratio_min = 0.0  # How closely the original header needs to match a potential replacement option
        self.valid_headers = None  # Only allow this list of header replacements if not None

    # noinspection PyUnusedLocal
    @staticmethod
    def input_validate_func(i: int, r: List[Any]) -> (bool, List[Any]):
        """
        Make modifications to an input row and determine if it should be used or discarded.
        Children can override this method to easily make changes to inputs.

        :param i: The index of the row in the input file
        :param r: The row data from the input file
        :return: Bool that determines if row should be kept and the (modified) row data
        """
        return True, r

    def contains_headers(self, headers: Iterable[str]) -> bool:
        """
        Determine if the parsed headers contains a given set of headers

        :param headers: Set of headers to search for
        :return: True if all of the provided headers exist
        """
        for header in headers:
            if header not in self.headers:
                return False
        return True

    def get_header_idx(self, header: str):
        """
        Get the index of the headers list with a given header

        :param header: Header token text
        :returns: Integer corresponding to the index or -1 if the header can not be found
        """
        try:
            return self.headers.index(header)
        except ValueError:
            return -1

    def get_header_indices(self, headers: Iterable[str]) -> Dict[str, Union[int, None]]:
        indices = {}
        for h in headers:
            idx = self.get_header_idx(h)
            indices[h] = idx if idx >= 0 else None

        return indices

    def get_output_file_path(self, file_path=None):
        if file_path is not None:
            return os.path.join(os.path.dirname(file_path), self.output_name)
        else:
            new_file_path = os.path.join('~/Desktop', self.output_name)
            self.logger.info('No file path was given, so the output file is at {}'.format(new_file_path))

        return new_file_path

    def remove_token_from_headers_map(self, header_map: Dict[str, str], token: str):
        if token in self.enumerable_headers:
            return

        for k in list(filter(lambda h: header_map[h] == token, header_map.keys())):
            del header_map[k]

    @staticmethod
    def normalize_header(header):
        while '  ' in header:
            header = header.replace('  ', ' ')
        return header.upper().strip()

    def parse_headers(self) -> (List[str]):
        m = {}

        if not self.headers:
            return self.headers

        # Standardize format of all keys in dictionary
        header_map = {
            self.normalize_header(k) if isinstance(k, str) else k: self.normalize_header(v) if isinstance(v, str) else v
            for k, v in self.header_map.items()
        }

        if self.headers_file_path:
            data = load_headers(self.headers_file_path)
            if data:
                m = data
                if self.valid_headers:
                    for h in list(m.keys()):
                        if h not in self.valid_headers:
                            del m[h]

            elif self.logger:  # pragma: no cover
                self.logger.error('{} is not a valid headers_filename'.format(self.headers_file_path))

        header_map = {**generate_header_lookup_dict(m, self.normalize_header),
                      **header_map}  # override values from file with header_map parameter dictionary

        return self._parse_each_header(header_map)

    @staticmethod
    def _generate_variations(header):
        return [header]

    def try_header_variations(self, header, header_map, all_headers) -> (bool, str):
        if not header_map:
            return False, header

        header = self.normalize_header(header)

        if header in header_map:
            return True, header_map[header]

        variations = self._generate_variations(header)

        best_k = None
        best_ratio = 0.0

        for var_header in variations:
            if var_header in all_headers:
                return True, var_header

            if var_header in header_map.keys():
                ret = header_map[var_header]
                return True, ret

            for k in filter(lambda _k: _k in var_header, header_map.keys()):
                ratio = len(k) / 1.0 / len(var_header)
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_k = k

        if best_ratio > self.header_ratio_min:
            ret = header_map[best_k]
            return True, ret

        # Check for missing/added spaces
        for var_header in variations:
            matches = get_close_matches(var_header, header_map.keys(), 1, 0.9)
            if len(matches) > 0:
                ret = header_map[matches[0]]
                self.remove_token_from_headers_map(header_map, ret)
                return True, ret

        return False, header

    def _parse_each_header(self, header_map):
        headers = self.headers[:]
        all_headers = self.valid_headers if self.valid_headers else []
        for i, _header in enumerate(headers):
            if _header is None or _header == '':
                headers[i] = self.default_not_found if self.default_not_found is not None else ''
                continue

            header = self.normalize_header(_header)

            if header in all_headers and header not in header_map and (
                    not self.valid_headers or header in self.valid_headers):
                headers[i] = header
                self.remove_token_from_headers_map(header_map, header)
                continue
            else:
                found, headers[i] = self.try_header_variations(header, header_map, all_headers)
                if found:
                    self.remove_token_from_headers_map(header_map, headers[i])

            if self.default_not_found and headers[i] == header and header not in all_headers:
                headers[i] = self.default_not_found

            if headers[i] in self.prefixable_headers:
                self.column_mods[i] = ColumnMod(prefix=_header + ': ')

            if headers[i] not in all_headers and self.valid_headers:  # pragma: no cover
                self.logger.error('{} is not a valid header'.format(headers[i]))

        return enumerate_headers(headers, self.enumerable_headers)

    def _process_input_data(self, data: List):
        """
        Processes each line of the input file and runs any existing input validation functions.

        :param data: List of rows from the input file
        :returns: Validated and modified input data
        """
        processed_input = []
        for i, r in enumerate(data):
            add, r = self.input_validate_func(i, r)

            if add:
                processed_input.append(r)

        return processed_input

    def _apply_column_mods(self, data: List):
        if not self.column_mods:
            return data

        for r in data:
            for i in self.column_mods:
                if i < len(r):
                    r[i] = self.column_mods[i].apply(r[i])

        return data

    def read_input_file(self, file_path: str) -> List:
        """
        Read the input file

        :param file_path: String path of the input file.
        """
        self.logger.info('read data from: {}'.format(file_path))
        return self._process_input_data(read_csv(file_path, delimiter=self.input_delimiter))

    @staticmethod
    def _run_processing_funcs(funcs: List[Callable], data: List):
        """
        Run the sequence of processing functions before writing the data to disk

        :param data: Data to be processed
        :return: Processed data
        """
        if data is None:
            data = []

        processed_input = data[:]

        for func in funcs:
            if processed_input is None:
                raise ProcessingFunctionReturnError
            processed_input = func(processed_input)

        return processed_input

    def run_processing_funcs(self, data):
        """
        Call the processing functions that run after the headers have been parsed
        :param data: Preprocessed input data
        :return: Data that has been sequentially processed by the list of functions
        """
        return self._run_processing_funcs(self.processing_funcs, data)

    def run_pre_processing_funcs(self, data):
        """
        Call the pre-processing functions that run before the headers have been parsed
        :param data: Input data
        :return: Data that has been sequentially processed by the list of functions
        """
        return self._run_processing_funcs(self.pre_processing_funcs, data)

    def run(self, file_path: str = None, file_paths: List[str] = None, data: List = None,
            dest_path: str = None, write_output: bool = True) -> BaseResult:
        """
        Runs the macro. Uses a combination of preset values and any necessary human input to generate an output file.

        :param file_path: String path of the input file. If None, user is prompted to select a file.
        :param file_paths: List of string paths of the input files.
        :param data: Array of pre-processed input data
        :param dest_path: Output file path
        :param write_output: Determine if output file(s) should be written on completion
        """

        start = time.time()

        if file_paths is None:
            file_paths = []

        if data is not None and (dest_path is not None or not write_output):
            self._run(self._process_input_data(data), dest_path, write_output)

        elif file_path is None and not file_paths:
            return self.result

        if file_path is not None and file_path not in file_paths:
            file_paths.append(file_path)

        # Avoid putting file paths in list multiple times
        self.result.input_file_paths.extend(list(filter(lambda x: x not in self.result.input_file_paths, file_paths)))
        combined_data = []

        for file_path in set(file_paths):
            self.current_file_path = file_path
            input_data = self.read_input_file(file_path)

            if self.combine_inputs:
                if self.has_headers and combined_data and len(input_data) > 0:
                    input_data.pop(0)

                combined_data.extend(input_data)
            else:
                self._run(input_data, self.get_output_file_path(file_path))

        if self.combine_inputs and data is None:
            self._run(combined_data, self.get_output_file_path(file_path))

        if write_output:
            self.result.write_all()  # write contents of all output files

        run_time = time.time() - start
        self.result.execution_time += run_time
        self.logger.info('{} seconds'.format(run_time))

        return self.result

    def _run(self, data, dest_path, write_output: bool = True):
        """
        Process data and write it to an output file

        :param data: Data to be processed and written
        :param dest_path: Output file path
        """
        data = self._apply_column_mods(
            self.run_processing_funcs(self.process_headers(self.run_pre_processing_funcs(data)))
        )

        filename = self.output_name if dest_path is None or os.path.isdir(dest_path) else os.path.basename(dest_path)
        if filename in self.result.output_files:
            self.result.get_file(filename).data.extend(data)
            return

        output_file = self.result.add_file(filename, headers=self.headers, file_type=self.output_type)
        output_file.data = data
        output_file.output_options = self.output_options

        if write_output:
            output_file.file_path = dest_path if dest_path is None or not os.path.isdir(dest_path) else os.path.join(
                dest_path, self.output_name)

    def process_headers(self, data):
        if self.has_headers:
            if self.headers is None and len(data) > 0:
                self.headers = data.pop(0)
            elif len(data) > 0:
                data.pop(0)

        if self.run_parse_headers and not self.has_parsed_headers:
            self.headers = self.parse_headers()
            self.has_parsed_headers = True

        return data


class FixedWidthTransform(BaseTransform):
    """
    Processes files just like BaseTransform but reads fixed-width text files instead of CSVs
    """

    def __init__(self, field_widths: Union[Dict, Iterable] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ti = FixedWidthTextParser(field_widths)
        self.has_headers = False

    def read_input_file(self, file_path: str):
        """
        Read an input file. Uses the TextImporter rules to split each line into an array

        :param file_path: Input file path
        :returns: List of processed input data from the input file
        """
        return self._process_input_data(self.ti.read_file(file_path))


class SingleLineFixedWidthTransform(FixedWidthTransform):
    """
    Splits single line text file into format that FixedWidthTransform can handle
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_length = 1024

    def read_input_file(self, file_path: str):
        """
        Read an input file. Reads part of file and then uses the TextImporter rules to split each line into an array

        :param file_path: Input file path
        :returns: List of processed input data from the input file
        """
        data = []
        with open(file_path, 'r') as f:
            while True:
                line = f.read(self.line_length)
                if line == '':
                    return self._process_input_data(data)

                if len(line) == self.line_length:
                    data.append(self.ti.read_fixed_width(line))
