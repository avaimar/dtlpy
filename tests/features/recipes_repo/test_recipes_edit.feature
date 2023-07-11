Feature: Recipes repository Update service testing

    Background: Initiate Platform Interface and create a project
        Given Platform Interface is initialized as dlp and Environment is set according to git branch
        And I create a project by the name of "recipes_edit"
        And I create a dataset with a random name

    @testrail-C4523154
    @DAT-46602
    Scenario: Update recipe
        When I update recipe
        Then Recipe in host equals recipe edited


