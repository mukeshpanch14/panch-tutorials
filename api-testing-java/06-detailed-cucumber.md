# Module 6: Detailed Guide - Cucumber BDD

Cucumber allows you to drive your RestAssured tests with plain English scenarios.

## 1. Scenario Outlines (Data Driven)
Run the same scenario multiple times with a table of data.

```gherkin
Scenario Outline: Check status codes for different endpoints
  Given I connect to the API
  When I verify the "<endpoint>"
  Then the status code should be <code>

  Examples:
    | endpoint | code |
    | /users   | 200  |
    | /unknown | 404  |
```

## 2. Data Tables (Complex Input)
Pass a list or map of data to a single step.

```gherkin
# Feature File
Given I create a user with details:
  | name | job    |
  | John | QA     |
  | Alice| Dev    |
```

```java
// Step Def
@Given("I create a user with details:")
public void createUser(DataTable table) {
    List<Map<String, String>> rows = table.asMaps();
    for (Map<String, String> row : rows) {
        System.out.println("Creating " + row.get("name"));
    }
}
```

## 3. Hooks (Lifecycle)
Like `@BeforeEach` in JUnit, but for Gherkin.

```java
@Before
public void setupScenario() {
    System.out.println("Starting new scenario...");
}

@After("@smoke") // Only runs for scenarios tagged with @smoke
public void tearDownSmoke() {
    System.out.println("Cleaning up smoke test...");
}
```

## 4. Runner Configuration
Customize how your tests run.

```java
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "pretty, html:target/cucumber-report.html")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.example.steps")
```
