"""Automatic convertion test, by taking each concept and verifying
that go-and-return convertion ends up with the same data.

"""

import os
import glob
import itertools
from rofetta import convert, input_formats, output_formats


TEST_FILE = 'test/todel.{ext}'


def compare_unordered_convertion(lines) -> str:
    "Just sort characters. Useful for convertions methods that are totally unordered"
    return ''.join(sorted(tuple(itertools.chain.from_iterable(lines))))


def template_test_convertion(filename, ext, target_ext):
    "Return the function testing conversion of given filename to target format"
    # line_builder: define how the lines are compared between initial and final file
    line_builder = compare_unordered_convertion if target_ext == 'lp' else tuple
    line_builder = set if ext == 'lp' else line_builder
    with open(filename) as fd:
        initial_data = line_builder(fd.readlines())
    def test_convertion():
        assert ext in input_formats
        intermediary = TEST_FILE.format(ext=target_ext)
        final = TEST_FILE.format(ext=ext)
        print(f'{filename} -> {intermediary}')
        convert(filename, intermediary)
        print(f'{intermediary} -> {final}')
        convert(intermediary, final)
        with open(final) as fd:
            final_data = line_builder(fd.readlines())
        assert initial_data == final_data
    return test_convertion


for fname in itertools.chain.from_iterable(glob.glob(f'contexts/*.{ext}') for ext in input_formats):
    name = os.path.splitext(os.path.basename(fname))[0]
    ext = os.path.splitext(fname)[1].strip('.')
    if ext not in output_formats:  continue  # can't convert back to the file, so no auto verification is possible
    for target_ext in output_formats - {ext}:
        globals()[f'test_conversion_{name}_to_{target_ext}'] = template_test_convertion(fname, ext, target_ext)
