Feature: Pipeline entity method testing

  Background: Initiate Platform Interface and create a pipeline
    Given Platform Interface is initialized as dlp and Environment is set according to git branch
    And I create a project by the name of "test_pipeline_flow"
    And I create a dataset with a random name
    When I create a new plain recipe
    And I update dataset recipe to the new recipe


  @pipelines.delete
  @testrail-C4525314
  @DAT-46580
  Scenario: pipeline flow
    When I create a package and service to pipeline
    And I create a pipeline from sdk
    And I upload item in "0000000162.jpg" to pipe dataset
    Then verify pipeline flow result

  @pipelines.delete
  @testrail-C4525314
  @DAT-46580
  Scenario: pipeline flow pipeline trigger
    When I create a package and service to pipeline
    And I create a pipeline from sdk with pipeline trigger
    And I upload item in "0000000162.jpg" to pipe dataset
    Then verify pipeline flow result

  @pipelines.delete
  @testrail-C4525314
  @DAT-46580
  Scenario: pipeline delete use sdk
    When I create a package and service to pipeline
    And I create a pipeline from json
    And I update the pipeline nodes
    And check pipeline nodes

  @pipelines.delete
  @testrail-C4533330
  @DAT-46580
  Scenario: pipeline with dataset task with new recipe
    When I create a new plain recipe
    When I create a pipeline with task node and new recipe
    Then I install pipeline in context
