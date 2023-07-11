import json
import time

import behave
import dtlpy as dl
import os


@behave.when(u'I create a dummy model package by the name of "{package_name}"')
def step_impl(context, package_name):
    metadata = dl.Package.get_ml_metadata(
        default_configuration={'weights_filename': 'model.pth',
                               'input_size': 256},
        output_type=dl.AnnotationType.BOX,
    )
    model_repo = os.path.join(os.environ["DATALOOP_TEST_ASSETS"], 'models_flow')
    module = dl.PackageModule.from_entry_point(
        entry_point=os.path.join(model_repo, 'main.py'))
    module.entry_point = 'main.py'
    context.package = context.project.packages.push(package_name=package_name,
                                                    src_path=model_repo,
                                                    package_type='ml',
                                                    modules=[module],
                                                    requirements=[
                                                        dl.PackageRequirement(
                                                            name='https://storage.googleapis.com/dtlpy/dtlpy-metrics/dtlpymetrics-latest-py3-none-any.whl'),
                                                        dl.PackageRequirement(name='matplotlib')],
                                                    service_config={
                                                        'runtime': dl.KubernetesRuntime(
                                                            runner_image='jjanzic/docker-python3-opencv',
                                                            pod_type=dl.InstanceCatalog.REGULAR_XS,
                                                            autoscaler=dl.KubernetesRabbitmqAutoscaler(
                                                                min_replicas=0,
                                                                max_replicas=1),
                                                            concurrency=1).to_json()},
                                                    metadata=metadata)


@behave.when(u'I create a model form package by the name of "{model_name}"')
def step_impl(context, model_name):
    context.model = context.package.models.create(model_name=model_name,
                                                  description='model for testing',
                                                  dataset_id=context.dataset.id,
                                                  scope='project',
                                                  model_artifacts=[dl.LinkArtifact(
                                                      url='https://storage.googleapis.com/model-mgmt-snapshots/ResNet50/model.pth',
                                                      filename='model.pth')],
                                                  status='created',
                                                  configuration={'weights_filename': 'model.pth',
                                                                 'batch_size': 16,
                                                                 'num_epochs': 10},
                                                  project_id=context.project.id,
                                                  labels=[label.tag for label in context.dataset.labels],
                                                  train_filter=dl.Filters(),
                                                  output_type=dl.AnnotationType.BOX
                                                  )


@behave.when(u'I "{func}" the model')
def step_impl(context, func):
    context.model = dl.models.get(model_id=context.model.id)
    if func == 'evaluate':
        context.execution = context.model.evaluate(dataset_id=context.dataset.id, filters=dl.Filters())
    else:
        context.execution = context.model.__getattribute__(func)()


@behave.then(u'model status should be "{status}"')
def step_impl(context, status):
    num_try = 45
    interval = 20
    completed = False

    if isinstance(context.execution, dl.Execution):
        for i in range(num_try):
            time.sleep(interval)
            context.execution = dl.executions.get(execution_id=context.execution.id)
            if context.execution.latest_status['status'] in ['success', 'failed']:
                completed = True
                break
    else:
        time.sleep(10)
        completed = True

    assert completed, "TEST FAILED: execution was not completed"
    context.model = dl.models.get(model_id=context.model.id)
    assert context.model.status == status, f"TEST FAILED: model status is not as expected, expected: {status}, got: {context.model.status}"


@behave.then(u'Dataset has a scores file')
def step_impl(context):
    model_filename = f'{context.model.id}.csv'
    filters = dl.Filters(field='hidden', values=True)
    filters.add(field='name', values=model_filename)
    items = context.dataset.items.list(filters=filters)
    assert items.items_count != 0, f'Found {items.items_count} items with name {model_filename}.'


@behave.when(u'i call the precision recall api')
def step_impl(context):
    payload = {
        'datasetId': context.dataset.id,
        'confThreshold': 0,
        'iouThreshold': 0,
        'metric': 'accuracy',
        'modelId': context.model.id,
    }
    success, response = dl.client_api.gen_request(req_type="post",
                                                  path=f"/ml/metrics/precisionRecall",
                                                  json_req=payload)
    assert success, f'Failed to call precision recall api, response: {response}'
    context.response = response.json()


@behave.then(u'i should get a json response')
def step_impl(context):
    assert isinstance(context.response, dict), f'Failed to call precision recall api, response: {context.response}'
    with open(os.path.join(os.environ["DATALOOP_TEST_ASSETS"], 'models_flow', 'precisionrecall.json'), 'r') as f:
        expected_output = json.load(f)
    assert context.response == expected_output, f'results are not as expected, expected: {expected_output}, got: {context.response}'


@behave.given(u'I upload "{item_num}" box annotation to item')
@behave.when(u'I upload "{item_num}" box annotation to item')
def step_impl(context, item_num):
    builder = context.item.annotations.builder()
    item_num = int(item_num)
    for i in range(item_num):
        builder.add(annotation_definition=dl.Box(top=i * 10, left=i * 10, bottom=i * 20, right=i * 20, label=str(i)))
    context.item.annotations.upload(builder)
