import time

from clusterone.client_exceptions import RemoteAquisitionFailure


def aquire_remote(project_name, session, client):

    username = session.get('username')
    retry_count, retry_interval = session.retry_count, session.retry_interval

    for _ in range(retry_count):
        time.sleep(retry_interval)

        project = client.get_project(project_name, username)
        git_url = project.get('git_auth_link')

        # API response might be evaluated as None or ""
        if not (git_url is None or git_url == ""):
            return git_url

    raise RemoteAquisitionFailure()


def main(context, full_name, source, public, description):

    client, session = context.client, context.session

    project = client.create_project(full_name, source, public, description)

    return project
