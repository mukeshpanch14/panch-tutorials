# Handling Dynamic Elements and Waits - Deep Dive

## Overview

This module covers Playwright's waiting strategies for handling dynamic content, asynchronous operations, and ensuring reliable test execution. Understanding waits is crucial for writing stable, non-flaky tests.

## Auto-Waiting

### What is Auto-Waiting?

Playwright automatically waits for elements to be actionable before performing operations. This eliminates the need for explicit waits in most cases.

### Auto-Wait Conditions

Playwright automatically waits for:

1. **Element to be attached to DOM**
2. **Element to be visible**
3. **Element to be stable** (not animating)
4. **Element to receive events** (not covered by other elements)
5. **Element to be enabled**

```java
// Automatically waits for all conditions
page.click("button");  // Waits for button to be ready
page.fill("input", "text");  // Waits for input to be ready
```

### Auto-Wait Examples

```java
// Click - waits for element to be actionable
page.click("button");

// Fill - waits for input to be ready
page.fill("input[name='username']", "testuser");

// Select - waits for select to be ready
page.selectOption("select", "option1");

// Check - waits for checkbox to be ready
page.check("input[type='checkbox']");
```

## Explicit Waits

### Wait for Selector

Wait for an element to appear:

```java
// Wait for selector to be visible
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE)
        .setTimeout(30000));

// Wait for selector to be attached (not necessarily visible)
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.ATTACHED)
        .setTimeout(30000));

// Wait for selector to be hidden
page.waitForSelector(".loading-spinner", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.HIDDEN)
        .setTimeout(30000));
```

### Wait for Load State

Wait for page load states:

```java
// Wait for load event
page.waitForLoadState(LoadState.LOAD);

// Wait for DOMContentLoaded
page.waitForLoadState(LoadState.DOMCONTENTLOADED);

// Wait for network to be idle
page.waitForLoadState(LoadState.NETWORKIDLE);

// Wait for commit
page.waitForLoadState(LoadState.COMMIT);
```

### Wait for URL

Wait for URL to match a pattern:

```java
// Wait for URL
page.waitForURL("**/dashboard", 
    new Page.WaitForURLOptions().setTimeout(30000));

// Wait for URL with regex
page.waitForURL(Pattern.compile(".*dashboard.*"), 
    new Page.WaitForURLOptions().setTimeout(30000));
```

### Wait for Navigation

Wait for navigation to complete:

```java
// Wait for navigation
page.waitForNavigation(() -> {
    page.click("a");
}, new Page.WaitForNavigationOptions()
    .setWaitUntil(WaitUntilState.NETWORKIDLE)
    .setTimeout(30000));
```

### Wait for Condition

Wait for custom conditions:

```java
// Wait for custom condition
page.waitForCondition(() -> {
    return page.locator(".status").textContent().equals("Ready");
}, new Page.WaitForConditionOptions().setTimeout(30000));

// Wait for element count
page.waitForCondition(() -> {
    return page.locator(".item").count() >= 5;
}, new Page.WaitForConditionOptions().setTimeout(30000));
```

## Timeout Configuration

### Global Timeout

Set global timeout for all operations:

```java
// Set global timeout
page.setDefaultTimeout(30000);  // 30 seconds

// Set global navigation timeout
page.setDefaultNavigationTimeout(60000);  // 60 seconds
```

### Per-Action Timeout

Set timeout for specific actions:

```java
// Timeout for click
page.click("button", new Page.ClickOptions().setTimeout(10000));

// Timeout for fill
page.fill("input", "text", new Page.FillOptions().setTimeout(10000));

// Timeout for wait
page.waitForSelector(".element", 
    new Page.WaitForSelectorOptions().setTimeout(15000));
```

### Browser Context Timeout

Set timeout at browser context level:

```java
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(1920, 1080)
);

// Set default timeout for context
context.setDefaultTimeout(30000);
context.setDefaultNavigationTimeout(60000);
```

## Handling AJAX Calls

### Wait for Network Idle

Wait for all network requests to complete:

```java
// Wait for network to be idle
page.waitForLoadState(LoadState.NETWORKIDLE);

// Wait after action
page.click("button");
page.waitForLoadState(LoadState.NETWORKIDLE);
```

### Wait for Specific Request

Wait for a specific API call:

```java
// Wait for request
page.waitForRequest("**/api/users", () -> {
    page.click("button");
});

// Wait for response
page.waitForResponse("**/api/users", () -> {
    page.click("button");
});
```

### Wait for Request/Response

```java
// Wait for request
Request request = page.waitForRequest("**/api/users", () -> {
    page.click("button");
});
System.out.println("Request URL: " + request.url());

// Wait for response
Response response = page.waitForResponse("**/api/users", () -> {
    page.click("button");
});
System.out.println("Response status: " + response.status());
```

## Handling Dynamic Content

### Wait for Element to Appear

```java
// Wait for element to appear
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE)
        .setTimeout(30000));

// Then interact
page.click(".dynamic-content button");
```

### Wait for Element to Disappear

```java
// Wait for loading spinner to disappear
page.waitForSelector(".loading-spinner", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.HIDDEN)
        .setTimeout(30000));

// Then verify content
String content = page.locator(".content").textContent();
```

### Wait for Text

```java
// Wait for text to appear
page.waitForSelector("text=Welcome", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE)
        .setTimeout(30000));

// Wait for text in element
page.waitForCondition(() -> {
    return page.locator(".status").textContent().contains("Ready");
}, new Page.WaitForConditionOptions().setTimeout(30000));
```

### Wait for Element Count

```java
// Wait for specific number of elements
page.waitForCondition(() -> {
    return page.locator(".item").count() == 5;
}, new Page.WaitForConditionOptions().setTimeout(30000));
```

## Flaky Test Prevention

### Common Causes of Flaky Tests

1. **Timing issues**: Elements not ready when accessed
2. **Race conditions**: Multiple async operations
3. **Network delays**: Slow API responses
4. **Animation**: Elements still animating
5. **Dynamic content**: Content loading asynchronously

### Best Practices

#### 1. Use Auto-Waiting

```java
// Good - auto-waiting
page.click("button");  // Automatically waits

// Avoid - manual sleep
Thread.sleep(5000);
page.click("button");
```

#### 2. Wait for Navigation

```java
// Good - wait for navigation
page.click("a");
page.waitForURL("**/new-page");

// Avoid - no wait
page.click("a");
// May fail if page hasn't loaded
```

#### 3. Wait for Dynamic Content

```java
// Good - wait for content
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE));

// Avoid - immediate access
page.locator(".dynamic-content").click();  // May fail
```

#### 4. Wait for Network

```java
// Good - wait for network
page.click("button");
page.waitForLoadState(LoadState.NETWORKIDLE);

// Avoid - no wait
page.click("button");
page.locator(".result").textContent();  // May fail
```

#### 5. Use Appropriate Timeouts

```java
// Good - appropriate timeout
page.waitForSelector(".element", 
    new Page.WaitForSelectorOptions()
        .setTimeout(30000));  // 30 seconds

// Avoid - too short timeout
page.waitForSelector(".element", 
    new Page.WaitForSelectorOptions()
        .setTimeout(1000));  // May fail on slow networks
```

## Custom Wait Helpers

### Wait Helper Class

```java
public class WaitHelper {
    private final Page page;
    
    public WaitHelper(Page page) {
        this.page = page;
    }
    
    public void waitForElement(String selector, int timeout) {
        page.waitForSelector(selector, 
            new Page.WaitForSelectorOptions()
                .setState(WaitForSelectorState.VISIBLE)
                .setTimeout(timeout));
    }
    
    public void waitForText(String text, int timeout) {
        page.waitForSelector("text=" + text, 
            new Page.WaitForSelectorOptions()
                .setState(WaitForSelectorState.VISIBLE)
                .setTimeout(timeout));
    }
    
    public void waitForElementCount(String selector, int count, int timeout) {
        page.waitForCondition(() -> {
            return page.locator(selector).count() == count;
        }, new Page.WaitForConditionOptions().setTimeout(timeout));
    }
    
    public void waitForUrl(String urlPattern, int timeout) {
        page.waitForURL(urlPattern, 
            new Page.WaitForURLOptions().setTimeout(timeout));
    }
    
    public void waitForNetworkIdle() {
        page.waitForLoadState(LoadState.NETWORKIDLE);
    }
}
```

### Using Wait Helper

```java
WaitHelper waitHelper = new WaitHelper(page);

// Wait for element
waitHelper.waitForElement(".dynamic-content", 30000);

// Wait for text
waitHelper.waitForText("Welcome", 30000);

// Wait for element count
waitHelper.waitForElementCount(".item", 5, 30000);

// Wait for URL
waitHelper.waitForUrl("**/dashboard", 30000);

// Wait for network
waitHelper.waitForNetworkIdle();
```

## Practical Examples

### Login with Wait

```java
public void login(String username, String password) {
    // Wait for login form to be ready
    page.waitForSelector("form.login", 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.VISIBLE));
    
    // Fill form
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", password);
    
    // Click login
    page.click("button[type='submit']");
    
    // Wait for navigation
    page.waitForURL("**/dashboard", 
        new Page.WaitForURLOptions().setTimeout(30000));
    
    // Wait for dashboard to load
    page.waitForLoadState(LoadState.NETWORKIDLE);
}
```

### Dynamic Content Loading

```java
public void waitForDynamicContent() {
    // Click button that loads content
    page.click("button.load-content");
    
    // Wait for loading spinner to disappear
    page.waitForSelector(".loading-spinner", 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.HIDDEN)
            .setTimeout(30000));
    
    // Wait for content to appear
    page.waitForSelector(".content", 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.VISIBLE)
            .setTimeout(30000));
    
    // Verify content
    String content = page.locator(".content").textContent();
    Assertions.assertNotNull(content);
}
```

### AJAX Form Submission

```java
public void submitForm() {
    // Fill form
    page.fill("input[name='name']", "Test");
    page.fill("input[name='email']", "test@example.com");
    
    // Submit form
    page.click("button[type='submit']");
    
    // Wait for success message
    page.waitForSelector(".success-message", 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.VISIBLE)
            .setTimeout(30000));
    
    // Verify success
    String message = page.locator(".success-message").textContent();
    Assertions.assertTrue(message.contains("Success"));
}
```

## Key Takeaways

- Playwright's auto-waiting eliminates most explicit waits
- Use explicit waits for dynamic content and async operations
- Configure appropriate timeouts for different scenarios
- Wait for navigation after actions that trigger page changes
- Wait for network idle when dealing with AJAX calls
- Use custom wait helpers for common wait patterns
- Avoid Thread.sleep() - use Playwright's wait mechanisms

## References

- [Playwright Auto-waiting](https://playwright.dev/java/docs/actionability)
- [Playwright Waits](https://playwright.dev/java/docs/waits)
- [Playwright Timeouts](https://playwright.dev/java/docs/timeouts)
- [Best Practices for Waits](https://playwright.dev/java/docs/best-practices)

