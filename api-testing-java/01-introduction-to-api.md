# Module 1: Introduction to APIs for QA Professionals

## 1. What is an API?
**API** stands for **Application Programming Interface**.

Think of an API as a **waiter** in a restaurant:
- **You (The Client)**: Look at the menu and give an order.
- **The Kitchen (The Server)**: Prepares the food.
- **The Waiter ( The API)**: Takes your order to the kitchen and brings the food back to you.

In software, it allows two different applications to talk to each other. For a QA professional, testing an API means verifying that this communication happens correctly, securely, and efficiently, without looking at the user interface (UI).

### Architecture Basics
- **Client-Server**: The client (e.g., a mobile app) sends a **Request**. The server processes it and sends back a **Response**.
- **REST (Representational State Transfer)**: The most common architectural style for web APIs today. It uses standard HTTP methods.

---

## 2. Types of API Methods (HTTP Verbs)
For a QA, knowing which method to use is critical.

| Method | CRUD Operation | Description | QA Perspective / Example |
| :--- | :--- | :--- | :--- |
| **GET** | **R**ead | Retrieve data from the server. | **Safe & Idempotent**. Repeated calls don't change data. <br> *Ex: Get user details for ID 123.* |
| **POST** | **C**reate | Send data to the server to create a new resource. | **Not Idempotent**. Calling it multiple times creates multiple records. <br> *Ex: Create a new user account.* |
| **PUT** | **U**pdate (Full) | Update an existing resource completely. | Replaces the entire record. If a field is missing in the request, it might be set to null. <br> *Ex: Update all details of a user.* |
| **PATCH** | **U**pdate (Partial)| Update only specific fields of a resource. | Safer than PUT for minor updates. <br> *Ex: specific Update only the email address.* |
| **DELETE**| **D**elete | Remove a resource. | **Idempotent** (mostly). Deleting a deleted user should ideally return 404 (Not Found) or 200 (OK). <br> *Ex: Remove a user account.* |

---

## 3. HTTP Status Codes (The QA Cheat Sheet)
When you test, the first thing you check is the status code.

### 2xx: Success
- **200 OK**: Generic success (Standard for GET, PUT).
- **201 Created**: Resource successfully created (Standard for POST).
- **204 No Content**: Action succeeded but no content returned (Common for DELETE).

### 4xx: Client Errors (You sent something wrong)
- **400 Bad Request**: Invalid input (e.g., missing required field).
- **401 Unauthorized**: Authentication missing or invalid (e.g., bad API key).
- **403 Forbidden**: Authenticated, but no permission (e.g., user trying to delete admin).
- **404 Not Found**: Resource doesn't exist.

### 5xx: Server Errors (They messed up)
- **500 Internal Server Error**: Generic server crash.
- **502 Bad Gateway**: Upstream server issue.
- **503 Service Unavailable**: Server is overloaded or down for maintenance.

---

## 4. Anatomy of an API Request

Understanding the structure of an API request is fundamental for QA testing. Every API request consists of several components.

### URL Structure

```
https://api.example.com/v1/users/123/orders?status=pending&limit=10
|_____|_______________|__|_____|___|______|________________________|
Protocol   Host      Version Resource Path    Query Parameters
       |___________________|
            Base URL
```

| Component | Description | Example |
| :--- | :--- | :--- |
| **Protocol** | HTTP or HTTPS (secure) | `https://` |
| **Host** | Domain name or IP address | `api.example.com` |
| **Base URL** | Protocol + Host (root of the API) | `https://api.example.com` |
| **Version** | API version identifier | `/v1`, `/v2` |
| **Resource Path** | The endpoint targeting a specific resource | `/users`, `/users/123` |
| **Path Parameters** | Dynamic segments in the URL path | `/users/{userId}` → `/users/123` |
| **Query Parameters** | Key-value pairs after `?` for filtering/options | `?status=pending&limit=10` |

### Complete Request Structure

A full API request contains:

```
┌─────────────────────────────────────────────────────────────┐
│                        REQUEST                               │
├─────────────────────────────────────────────────────────────┤
│  REQUEST LINE                                                │
│  POST /v1/users HTTP/1.1                                    │
├─────────────────────────────────────────────────────────────┤
│  HEADERS                                                     │
│  Host: api.example.com                                       │
│  Content-Type: application/json                              │
│  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...              │
│  Accept: application/json                                    │
├─────────────────────────────────────────────────────────────┤
│  BODY (for POST, PUT, PATCH)                                │
│  {                                                           │
│    "name": "John Doe",                                       │
│    "email": "john@example.com"                               │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Types of Parameters

Parameters are the inputs you send to an API. Understanding each type is critical for thorough testing.

### 5.1 Path Parameters

Path parameters are part of the URL path and typically identify a specific resource.

**Syntax**: `/resource/{parameter}` or `/resource/:parameter`

**Examples**:
```
GET /users/{userId}          → GET /users/123
GET /users/{userId}/orders   → GET /users/123/orders
GET /orders/{orderId}/items/{itemId} → GET /orders/456/items/789
```

**QA Test Cases for Path Parameters**:
| Test Scenario | Example | Expected Behavior |
| :--- | :--- | :--- |
| Valid ID | `/users/123` | 200 OK with user data |
| Non-existent ID | `/users/99999` | 404 Not Found |
| Invalid format (string instead of number) | `/users/abc` | 400 Bad Request |
| Zero | `/users/0` | 400 or 404 (depends on API design) |
| Negative number | `/users/-1` | 400 Bad Request |
| Special characters | `/users/12%3B3` | 400 Bad Request |
| SQL injection attempt | `/users/1;DROP TABLE users` | 400 Bad Request (must not execute) |
| Empty path parameter | `/users/` | 404 or routes to `/users` |

### 5.2 Query Parameters

Query parameters appear after `?` in the URL and are used for filtering, sorting, pagination, and optional inputs.

**Syntax**: `?key1=value1&key2=value2`

**Common Use Cases**:
```
GET /users?page=1&limit=20              # Pagination
GET /users?sort=name&order=asc          # Sorting
GET /users?status=active&role=admin     # Filtering
GET /products?search=laptop&category=electronics  # Search
GET /orders?startDate=2024-01-01&endDate=2024-12-31  # Date range
```

**QA Test Cases for Query Parameters**:
| Test Scenario | Example | Expected Behavior |
| :--- | :--- | :--- |
| Valid parameters | `?page=1&limit=10` | 200 OK with paginated results |
| Missing optional parameter | `?page=1` (no limit) | Uses default limit |
| Invalid data type | `?page=abc` | 400 Bad Request or default value |
| Negative values | `?page=-1` | 400 Bad Request or first page |
| Exceeding max limit | `?limit=10000` | 400 or capped to max allowed |
| Special characters | `?search=John%20Doe` | URL-encoded values work |
| Empty value | `?status=` | Depends on API (empty or ignored) |
| Duplicate keys | `?status=active&status=inactive` | Last value wins or array |
| Unknown parameter | `?unknownParam=value` | Ignored or 400 Bad Request |
| SQL/XSS injection | `?search=<script>alert(1)</script>` | Sanitized, no execution |

### 5.3 Header Parameters

Headers carry metadata about the request such as authentication, content type, and custom application data.

**Syntax**: `Header-Name: Header-Value`

**Examples**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
X-Api-Version: 2.0
```

*(Detailed header information in Section 6)*

### 5.4 Body Parameters

Body parameters are sent in the request body, typically with POST, PUT, and PATCH requests.

**Supported Formats**:
- `application/json` - Most common for REST APIs
- `application/xml` - Legacy systems
- `application/x-www-form-urlencoded` - HTML form data
- `multipart/form-data` - File uploads

*(Detailed body information in Section 7)*

---

## 6. HTTP Headers

Headers provide essential metadata for API communication. As a QA, you must understand both request and response headers.

### 6.1 Common Request Headers

| Header | Purpose | Example Values | QA Testing Focus |
| :--- | :--- | :--- | :--- |
| **Content-Type** | Format of the request body | `application/json`, `application/xml`, `multipart/form-data` | Test with mismatched content types |
| **Accept** | Expected response format | `application/json`, `application/xml`, `*/*` | Verify content negotiation |
| **Authorization** | Authentication credentials | `Bearer <token>`, `Basic <base64>`, `ApiKey <key>` | Test invalid/expired/missing tokens |
| **User-Agent** | Client application identifier | `Mozilla/5.0`, `MyApp/1.0` | Test different client behaviors |
| **Accept-Language** | Preferred response language | `en-US`, `fr-FR`, `es` | Test localization |
| **Accept-Encoding** | Supported compression | `gzip, deflate, br` | Test compressed responses |
| **Cache-Control** | Caching directives | `no-cache`, `max-age=3600` | Test cache behavior |
| **X-Request-ID** | Unique request identifier | UUID | Useful for debugging/tracing |
| **X-Correlation-ID** | Track requests across services | UUID | Microservices tracing |

### 6.2 Common Response Headers

| Header | Purpose | Example Values | QA Testing Focus |
| :--- | :--- | :--- | :--- |
| **Content-Type** | Format of response body | `application/json; charset=utf-8` | Verify matches Accept header |
| **Content-Length** | Size of response body in bytes | `1234` | Verify accuracy |
| **Cache-Control** | Caching instructions | `no-store`, `max-age=86400` | Test cache policies |
| **ETag** | Resource version identifier | `"33a64df551425fcc55e4d42a148795d9f25f89d4"` | Test conditional requests |
| **Last-Modified** | When resource was last changed | `Wed, 21 Oct 2024 07:28:00 GMT` | Test with If-Modified-Since |
| **X-RateLimit-Limit** | Max requests allowed | `1000` | Test rate limiting |
| **X-RateLimit-Remaining** | Requests remaining | `999` | Monitor during load testing |
| **X-RateLimit-Reset** | When limit resets (Unix timestamp) | `1640995200` | Test reset behavior |
| **Location** | URL for redirects or created resources | `https://api.example.com/users/123` | Verify on 201, 301, 302 |
| **WWW-Authenticate** | Auth method for 401 responses | `Bearer realm="api"` | Check authentication challenges |

### 6.3 QA Test Cases for Headers

| Test Scenario | How to Test | Expected Behavior |
| :--- | :--- | :--- |
| Missing Content-Type | Send POST without Content-Type | 400 or 415 Unsupported Media Type |
| Wrong Content-Type | Send JSON with `Content-Type: text/plain` | 400 or 415 |
| Missing Authorization | Omit Authorization header | 401 Unauthorized |
| Invalid Authorization | Send malformed token | 401 Unauthorized |
| Expired token | Use expired JWT | 401 Unauthorized |
| Case sensitivity | `content-type` vs `Content-Type` | Headers are case-insensitive (HTTP/1.1) |
| Header injection | Include `\r\n` in header value | Sanitized, no injection |
| Oversized headers | Send very large header values | 431 Request Header Fields Too Large |
| Accept negotiation | Request XML when only JSON supported | 406 Not Acceptable |

---

## 7. Request Body

The request body contains data sent to the server, typically with POST, PUT, and PATCH methods.

### 7.1 JSON Data Types

JSON (JavaScript Object Notation) is the most common format. Understanding data types is crucial for validation testing.

```json
{
  "string": "Hello World",           // String - text in double quotes
  "integer": 42,                      // Number - whole number
  "float": 3.14159,                   // Number - decimal
  "boolean_true": true,               // Boolean - true
  "boolean_false": false,             // Boolean - false
  "null_value": null,                 // Null - explicit absence of value
  "array": [1, 2, 3, "four"],         // Array - ordered list
  "object": {                         // Object - nested key-value pairs
    "nested_key": "nested_value"
  }
}
```

### 7.2 Data Type Details

| Data Type | Description | Valid Examples | Invalid Examples |
| :--- | :--- | :--- | :--- |
| **String** | Text enclosed in double quotes | `"hello"`, `""`, `"123"` | `'hello'` (single quotes), `hello` (no quotes) |
| **Number (Integer)** | Whole numbers | `0`, `42`, `-17`, `1000000` | `"42"` (quoted = string) |
| **Number (Float)** | Decimal numbers | `3.14`, `-0.001`, `2.0` | `3,14` (comma not valid) |
| **Boolean** | True or false | `true`, `false` | `"true"` (quoted = string), `True`, `1` |
| **Null** | Absence of value | `null` | `"null"` (quoted = string), `undefined`, `None` |
| **Array** | Ordered collection | `[]`, `[1,2,3]`, `["a","b"]` | `[1,2,]` (trailing comma) |
| **Object** | Key-value collection | `{}`, `{"key": "value"}` | `{key: "value"}` (unquoted key) |

### 7.3 Sample Request Bodies

**Creating a User (POST /users)**:
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "age": 30,
  "isActive": true,
  "roles": ["user", "editor"],
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001",
    "country": "USA"
  },
  "preferences": {
    "newsletter": true,
    "theme": "dark"
  },
  "phoneNumbers": [
    {"type": "home", "number": "555-1234"},
    {"type": "work", "number": "555-5678"}
  ]
}
```

**Updating a User (PUT /users/123)** - Full replacement:
```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john.smith@example.com",
  "age": 31,
  "isActive": true,
  "roles": ["user", "admin"],
  "address": {
    "street": "456 Oak Ave",
    "city": "Los Angeles",
    "state": "CA",
    "zipCode": "90001",
    "country": "USA"
  }
}
```

**Partial Update (PATCH /users/123)**:
```json
{
  "email": "newemail@example.com",
  "address": {
    "city": "Chicago"
  }
}
```

### 7.4 QA Test Cases for Request Body

| Test Category | Test Scenario | Expected Behavior |
| :--- | :--- | :--- |
| **Required Fields** | Missing required field | 400 Bad Request with field name |
| | All required fields present | 200/201 Success |
| | Required field with null value | 400 Bad Request |
| | Required field with empty string | Depends on validation rules |
| **Data Types** | String instead of number | 400 Bad Request |
| | Number instead of string | 400 or auto-conversion |
| | String "true" instead of boolean true | 400 Bad Request |
| | Float instead of integer | Depends on API (may truncate) |
| **String Validation** | Empty string `""` | Depends on rules |
| | String exceeds max length | 400 Bad Request |
| | String below min length | 400 Bad Request |
| | Special characters | Should be accepted (properly escaped) |
| | Unicode characters | Should be accepted |
| | HTML/Script tags | Sanitized or rejected |
| **Number Validation** | Zero | Depends on business rules |
| | Negative numbers | Depends on field (age: reject, balance: maybe) |
| | Extremely large numbers | 400 or overflow handling |
| | Decimal precision | Verify rounding behavior |
| **Array Validation** | Empty array `[]` | Depends on rules |
| | Array exceeds max items | 400 Bad Request |
| | Duplicate items in array | Depends on uniqueness rules |
| | Wrong type in array | 400 Bad Request |
| **Object Validation** | Empty object `{}` | Depends on rules |
| | Extra/unknown fields | Ignored or 400 (depends on API) |
| | Deeply nested objects | Test depth limits |
| **Security** | SQL injection in strings | Sanitized, no execution |
| | XSS in strings | Sanitized, no execution |
| | Malformed JSON | 400 Bad Request |
| | Extremely large payload | 413 Payload Too Large |

### 7.5 Form Data and File Uploads

**application/x-www-form-urlencoded** (HTML forms):
```
firstName=John&lastName=Doe&email=john%40example.com
```

**multipart/form-data** (File uploads):
```
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="document.pdf"
Content-Type: application/pdf

(binary file content)
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="description"

My uploaded document
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**QA Test Cases for File Uploads**:
| Test Scenario | Expected Behavior |
| :--- | :--- |
| Valid file type | 200/201 Success |
| Invalid file type (exe when expecting pdf) | 400/415 Unsupported |
| File exceeds size limit | 413 Payload Too Large |
| Empty file | 400 Bad Request |
| Malicious file (virus) | Rejected by security scan |
| File with double extension (file.pdf.exe) | Rejected |
| Filename with special characters | Sanitized |

---

## 8. Response Structure

Understanding response structure helps QA validate API outputs effectively.

### 8.1 Successful Response Examples

**Single Resource (GET /users/123)**:
```json
{
  "status": "success",
  "data": {
    "id": 123,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-06-20T14:45:00Z"
  }
}
```

**Collection with Pagination (GET /users?page=1&limit=10)**:
```json
{
  "status": "success",
  "data": [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Wilson", "email": "bob@example.com"}
  ],
  "meta": {
    "currentPage": 1,
    "perPage": 10,
    "totalPages": 5,
    "totalCount": 47
  },
  "links": {
    "self": "/users?page=1&limit=10",
    "first": "/users?page=1&limit=10",
    "prev": null,
    "next": "/users?page=2&limit=10",
    "last": "/users?page=5&limit=10"
  }
}
```

**Created Resource (POST /users)** - 201 Created:
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "id": 124,
    "firstName": "New",
    "lastName": "User",
    "email": "new.user@example.com",
    "createdAt": "2024-07-01T09:00:00Z"
  }
}
```

### 8.2 Error Response Examples

**Validation Error (400 Bad Request)**:
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "Email must be a valid email address"
    },
    {
      "field": "age",
      "code": "OUT_OF_RANGE",
      "message": "Age must be between 18 and 120"
    },
    {
      "field": "password",
      "code": "TOO_SHORT",
      "message": "Password must be at least 8 characters"
    }
  ],
  "timestamp": "2024-07-01T10:30:00Z",
  "path": "/api/v1/users",
  "requestId": "req-abc123"
}
```

**Authentication Error (401 Unauthorized)**:
```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "Authentication required",
  "details": "Token is missing or invalid",
  "timestamp": "2024-07-01T10:30:00Z"
}
```

**Authorization Error (403 Forbidden)**:
```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "Access denied",
  "details": "You do not have permission to delete this resource",
  "requiredRole": "admin",
  "currentRole": "user"
}
```

**Not Found Error (404)**:
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "Resource not found",
  "details": "User with ID 99999 does not exist"
}
```

**Server Error (500)**:
```json
{
  "status": "error",
  "code": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "requestId": "req-xyz789",
  "timestamp": "2024-07-01T10:30:00Z"
}
```

### 8.3 QA Validation Checklist for Responses

| Validation Area | What to Check |
| :--- | :--- |
| **Status Code** | Matches expected code for the operation |
| **Response Time** | Within acceptable limits (SLA) |
| **Content-Type Header** | Matches expected format |
| **Response Structure** | Follows documented schema |
| **Data Types** | Fields have correct types |
| **Required Fields** | All documented fields present |
| **Field Values** | Values are accurate and logical |
| **Null Handling** | Null vs missing vs empty handled correctly |
| **Date Formats** | Consistent format (ISO 8601 recommended) |
| **Pagination** | Meta information is accurate |
| **Error Messages** | Descriptive but not exposing sensitive info |
| **Sensitive Data** | Passwords, tokens not returned |
| **Character Encoding** | UTF-8, special characters display correctly |

---

## 9. Authentication and Authorization

Understanding authentication types is essential for security testing.

### 9.1 Authentication Types

| Type | How It Works | Header Example | Use Case |
| :--- | :--- | :--- | :--- |
| **API Key** | Static key sent with requests | `X-API-Key: abc123` or `?api_key=abc123` | Simple integrations |
| **Basic Auth** | Base64 encoded username:password | `Authorization: Basic dXNlcjpwYXNz` | Legacy systems |
| **Bearer Token** | Token (often JWT) sent in header | `Authorization: Bearer eyJhbG...` | Modern APIs |
| **OAuth 2.0** | Token obtained through auth flow | `Authorization: Bearer <access_token>` | Third-party access |
| **Digest Auth** | Challenge-response mechanism | `Authorization: Digest username="user"...` | More secure than Basic |
| **HMAC** | Signature-based authentication | Custom header with signature | High-security APIs |

### 9.2 JWT (JSON Web Token) Structure

JWTs are widely used. Understanding their structure helps in testing.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
|___________________________________|._______________________________________________|.___________________________________|
            Header (Base64)                        Payload (Base64)                         Signature
```

**Decoded JWT Example**:
```json
// Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// Payload
{
  "sub": "1234567890",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin",
  "iat": 1516239022,
  "exp": 1516242622
}
```

### 9.3 QA Test Cases for Authentication

| Test Scenario | Expected Behavior |
| :--- | :--- |
| Valid credentials/token | 200 OK - Access granted |
| Missing auth header | 401 Unauthorized |
| Invalid API key | 401 Unauthorized |
| Malformed token | 401 Unauthorized |
| Expired token | 401 Unauthorized |
| Token for wrong environment | 401 Unauthorized |
| Revoked token | 401 Unauthorized |
| Tampered JWT (modified payload) | 401 Unauthorized |
| Wrong algorithm in JWT | 401 Unauthorized |
| Token with insufficient permissions | 403 Forbidden |
| Brute force protection | 429 Too Many Requests after X attempts |
| Token in response body (not header) | Verify secure transmission |

### 9.4 Authorization Testing

| Test Scenario | Example | Expected Behavior |
| :--- | :--- | :--- |
| Access own resource | User A accesses /users/A | 200 OK |
| Access other's resource | User A accesses /users/B | 403 Forbidden |
| Role-based access | User role accesses admin endpoint | 403 Forbidden |
| Elevated privileges | Modify own role to admin | 403 Forbidden |
| Deleted user token | Use token after user deletion | 401 Unauthorized |
| Cross-tenant access | Tenant A accesses Tenant B data | 403 Forbidden |

---

## 10. Additional Important Concepts

### 10.1 Idempotency

An operation is **idempotent** if calling it multiple times produces the same result as calling it once.

| Method | Idempotent? | Explanation |
| :--- | :--- | :--- |
| GET | Yes | Reading data doesn't change it |
| PUT | Yes | Replacing a resource with same data = same result |
| DELETE | Yes | Deleting an already-deleted resource = still deleted |
| POST | No | Each call typically creates a new resource |
| PATCH | Depends | Can be idempotent if designed properly |

**QA Relevance**: Test idempotent operations by calling them multiple times and verifying consistent results.

### 10.2 Rate Limiting

APIs limit requests to prevent abuse. Common response:

**429 Too Many Requests**:
```json
{
  "status": "error",
  "code": "RATE_LIMITED",
  "message": "Too many requests",
  "retryAfter": 60
}
```

**Rate Limit Headers**:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

**QA Test Cases**:
- Verify rate limit headers are present
- Test behavior when limit is exceeded
- Verify reset works correctly
- Test different rate limits for different endpoints/users

### 10.3 API Versioning

Common versioning strategies:

| Strategy | Example | Pros/Cons |
| :--- | :--- | :--- |
| URL Path | `/v1/users`, `/v2/users` | Clear, easy to test, but pollutes URL |
| Query Parameter | `/users?version=1` | Flexible, but can be forgotten |
| Header | `X-API-Version: 1` or `Accept: application/vnd.api.v1+json` | Clean URLs, but less visible |

**QA Test Cases**:
- Test all supported versions
- Verify deprecated version warnings
- Test version fallback behavior
- Ensure backward compatibility claims

### 10.4 Timeouts

| Timeout Type | Description | Typical Values |
| :--- | :--- | :--- |
| Connection Timeout | Time to establish connection | 5-30 seconds |
| Read Timeout | Time to receive response | 30-120 seconds |
| Idle Timeout | Time before idle connection closes | 60-300 seconds |

**QA Test Cases**:
- Test with slow network simulation
- Verify timeout error messages
- Test retry behavior after timeout
- Load test to identify timeout thresholds

### 10.5 CORS (Cross-Origin Resource Sharing)

CORS headers control which domains can access the API from browsers.

**Key Headers**:
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

**QA Relevance**: Test API calls from browser-based applications to verify CORS is correctly configured.

---

## 11. Quick Reference Card

### HTTP Methods
| Method | CRUD | Idempotent | Has Body |
| :--- | :--- | :--- | :--- |
| GET | Read | Yes | No |
| POST | Create | No | Yes |
| PUT | Update (Full) | Yes | Yes |
| PATCH | Update (Partial) | Depends | Yes |
| DELETE | Delete | Yes | Usually No |

### Common Status Codes
| Code | Meaning | When Used |
| :--- | :--- | :--- |
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Auth missing/invalid |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Semantic errors |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Server crash |
| 502 | Bad Gateway | Upstream error |
| 503 | Service Unavailable | Server overloaded |

### Content Types
| Type | Usage |
| :--- | :--- |
| `application/json` | JSON data (most common) |
| `application/xml` | XML data |
| `application/x-www-form-urlencoded` | Form data |
| `multipart/form-data` | File uploads |
| `text/plain` | Plain text |

---

## 12. Summary

As a QA professional testing APIs, always verify:

1. **Request Construction**: Correct URL, method, headers, and body
2. **Response Validation**: Status code, headers, body structure, data types
3. **Authentication**: Valid/invalid tokens, permissions, security
4. **Error Handling**: Appropriate error codes and messages
5. **Edge Cases**: Boundary values, empty inputs, special characters
6. **Security**: Injection attacks, sensitive data exposure
7. **Performance**: Response times, rate limiting, timeouts
8. **Documentation**: API behaves as documented

This foundation prepares you for hands-on API testing using tools like Postman, RestAssured, and other frameworks covered in subsequent modules.
