Feature: Pipeline update testing

  Background: Initiate Platform Interface and create a pipeline
    Given Platform Interface is initialized as dlp and Environment is set according to git branch
    And I create a project by the name of "test_pipeline_flow"
    And I create a dataset with a random name
    When I create a new plain recipe
    And I update dataset recipe to the new recipe

  @pipelines.delete
  @testrail-C4523145
  @DAT-46582
  Scenario: Update pipeline
    Given I create pipeline with the name "pipeline"
    And I create "dataset" node with params
      | key      | value |
      | position | (1,1) |
    And I create "dataset" node with params
      | key      | value |
      | position | (2,2) |
    When I add and connect all nodes in list to pipeline entity
    And I install pipeline in context
    And I update pipeline description
    Then Pipeline received equals Pipeline changed except for "description"

