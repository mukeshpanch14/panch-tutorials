# Network Interception and API Testing - Deep Dive

## Overview

This module covers network interception, API mocking, and API testing with Playwright. These features enable testing of complex scenarios involving network requests, API responses, and backend integration.

## Network Interception

### What is Network Interception?

Network interception allows you to intercept, modify, or mock network requests and responses. This is useful for:
- Mocking API responses
- Testing error scenarios
- Simulating slow networks
- Validating request/response data

### Basic Interception

```java
// Intercept and mock request
page.route("**/api/users", route -> {
    route.fulfill(new Route.FulfillOptions()
        .setStatus(200)
        .setBody("{\"users\": []}")
        .setContentType("application/json"));
});

// Navigate and trigger request
page.navigate("https://example.com");
page.click("button.load-users");
```

### Intercepting Requests

```java
// Intercept all requests
page.route("**/*", route -> {
    System.out.println("Request: " + route.request().url());
    route.continue_();
});

// Intercept specific URL pattern
page.route("**/api/**", route -> {
    System.out.println("API Request: " + route.request().url());
    route.continue_();
});

// Intercept and modify request
page.route("**/api/users", route -> {
    Request request = route.request();
    System.out.println("Method: " + request.method());
    System.out.println("URL: " + request.url());
    System.out.println("Headers: " + request.headers());
    route.continue_();
});
```

### Mocking Responses

```java
// Mock successful response
page.route("**/api/users", route -> {
    route.fulfill(new Route.FulfillOptions()
        .setStatus(200)
        .setBody("{\"users\": [{\"id\": 1, \"name\": \"John\"}]}")
        .setContentType("application/json"));
});

// Mock error response
page.route("**/api/users", route -> {
    route.fulfill(new Route.FulfillOptions()
        .setStatus(500)
        .setBody("{\"error\": \"Internal Server Error\"}")
        .setContentType("application/json"));
});

// Mock with delay
page.route("**/api/users", route -> {
    try {
        Thread.sleep(2000);  // 2 second delay
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    route.fulfill(new Route.FulfillOptions()
        .setStatus(200)
        .setBody("{\"users\": []}"));
});
```

### Conditional Interception

```java
// Intercept based on request method
page.route("**/api/users", route -> {
    if ("POST".equals(route.request().method())) {
        route.fulfill(new Route.FulfillOptions()
            .setStatus(201)
            .setBody("{\"id\": 1, \"name\": \"New User\"}"));
    } else {
        route.continue_();
    }
});

// Intercept based on request body
page.route("**/api/users", route -> {
    String body = route.request().postData();
    if (body != null && body.contains("admin")) {
        route.fulfill(new Route.FulfillOptions()
            .setStatus(403)
            .setBody("{\"error\": \"Forbidden\"}"));
    } else {
        route.continue_();
    }
});
```

### Unroute

```java
// Remove route interception
page.unroute("**/api/users");

// Remove all routes
page.unrouteAll();
```

## Request/Response Inspection

### Inspecting Requests

```java
// Listen to requests
page.onRequest(request -> {
    System.out.println("Request URL: " + request.url());
    System.out.println("Request Method: " + request.method());
    System.out.println("Request Headers: " + request.headers());
    if (request.postData() != null) {
        System.out.println("Request Body: " + request.postData());
    }
});

// Listen to responses
page.onResponse(response -> {
    System.out.println("Response URL: " + response.url());
    System.out.println("Response Status: " + response.status());
    System.out.println("Response Headers: " + response.headers());
});
```

### Waiting for Requests

```java
// Wait for request
Request request = page.waitForRequest("**/api/users", () -> {
    page.click("button.load-users");
});

System.out.println("Request URL: " + request.url());
System.out.println("Request Method: " + request.method());

// Wait for response
Response response = page.waitForResponse("**/api/users", () -> {
    page.click("button.load-users");
});

System.out.println("Response Status: " + response.status());
System.out.println("Response Body: " + response.text());
```

### Request/Response Examples

```java
// Example: Validate API call
public void validateApiCall() {
    // Wait for request
    Request request = page.waitForRequest("**/api/users", () -> {
        page.click("button.load-users");
    });
    
    // Validate request
    Assertions.assertEquals("GET", request.method());
    Assertions.assertTrue(request.url().contains("/api/users"));
    
    // Wait for response
    Response response = page.waitForResponse("**/api/users", () -> {
        page.click("button.load-users");
    });
    
    // Validate response
    Assertions.assertEquals(200, response.status());
    String body = response.text();
    Assertions.assertTrue(body.contains("users"));
}
```

## API Testing

### What is API Testing?

Playwright can make direct HTTP requests to APIs, enabling API testing alongside UI testing.

### Creating API Request Context

```java
// Create API request context
APIRequestContext requestContext = playwright.request().newContext();

// Create with options
APIRequestContext requestContext = playwright.request().newContext(
    new APIRequest.NewContextOptions()
        .setBaseURL("https://api.example.com")
        .setExtraHTTPHeaders(Map.of("Authorization", "Bearer token"))
);
```

### Making API Requests

```java
// GET request
APIResponse response = requestContext.get("https://api.example.com/users");
System.out.println("Status: " + response.status());
System.out.println("Body: " + response.text());

// POST request
APIResponse response = requestContext.post("https://api.example.com/users",
    new APIRequestContext.PostOptions()
        .setData("{\"name\": \"John\", \"email\": \"john@example.com\"}")
        .setHeader("Content-Type", "application/json"));

// PUT request
APIResponse response = requestContext.put("https://api.example.com/users/1",
    new APIRequestContext.PutOptions()
        .setData("{\"name\": \"Jane\"}")
        .setHeader("Content-Type", "application/json"));

// DELETE request
APIResponse response = requestContext.delete("https://api.example.com/users/1");

// PATCH request
APIResponse response = requestContext.patch("https://api.example.com/users/1",
    new APIRequestContext.PatchOptions()
        .setData("{\"name\": \"Updated\"}")
        .setHeader("Content-Type", "application/json"));
```

### API Request Options

```java
// Request with headers
APIResponse response = requestContext.get("https://api.example.com/users",
    new APIRequestContext.GetOptions()
        .setHeader("Authorization", "Bearer token")
        .setHeader("Content-Type", "application/json"));

// Request with query parameters
APIResponse response = requestContext.get("https://api.example.com/users",
    new APIRequestContext.GetOptions()
        .setQueryParam("page", "1")
        .setQueryParam("limit", "10"));

// Request with timeout
APIResponse response = requestContext.get("https://api.example.com/users",
    new APIRequestContext.GetOptions()
        .setTimeout(30000));
```

### Handling API Responses

```java
// Get response status
int status = response.status();
Assertions.assertEquals(200, status);

// Get response headers
Map<String, String> headers = response.headers();
String contentType = headers.get("content-type");

// Get response body
String text = response.text();
JSONObject json = new JSONObject(text);

// Get response as JSON
JSONObject json = response.json();

// Get response as buffer
byte[] buffer = response.body();
```

## Network Conditions

### Simulating Slow Networks

```java
// Simulate slow 3G
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setNetworkConditions(NetworkConditions.SLOW_3G));

// Simulate fast 3G
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setNetworkConditions(NetworkConditions.FAST_3G));

// Custom network conditions
NetworkConditions customConditions = new NetworkConditions()
    .setDownloadThroughput(500 * 1024)  // 500 KB/s
    .setUploadThroughput(500 * 1024)    // 500 KB/s
    .setLatency(100);                    // 100ms

BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setNetworkConditions(customConditions));
```

### Offline Mode

```java
// Set offline mode
context.setOffline(true);

// Set online mode
context.setOffline(false);
```

## Practical Examples

### Mocking API Responses

```java
public class ApiMockingTest {
    private Page page;
    
    public ApiMockingTest(Page page) {
        this.page = page;
    }
    
    public void mockSuccessfulResponse() {
        // Mock successful API response
        page.route("**/api/users", route -> {
            route.fulfill(new Route.FulfillOptions()
                .setStatus(200)
                .setBody("{\"users\": [{\"id\": 1, \"name\": \"John\"}]}")
                .setContentType("application/json"));
        });
        
        // Navigate and trigger request
        page.navigate("https://example.com");
        page.click("button.load-users");
        
        // Verify UI updated
        String userList = page.locator(".user-list").textContent();
        Assertions.assertTrue(userList.contains("John"));
    }
    
    public void mockErrorResponse() {
        // Mock error response
        page.route("**/api/users", route -> {
            route.fulfill(new Route.FulfillOptions()
                .setStatus(500)
                .setBody("{\"error\": \"Internal Server Error\"}")
                .setContentType("application/json"));
        });
        
        // Navigate and trigger request
        page.navigate("https://example.com");
        page.click("button.load-users");
        
        // Verify error message displayed
        String errorMessage = page.locator(".error-message").textContent();
        Assertions.assertTrue(errorMessage.contains("Error"));
    }
}
```

### API Testing

```java
public class ApiTest {
    private APIRequestContext requestContext;
    
    public ApiTest(Playwright playwright) {
        requestContext = playwright.request().newContext(
            new APIRequest.NewContextOptions()
                .setBaseURL("https://api.example.com")
        );
    }
    
    public void testGetUsers() {
        // GET request
        APIResponse response = requestContext.get("/users");
        
        // Validate response
        Assertions.assertEquals(200, response.status());
        JSONObject json = response.json();
        Assertions.assertTrue(json.has("users"));
    }
    
    public void testCreateUser() {
        // POST request
        APIResponse response = requestContext.post("/users",
            new APIRequestContext.PostOptions()
                .setData("{\"name\": \"John\", \"email\": \"john@example.com\"}")
                .setHeader("Content-Type", "application/json"));
        
        // Validate response
        Assertions.assertEquals(201, response.status());
        JSONObject json = response.json();
        Assertions.assertTrue(json.has("id"));
    }
    
    public void testUpdateUser() {
        // PUT request
        APIResponse response = requestContext.put("/users/1",
            new APIRequestContext.PutOptions()
                .setData("{\"name\": \"Jane\"}")
                .setHeader("Content-Type", "application/json"));
        
        // Validate response
        Assertions.assertEquals(200, response.status());
        JSONObject json = response.json();
        Assertions.assertEquals("Jane", json.getString("name"));
    }
    
    public void testDeleteUser() {
        // DELETE request
        APIResponse response = requestContext.delete("/users/1");
        
        // Validate response
        Assertions.assertEquals(204, response.status());
    }
}
```

### Combined UI and API Testing

```java
public class CombinedTest {
    private Page page;
    private APIRequestContext requestContext;
    
    public CombinedTest(Page page, Playwright playwright) {
        this.page = page;
        this.requestContext = playwright.request().newContext();
    }
    
    public void testUserCreation() {
        // Create user via API
        APIResponse response = requestContext.post("https://api.example.com/users",
            new APIRequestContext.PostOptions()
                .setData("{\"name\": \"John\", \"email\": \"john@example.com\"}")
                .setHeader("Content-Type", "application/json"));
        
        Assertions.assertEquals(201, response.status());
        JSONObject user = response.json();
        int userId = user.getInt("id");
        
        // Verify user in UI
        page.navigate("https://example.com/users");
        page.waitForSelector(".user-list");
        String userList = page.locator(".user-list").textContent();
        Assertions.assertTrue(userList.contains("John"));
    }
}
```

## Best Practices

### 1. Use Route Interception for Mocking

```java
// Good - mock API responses
page.route("**/api/users", route -> {
    route.fulfill(new Route.FulfillOptions()
        .setStatus(200)
        .setBody("{\"users\": []}"));
});

// Avoid - modify actual API
// This would affect real API calls
```

### 2. Clean Up Routes

```java
// Good - remove routes after use
@AfterEach
void tearDown() {
    page.unrouteAll();
}

// Avoid - routes remain active
```

### 3. Validate Request/Response

```java
// Good - validate API calls
Request request = page.waitForRequest("**/api/users", () -> {
    page.click("button");
});
Assertions.assertEquals("GET", request.method());

// Avoid - no validation
page.click("button");
```

### 4. Use API Context for API Testing

```java
// Good - separate API context
APIRequestContext apiContext = playwright.request().newContext();

// Avoid - using page for API calls
// Use API context instead
```

## Key Takeaways

- Network interception enables mocking and testing of API calls
- API testing allows direct HTTP requests without browser
- Request/response inspection helps validate API interactions
- Network conditions can simulate different network speeds
- Combine UI and API testing for comprehensive coverage
- Always clean up routes and contexts after use

## References

- [Playwright Network](https://playwright.dev/java/docs/network)
- [Playwright API Testing](https://playwright.dev/java/docs/api-testing)
- [Playwright Route Interception](https://playwright.dev/java/docs/network#handle-requests)
- [Playwright Request/Response](https://playwright.dev/java/docs/network#handle-responses)

