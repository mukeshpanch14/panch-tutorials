# Java with Playwright for Web Automation Testing - Learning Plan

A structured, developer-focused guide to mastering **Java with Playwright** for web application automation testing. Each section includes learning objectives, key concepts, practical examples, and official resources for deeper exploration.

## 1. Java Fundamentals for Testing

**Objective:**  
Build a solid foundation in Java programming concepts essential for test automation.

**Key Concepts:**
- Java basics: classes, methods, variables, data types
- Object-oriented programming: inheritance, polymorphism, encapsulation
- Collections: List, Map, Set
- Exception handling: try-catch, custom exceptions
- Maven/Gradle build tools: project structure, dependencies

**Example:**
```java
public class TestBase {
    protected WebDriver driver;
    
    @BeforeEach
    void setUp() {
        // Setup code
    }
    
    @AfterEach
    void tearDown() {
        // Cleanup code
    }
}
```

**References:**
- [Java Documentation](https://docs.oracle.com/javase/tutorial/)
- [Maven Getting Started](https://maven.apache.org/guides/getting-started/)
- [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html)

**Deep Dive:** [View detailed guide](./01-java-fundamentals.md)

---

## 2. Introduction to Playwright

**Objective:**  
Understand what Playwright is, its advantages, and how it differs from other automation tools.

**Key Concepts:**
- What is Playwright: cross-browser automation framework
- Key features: auto-waiting, network interception, multi-browser support
- Playwright vs Selenium: differences and use cases
- Supported browsers: Chromium, Firefox, WebKit
- Architecture: Playwright API, browser contexts, pages

**Example:**
```java
import com.microsoft.playwright.*;

public class FirstTest {
    public static void main(String[] args) {
        Playwright playwright = Playwright.create();
        Browser browser = playwright.chromium().launch();
        Page page = browser.newPage();
        page.navigate("https://example.com");
        browser.close();
        playwright.close();
    }
}
```

**References:**
- [Playwright Documentation](https://playwright.dev/java/)
- [Why Playwright?](https://playwright.dev/java/docs/intro)
- [Playwright vs Selenium](https://playwright.dev/java/docs/why-playwright)

**Deep Dive:** [View detailed guide](./02-introduction-playwright.md)

---

## 3. Setting Up Playwright with Java

**Objective:**  
Set up a Java project with Playwright dependencies and configure the development environment.

**Key Concepts:**
- Maven/Gradle dependency configuration
- Installing Playwright browsers
- Project structure: test directories, resources
- IDE setup: IntelliJ IDEA, Eclipse
- Running first Playwright test

**Example:**
```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.microsoft.playwright</groupId>
    <artifactId>playwright</artifactId>
    <version>1.40.0</version>
</dependency>
```

**References:**
- [Playwright Java Installation](https://playwright.dev/java/docs/intro)
- [Maven Repository](https://mvnrepository.com/artifact/com.microsoft.playwright/playwright)

**Deep Dive:** [View detailed guide](./03-setting-up-playwright.md)

---

## 4. Basic Playwright Operations

**Objective:**  
Learn fundamental Playwright operations for interacting with web pages.

**Key Concepts:**
- Navigation: `navigate()`, `goBack()`, `goForward()`, `reload()`
- Locators: CSS selectors, XPath, text selectors, role-based locators
- Element interactions: `click()`, `fill()`, `type()`, `press()`
- Reading values: `textContent()`, `innerText()`, `getAttribute()`
- Waiting strategies: auto-wait, explicit waits

**Example:**
```java
page.navigate("https://example.com");
page.fill("input[name='username']", "testuser");
page.click("button[type='submit']");
String title = page.title();
```

**References:**
- [Playwright Locators](https://playwright.dev/java/docs/locators)
- [Playwright Actions](https://playwright.dev/java/docs/input)

**Deep Dive:** [View detailed guide](./04-basic-operations.md)

---

## 5. Advanced Locator Strategies

**Objective:**  
Master various locator strategies and best practices for reliable element identification.

**Key Concepts:**
- CSS selectors: basic and advanced
- XPath: absolute and relative paths
- Text-based locators: `getByText()`, `getByLabel()`, `getByRole()`
- Chaining locators: `locator().locator()`
- Custom locators: data-testid, custom attributes
- Locator best practices: stability, maintainability

**Example:**
```java
// Role-based locator
page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Submit")).click();

// Text-based locator
page.getByText("Welcome").click();

// Chained locator
page.locator("div.container").getByText("Item").click();
```

**References:**
- [Playwright Locators Guide](https://playwright.dev/java/docs/locators)
- [Best Practices for Locators](https://playwright.dev/java/docs/best-practices)

**Deep Dive:** [View detailed guide](./05-advanced-locators.md)

---

## 6. Test Framework Integration (JUnit/TestNG)

**Objective:**  
Integrate Playwright with Java test frameworks for structured test execution.

**Key Concepts:**
- JUnit 5: annotations, assertions, test lifecycle
- TestNG: test groups, parallel execution, data providers
- Test structure: setup, execution, teardown
- Assertions: Playwright assertions vs JUnit/TestNG assertions
- Test organization: test classes, test suites

**Example:**
```java
import org.junit.jupiter.api.*;
import com.microsoft.playwright.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class LoginTest {
    static Playwright playwright;
    static Browser browser;
    Page page;
    
    @BeforeAll
    static void setUp() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch();
    }
    
    @BeforeEach
    void createPage() {
        page = browser.newPage();
    }
    
    @Test
    void testLogin() {
        page.navigate("https://example.com/login");
        // Test implementation
    }
}
```

**References:**
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [TestNG Documentation](https://testng.org/doc/documentation-main.html)
- [Playwright Test Runner](https://playwright.dev/java/docs/test-intro)

**Deep Dive:** [View detailed guide](./06-test-framework-integration.md)

---

## 7. Page Object Model (POM) Pattern

**Objective:**  
Implement the Page Object Model pattern for maintainable and reusable test code.

**Key Concepts:**
- POM principles: encapsulation, reusability
- Creating page classes: element locators, action methods
- Page factory pattern
- Component-based page objects
- Base page class: common functionality

**Example:**
```java
public class LoginPage {
    private final Page page;
    
    public LoginPage(Page page) {
        this.page = page;
    }
    
    private Locator usernameField() {
        return page.locator("#username");
    }
    
    public void login(String username, String password) {
        usernameField().fill(username);
        page.locator("#password").fill(password);
        page.locator("button[type='submit']").click();
    }
}
```

**References:**
- [Page Object Model Pattern](https://playwright.dev/java/docs/pom)
- [Selenium Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

**Deep Dive:** [View detailed guide](./07-page-object-model.md)

---

## 8. Handling Dynamic Elements and Waits

**Objective:**  
Master waiting strategies for handling dynamic content and asynchronous operations.

**Key Concepts:**
- Auto-waiting: Playwright's built-in waits
- Explicit waits: `waitForSelector()`, `waitForLoadState()`
- Custom wait conditions
- Handling AJAX calls and dynamic content
- Timeout configuration: global and per-action timeouts
- Flaky test prevention

**Example:**
```java
// Wait for element to be visible
page.waitForSelector(".dynamic-content", new Page.WaitForSelectorOptions().setState(WaitForSelectorState.VISIBLE));

// Wait for network idle
page.waitForLoadState(LoadState.NETWORKIDLE);

// Wait for custom condition
page.waitForCondition(() -> page.locator(".status").textContent().equals("Ready"));
```

**References:**
- [Playwright Auto-waiting](https://playwright.dev/java/docs/actionability)
- [Playwright Waits](https://playwright.dev/java/docs/waits)

**Deep Dive:** [View detailed guide](./08-handling-waits.md)

---

## 9. Working with Frames, Windows, and Tabs

**Objective:**  
Handle complex browser scenarios involving multiple windows, tabs, and iframes.

**Key Concepts:**
- Frame handling: accessing nested frames, frame switching
- Window management: new windows, tabs, popups
- Context switching: browser contexts
- Multi-window scenarios: window handles, focus management

**Example:**
```java
// Frame handling
Frame frame = page.frame("frame-name");
frame.click("button");

// New window
Page newPage = page.context().waitForPage(() -> {
    page.click("a[target='_blank']");
});
newPage.waitForLoadState();
```

**References:**
- [Playwright Frames](https://playwright.dev/java/docs/frames)
- [Playwright Browser Contexts](https://playwright.dev/java/docs/browser-contexts)

**Deep Dive:** [View detailed guide](./09-frames-windows.md)

---

## 10. Network Interception and API Testing

**Objective:**  
Intercept and mock network requests, and perform API testing with Playwright.

**Key Concepts:**
- Request/response interception: `route()`, `unroute()`
- Mocking API responses: stubbing network calls
- Request/response inspection: headers, body, status codes
- API testing: making HTTP requests
- Network conditions: simulating slow networks

**Example:**
```java
// Intercept and mock
page.route("**/api/users", route -> {
    route.fulfill(new Route.FulfillOptions()
        .setStatus(200)
        .setBody("{\"users\": []}"));
});

// API request
APIRequestContext requestContext = playwright.request().newContext();
APIResponse response = requestContext.get("https://api.example.com/users");
```

**References:**
- [Playwright Network](https://playwright.dev/java/docs/network)
- [Playwright API Testing](https://playwright.dev/java/docs/api-testing)

**Deep Dive:** [View detailed guide](./10-network-api-testing.md)

---

## 11. File Operations and Downloads

**Objective:**  
Handle file uploads, downloads, and file system operations in tests.

**Key Concepts:**
- File uploads: `setInputFiles()`, multiple files
- File downloads: download events, file paths
- Reading/writing files: file system operations
- Screenshot capture: full page, element screenshots
- PDF generation: page to PDF conversion

**Example:**
```java
// File upload
page.setInputFiles("input[type='file']", Paths.get("path/to/file.pdf"));

// File download
Download download = page.waitForDownload(() -> {
    page.click("a.download-link");
});
download.saveAs(Paths.get("downloaded-file.pdf"));

// Screenshot
page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get("screenshot.png")));
```

**References:**
- [Playwright File Operations](https://playwright.dev/java/docs/downloads)
- [Playwright Screenshots](https://playwright.dev/java/docs/screenshots)

**Deep Dive:** [View detailed guide](./11-file-operations.md)

---

## 12. Advanced Browser Features

**Objective:**  
Leverage advanced Playwright features for complex testing scenarios.

**Key Concepts:**
- Browser contexts: isolation, cookies, storage
- Geolocation and permissions: location, notifications
- Device emulation: mobile devices, viewport sizes
- Browser extensions: loading extensions
- JavaScript execution: `evaluate()`, `evaluateHandle()`

**Example:**
```java
// Device emulation
BrowserContext context = browser.newContext(new Browser.NewContextOptions()
    .setViewportSize(375, 667)
    .setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"));

// Geolocation
context.setGeolocation(new Geolocation(40.7128, -74.0060));
context.setPermissions(Collections.singletonList("geolocation"), new BrowserContext.SetPermissionsOptions()
    .setOrigin("https://example.com"));
```

**References:**
- [Playwright Browser Contexts](https://playwright.dev/java/docs/browser-contexts)
- [Playwright Devices](https://playwright.dev/java/docs/emulation)

**Deep Dive:** [View detailed guide](./12-advanced-browser-features.md)

---

## 13. Test Data Management

**Objective:**  
Implement effective strategies for managing test data and test fixtures.

**Key Concepts:**
- Test data sources: JSON, CSV, Excel, databases
- Data-driven testing: parameterized tests
- Test fixtures: setup and teardown data
- Random data generation: Faker library
- Data cleanup: database resets, API cleanup

**Example:**
```java
// JSON data
ObjectMapper mapper = new ObjectMapper();
TestData data = mapper.readValue(new File("test-data.json"), TestData.class);

// Parameterized test
@ParameterizedTest
@CsvSource({"user1, pass1", "user2, pass2"})
void testLogin(String username, String password) {
    // Test implementation
}
```

**References:**
- [JUnit 5 Parameterized Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests)
- [Java Faker](https://github.com/DiUS/java-faker)

**Deep Dive:** [View detailed guide](./13-test-data-management.md)

---

## 14. Reporting and Test Execution

**Objective:**  
Generate comprehensive test reports and configure test execution strategies.

**Key Concepts:**
- Test reporting: HTML reports, Allure, ExtentReports
- Test execution: parallel execution, test grouping
- CI/CD integration: Jenkins, GitHub Actions, GitLab CI
- Test retries: flaky test handling
- Test tagging: categories, priorities

**Example:**
```java
// Allure reporting
@Epic("Authentication")
@Feature("Login")
@Story("User Login")
@Test
void testLogin() {
    // Test implementation
}

// Parallel execution (TestNG)
@Test(threadPoolSize = 3, invocationCount = 10)
void parallelTest() {
    // Test implementation
}
```

**References:**
- [Allure TestOps](https://docs.qameta.io/allure/)
- [ExtentReports](https://www.extentreports.com/)
- [Playwright Test Reports](https://playwright.dev/java/docs/test-reporters)

**Deep Dive:** [View detailed guide](./14-reporting-execution.md)

---

## 15. Debugging and Troubleshooting

**Objective:**  
Debug test failures and troubleshoot common issues in Playwright tests.

**Key Concepts:**
- Playwright Inspector: step-through debugging
- Trace viewer: recording test execution
- Console logging: debug logs, network logs
- Screenshot on failure: automatic screenshots
- Common issues: timing, selectors, browser compatibility

**Example:**
```java
// Run with inspector
// Set environment variable: PWDEBUG=1

// Trace recording
BrowserContext context = browser.newContext();
context.tracing().start(new Tracing.StartOptions()
    .setScreenshots(true)
    .setSnapshots(true));
// ... test execution ...
context.tracing().stop(new Tracing.StopOptions()
    .setPath(Paths.get("trace.zip")));
```

**References:**
- [Playwright Debugging](https://playwright.dev/java/docs/debug)
- [Playwright Trace Viewer](https://playwright.dev/java/docs/trace-viewer)

**Deep Dive:** [View detailed guide](./15-debugging-troubleshooting.md)

---

## 16. Best Practices and Design Patterns

**Objective:**  
Apply best practices and design patterns for maintainable and scalable test automation.

**Key Concepts:**
- Test organization: structure, naming conventions
- Code reusability: helper classes, utilities
- Configuration management: properties files, environment variables
- Error handling: custom exceptions, retry logic
- Test maintenance: refactoring, code reviews

**Example:**
```java
// Configuration class
public class TestConfig {
    private static Properties props;
    
    static {
        props = new Properties();
        try {
            props.load(new FileInputStream("config.properties"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String getBaseUrl() {
        return props.getProperty("base.url");
    }
}
```

**References:**
- [Playwright Best Practices](https://playwright.dev/java/docs/best-practices)
- [Test Automation Design Patterns](https://www.selenium.dev/documentation/test_practices/)

**Deep Dive:** [View detailed guide](./16-best-practices.md)

---

## 17. Real-World Test Scenarios

**Objective:**  
Apply learned concepts to real-world testing scenarios and complex applications.

**Examples:**
- E-commerce testing: product search, cart, checkout
- Form validation: multi-step forms, file uploads
- Authentication flows: login, registration, password reset
- API integration testing: frontend-backend validation
- Cross-browser testing: compatibility validation
- Performance testing: load time, response time

**References:**
- [Playwright Examples](https://github.com/microsoft/playwright-java)
- [Playwright Community](https://github.com/microsoft/playwright/discussions)

**Deep Dive:** [View detailed guide](./17-real-world-scenarios.md)

---

## 18. Capstone Projects

**Objective:**  
Apply all learned concepts through comprehensive end-to-end test automation projects.

**Projects:**
1. **E-commerce Test Suite** — Complete test automation for an online store
2. **SaaS Application Testing** — Multi-tenant application testing with data isolation
3. **API + UI Integration Testing** — Combined API and UI test automation
4. **Cross-Browser Test Framework** — Comprehensive browser compatibility testing

**References:**
- [Playwright Java Examples](https://github.com/microsoft/playwright-java/tree/main/playwright/src/main/java/com/microsoft/playwright/examples)
- [Playwright Test Examples](https://github.com/microsoft/playwright/tree/main/tests)

---

### Next Steps

You can use this guide as a self-paced learning roadmap or training material. For best results:
- Follow the order of topics progressively
- Practice each concept with hands-on exercises
- Build a portfolio of test automation projects
- Contribute to open-source Playwright projects

---

**Author:** Developer Enablement  
**Version:** v1.0  
**Last Updated:** 2025
