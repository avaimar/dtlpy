Feature: Models repository clone testing

  Background: Initiate Platform Interface and create a project
    Given Platform Interface is initialized as dlp and Environment is set according to git branch
    And I create a project by the name of "model_mgmt"
    And I create a dataset with a random name
    And I upload an item by the name of "test_item.jpg"
    When I upload labels to dataset
    And I upload "5" box annotation to item

  @DAT-55187
  Scenario: test clone model
    When I create a dummy model package by the name of "dummymodel" with entry point "main.py"
    And I create a model from package by the name of "test-model" with status "trained"
    When i "deploy" the model
    Then model status should be "deployed" with execution "False" that has function "None"
    When i "evaluate" the model
    Then model status should be "deployed" with execution "True" that has function "evaluate_model"
    When i "evaluate" the model
    Then model status should be "deployed" with execution "True" that has function "evaluate_model"
    Then model metadata should include operation "evaluate" with filed "datasets" and length "1"
    When i clone a model
    Then model input should be equal "image", and output should be equal "box"
    Then model do not have operation "evaluate"

