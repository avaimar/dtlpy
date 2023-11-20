import behave
import os


@behave.given(u'Feature: There is a package and service')
def step_impl(context):
    src_path = os.path.join(os.environ['DATALOOP_TEST_ASSETS'], 'packages_checkout_create', 'package.json')
    services, context.package = context.project.packages.deploy_from_file(project=context.project,
                                                                          json_filepath=src_path)
    context.service = services[0]
    context.to_delete_packages_ids.append(context.package.id)
    context.feature.package = context.package
    context.to_delete_services_ids.append(context.service.id)
    context.feature.service = context.service


@behave.when(u'I checkout')
def step_impl(context):
    entity = context.table.headings[0]
    if entity == 'project':
        context.project.checkout()
    elif entity == 'dataset':
        context.dataset.checkout()
    elif entity == 'package':
        context.package.checkout()
    elif entity == 'service':
        context.service.checkout()
    else:
        assert False, 'Unknown entity param'


@behave.then(u'I am checked out')
def step_impl(context):
    entity = context.table.headings[0]
    if entity == 'project':
        assert context.dl.projects.get().id == context.project.id
    elif entity == 'dataset':
        assert context.project.datasets.get().id == context.dataset.id
    elif entity == 'package':
        assert context.project.packages.get().id == context.package.id
    elif entity == 'service':
        assert context.project.services.get().id == context.service.id
    else:
        assert False, 'Unknown entity param'


@behave.given(u'Feature: I pack to project directory in "{package_codebase}"')
def step_impl(context, package_codebase):
    package_codebase = os.path.join(os.environ['DATALOOP_TEST_ASSETS'], package_codebase)
    context.codebase = context.project.codebases.pack(
        directory=package_codebase,
        name='package-codebase',
        description="some description",
    )


@behave.given(u'Feature: There is a Codebase directory with a python file in path "{code_path}"')
def step_impl(context, code_path):
    code_path = os.path.join(os.environ['DATALOOP_TEST_ASSETS'], code_path)
    dirs = os.listdir(code_path)
    assert "some_code.py" in dirs
    context.feature.codebase_local_dir = code_path


@behave.given(u'Feature: I create a dataset by the name of "{dataset_name}"')
def step_impl(context, dataset_name):
    context.feature.dataset = context.project.datasets.create(dataset_name=dataset_name, index_driver=context.index_driver_var)


@behave.given(u'Get feature entities')
def step_impl(context):
    if hasattr(context.feature, 'done_setting') and context.feature.done_setting:
        for param in context.table.headings:
            if param == 'dataset':
                context.dataset = context.feature.dataset
            elif param == 'package':
                context.package = context.feature.package
            elif param == 'service':
                context.service = context.feature.service


@behave.given(u'Done setting')
def step_impl(context):
    context.feature.done_setting = True
