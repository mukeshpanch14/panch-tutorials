# Reporting and Test Execution - Deep Dive

## Overview

This module covers test reporting, test execution strategies, CI/CD integration, test retries, and test tagging. These features are essential for maintaining test quality and providing visibility into test results.

## Test Reporting

### HTML Reports

#### Basic HTML Report

```java
// Generate HTML report
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("reports/screenshot.png")));

// Save page content
String html = page.content();
Files.writeString(Paths.get("reports/page.html"), html);
```

### Allure Reporting

#### Setup

Add dependencies to `pom.xml`:

```xml
<dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit5</artifactId>
    <version>2.24.0</version>
</dependency>
```

#### Using Allure

```java
import io.qameta.allure.*;

@Epic("Authentication")
@Feature("Login")
@Story("User Login")
public class LoginTest extends BaseTest {
    
    @Test
    @DisplayName("Should login successfully")
    @Description("Test user login with valid credentials")
    @Severity(SeverityLevel.CRITICAL)
    @Step("Login with username: {username}")
    void testLogin(@Parameter("username") String username) {
        page.navigate("https://example.com/login");
        page.fill("input[name='username']", username);
        page.fill("input[name='password']", "password");
        page.click("button[type='submit']");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
    
    @Test
    @DisplayName("Should show error on invalid credentials")
    @Description("Test login with invalid credentials")
    @Severity(SeverityLevel.NORMAL)
    @Attachment(value = "Screenshot", type = "image/png")
    void testInvalidLogin() {
        page.navigate("https://example.com/login");
        page.fill("input[name='username']", "invalid");
        page.fill("input[name='password']", "wrong");
        page.click("button[type='submit']");
        
        // Attach screenshot
        byte[] screenshot = page.screenshot();
        Allure.addAttachment("Screenshot", "image/png", 
            new ByteArrayInputStream(screenshot));
        
        Assertions.assertTrue(page.locator(".error").isVisible());
    }
}
```

### ExtentReports

#### Setup

Add dependency to `pom.xml`:

```xml
<dependency>
    <groupId>com.aventstack</groupId>
    <artifactId>extentreports</artifactId>
    <version>5.0.9</version>
</dependency>
```

#### Using ExtentReports

```java
import com.aventstack.extentreports.*;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;

public class ExtentReportTest extends BaseTest {
    private static ExtentReports extent;
    private ExtentTest test;
    
    @BeforeAll
    static void setUpAll() {
        ExtentSparkReporter reporter = new ExtentSparkReporter("reports/extent-report.html");
        extent = new ExtentReports();
        extent.attachReporter(reporter);
    }
    
    @BeforeEach
    void setUp() {
        super.setUp();
        test = extent.createTest("Login Test");
    }
    
    @Test
    void testLogin() {
        test.log(Status.INFO, "Navigating to login page");
        page.navigate("https://example.com/login");
        
        test.log(Status.INFO, "Filling login form");
        page.fill("input[name='username']", "testuser");
        page.fill("input[name='password']", "password");
        
        test.log(Status.INFO, "Clicking login button");
        page.click("button[type='submit']");
        
        test.log(Status.PASS, "Login successful");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
    
    @AfterEach
    void tearDown() {
        extent.flush();
        super.tearDown();
    }
}
```

## Test Execution

### Parallel Execution

#### JUnit 5 Parallel Execution

```java
// junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
```

#### TestNG Parallel Execution

```java
// testng.xml
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

### Test Grouping

#### JUnit 5 Tags

```java
@Test
@Tag("smoke")
void testLogin() {
    // Test implementation
}

@Test
@Tag("regression")
void testInvalidLogin() {
    // Test implementation
}

// Run specific tags
// mvn test -Dgroups=smoke
```

#### TestNG Groups

```java
@Test(groups = {"smoke", "login"})
public void testLogin() {
    // Test implementation
}

@Test(groups = {"regression", "login"})
public void testInvalidLogin() {
    // Test implementation
}

// Run specific groups
// mvn test -Dgroups=smoke
```

## CI/CD Integration

### GitHub Actions

#### GitHub Actions Workflow

```yaml
name: Playwright Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up JDK 11
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'temurin'
      
      - name: Install Playwright Browsers
        run: mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install"
      
      - name: Run tests
        run: mvn test
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: target/surefire-reports/
```

### Jenkins

#### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'target/surefire-reports/*.xml'
                    publishHTML([
                        reportDir: 'target/surefire-reports',
                        reportFiles: 'index.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
    }
}
```

### GitLab CI

#### GitLab CI Configuration

```yaml
stages:
  - test

playwright-tests:
  stage: test
  image: maven:3.8-openjdk-11
  before_script:
    - apt-get update && apt-get install -y libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
  script:
    - mvn clean test
  artifacts:
    when: always
    paths:
      - target/surefire-reports/
    reports:
      junit: target/surefire-reports/TEST-*.xml
```

## Test Retries

### JUnit 5 Retries

```java
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.extension.RegisterExtension;

@ExtendWith(RetryExtension.class)
public class RetryTest extends BaseTest {
    
    @RegisterExtension
    static RetryExtension retryExtension = new RetryExtension(3);
    
    @Test
    @RetryOnFailure(maxAttempts = 3)
    void testWithRetry() {
        // Test implementation
    }
}
```

### TestNG Retries

```java
import org.testng.IRetryAnalyzer;
import org.testng.ITestResult;

public class RetryAnalyzer implements IRetryAnalyzer {
    private int retryCount = 0;
    private static final int MAX_RETRY_COUNT = 3;
    
    @Override
    public boolean retry(ITestResult result) {
        if (retryCount < MAX_RETRY_COUNT) {
            retryCount++;
            return true;
        }
        return false;
    }
}

// Usage
@Test(retryAnalyzer = RetryAnalyzer.class)
public void testWithRetry() {
    // Test implementation
}
```

## Test Tagging

### Categories

```java
// JUnit 5
@Test
@Tag("smoke")
@Tag("critical")
void testLogin() {
    // Test implementation
}

// TestNG
@Test(groups = {"smoke", "critical"})
public void testLogin() {
    // Test implementation
}
```

### Priorities

```java
// TestNG
@Test(priority = 1)
public void testLogin() {
    // Test implementation
}

@Test(priority = 2)
public void testDashboard() {
    // Test implementation
}
```

## Practical Examples

### Comprehensive Test Report

```java
public class ComprehensiveTest extends BaseTest {
    private ExtentTest test;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        test = ExtentManager.createTest("Login Test");
    }
    
    @Test
    void testLogin() {
        try {
            test.log(Status.INFO, "Starting login test");
            
            test.log(Status.INFO, "Navigating to login page");
            page.navigate("https://example.com/login");
            
            test.log(Status.INFO, "Filling login form");
            page.fill("input[name='username']", "testuser");
            page.fill("input[name='password']", "password");
            
            test.log(Status.INFO, "Clicking login button");
            page.click("button[type='submit']");
            
            test.log(Status.PASS, "Login successful");
            Assertions.assertTrue(page.url().contains("dashboard"));
        } catch (Exception e) {
            test.log(Status.FAIL, "Test failed: " + e.getMessage());
            test.addScreenCaptureFromPath(
                takeScreenshot("login-failure.png"));
            throw e;
        }
    }
```

## Key Takeaways

- Use appropriate reporting frameworks (Allure, ExtentReports) for test visibility
- Implement parallel execution for faster test runs
- Use test grouping and tagging for organized test execution
- Integrate tests with CI/CD pipelines for automated testing
- Implement test retries for flaky tests
- Generate comprehensive test reports with screenshots and logs

## References

- [Allure TestOps](https://docs.qameta.io/allure/)
- [ExtentReports](https://www.extentreports.com/)
- [Playwright Test Reports](https://playwright.dev/java/docs/test-reporters)
- [JUnit 5 Parallel Execution](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parallel-execution)
- [TestNG Parallel Execution](https://testng.org/doc/documentation-main.html#parallel-running)

