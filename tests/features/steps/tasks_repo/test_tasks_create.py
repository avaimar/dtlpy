import behave
import json
from .. import fixtures


@behave.when(u'I create Task')
def step_impl(context):
    context.params = {param.split('=')[0]: fixtures.get_value(params=param.split('='), context=context) for param in
                      context.table.headings if
                      fixtures.get_value(params=param.split('='), context=context) is not None}
    context.task = context.dataset.tasks.create(**context.params)


@behave.when(u'I create Task in second project')
def step_impl(context):
    context.params = {param.split('=')[0]: fixtures.get_value(params=param.split('='), context=context) for param in
                      context.table.headings if
                      fixtures.get_value(params=param.split('='), context=context) is not None}
    context.task = context.second_dataset.tasks.create(**context.params)


@behave.then(u'I receive a task entity')
def step_impl(context):
    assert isinstance(context.task, context.dl.entities.Task)


def compare_items_list(items_a, items_b):
    equals = len(items_b) == len(items_a)
    for item in items_a:
        equals = equals and item in items_b
    return equals


@behave.then(u'Task has the correct attributes for type "{task_type}"')
def step_impl(context, task_type):
    if task_type == "annotation":
        context.task = context.task.tasks.get(task_id=context.task.id)
    elif task_type == "qa":
        context.task = context.task.tasks.get(task_id=context.qa_task.id)
    for key, val in context.params.items():
        if key == 'filters':
            task_query = json.loads(context.task.query)
            task_query.pop('sort')
            assert task_query == val.prepare()
        elif key == 'items':
            task_items = [item.id for item in context.task.get_items().items]
            assert compare_items_list(items_a=task_items, items_b=[item.id for item in val])
        elif key == 'assignee_ids':
            task_assignments = [assignment.annotator for assignment in context.task.assignments.list()]
            assert compare_items_list(items_a=task_assignments, items_b=val)
        elif key == 'workload':
            task_assignments = [assignment.annotator for assignment in context.task.assignments.list()]
            assert compare_items_list(items_a=task_assignments, items_b=[w_l.assignee_id for w_l in val])
        elif key == 'due_date':
            assert context.task.due_date == val * 1000
        elif key == 'task_name':
            assert val in context.task.name
        elif key == 'dataset':
            assert context.task.dataset_id == val.id
        elif key == 'project_id':
            assert context.task.project_id == val
        elif key == 'recipe_id':
            assert context.task.recipe_id == val
        elif key == 'metadata':
            assert context.task.metadata[list(val.keys())[0]] == val[list(val.keys())[0]]
        elif key == 'batch_size':
            task_assignments = [assignment.total_items for assignment in context.task.assignments.list()]
            assert all([int(val) == total for total in task_assignments])
        elif key == 'allowed_assignees':
            task_assignments = [assignment.annotator for assignment in context.task.assignments.list()]
            assert compare_items_list(items_a=task_assignments, items_b=val)
