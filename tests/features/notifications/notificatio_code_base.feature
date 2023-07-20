#@qa-nightly
#@bot.create
#Feature: Executions repository create service testing
#
#  Background: Initiate Platform Interface and create a project
#    Given Platform Interface is initialized as dlp and Environment is set according to git branch
#    And I create a project by the name of "execution_create"
#    And I create a dataset with a random name
#
#  @services.delete
#  @packages.delete
#  @DAT-46787
#  Scenario: Code base error should raise notification
#    Given There is a package (pushed from "faas/initError") by the name of "codebase-error"
#    And There is a service by the name of "codebase-error" with module name "default_module" saved to context "service"
#    And I delete service code base
#    And I upload item in "0000000162.jpg" to dataset
#    When I create an execution with "inputs"
#      | sync=False | inputs=Item |
#    Then I receive "CodebaseError" notification
#    And Service is deactivated by system