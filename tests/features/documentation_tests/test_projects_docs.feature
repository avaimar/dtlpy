Feature: Projects repository create service testing

    Background: Background name
        Given Platform Interface is initialized as dlp and Environment is set according to git branch

    @testrail-C4523098
    @DAT-46509
    Scenario: Projects Commands
        When Create a Project "my-new-project"
        Then Get my projects
        And Get a project by name "my-new-project"
        And Get a project by project ID
        And Print a Project
        And Delete project by context.project




