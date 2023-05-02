Feature: Assignments repository list method testing

    Background: Initiate Platform Interface and create a project
        Given Platform Interface is initialized as dlp and Environment is set according to git branch
        And I create a project by the name of "assignments_list"
        And I create a dataset with a random name
        And There are items, path = "filters/image.jpg"
            |annotated_type={"box": 3, "polygon": 3}|metadata={"user.good": 3, "user.bad": 3}|
        And I save dataset items to context
        When Add Members "annotator0@dataloop.ai" as "annotator"
        And Add Members "annotator1@dataloop.ai" as "annotator"
        And Add Members "annotator2@dataloop.ai" as "annotator"
        And I create Task
            | task_name=assignments_list | due_date=auto | assignee_ids=annotator0@dataloop.ai | items=2 |

    @testrail-C4523058
    Scenario: List
        When I list assignments
        Then I receive a list of "1" assignments
        When I create an Assignment from "task" entity
            | assignee_id=annotator1@dataloop.ai | items=2 |
        And I list assignments
        Then I receive a list of "2" assignments
        When I create an Assignment from "task" entity
            | assignee_id=annotator2@dataloop.ai | items=2 |
        And I list assignments
        Then I receive a list of "3" assignments
