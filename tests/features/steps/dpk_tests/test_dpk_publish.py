import json
import os
import random
import dtlpy as dl

import behave


@behave.when(u'I publish a dpk to the platform')
def step_impl(context):
    context.dpk.name = context.dpk.name + str(random.randint(10000, 1000000))
    context.published_dpk = context.project.dpks.publish(context.dpk)
    if hasattr(context.feature, 'dpks'):
        context.feature.dpks.append(context.published_dpk)
    else:
        context.feature.dpks = [context.published_dpk]


@behave.when(u'I add context to the dpk')
def step_impl(context):
    dpk_context = {
        "project": context.project.id
    }
    context.dpk.context = dpk_context
    context.dpk.scope = "organization"


@behave.when(u'I add pipeline template "{template_path}" to the dpk')
def step_impl(context, template_path):
    pipeline_template_path = template_path
    path = os.path.join(os.environ['DATALOOP_TEST_ASSETS'], pipeline_template_path)
    with open(path, 'r') as file:
        json_object = json.load(file)
    context.dpk.components[json_object["name"]] = {
        "type": "pipelineTemplate",
        "spec": json_object
    }


@behave.then(u'The pipeline template "{template}" should be created')
def step_impl(context, template):
    pipeline_template_name = context.dpk.components[template]["spec"]["name"]
    success, response = context.project._client_api.gen_request(req_type='POST', path='/pipelines/templates/query',
                                                                json_req={
                                                                    "org": {
                                                                        "filter": { "$and": [{"name": pipeline_template_name }]}
                                                                    }
                                                                })
    template = response.json()["org"]["items"][0]
    assert template["name"] == pipeline_template_name


@behave.when(u"I add the context.dataset to the dpk model")
def step_impl(context):
    context.dpk.components.models[0]['datasetId'] = context.dataset.id


@behave.then(u'The user defined properties should have the same values')
def step_impl(context):
    dpk = context.dpk
    p_dpk = context.published_dpk
    assert dpk.display_name == p_dpk.display_name
    assert dpk.version if dpk.version else "1.0.0" == p_dpk.version
    assert dpk.categories == p_dpk.categories
    assert dpk.icon == p_dpk.icon
    assert dpk.tags == p_dpk.tags
    assert dpk.scope == p_dpk.scope
    assert dpk.description == p_dpk.description
    assert dpk.components.to_json() == p_dpk.components.to_json()


@behave.then(u'id, name, createdAt, codebase, url and creator should have values')
def step_impl(context):
    dpk = context.published_dpk
    assert dpk.id is not None
    assert dpk.name is not None
    assert dpk.created_at is not None
    assert dpk.codebase is not None
    assert dpk.url is not None


@behave.when(u'I set the model in the context')
def step_impl(context):
    composition = context.project.compositions.get(composition_id=context.app.composition_id)
    context.model = context.project.models.get(model_id=composition["models"][0]["modelId"])


@behave.when(u'I add models list to context.models and expect to get "{total_models}" models')
def step_impl(context, total_models):
    context.models = context.project.models.list().items
    assert len(context.models) == int(total_models)
