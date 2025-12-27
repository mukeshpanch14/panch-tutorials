# Sample API Test Suite

This project contains automated tests for the local API running at `http://localhost:8000`.

## Prequisites
1.  Ensure the API server is running on port 8000.
2.  Java 11+ and Maven installed.

## Running Tests
Run the entire suite from this directory:

```bash
mvn test
```

## Structure
-   `src/test/java/com/example/api`: Contains all test files.
-   `BaseTest.java`: Sets up the base URI.
-   `HealthCheckTest.java`: Verifies API availability.
-   `ItemsTest.java`: Verifies CRUD operations on Items.
