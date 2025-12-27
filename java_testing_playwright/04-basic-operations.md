# Basic Playwright Operations - Deep Dive

## Overview

This module covers the fundamental Playwright operations for interacting with web pages, including navigation, element location, user interactions, and reading page content.

## Navigation

### Basic Navigation

Navigate to a URL:

```java
// Navigate to a URL
page.navigate("https://example.com");

// Navigate with options
page.navigate("https://example.com", new Page.NavigateOptions()
    .setWaitUntil(WaitUntilState.NETWORKIDLE)
    .setTimeout(60000));
```

### Navigation States

Playwright supports different wait states:

```java
// Wait for load event (default)
page.navigate("https://example.com", 
    new Page.NavigateOptions().setWaitUntil(WaitUntilState.LOAD));

// Wait for DOMContentLoaded
page.navigate("https://example.com", 
    new Page.NavigateOptions().setWaitUntil(WaitUntilState.DOMCONTENTLOADED));

// Wait for network to be idle
page.navigate("https://example.com", 
    new Page.NavigateOptions().setWaitUntil(WaitUntilState.NETWORKIDLE));

// Wait for commit (fastest)
page.navigate("https://example.com", 
    new Page.NavigateOptions().setWaitUntil(WaitUntilState.COMMIT));
```

### Browser History

Navigate through browser history:

```java
// Go back
page.goBack();

// Go forward
page.goForward();

// Reload page
page.reload();

// Reload with options
page.reload(new Page.ReloadOptions()
    .setWaitUntil(WaitUntilState.NETWORKIDLE));
```

## Locators

### What are Locators?

Locators are Playwright's way of finding elements on a page. They automatically wait for elements to be actionable.

### Basic Locators

```java
// CSS selector
Locator button = page.locator("button");

// ID selector
Locator element = page.locator("#myId");

// Class selector
Locator element = page.locator(".myClass");

// Attribute selector
Locator element = page.locator("[data-testid='submit']");

// XPath
Locator element = page.locator("xpath=//button[@type='submit']");
```

### Text-Based Locators

```java
// Get by text (exact match)
Locator element = page.getByText("Click me");

// Get by text (partial match)
Locator element = page.getByText("Click", new Page.GetByTextOptions()
    .setExact(false));

// Get by label
Locator element = page.getByLabel("Username");

// Get by placeholder
Locator element = page.getByPlaceholder("Enter username");

// Get by role
Locator button = page.getByRole(AriaRole.BUTTON, 
    new Page.GetByRoleOptions().setName("Submit"));
```

### Chaining Locators

```java
// Chain locators
Locator element = page.locator("div.container")
    .locator("button")
    .getByText("Submit");

// Filter locators
Locator visibleButton = page.locator("button")
    .filter(new Locator.FilterOptions().setHasText("Click"));
```

## Element Interactions

### Clicking Elements

```java
// Simple click
page.click("button");

// Click with options
page.click("button", new Page.ClickOptions()
    .setButton(MouseButton.RIGHT)  // Right click
    .setClickCount(2)               // Double click
    .setDelay(100));                // Delay between mousedown and mouseup

// Force click (bypass actionability checks)
page.click("button", new Page.ClickOptions().setForce(true));
```

### Filling Input Fields

```java
// Fill input field
page.fill("input[name='username']", "testuser");

// Type with delay (simulates human typing)
page.type("input[name='username']", "testuser", 
    new Page.TypeOptions().setDelay(100));

// Clear and fill
page.fill("input[name='username']", "");  // Clear
page.fill("input[name='username']", "newuser");  // Fill
```

### Keyboard Actions

```java
// Press a key
page.press("input", "Enter");

// Press key combination
page.keyboard().press("Control+A");
page.keyboard().press("Control+C");

// Type text
page.keyboard().type("Hello World");

// Press and hold
page.keyboard().down("Shift");
page.keyboard().press("ArrowRight");
page.keyboard().up("Shift");
```

### Mouse Actions

```java
// Hover over element
page.hover("button");

// Drag and drop
page.dragAndDrop("#source", "#target");

// Mouse move
page.mouse().move(100, 100);

// Mouse click
page.mouse().click(100, 100);

// Mouse double click
page.mouse().dblclick(100, 100);
```

## Reading Values

### Text Content

```java
// Get text content (includes hidden text)
String text = page.locator("div").textContent();

// Get inner text (only visible text)
String text = page.locator("div").innerText();

// Get all text content
List<String> texts = page.locator("div").allTextContents();
```

### Attributes

```java
// Get attribute value
String href = page.locator("a").getAttribute("href");

// Get all attributes
String id = page.locator("div").getAttribute("id");
String className = page.locator("div").getAttribute("class");
```

### Input Values

```java
// Get input value
String value = page.locator("input[name='username']").inputValue();

// Get checkbox state
boolean checked = page.locator("input[type='checkbox']").isChecked();

// Get select value
String selectedValue = page.locator("select").inputValue();
```

### Page Information

```java
// Get page title
String title = page.title();

// Get page URL
String url = page.url();

// Get page content
String content = page.content();
```

## Waiting Strategies

### Auto-Waiting

Playwright automatically waits for elements to be actionable:

```java
// Automatically waits for:
// - Element to be attached to DOM
// - Element to be visible
// - Element to be stable
// - Element to receive events
// - Element to be enabled

page.click("button");  // Auto-waits for button to be ready
```

### Explicit Waits

Wait for specific conditions:

```java
// Wait for selector
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE)
        .setTimeout(30000));

// Wait for load state
page.waitForLoadState(LoadState.NETWORKIDLE);

// Wait for URL
page.waitForURL("**/dashboard", 
    new Page.WaitForURLOptions().setTimeout(30000));

// Wait for navigation
page.waitForNavigation(() -> {
    page.click("a");
});
```

### Custom Wait Conditions

```java
// Wait for custom condition
page.waitForCondition(() -> {
    return page.locator(".status").textContent().equals("Ready");
}, new Page.WaitForConditionOptions().setTimeout(30000));
```

## Complete Example

### Login Test

```java
import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

public class LoginTest {
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
    void testLogin() {
        // Navigate to login page
        page.navigate("https://example.com/login");
        
        // Fill username
        page.fill("input[name='username']", "testuser");
        
        // Fill password
        page.fill("input[name='password']", "password123");
        
        // Click login button
        page.click("button[type='submit']");
        
        // Wait for navigation
        page.waitForURL("**/dashboard");
        
        // Verify login success
        String title = page.title();
        Assertions.assertTrue(title.contains("Dashboard"));
        
        // Verify user is logged in
        String welcomeText = page.locator(".welcome-message").textContent();
        Assertions.assertTrue(welcomeText.contains("testuser"));
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

## Best Practices

### 1. Use Text-Based Locators

Prefer text-based locators when possible:

```java
// Good - text-based locator
page.getByText("Submit").click();

// Avoid - fragile CSS selector
page.click("button.btn-primary:nth-child(2)");
```

### 2. Use Data Attributes

Use data-testid for stable selectors:

```java
// Good - stable selector
page.locator("[data-testid='submit-button']").click();

// Avoid - class-based selector (can change)
page.locator(".btn-submit").click();
```

### 3. Wait for Navigation

Always wait for navigation after actions that trigger navigation:

```java
// Good - wait for navigation
page.click("a");
page.waitForURL("**/new-page");

// Avoid - no wait
page.click("a");
// May fail if page hasn't loaded yet
```

### 4. Use Locator Objects

Store locators in variables for reuse:

```java
// Good - reusable locator
Locator submitButton = page.locator("button[type='submit']");
submitButton.click();
submitButton.isVisible();

// Avoid - repeated selector
page.click("button[type='submit']");
page.locator("button[type='submit']").isVisible();
```

### 5. Handle Dynamic Content

Wait for dynamic content to load:

```java
// Wait for dynamic content
page.waitForSelector(".dynamic-content", 
    new Page.WaitForSelectorOptions()
        .setState(WaitForSelectorState.VISIBLE));

// Then interact
page.click(".dynamic-content button");
```

## Common Patterns

### Form Filling

```java
public void fillForm(String username, String email, String password) {
    page.fill("input[name='username']", username);
    page.fill("input[name='email']", email);
    page.fill("input[name='password']", password);
    page.click("button[type='submit']");
}
```

### Element Visibility Check

```java
public boolean isElementVisible(String selector) {
    try {
        return page.locator(selector).isVisible();
    } catch (Exception e) {
        return false;
    }
}
```

### Wait for Text

```java
public void waitForText(String text) {
    page.waitForSelector("text=" + text, 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.VISIBLE));
}
```

## Key Takeaways

- Navigation supports different wait states for optimal performance
- Locators automatically wait for elements to be actionable
- Text-based locators are more maintainable than CSS selectors
- Always wait for navigation after actions that trigger page changes
- Use data-testid attributes for stable selectors
- Store locators in variables for reuse and better readability

## References

- [Playwright Locators](https://playwright.dev/java/docs/locators)
- [Playwright Actions](https://playwright.dev/java/docs/input)
- [Playwright Navigation](https://playwright.dev/java/docs/navigations)
- [Playwright Auto-waiting](https://playwright.dev/java/docs/actionability)
