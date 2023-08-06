# FileTransforms

This project started as a few basic Python functions to replace some very old Excel VBA macros that were used to reformatted client files. The original iteration had a lot of hard-coded header values, but this package can be used to generate a wide variety of outputs with relative ease.

### Converting Excel Workbooks

This package originally included a function that would convert Excel files to CSVs automatically, but it was removed because it was kind of hacky and required a lot of dependencies. If you need a quick and dirty method to do this, install `csvkit` and use the following function.

``` python
def convert_to_csv(file_path, file_type=None):
    csv_file_path = file_path + '.csv'
    file_type = '-f ' + file_type if file_type is not None else ''
    check_call('in2csv {} "{}" > "{}"'.format(file_type, file_path, csv_file_path),
               stdout=DEVNULL, stderr=STDOUT, shell=True)
    return csv_file_path
```

### Warning
Some functions in the BaseTransform class had to be heavily modified to not rely upon hard-coded header values, but they have not been thoroughly tested yet. The original code was developed over several years and had to accomodate a wide variety of wild input formats, so more major refactoring of BaseTransform is to be expected.
