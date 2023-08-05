from click.testing import CliRunner

from clusterone import ClusteroneClient
from clusterone.persistance.session import Session
from clusterone.client_exceptions import RemoteAquisitionFailure
from clusterone.clusterone_cli import cli
from clusterone.commands.create.dataset import cmd

DATASET_RESPONSE_LITERAL = {
    "display_name": "someDatasetName",
    "name": "somedatasetname",
    "full_name": "somedatasetfullname",
    "source": "gitlab",
    "description": "This is a sample project description",
}

def test_passing(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Session, 'save', autospec=True, return_value=None)

    ClusteroneClient.create_dataset = mocker.Mock(return_value=DATASET_RESPONSE_LITERAL)
    cmd.time = mocker.Mock()

    CliRunner().invoke(cli, ['create', 'dataset', 'someDatasetName', 's3', '--description', 'This is a sample project description'])

    ClusteroneClient.create_dataset.assert_called_with('someDatasetName', description='This is a sample project description', public=False, source='s3')


def test_default(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Session, 'save', autospec=True, return_value=None)

    cmd.time = mocker.Mock()

    CliRunner().invoke(cli, ['create', 'dataset', 'someDatasetName'])

    ClusteroneClient.create_dataset.assert_called_with('someDatasetName', description='', public=False, source='github')


def test_message(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Session, 'save', autospec=True, return_value=None)
    ClusteroneClient.get_dataset = mocker.Mock(
        return_value={'git_auth_link': 'https://user:58459eb14@git.clusterone.com/user/somedatasetname.git'})
    ClusteroneClient.create_dataset = mocker.Mock(return_value="someDatasetName")
    cmd.time = mocker.Mock()

    result = CliRunner().invoke(cli, ['create', 'dataset', 'whatever-really'])

    assert 'Dataset creating, this might take up to a minute' in result.output


def test_outputs_remote_url(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    mocker.patch.object(Session, 'save', autospec=True, return_value=None)
    mocker.patch.object(Session, '__init__', autospec=True, return_value=None)
    Session.config = mocker.Mock()
    Session.retry_count, Session.retry_interval = 1, 1
    Session.config.read = mocker.Mock(return_value='{"username": "a", "token": "b"}')

    ClusteroneClient.create_dataset = mocker.Mock(return_value=DATASET_RESPONSE_LITERAL)
    cmd.time = mocker.Mock()

    result = CliRunner().invoke(cli, ['create', 'dataset', 'whatever-really'])

    assert 'somedatasetfullname' in result.output
