from click.testing import CliRunner

from yo import cli


def test_yo_default_command():
    runner = CliRunner()
    result = runner.invoke(cli)
    print(result)
