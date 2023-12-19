Feature: DPK with operation field

  Background:
    Given Platform Interface is initialized as dlp and Environment is set according to git branch
    And I create a project by the name of "dpk_model_operation"
    And I create a dataset by the name of "model" in the project

  @DAT-53253
  Scenario: Install dpk with 2 models one with operationType "deploy" - Should install only 1 service
    Given I fetch the dpk from 'apps/app_include_operation.json' file
    When I add the context.dataset to the dpk model
    And I publish a dpk to the platform
    And  I install the app
    And I list services in project
    Then I receive a Service list of "1" objects
    And I uninstall the app

  @DAT-57107
  Scenario: Install dpk with operation 'deploy' without compute - Should install only 1 service
    Given I fetch the dpk from 'apps/app_model_operation_type_without_compute.json' file
    When I add the context.dataset to the dpk model
    And I publish a dpk to the platform
    And  I install the app
    And I list services in project
    Then I receive a Service list of "1" objects
    And I uninstall the app