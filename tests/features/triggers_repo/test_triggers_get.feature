@bot.create
Feature: Triggers repository get service testing

    Background: Initiate Platform Interface and create a project
        Given Platform Interface is initialized as dlp and Environment is set according to git branch
        And I create a project by the name of "triggers_get"
        And I create a dataset with a random name
        And There is a package (pushed from "triggers/item") by the name of "triggers-get"
        And There is a service by the name of "triggers-get" with module name "default_module" saved to context "service"
        And I create a trigger
            |name=triggers-create|filters=None|resource=Item|action=Created|active=True|executionMode=Once|

    @services.delete
    @packages.delete
    @testrail-C4523179
    @DAT-46645
    Scenario: Get by id
        When I get trigger by id
        Then I receive a Trigger object
        And Trigger received equals to trigger created

    @services.delete
    @packages.delete
    @testrail-C4523179
    @DAT-46645
    Scenario: Get by name
        When I get trigger by name
        Then I receive a Trigger object
        And Trigger received equals to trigger created


