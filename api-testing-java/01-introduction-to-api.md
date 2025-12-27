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
