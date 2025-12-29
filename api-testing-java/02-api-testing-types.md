# Module 2: Key Types of API Testing

As a QA professional, you don't just "test" APIs; you apply specific strategies based on the goal.

## 1. API Automation Testing
**Goal**: Ensure the API functions correctly over time without manual intervention.

- **Why Automate?**
    - APIs are stable (UI changes often, APIs change less).
    - Faster execution than UI tests (seconds vs minutes).
    - find bugs earlier (Shift Left).
- **Core Strategy**:
    - **Positive Testing**: Happy path (Valid inputs -> 200 OK).
    - **Negative Testing**: Invalid inputs -> Proper error codes (400/401).
    - **Schema Validation**: Ensure the JSON structure matches expectations.
- **Top Tools (Java Ecosystem)**:
    - **RestAssured**: Industry standard, fluent BDD syntax.
    - **HttpClient (Java 11+)**: Native, no external dependency, good for simple needs.
    - **Retrofit**: Type-safe HTTP client (often used in Android, but great for testing too).

---

## 2. Smoke Testing (Sanity Check)
**Goal**: Verify that the critical functionalities are working before deep testing.

- **When to run**: Immediately after a new deployment/build.
- **What to test**:
    - Can I login? (POST /login)
    - Can I get the user profile? (GET /user)
    - Is the server up? (Health Check endpoint)
- **QA Tip**: Keep this suite fast (under 2 minutes). If smoke fails, reject the build.

---

## 3. Load & Performance Testing
**Goal**: Check how the API behaves under pressure.

- **Load Testing**:
    - Simulating **expected** traffic (e.g., 1000 users).
    - *Metric*: Does response time stay under 200ms?
- **Stress Testing**:
    - Simulating **extreme** traffic until it breaks.
    - *Metric*: At what point does the server return 500 errors?
- **Tools**:
    - **JMeter**: classic, powerful, supports Java scripting.
    - **Gatling**: Code-based (Scala/Java/Kotlin), excellent for high load.
    - **K6**: JavaScript-based, modern and developer-friendly.

---

### Summary Table

| Type | Focus | Frequency | Key Metric |
| :--- | :--- | :--- | :--- |
| **Functional** | Logic & Data | Every Commit (CI/CD) | Correctness |
| **Smoke** | Critical Paths | Every Deployment | Basic Availability |
| **Performance**| Speed & Stability| Major Releases | Response Time / Throughput |
