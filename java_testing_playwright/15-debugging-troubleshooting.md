# Debugging and Troubleshooting - Deep Dive

## Overview

This module covers debugging techniques, troubleshooting common issues, and tools available in Playwright for identifying and fixing test failures. Understanding these concepts is crucial for maintaining stable and reliable tests.

## Playwright Inspector

### Enabling Inspector

```bash
# Set environment variable
export PWDEBUG=1

# Or run with debug flag
mvn test -DPWDEBUG=1
```

### Using Inspector

```java
// Run with inspector
// Set environment variable: PWDEBUG=1
// Playwright will open inspector automatically

// Or use in code
page.pause();  // Pauses execution and opens inspector
```

### Inspector Features

- **Step-through debugging**: Step through each action
- **Selector inspection**: Click on elements to see selectors
- **Console access**: Execute JavaScript in browser console
- **Network monitoring**: View network requests and responses
- **Timeline view**: See execution timeline

## Trace Viewer

### Recording Traces

```java
// Start trace recording
BrowserContext context = browser.newContext();
context.tracing().start(new Tracing.StartOptions()
    .setScreenshots(true)
    .setSnapshots(true)
    .setSources(true));

// Test execution
page.navigate("https://example.com");
page.click("button");
page.fill("input", "text");

// Stop trace recording
context.tracing().stop(new Tracing.StopOptions()
    .setPath(Paths.get("trace.zip")));
```

### Viewing Traces

```bash
# Open trace viewer
npx playwright show-trace trace.zip

# Or in code
playwright.showTrace(Paths.get("trace.zip"));
```

### Trace Options

```java
// Configure trace options
context.tracing().start(new Tracing.StartOptions()
    .setScreenshots(true)      // Capture screenshots
    .setSnapshots(true)        // Capture DOM snapshots
    .setSources(true)          // Capture source code
    .setScreenshotOnlyOnFailure(true));  // Screenshots only on failure
```

## Console Logging

### Page Console Logs

```java
// Listen to console logs
page.onConsoleMessage(msg -> {
    System.out.println("Console: " + msg.text());
});

// Listen to specific log levels
page.onConsoleMessage(msg -> {
    if (msg.type().equals("error")) {
        System.out.println("Error: " + msg.text());
    }
});
```

### Network Logging

```java
// Listen to requests
page.onRequest(request -> {
    System.out.println("Request: " + request.method() + " " + request.url());
});

// Listen to responses
page.onResponse(response -> {
    System.out.println("Response: " + response.status() + " " + response.url());
    if (response.status() >= 400) {
        System.out.println("Error response: " + response.text());
    }
});
```

### Page Errors

```java
// Listen to page errors
page.onPageError(error -> {
    System.out.println("Page error: " + error.message());
});

// Listen to requests failed
page.onRequestFailed(request -> {
    System.out.println("Request failed: " + request.url());
    System.out.println("Failure: " + request.failure().errorText());
});
```

## Screenshot on Failure

### Automatic Screenshots

```java
// Take screenshot on failure
@AfterEach
void tearDown(TestInfo testInfo) {
    if (testInfo.getTags().contains("failed")) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("screenshots/" + testInfo.getDisplayName() + ".png"))
            .setFullPage(true));
    }
    context.close();
}
```

### Screenshot Helper

```java
public class ScreenshotHelper {
    private Page page;
    
    public ScreenshotHelper(Page page) {
        this.page = page;
    }
    
    public void screenshotOnFailure(String testName, Throwable error) {
        try {
            page.screenshot(new Page.ScreenshotOptions()
                .setPath(Paths.get("screenshots/" + testName + "-failure.png"))
                .setFullPage(true));
        } catch (Exception e) {
            System.err.println("Failed to take screenshot: " + e.getMessage());
        }
    }
}
```

## Common Issues

### Element Not Found

#### Issue

```java
// Element not found error
page.click("button");  // TimeoutException: Element not found
```

#### Solutions

```java
// Solution 1: Wait for element
page.waitForSelector("button", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE));
page.click("button");

// Solution 2: Use auto-waiting
page.click("button");  // Automatically waits

// Solution 3: Check element existence
if (page.locator("button").count() > 0) {
    page.click("button");
}

// Solution 4: Use more specific selector
page.click("button[type='submit'][data-testid='submit']");
```

### Timing Issues

#### Issue

```java
// Element not ready when accessed
page.click("button");
page.locator(".result").textContent();  // TimeoutException
```

#### Solutions

```java
// Solution 1: Wait for navigation
page.click("button");
page.waitForURL("**/dashboard");

// Solution 2: Wait for load state
page.click("button");
page.waitForLoadState(LoadState.NETWORKIDLE);

// Solution 3: Wait for element
page.click("button");
page.waitForSelector(".result", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE));

// Solution 4: Wait for custom condition
page.click("button");
page.waitForCondition(() -> {
    return page.locator(".result").textContent() != null;
});
```

### Flaky Tests

#### Issue

```java
// Test passes sometimes, fails other times
page.click("button");
String result = page.locator(".result").textContent();
```

#### Solutions

```java
// Solution 1: Use auto-waiting
page.click("button");  // Automatically waits
String result = page.locator(".result").textContent();

// Solution 2: Increase timeout
page.waitForSelector(".result", 
    new Page.WaitForSelectorOptions()
        .setTimeout(60000));  // 60 seconds

// Solution 3: Wait for stable state
page.click("button");
page.waitForLoadState(LoadState.NETWORKIDLE);
page.waitForSelector(".result");

// Solution 4: Retry logic
int maxRetries = 3;
for (int i = 0; i < maxRetries; i++) {
    try {
        page.click("button");
        page.waitForSelector(".result");
        break;
    } catch (Exception e) {
        if (i == maxRetries - 1) throw e;
        Thread.sleep(1000);
    }
}
```

### Selector Issues

#### Issue

```java
// Selector matches multiple elements
page.click("button");  // AmbiguousLocatorError
```

#### Solutions

```java
// Solution 1: Use more specific selector
page.click("button[type='submit'][data-testid='login']");

// Solution 2: Use first() or last()
page.locator("button").first().click();

// Solution 3: Use text-based locator
page.getByText("Submit").click();

// Solution 4: Use role-based locator
page.getByRole(AriaRole.BUTTON, 
    new Page.GetByRoleOptions().setName("Submit")).click();
```

## Debugging Techniques

### Debug Mode

```java
// Run with debug mode
// Set environment variable: DEBUG=pw:api

// Or in code
Browser browser = playwright.chromium().launch(
    new BrowserType.LaunchOptions()
        .setHeadless(false)  // Show browser
        .setSlowMo(1000));   // Slow down actions
```

### Breakpoints

```java
// Pause execution
page.pause();  // Opens inspector

// Or use debugger statement
page.evaluate("debugger;");
```

### Logging

```java
// Add logging
System.out.println("Navigating to page");
page.navigate("https://example.com");

System.out.println("Filling form");
page.fill("input", "text");

System.out.println("Clicking button");
page.click("button");
```

### Network Debugging

```java
// Monitor network activity
page.onRequest(request -> {
    System.out.println(">>> " + request.method() + " " + request.url());
});

page.onResponse(response -> {
    System.out.println("<<< " + response.status() + " " + response.url());
});

page.onRequestFailed(request -> {
    System.out.println("FAIL " + request.url() + " " + request.failure().errorText());
});
```

## Troubleshooting Checklist

### Before Debugging

1. **Check browser version**: Ensure Playwright browsers are up to date
2. **Check selectors**: Verify selectors are correct and unique
3. **Check timing**: Ensure elements are loaded before interaction
4. **Check network**: Verify network requests are completing
5. **Check logs**: Review console and network logs

### During Debugging

1. **Enable inspector**: Use `PWDEBUG=1` or `page.pause()`
2. **Record trace**: Enable trace recording for detailed analysis
3. **Take screenshots**: Capture screenshots at key points
4. **Monitor network**: Watch network requests and responses
5. **Check console**: Review browser console for errors

### After Debugging

1. **Fix root cause**: Address the underlying issue
2. **Add waits**: Add appropriate waits if needed
3. **Improve selectors**: Use more stable selectors
4. **Add logging**: Add logging for future debugging
5. **Document solution**: Document the fix for future reference

## Practical Examples

### Debugging Test Failure

```java
public class DebuggingExample {
    private Page page;
    
    public DebuggingExample(Page page) {
        this.page = page;
    }
    
    public void debugTest() {
        try {
            // Enable logging
            page.onConsoleMessage(msg -> {
                System.out.println("Console: " + msg.text());
            });
            
            page.onRequest(request -> {
                System.out.println("Request: " + request.url());
            });
            
            page.onResponse(response -> {
                System.out.println("Response: " + response.status() + " " + response.url());
            });
            
            // Navigate
            System.out.println("Navigating to page");
            page.navigate("https://example.com");
            
            // Wait for element
            System.out.println("Waiting for button");
            page.waitForSelector("button", 
                new Page.WaitForSelectorOptions()
                    .setState(WaitForSelectorState.VISIBLE)
                    .setTimeout(30000));
            
            // Click
            System.out.println("Clicking button");
            page.click("button");
            
            // Wait for result
            System.out.println("Waiting for result");
            page.waitForSelector(".result", 
                new Page.WaitForSelectorOptions()
                    .setState(WaitForSelectorState.VISIBLE)
                    .setTimeout(30000));
            
            // Verify
            String result = page.locator(".result").textContent();
            System.out.println("Result: " + result);
            Assertions.assertNotNull(result);
            
        } catch (Exception e) {
            // Take screenshot on failure
            page.screenshot(new Page.ScreenshotOptions()
                .setPath(Paths.get("screenshots/debug-failure.png"))
                .setFullPage(true));
            throw e;
        }
    }
}
```

### Trace Recording Example

```java
public class TraceExample extends BaseTest {
    @Test
    void testWithTrace() {
        // Start trace
        context.tracing().start(new Tracing.StartOptions()
            .setScreenshots(true)
            .setSnapshots(true)
            .setSources(true));
        
        try {
            // Test execution
            page.navigate("https://example.com");
            page.click("button");
            page.fill("input", "text");
            
        } finally {
            // Stop trace
            context.tracing().stop(new Tracing.StopOptions()
                .setPath(Paths.get("trace.zip")));
        }
    }
}
```

## Key Takeaways

- Use Playwright Inspector for step-through debugging
- Record traces for detailed test execution analysis
- Enable console and network logging for visibility
- Take screenshots on failure for debugging
- Address common issues systematically
- Use appropriate waits and selectors
- Document solutions for future reference

## References

- [Playwright Debugging](https://playwright.dev/java/docs/debug)
- [Playwright Trace Viewer](https://playwright.dev/java/docs/trace-viewer)
- [Playwright Inspector](https://playwright.dev/java/docs/debug#playwright-inspector)
- [Troubleshooting Guide](https://playwright.dev/java/docs/troubleshooting)

