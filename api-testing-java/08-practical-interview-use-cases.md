# Module 4: Practical Interview Use Cases

This section covers specific scenarios often asked about in interviews to see if you have "hands-on" experience.

## 1. Handling Authentication (Bearer Token)
Most real APIs are protected. You need to login, get a token, and use it.

```java
@Test
public void testGetSecureData() {
    // 1. Get Token (POST request)
    String token = given()
            .contentType("application/json")
            .body("{ \"username\": \"admin\", \"password\": \"password123\" }")
        .when()
            .post("/auth/login")
        .then()
            .extract().path("token"); // Extract token string

    // 2. Use Token in Next Request (GET request)
    given()
        .header("Authorization", "Bearer " + token)
    .when()
        .get("/secure-data")
    .then()
        .statusCode(200);
}
```

---

## 2. Request Chaining (E2E Scenario)
**Scenario**: Create a user -> Get that user -> Update that user -> Delete that user.
**Interview Tip**: This shows you understand data flow, not just single endpoints.

```java
@Test
public void testUserLifecycle() {
    // Step 1: Create User
    int userId = given()
        .contentType("application/json")
        .body("{ \"name\": \"John\", \"job\": \"QA\" }")
    .when()
        .post("/users")
    .then()
        .statusCode(201)
        .extract().path("id"); // Captured ID for next steps

    // Step 2: Update User using the captured ID
    given()
        .contentType("application/json")
        .body("{ \"name\": \"John\", \"job\": \"Senior QA\" }")
    .when()
        .put("/users/" + userId) // Dynamic URL
    .then()
        .statusCode(200);
}
```

---

## 3. Complex JSON Validation
**Scenario**: Verify that *at least one* user in a list has a specific email.

Response Structure:
```json
{
  "page": 1,
  "data": [
    { "id": 7, "email": "michael.lawson@reqres.in" },
    { "id": 8, "email": "lindsay.ferguson@reqres.in" }
  ]
}
```

**Test Code**:
```java
.then()
    // Check if ANY item in the 'data' array has this email
    .body("data.email", hasItem("lindsay.ferguson@reqres.in"))
    // Check if the list size is 6
    .body("data", hasSize(6)); 
```

---

## 4. POJO Mapping (Serialization/Deserialization)
**Interview Question**: "How do you manage large payloads?"
**Answer**: "I use POJOs (Plain Old Java Objects) with libraries like Jackson or Gson to avoid hardcoding strings."

**Step 1: Create a Class**
```java
public class User {
    private String name;
    private String job;
    
    // Constructors, Getters, Setters
    public User(String name, String job) {
        this.name = name;
        this.job = job;
    }
}
```

**Step 2: Use Object in Test**
```java
@Test
public void testCreateUserWithPOJO() {
    User user = new User("Alice", "Manager"); // Java Object

    given()
        .contentType("application/json")
        .body(user) // RestAssured automatically converts this to JSON!
    .when()
        .post("/users")
    .then()
        .statusCode(201);
}
```

---

## 5. Negative Testing
Don't just test 200 OK. Test that the API protects itself.

- **401 Unauthorized**: Try accessing a secure endpoint **without** a token.
- **400 Bad Request**: Send an incomplete payload (e.g., missing mandatory 'email' field).

```java
@Test
public void testMissingRequiredField() {
    String badPayload = "{ \"job\": \"Leader\" }"; // Missing 'name'

    given()
        .contentType("application/json")
        .body(badPayload)
    .when()
        .post("/users")
    .then()
        .statusCode(400); // Expect failure
}
```
