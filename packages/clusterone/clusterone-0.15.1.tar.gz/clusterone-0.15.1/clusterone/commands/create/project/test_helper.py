import pytest
from clusterone.client_exceptions import RemoteAquisitionFailure

from clusterone.persistance.session import Session
from clusterone import ClusteroneClient
from clusterone.clusterone_cli import Context

from . import helper
from .helper import main


def test_client_call(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    ClusteroneClient.create_project = mocker.Mock()

    helper.time.sleep = mocker.Mock()

    session = Session()
    session.load()
    client = ClusteroneClient(token=session.get('token'), username=session.get('username'))
    context = Context(client, session, None)

    ClusteroneClient.get_project.return_value = {'git_auth_link': "some text"}

    main(context, "ProjectName", "Github", "private", "Description...")

    ClusteroneClient.create_project.assert_called_with("ProjectName", "Github", "private", "Description...")


def test_returns_remote_link(mocker):
    mocker.patch.object(ClusteroneClient, '__init__', autospec=True, return_value=None)
    ClusteroneClient.get_project = mocker.Mock()
    ClusteroneClient.create_project = mocker.Mock()
    ClusteroneClient.create_project.return_value = {'full_name': "exceptional.project_full_name"}
    helper.time.sleep = mocker.Mock()

    session = Session()
    session.load()
    client = ClusteroneClient(token=session.get('token'), username=session.get('username'))
    context = Context(client, session, None)

    created_project = client.create_project("ProjectName", "Github", "private", "Description...")

    assert created_project == {'full_name': "exceptional.project_full_name"}
