# Module 4: Detailed Guide - JUnit 5

JUnit 5 (Jupiter) is the runner for your API tests. You must master its annotations and logic flow.

## 1. Lifecycle Annotations
Controlling **when** code runs is crucial for setting up data or cleaning up.

| Annotation | Description |
| :--- | :--- |
| `@Test` | Marks a method as a test case. |
| `@BeforeAll` | Runs **once** before all tests in the class (must be static). Good for global setup (e.g., establishing DB connection). |
| `@BeforeEach` | Runs before **every** single test method. Good for resetting variables. |
| `@AfterEach` | Runs after **every** test. Good for cleanup. |
| `@AfterAll` | Runs **once** after all tests are done (must be static). |

## 2. Assertions
Validating results. If an assertion fails, the test fails.

```java
import static org.junit.jupiter.api.Assertions.*;

assertEquals(200, responseCode);
assertNotNull(responseBody);
assertTrue(responseBody.contains("success"));
assertAll("User Details",
    () -> assertEquals("John", user.getName()),
    () -> assertEquals("admin", user.getRole())
);
```

## 3. Parameterized Tests (Data Driven)
Run the same test with different inputs.

```java
@ParameterizedTest
@ValueSource(strings = { "/users", "/products", "/orders" })
void testEndpointsAreUp(String endpoint) {
    int code = getStatusCode(endpoint);
    assertEquals(200, code);
}
```

## 4. The "Pure Java" Client (Java 11+)
Sometimes you don't need RestAssured. Java has a built-in `HttpClient`.

```java
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://reqres.in/api/users/2"))
        .GET()
        .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
assertEquals(200, response.statusCode());
```
