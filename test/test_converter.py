import sys
import os
# With the next line we add to path the project folder to navigate into functions folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from click.testing import CliRunner
from cli.tissue_to_mr import converter


def test_converter():
    runner = CliRunner()
    result = runner.invoke(converter, ['-i', 'input.nii', '--type', 'MR', '-o', 'output.nii'])
    assert result.exit_code == 0
    assert 'Input: input.nii Type: MR' in result.output