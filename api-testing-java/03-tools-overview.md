# Module 3: Tools Overview

A quick comparison of the three primary tools you'll use in Java API testing.

## 1. JUnit 5
**What is it?**: The foundation. It's a testing framework that runs the tests, handles assertions (Pass/Fail), and manages lifecycle (Setup/Teardown).
**When to use**: Always. It's the engine that powers your test suite.
**Hello World**:
```java
@Test
void hello() {
    System.out.println("Hello JUnit");
    Assertions.assertTrue(true);
}
```

## 2. RestAssured
**What is it?**: A library specifically designed to simplify HTTP requests in Java. It replaces verbose code with a fluent BDD-style syntax (Given-When-Then).
**When to use**: For standard API testing where you want clean, readable code without writing helper classes from scratch.
**Hello World**:
```java
given().when().get("/google").then().statusCode(200);
```

## 3. Cucumber
**What is it?**: A BDD (Behavior Driven Development) tool that lets you write tests in English (Gherkin). It needs "glue code" to actually run.
**When to use**: When non-technical stakeholders (PO, PM) need to read and understand the tests.
**Hello World (Gherkin)**:
```gherkin
Scenario: Hello Cucumber
  Given I have a greeter
  When I say hello
  Then I should hear "World"
```
