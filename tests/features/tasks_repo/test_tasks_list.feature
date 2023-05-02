Feature: Tasks repository list method testing

    Background: Initiate Platform Interface and create a project
        Given Platform Interface is initialized as dlp and Environment is set according to git branch
        And I create a project by the name of "tasks_list"
        And I create a dataset with a random name
        And There are items, path = "filters/image.jpg"
            |annotated_type={"box": 3, "polygon": 3}|metadata={"user.good": 3, "user.bad": 3}|
        When Add Members "annotator1@dataloop.ai" as "annotator"
        And Add Members "annotator2@dataloop.ai" as "annotator"


    @second_project.delete
    @DAT-47055
    Scenario: list
        Given There is a second project and dataset
        When Add Members "annotator1@dataloop.ai" as "annotator" to second_project
        And Add Members "annotator2@dataloop.ai" as "annotator" to second_project
        Given There are items for another dataset, path = "filters/image.jpg"
            |annotated_type={"box": 3, "polygon": 3}|metadata={"user.good": 3, "user.bad": 3}|
        When I create Task
            | task_name=list_tasks | due_date=auto | project_id=auto | recipe_id=auto | assignee_ids=auto |
        And I create Task in second project
            | task_name=list_tasks | due_date=auto | project_id=second |  recipe_id=second | assignee_ids=auto |
        And I create Task
            | task_name=list_tasks | due_date=auto | recipe_id=auto | project_id=auto | assignee_ids=auto |
        And I create Task
            | task_name=list_tasks_different_name | due_date=next_week | project_id=auto | recipe_id=auto | assignee_ids=auto |

        When I list Tasks by param "project_ids" value "current_project"
        Then I receive a list of "3" tasks

        When I list Tasks by param "project_ids" value "second_project"
        Then I receive a list of "1" tasks

        When I list Tasks by param "project_ids" value "both"
        Then I receive a list of "4" tasks

        When I list Tasks by param "task_name" value "list_tasks"
        Then I receive a list of "2" tasks

        When I list Tasks by param "task_name" value "list_tasks_different_name"
        Then I receive a list of "1" tasks

        When I list Tasks by param "task_name" value "random_name"
        Then I receive a list of "0" tasks

        When I list Tasks by param "recipe" value "current_project"
        Then I receive a list of "3" tasks

        When I list Tasks by param "recipe" value "second_project"
        Then I receive a list of "1" tasks

        When I list Tasks by param "creator" value "self"
        Then I receive a list of "4" tasks

        When I list Tasks by param "min_date" value "2_days_from_now"
        Then I receive a list of "1" tasks

        When I list Tasks by param "min_date" value "2_weeks_from_now"
        Then I receive a list of "0" tasks

        When I list Tasks by param "max_date" value "2_days_from_now"
        Then I receive a list of "3" tasks

        When I list Tasks by param "max_date" value "2_weeks_from_now"
        Then I receive a list of "4" tasks

        When I list Tasks by param "max_date" value "today"
        Then I receive a list of "0" tasks
