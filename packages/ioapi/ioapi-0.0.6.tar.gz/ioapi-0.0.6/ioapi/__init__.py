"""GraphQL client for IOExplorer API.

"""
from functools import partial
import pkg_resources
import re
import os
import json
import snug
import quiz

_ = quiz.SELECTOR

URL = os.environ["IOEXPLORER_GRAPHQL_URL"]
_SCHEMA_PATH = pkg_resources.resource_filename('ioapi', 'schema.json')


def auth_factory(auth):
    if isinstance(auth, str):
        return snug.header_adder({'Authorization': 'bearer {auth}'})
    else:
        assert isinstance(auth, tuple)
        return auth


class SequelizeJSON(quiz.Scalar):
    """A JSON string"""
    def __init__(self, data):
        self.data = data

    def __gql_dump__(self):
        return re.sub(r'("([^\"]+?)")\s*:', r'\2:', json.dumps(self.data))

    @classmethod
    def __gql_load__(cls, data):
        return data


schema = quiz.Schema.from_path(_SCHEMA_PATH, module=__name__, scalars=[SequelizeJSON])
schema.populate_module()
query = schema.query

def execute(obj, auth=(), url=URL, **kwargs):
    return quiz.execute(obj, auth=auth_factory(auth), url=url, **kwargs)


def execute_async(obj, auth=(), url=URL, **kwargs):
    return quiz.execute_async(obj, auth=auth_factory(auth), url=url, **kwargs)


executor = partial(partial, execute)
async_executor = partial(partial, execute_async)
