# Module 5: Detailed Guide - RestAssured

RestAssured is the industry standard for Java API testing because of its powerful DSL (Domain Specific Language).

## 1. The Gherkin Syntax
It mimics BDD:
- **Given**: Configuration (Headers, Params, Auth, Body).
- **When**: Action (GET, POST, PUT, DELETE).
- **Then**: Validation (Status Code, Body Matchers, Time).

## 2. Request Specifications (DRY Principle)
Don't repeat the base URL or headers in every test.

```java
RequestSpecification requestSpec = new RequestSpecBuilder()
    .setBaseUri("https://reqres.in/api")
    .setContentType(ContentType.JSON)
    .build();

// Use it in tests
given()
    .spec(requestSpec)
.when()
    .get("/users")
.then()
    .statusCode(200);
```

## 3. Handling Authentication
RestAssured supports many auth types out of the box.

```java
// Basic Auth
given().auth().basic("username", "password")...

// OAuth2 / Bearer Token
given().auth().oauth2("your_token_string")...

// Custom Header
given().header("Authorization", "Bearer your_token_string")...
```

## 4. Extracting Data
Sometimes you need to get a value out of the response to use later.

```java
// Extract single value
String userId = given().when().get("/users").path("data[0].id");

// Extract entire response to work with complex logic
Response response = given().when().get("/users");
String email = response.jsonPath().getString("data[0].email");
```

## 5. JSON Schema Validation
Ensure the **entire structure** is correct, not just specific fields.
*(Requires separate `json-schema-validator` dependency equivalent)*

```java
.then()
    .assertThat()
    .body(matchesJsonSchemaInClasspath("user-schema.json"));
```
