# Test Framework Integration (JUnit/TestNG) - Deep Dive

## Overview

This module covers integrating Playwright with Java test frameworks (JUnit 5 and TestNG) for structured test execution, including setup/teardown, assertions, test organization, and parallel execution.

## JUnit 5 Integration

### JUnit 5 Setup

Add JUnit 5 dependency to `pom.xml`:

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.0</version>
    <scope>test</scope>
</dependency>
```

### Basic JUnit 5 Test

```java
import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

public class BasicJUnitTest {
    static Playwright playwright;
    static Browser browser;
    BrowserContext context;
    Page page;
    
    @BeforeAll
    static void setUpAll() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new BrowserType.LaunchOptions().setHeadless(false)
        );
    }
    
    @BeforeEach
    void setUp() {
        context = browser.newContext();
        page = context.newPage();
    }
    
    @Test
    @DisplayName("Navigate to Playwright website")
    void testNavigate() {
        page.navigate("https://playwright.dev");
        String title = page.title();
        Assertions.assertTrue(title.contains("Playwright"));
    }
    
    @AfterEach
    void tearDown() {
        context.close();
    }
    
    @AfterAll
    static void tearDownAll() {
        browser.close();
        playwright.close();
    }
}
```

### JUnit 5 Annotations

```java
@BeforeAll      // Runs once before all tests
@BeforeEach     // Runs before each test
@Test           // Marks a test method
@AfterEach      // Runs after each test
@AfterAll       // Runs once after all tests
@DisplayName    // Custom test name
@Disabled       // Skip test
@Tag            // Tag for filtering
@Order          // Test execution order
```

### Test Organization

```java
@DisplayName("Login Tests")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class LoginTest {
    static Playwright playwright;
    static Browser browser;
    BrowserContext context;
    Page page;
    
    @BeforeAll
    static void setUpAll() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch();
    }
    
    @BeforeEach
    void setUp() {
        context = browser.newContext();
        page = context.newPage();
    }
    
    @Test
    @Order(1)
    @DisplayName("Should login successfully")
    @Tag("smoke")
    void testSuccessfulLogin() {
        page.navigate("https://example.com/login");
        page.fill("input[name='username']", "testuser");
        page.fill("input[name='password']", "password");
        page.click("button[type='submit']");
        page.waitForURL("**/dashboard");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
    
    @Test
    @Order(2)
    @DisplayName("Should show error on invalid credentials")
    @Tag("regression")
    void testInvalidLogin() {
        page.navigate("https://example.com/login");
        page.fill("input[name='username']", "invalid");
        page.fill("input[name='password']", "wrong");
        page.click("button[type='submit']");
        String errorMessage = page.locator(".error").textContent();
        Assertions.assertTrue(errorMessage.contains("Invalid"));
    }
    
    @AfterEach
    void tearDown() {
        context.close();
    }
    
    @AfterAll
    static void tearDownAll() {
        browser.close();
        playwright.close();
    }
}
```

### JUnit 5 Assertions

```java
import org.junit.jupiter.api.Assertions;

// Basic assertions
Assertions.assertTrue(condition);
Assertions.assertFalse(condition);
Assertions.assertEquals(expected, actual);
Assertions.assertNotEquals(expected, actual);
Assertions.assertNull(object);
Assertions.assertNotNull(object);

// String assertions
Assertions.assertTrue(text.contains("expected"));
Assertions.assertTrue(text.startsWith("prefix"));
Assertions.assertTrue(text.endsWith("suffix"));

// Collection assertions
Assertions.assertTrue(list.isEmpty());
Assertions.assertEquals(expectedSize, list.size());
Assertions.assertTrue(list.contains(item));

// Exception assertions
Assertions.assertThrows(Exception.class, () -> {
    // Code that should throw exception
});
```

### Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.CsvSource;

@ParameterizedTest
@ValueSource(strings = {"user1", "user2", "user3"})
void testLoginWithDifferentUsers(String username) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", "password");
    page.click("button[type='submit']");
    Assertions.assertTrue(page.url().contains("dashboard"));
}

@ParameterizedTest
@CsvSource({
    "user1, pass1",
    "user2, pass2",
    "user3, pass3"
})
void testLoginWithCredentials(String username, String password) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", password);
    page.click("button[type='submit']");
    Assertions.assertTrue(page.url().contains("dashboard"));
}
```

## TestNG Integration

### TestNG Setup

Add TestNG dependency to `pom.xml`:

```xml
<dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.8.0</version>
    <scope>test</scope>
</dependency>
```

### Basic TestNG Test

```java
import com.microsoft.playwright.*;
import org.testng.annotations.*;

public class BasicTestNGTest {
    static Playwright playwright;
    static Browser browser;
    BrowserContext context;
    Page page;
    
    @BeforeSuite
    public void setUpSuite() {
        playwright = Playwright.create();
    }
    
    @BeforeClass
    public void setUpClass() {
        browser = playwright.chromium().launch(
            new BrowserType.LaunchOptions().setHeadless(false)
        );
    }
    
    @BeforeMethod
    public void setUp() {
        context = browser.newContext();
        page = context.newPage();
    }
    
    @Test
    public void testNavigate() {
        page.navigate("https://playwright.dev");
        String title = page.title();
        Assert.assertTrue(title.contains("Playwright"));
    }
    
    @AfterMethod
    public void tearDown() {
        context.close();
    }
    
    @AfterClass
    public void tearDownClass() {
        browser.close();
    }
    
    @AfterSuite
    public void tearDownSuite() {
        playwright.close();
    }
}
```

### TestNG Annotations

```java
@BeforeSuite      // Runs once before all tests in suite
@BeforeClass      // Runs once before all tests in class
@BeforeMethod     // Runs before each test method
@Test             // Marks a test method
@AfterMethod      // Runs after each test method
@AfterClass       // Runs once after all tests in class
@AfterSuite       // Runs once after all tests in suite
@BeforeGroups     // Runs before test groups
@AfterGroups      // Runs after test groups
```

### Test Groups

```java
@Test(groups = {"smoke", "login"})
public void testLogin() {
    // Test implementation
}

@Test(groups = {"regression", "login"})
public void testInvalidLogin() {
    // Test implementation
}

@Test(groups = {"smoke", "dashboard"})
public void testDashboard() {
    // Test implementation
}
```

### TestNG Data Providers

```java
@DataProvider(name = "loginCredentials")
public Object[][] loginCredentials() {
    return new Object[][] {
        {"user1", "pass1"},
        {"user2", "pass2"},
        {"user3", "pass3"}
    };
}

@Test(dataProvider = "loginCredentials")
public void testLoginWithDataProvider(String username, String password) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", password);
    page.click("button[type='submit']");
    Assert.assertTrue(page.url().contains("dashboard"));
}
```

### TestNG Parallel Execution

```java
// TestNG XML configuration
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Playwright Tests" parallel="methods" thread-count="3">
    <test name="Login Tests">
        <classes>
            <class name="com.example.LoginTest"/>
        </classes>
    </test>
</suite>

// Or in test class
@Test(threadPoolSize = 3, invocationCount = 10)
public void parallelTest() {
    // Test implementation
}
```

### TestNG Assertions

```java
import org.testng.Assert;

// Basic assertions
Assert.assertTrue(condition);
Assert.assertFalse(condition);
Assert.assertEquals(actual, expected);
Assert.assertNotEquals(actual, expected);
Assert.assertNull(object);
Assert.assertNotNull(object);

// String assertions
Assert.assertTrue(text.contains("expected"));
Assert.assertTrue(text.startsWith("prefix"));
Assert.assertTrue(text.endsWith("suffix"));

// Soft assertions
SoftAssert softAssert = new SoftAssert();
softAssert.assertTrue(condition1);
softAssert.assertTrue(condition2);
softAssert.assertAll(); // Throws if any assertion failed
```

## Base Test Class

### JUnit 5 Base Class

```java
import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

public abstract class BaseTest {
    protected static Playwright playwright;
    protected static Browser browser;
    protected BrowserContext context;
    protected Page page;
    
    @BeforeAll
    static void setUpAll() {
        playwright = Playwright.create();
        browser = playwright.chromium().launch(
            new BrowserType.LaunchOptions()
                .setHeadless(Boolean.parseBoolean(
                    System.getProperty("headless", "true")
                ))
        );
    }
    
    @BeforeEach
    void setUp() {
        context = browser.newContext();
        page = context.newPage();
    }
    
    @AfterEach
    void tearDown() {
        if (context != null) {
            context.close();
        }
    }
    
    @AfterAll
    static void tearDownAll() {
        if (browser != null) {
            browser.close();
        }
        if (playwright != null) {
            playwright.close();
        }
    }
    
    protected void navigateTo(String url) {
        page.navigate(url);
    }
    
    protected void takeScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("target/screenshots/" + name + ".png")));
    }
}
```

### TestNG Base Class

```java
import com.microsoft.playwright.*;
import org.testng.annotations.*;

public abstract class BaseTest {
    protected static Playwright playwright;
    protected static Browser browser;
    protected BrowserContext context;
    protected Page page;
    
    @BeforeSuite
    public void setUpSuite() {
        playwright = Playwright.create();
    }
    
    @BeforeClass
    public void setUpClass() {
        browser = playwright.chromium().launch(
            new BrowserType.LaunchOptions()
                .setHeadless(Boolean.parseBoolean(
                    System.getProperty("headless", "true")
                ))
        );
    }
    
    @BeforeMethod
    public void setUp() {
        context = browser.newContext();
        page = context.newPage();
    }
    
    @AfterMethod
    public void tearDown() {
        if (context != null) {
            context.close();
        }
    }
    
    @AfterClass
    public void tearDownClass() {
        if (browser != null) {
            browser.close();
        }
    }
    
    @AfterSuite
    public void tearDownSuite() {
        if (playwright != null) {
            playwright.close();
        }
    }
    
    protected void navigateTo(String url) {
        page.navigate(url);
    }
    
    protected void takeScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("target/screenshots/" + name + ".png")));
    }
}
```

## Using Base Test Class

```java
// JUnit 5
public class LoginTest extends BaseTest {
    @Test
    void testLogin() {
        navigateTo("https://example.com/login");
        page.fill("input[name='username']", "testuser");
        page.fill("input[name='password']", "password");
        page.click("button[type='submit']");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
}

// TestNG
public class LoginTest extends BaseTest {
    @Test
    public void testLogin() {
        navigateTo("https://example.com/login");
        page.fill("input[name='username']", "testuser");
        page.fill("input[name='password']", "password");
        page.click("button[type='submit']");
        Assert.assertTrue(page.url().contains("dashboard"));
    }
}
```

## Playwright Assertions vs Framework Assertions

### Playwright Assertions

```java
import com.microsoft.playwright.assertions.PlaywrightAssertions;

// Playwright assertions (auto-wait)
PlaywrightAssertions.assertThat(page.locator("button")).isVisible();
PlaywrightAssertions.assertThat(page.locator("input")).hasValue("expected");
PlaywrightAssertions.assertThat(page).hasURL("**/dashboard");
PlaywrightAssertions.assertThat(page).hasTitle("Expected Title");
```

### Framework Assertions

```java
// JUnit 5
Assertions.assertTrue(page.locator("button").isVisible());
Assertions.assertEquals("expected", page.locator("input").inputValue());

// TestNG
Assert.assertTrue(page.locator("button").isVisible());
Assert.assertEquals(page.locator("input").inputValue(), "expected");
```

### When to Use Each

- **Playwright Assertions**: When you need auto-waiting and better error messages
- **Framework Assertions**: When you need framework-specific features (soft assertions, etc.)

## Test Execution

### Running JUnit 5 Tests

```bash
# Maven
mvn test

# Run specific test class
mvn test -Dtest=LoginTest

# Run specific test method
mvn test -Dtest=LoginTest#testLogin

# Run tests with specific tag
mvn test -Dgroups=smoke

# Gradle
./gradlew test

# Run specific test class
./gradlew test --tests LoginTest

# Run specific test method
./gradlew test --tests LoginTest.testLogin
```

### Running TestNG Tests

```bash
# Maven
mvn test

# Run specific test class
mvn test -Dtest=LoginTest

# Run with testng.xml
mvn test -DsuiteXmlFile=testng.xml

# Gradle
./gradlew test

# Run with testng.xml
./gradlew test -DsuiteXmlFile=testng.xml
```

## Key Takeaways

- JUnit 5 and TestNG both work well with Playwright
- Use base test classes for common setup/teardown
- Leverage framework features (parameterized tests, groups, etc.)
- Choose assertions based on your needs (auto-waiting vs framework features)
- Organize tests with annotations and tags
- Use parallel execution for faster test runs

## References

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [TestNG Documentation](https://testng.org/doc/documentation-main.html)
- [Playwright Test Runner](https://playwright.dev/java/docs/test-intro)
- [JUnit 5 Assertions](https://junit.org/junit5/docs/current/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html)

