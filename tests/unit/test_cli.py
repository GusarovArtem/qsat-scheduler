
from typer.testing import CliRunner

from qsat.cli import app

runner = CliRunner()

def test_help_exists_cleanly():
    # --help must always work offline and return exit code 0
    result = runner.invoke(app, ['--help'])
    assert result.exit_code == 0
    assert "passes" in result.output.lower() or "observer" in result.output.lower()