# Best Practices and Design Patterns - Deep Dive

## Overview

This module covers best practices and design patterns for writing maintainable, scalable, and reliable Playwright tests. Following these practices ensures test code quality and reduces maintenance overhead.

## Test Organization

### Directory Structure

```
src/
├── main/
│   └── java/
│       └── com/
│           └── example/
│               ├── pages/
│               │   ├── LoginPage.java
│               │   └── DashboardPage.java
│               ├── components/
│               │   ├── NavigationComponent.java
│               │   └── HeaderComponent.java
│               ├── utils/
│               │   ├── TestConfig.java
│               │   └── TestData.java
│               └── base/
│                   └── BaseTest.java
└── test/
    └── java/
        └── com/
            └── example/
                ├── tests/
                │   ├── login/
                │   │   └── LoginTest.java
                │   └── dashboard/
                │       └── DashboardTest.java
                └── resources/
                    ├── test-data.json
                    └── config.properties
```

### Naming Conventions

```java
// Test classes: {Feature}Test
public class LoginTest extends BaseTest { }

// Page objects: {Page}Page
public class LoginPage extends BasePage { }

// Test methods: test{Action}{ExpectedResult}
@Test
void testLoginWithValidCredentials() { }

// Helper methods: {action}{Object}
public void clickSubmitButton() { }
```

## Code Reusability

### Helper Classes

```java
public class TestHelper {
    private Page page;
    
    public TestHelper(Page page) {
        this.page = page;
    }
    
    public void waitForElement(String selector) {
        page.waitForSelector(selector, 
            new Page.WaitForSelectorOptions()
                .setState(WaitForSelectorState.VISIBLE)
                .setTimeout(30000));
    }
    
    public void takeScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("screenshots/" + name + ".png"))
            .setFullPage(true));
    }
    
    public void scrollToElement(String selector) {
        page.evaluate("(selector) => {" +
            "  const element = document.querySelector(selector);" +
            "  element.scrollIntoView({ behavior: 'smooth' });" +
            "}", selector);
    }
}
```

### Utility Classes

```java
public class StringUtils {
    public static String generateRandomString(int length) {
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        Random random = new Random();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append(chars.charAt(random.nextInt(chars.length())));
        }
        return sb.toString();
    }
    
    public static String generateEmail() {
        return "test_" + System.currentTimeMillis() + "@example.com";
    }
}
```

## Configuration Management

### Properties File

```properties
# config.properties
browser=chromium
headless=false
base.url=https://example.com
timeout=30000
screenshot.on.failure=true
```

### Configuration Class

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class TestConfig {
    private static Properties props;
    
    static {
        props = new Properties();
        try {
            props.load(new FileInputStream("src/test/resources/config.properties"));
        } catch (IOException e) {
            throw new RuntimeException("Failed to load config", e);
        }
    }
    
    public static String getBrowser() {
        return props.getProperty("browser", "chromium");
    }
    
    public static boolean isHeadless() {
        return Boolean.parseBoolean(props.getProperty("headless", "false"));
    }
    
    public static String getBaseUrl() {
        return props.getProperty("base.url");
    }
    
    public static int getTimeout() {
        return Integer.parseInt(props.getProperty("timeout", "30000"));
    }
    
    public static boolean isScreenshotOnFailure() {
        return Boolean.parseBoolean(props.getProperty("screenshot.on.failure", "true"));
    }
}
```

### Environment Variables

```java
public class TestConfig {
    public static String getBrowser() {
        return System.getenv().getOrDefault("BROWSER", "chromium");
    }
    
    public static boolean isHeadless() {
        return Boolean.parseBoolean(
            System.getenv().getOrDefault("HEADLESS", "false"));
    }
    
    public static String getBaseUrl() {
        return System.getenv().getOrDefault("BASE_URL", "https://example.com");
    }
}
```

## Error Handling

### Custom Exceptions

```java
public class ElementNotFoundException extends Exception {
    public ElementNotFoundException(String message) {
        super(message);
    }
    
    public ElementNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class PageNotLoadedException extends Exception {
    public PageNotLoadedException(String url) {
        super("Page not loaded: " + url);
    }
}
```

### Retry Logic

```java
public class RetryHelper {
    public static <T> T retry(Callable<T> action, int maxRetries) throws Exception {
        Exception lastException = null;
        for (int i = 0; i < maxRetries; i++) {
            try {
                return action.call();
            } catch (Exception e) {
                lastException = e;
                if (i < maxRetries - 1) {
                    Thread.sleep(1000 * (i + 1));  // Exponential backoff
                }
            }
        }
        throw lastException;
    }
}

// Usage
String result = RetryHelper.retry(() -> {
    return page.locator(".result").textContent();
}, 3);
```

### Error Handling in Tests

```java
public class ErrorHandlingTest extends BaseTest {
    @Test
    void testWithErrorHandling() {
        try {
            page.navigate("https://example.com");
            page.click("button");
            page.waitForSelector(".result");
        } catch (TimeoutException e) {
            // Take screenshot
            page.screenshot(new Page.ScreenshotOptions()
                .setPath(Paths.get("screenshots/timeout-error.png")));
            // Log error
            System.err.println("Timeout error: " + e.getMessage());
            throw e;
        } catch (Exception e) {
            // Handle other errors
            System.err.println("Unexpected error: " + e.getMessage());
            throw e;
        }
    }
}
```

## Test Maintenance

### Refactoring

```java
// Before: Duplicated code
@Test
void testLogin1() {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", "user1");
    page.fill("input[name='password']", "pass1");
    page.click("button[type='submit']");
}

@Test
void testLogin2() {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", "user2");
    page.fill("input[name='password']", "pass2");
    page.click("button[type='submit']");
}

// After: Using page object
@Test
void testLogin1() {
    LoginPage loginPage = new LoginPage(page);
    loginPage.navigateToLogin();
    loginPage.login("user1", "pass1");
}

@Test
void testLogin2() {
    LoginPage loginPage = new LoginPage(page);
    loginPage.navigateToLogin();
    loginPage.login("user2", "pass2");
}
```

### Code Reviews

#### Review Checklist

1. **Test readability**: Are tests easy to understand?
2. **Code duplication**: Is there duplicated code?
3. **Naming**: Are names descriptive and consistent?
4. **Error handling**: Is error handling appropriate?
5. **Maintainability**: Is the code easy to maintain?

### Documentation

```java
/**
 * Tests user login functionality
 * 
 * @author Test Team
 * @version 1.0
 */
public class LoginTest extends BaseTest {
    
    /**
     * Tests successful login with valid credentials
     * 
     * Steps:
     * 1. Navigate to login page
     * 2. Enter username and password
     * 3. Click login button
     * 4. Verify redirect to dashboard
     */
    @Test
    void testSuccessfulLogin() {
        // Test implementation
    }
}
```

## Design Patterns

### Page Object Model

```java
public class LoginPage extends BasePage {
    private final Page page;
    
    public LoginPage(Page page) {
        super(page);
        this.page = page;
    }
    
    private Locator usernameField() {
        return page.locator("input[name='username']");
    }
    
    private Locator passwordField() {
        return page.locator("input[name='password']");
    }
    
    private Locator loginButton() {
        return page.locator("button[type='submit']");
    }
    
    public DashboardPage login(String username, String password) {
        usernameField().fill(username);
        passwordField().fill(password);
        loginButton().click();
        page.waitForURL("**/dashboard");
        return new DashboardPage(page);
    }
}
```

### Factory Pattern

```java
public class PageFactory {
    public static LoginPage createLoginPage(Page page) {
        return new LoginPage(page);
    }
    
    public static DashboardPage createDashboardPage(Page page) {
        return new DashboardPage(page);
    }
}

// Usage
LoginPage loginPage = PageFactory.createLoginPage(page);
```

### Builder Pattern

```java
public class TestDataBuilder {
    private String username;
    private String password;
    private String email;
    
    public TestDataBuilder withUsername(String username) {
        this.username = username;
        return this;
    }
    
    public TestDataBuilder withPassword(String password) {
        this.password = password;
        return this;
    }
    
    public TestDataBuilder withEmail(String email) {
        this.email = email;
        return this;
    }
    
    public User build() {
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        user.setEmail(email);
        return user;
    }
}

// Usage
User user = new TestDataBuilder()
    .withUsername("testuser")
    .withPassword("password")
    .withEmail("test@example.com")
    .build();
```

## Best Practices Summary

### 1. Use Page Object Model

```java
// Good - Page Object Model
LoginPage loginPage = new LoginPage(page);
loginPage.login("user", "pass");

// Avoid - Direct Playwright calls in tests
page.fill("input[name='username']", "user");
page.fill("input[name='password']", "pass");
page.click("button[type='submit']");
```

### 2. Use Descriptive Names

```java
// Good - Descriptive
@Test
void testLoginWithValidCredentials() { }

// Avoid - Unclear
@Test
void test1() { }
```

### 3. Keep Tests Independent

```java
// Good - Independent tests
@Test
void testLogin() {
    // Does not depend on other tests
}

// Avoid - Dependent tests
@Test
void testLogin() {
    // Sets up state
}

@Test
void testDashboard() {
    // Depends on testLogin
}
```

### 4. Use Configuration

```java
// Good - Configuration
String baseUrl = TestConfig.getBaseUrl();
page.navigate(baseUrl);

// Avoid - Hardcoded values
page.navigate("https://example.com");
```

### 5. Handle Errors Gracefully

```java
// Good - Error handling
try {
    page.click("button");
} catch (TimeoutException e) {
    page.screenshot(new Page.ScreenshotOptions()
        .setPath(Paths.get("error.png")));
    throw e;
}

// Avoid - No error handling
page.click("button");  // May fail silently
```

## Key Takeaways

- Organize tests with clear directory structure
- Use descriptive naming conventions
- Create reusable helper and utility classes
- Manage configuration through properties files or environment variables
- Implement proper error handling and retry logic
- Follow design patterns (POM, Factory, Builder)
- Maintain code through refactoring and code reviews
- Document tests for better understanding

## References

- [Playwright Best Practices](https://playwright.dev/java/docs/best-practices)
- [Test Automation Design Patterns](https://www.selenium.dev/documentation/test_practices/)
- [Page Object Model](https://playwright.dev/java/docs/pom)
- [Test Organization](https://playwright.dev/java/docs/test-intro)

