from typing import Dict, Callable
import struct


class FixedWidthTextParser:
    """
    Imports a fixed width file
    """

    def __init__(self, field_widths, as_dict=False):
        """
        Set the initial field widths values. Negative values indicate that section should be skipped.

        :param field_widths: A single list of integers (or dictionary with int values) that indicate the field widths
        """
        self.parse_func: Callable = None
        self.parse_dict: Dict[str, Callable] = {}

        if isinstance(field_widths, dict):
            as_dict = True

        if as_dict:
            self.field_widths_length = {}
            for s in field_widths:
                self.parse_dict[s] = self._build_fmt_string(field_widths[s])
                self.field_widths_length[s] = self._fw_length(field_widths[s])
        else:
            field_widths = list(field_widths)
            self.parse = self._build_fmt_string(field_widths)
            self.field_widths_length = self._fw_length(field_widths)

        self.field_widths = field_widths
        self._as_dict = as_dict

    @staticmethod
    def _build_fmt_string(field_widths):
        """
        Build the formatting function that splits the input text.

        :param field_widths: A list of integers that indicate the field widths
        :returns: A function that is used to split a string into a list of strings
        """
        fmt_string = ' '.join('{}{}'.format(abs(fw), 'x' if fw < 0 else 's') for fw in field_widths)
        field_struct = struct.Struct(fmt_string)
        return field_struct.unpack_from

    @staticmethod
    def _fw_length(field_widths):
        """
        Calculate the total length of the field width definition. Absolute values are used so that negative values
        (which indicate skipped characters) are accounted for properly.

        :param field_widths: A list of integers that indicate the field widths
        :returns: The sum of field width lengths
        """
        return sum(map(abs, field_widths))

    def _build_trimmed_fw(self, field_widths, line):
        """
        Build a custom parsing function that works on input strings that don't include padding for optional fields.

        :param field_widths: A list of integers that indicate the field widths
        :param line: A single line of text that needs to be separated
        :returns: A function that is used to split a string into a list of strings
        """
        while self._fw_length(field_widths) > len(line):
            field_widths.pop()  # Drop fields that aren't present in input string
        diff = len(line) - self._fw_length(field_widths)
        if diff > 0:
            field_widths.append(diff)
        return self._build_fmt_string(field_widths)

    def read_fixed_width(self, s: str):
        """
        Parse a single line of input with the field widths values.

        :param s: A single line of text that needs to be separated
        :returns: A list of values that are parsed from the input text based on the field widths.
                  This list is empty if a field widths dictionary cannot be matched to the input text.
        """

        if self._as_dict:
            # Choose the appropriate field_widths list from the dictionary
            key = None
            for k in self.field_widths:
                if len(k) <= len(s) and k == s[:len(k)]:
                    key = k
                    break

            if key is None:
                return []

            if len(s) >= self.field_widths_length[key]:
                parser = self.parse_dict[key]
            else:
                parser = self._build_trimmed_fw(self.field_widths[key][:], s)

        else:
            # Only one field_widths list is available
            if len(s) >= self.field_widths_length:
                parser = self.parse
            else:
                parser = self._build_trimmed_fw(self.field_widths[:], s)

        ret = []
        parsed = parser(str.encode(s))
        for p in parsed:
            ret.append(p.decode(encoding='latin-1').strip())

        return ret

    def read_file(self, file_path):
        """
        Parse all the lines of a file.

        :param file_path: Input file path
        :returns: A list of parsed lines from the input file.
        """
        with open(file_path, 'r') as f:
            return list(map(lambda line: self.read_fixed_width(line), f))
