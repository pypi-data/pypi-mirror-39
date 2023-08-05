from click.testing import CliRunner
from lazy import cli


def test_lazy():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
