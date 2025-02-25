import json
import os
import random

import behave
from .. import fixtures


@behave.when(u"I fetch the dpk from '{file_name}' file")
@behave.given(u"I fetch the dpk from '{file_name}' file")
def step_impl(context, file_name):
    path = os.path.join(os.environ['DATALOOP_TEST_ASSETS'], file_name)
    with open(path, 'r') as file:
        json_object = json.load(file)

    json_object = fixtures.update_dtlpy_version(json_object)
    if "context" in json_object.keys():
        if json_object['context'].get("project", None) is not None:
            json_object['context']['project'] = context.project.id
        if json_object['context'].get("organization", None) is not None:
            json_object['context']['organization'] = context.project.org['id']

    context.dpk = context.dl.entities.Dpk.from_json(_json=json_object,
                                                    client_api=context.dl.client_api,
                                                    project=context.project
                                                    )
    context.json_object = json_object


@behave.when(u"I add codebase to dpk")
@behave.given(u"I add codebase to dpk")
def step_impl(context):
    context.dpk.codebase = context.codebase


@behave.then(u"I have a dpk entity")
def step_impl(context):
    assert hasattr(context, 'dpk')


@behave.then(u"I have json object to compare")
def step_impl(context):
    assert hasattr(context, 'json_object')


@behave.then(u"The dpk is filled with the same values")
def step_impl(context):
    if 'name' in context.json_object:
        assert context.dpk.name == context.json_object['name']
    if 'id' in context.json_object:
        assert context.dpk.id == context.json_object['id']
    if 'scope' in context.json_object:
        assert context.dpk.scope == context.json_object['scope']
    if 'version' in context.json_object:
        assert context.dpk.version == context.json_object['version']
    if 'creator' in context.json_object:
        assert context.dpk.creator == context.json_object['creator']
    if 'displayName' in context.json_object:
        assert context.dpk.display_name == context.json_object['displayName']
    if 'description' in context.json_object:
        assert context.dpk.description == context.json_object['description']
    if 'icon' in context.json_object:
        assert context.dpk.icon == context.json_object['icon']
    if 'categories' in context.json_object:
        assert context.dpk.categories == context.json_object['categories']
    if 'components' in context.json_object:
        assert context.dpk.components.panels == \
               context.json_object['components']['panels']
    if 'createdAt' in context.json_object:
        assert context.dpk.created_at == context.json_object['createdAt']
    if 'updatedAt' in context.json_object:
        assert context.dpk.updated_at == context.json_object['updatedAt']
    if 'codebase' in context.json_object:
        assert context.dpk.codebase == context.json_object['codebase']
    if 'url' in context.json_object:
        assert context.dpk.url == context.json_object['url']
    if 'tags' in context.json_object:
        assert context.dpk.tags == context.json_object['tags']


@behave.given(u"I publish a dpk to the platform")
def step_impl(context):
    context.dpk.name = context.dpk.name + str(random.randint(10000, 1000000))
    context.dpk = context.dl.entities.Dpk.publish(context.dpk)
    if hasattr(context.feature, 'dpks'):
        context.feature.dpks.append(context.dpk)
    else:
        context.feature.dpks = [context.dpk]


@behave.when(u"I update dpk dtlpy to current version for service in index {i}")
def step_impl(context, i):
    context.dpk.components.services[int(i)]['versions'] = {'dtlpy': context.dl.__version__, "verify": True}
