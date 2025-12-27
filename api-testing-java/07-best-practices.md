# Module 7: API Testing Best Practices

Writing a test that passes is easy. Writing a test suite that is maintainable, fast, and stable is an art.

## 1. Separation of Concerns (Test Layer vs Object Layer)
Do NOT mix test logic with API calls.
*   **Bad**: Writing the `given().baseUri...` inside every `@Test` method.
*   **Good**: Create an `ApiClient` class that handles the `RestAssured` calls and returns a `Response`. The `@Test` should only call `apiClient.createUser()` and assert the result.

## 2. Use POJOs (Plain Old Java Objects)
Never use String concatenation for JSON bodies. It's error-prone.
*   **Bad**: `String body = "{ \"name\": \"" + name + "\" }";`
*   **Good**: Pass a `User` object. RestAssured (via Jackson) handles the conversion.

## 3. Test Data Management
*   **Create Your Own Data**: Relying on existing data (e.g., User ID 1) makes tests flaky if that data changes.
*   **Pattern**: Create -> Test -> Delete.
*   **Dynamic**: Use libraries like **JavaFaker** to generate random names/emails so tests don't collide.

## 4. Logging & Reporting
*   **Logging**: Use `.log().ifValidationFails()` in RestAssured to see the request/response only when things break.
*   **Reporting**: Integrate Allure or ExtentReports. A command-line output is not enough for a manager.

## 5. Arrange-Act-Assert (AAA)
Keep tests visually structured.
```java
// Arrange
User user = new User("John", "QA");

// Act
Response response = userApi.create(user);

// Assert
assertEquals(201, response.getStatusCode());
```
