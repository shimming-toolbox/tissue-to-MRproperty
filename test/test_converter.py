import sys
import os
# With the next line we add to path the project folder to navigate into functions folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from click.testing import CliRunner
from cli.tissue_to_mr import hello
from functions.utils.utils import is_nifti


def test_converter():
    runner = CliRunner()
    result = runner.invoke(hello, ['-i', 'input.nii', '--type', 'MR', '-o', 'output.nii'])
    assert result.exit_code == 0
    assert 'Input: input.nii Type: MR' in result.output


def test_is_nifti():
    good_filepath = 'example.nii'
    wrong_filepath = 'example.txt'

    assert is_nifti(good_filepath), "is_nifti failed for a correct filepath"
    assert is_nifti(wrong_filepath) is False, "is_nifti failed for a wrong filepath"
