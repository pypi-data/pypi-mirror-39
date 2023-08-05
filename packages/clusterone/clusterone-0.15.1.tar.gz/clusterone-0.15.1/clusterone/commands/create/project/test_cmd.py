from click.testing import CliRunner
from clusterone import ClusteroneClient

from clusterone.commands.create.project import cmd
from clusterone.clusterone_cli import cli

def test_all_parameters(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['create', 'project', 'someProjectName', '--description', 'This is a sample project description'])

    cmd.main.assert_called_with(mocker.ANY, 'someProjectName', 'github', False, 'This is a sample project description')

def test_name_only(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock()

    CliRunner().invoke(cli, ['create', 'project', 'test'])

    cmd.main.assert_called_with(mocker.ANY, 'test', 'github', False, '')

def test_message(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock()

    result = CliRunner().invoke(cli, ['create', 'project', 'whatever-really'])

    assert 'Project creating, this might take up to a minute' in result.output

def test_outputs_fullname(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    cmd.main = mocker.Mock(return_value={'full_name': "sample.project.fullname", 'name': "sample.project.name"})

    result = CliRunner().invoke(cli, ['create', 'project', 'whatever-really'])

    assert "sample.project.fullname" in result.output

