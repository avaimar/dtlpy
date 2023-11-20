Feature: Datasets repository list service testing

    Background: Initiate Platform Interface and create a project
        Given Platform Interface is initialized as dlp and Environment is set according to git branch
        And I create a project by the name of "datasets_list"

    @testrail-C4523089
    @DAT-46497
    Scenario: List all datasets when no dataset exists
        Given There are no datasets
        When I list all datasets
        Then I receive an empty datasets list

    @testrail-C4523089
    @DAT-46497
    Scenario: List all datasets when datasets exist
        Given There are no datasets
        And I create a dataset by the name of "Dataset" and count
        When I list all datasets
        Then I receive a datasets list of "1" dataset
        And The dataset in the list equals the dataset I created


