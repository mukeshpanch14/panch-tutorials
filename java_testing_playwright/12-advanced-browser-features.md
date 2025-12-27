# Advanced Browser Features - Deep Dive

## Overview

This module covers advanced Playwright features including browser contexts, geolocation, permissions, device emulation, browser extensions, and JavaScript execution. These features enable testing of complex scenarios and edge cases.

## Browser Contexts

### What are Browser Contexts?

Browser contexts are isolated browser sessions. Each context has:
- Separate cookies and storage
- Independent browser history
- Isolated JavaScript execution
- Separate network activity

### Creating Contexts

```java
// Create basic context
BrowserContext context = browser.newContext();

// Create context with options
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(1920, 1080)
        .setUserAgent("Custom User Agent")
        .setLocale("en-US")
        .setTimezoneId("America/New_York")
        .setPermissions(Collections.singletonList("geolocation"))
        .setGeolocation(new Geolocation(40.7128, -74.0060))
        .setColorScheme(ColorScheme.DARK)
        .setReducedMotion(ReducedMotion.REDUCE)
        .setForcedColors(ForcedColors.NONE)
);
```

### Context Options

```java
// Viewport size
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(1920, 1080));

// User agent
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setUserAgent("Mozilla/5.0 (Custom User Agent)"));

// Locale
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setLocale("en-US"));

// Timezone
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setTimezoneId("America/New_York"));

// Color scheme
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setColorScheme(ColorScheme.DARK));

// Reduced motion
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setReducedMotion(ReducedMotion.REDUCE));
```

### Context Isolation

```java
// Example: Isolated user sessions
public void testMultipleUsers() {
    // Create context for user 1
    BrowserContext user1Context = browser.newContext();
    Page user1Page = user1Context.newPage();
    user1Page.navigate("https://example.com");
    user1Page.fill("input[name='username']", "user1");
    user1Page.fill("input[name='password']", "pass1");
    user1Page.click("button[type='submit']");
    
    // Create context for user 2
    BrowserContext user2Context = browser.newContext();
    Page user2Page = user2Context.newPage();
    user2Page.navigate("https://example.com");
    user2Page.fill("input[name='username']", "user2");
    user2Page.fill("input[name='password']", "pass2");
    user2Page.click("button[type='submit']");
    
    // Contexts are isolated - cookies don't interfere
}
```

## Geolocation and Permissions

### Setting Geolocation

```java
// Set geolocation
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setGeolocation(new Geolocation(40.7128, -74.0060))  // New York
        .setPermissions(Collections.singletonList("geolocation")));

// Update geolocation
context.setGeolocation(new Geolocation(37.7749, -122.4194));  // San Francisco
```

### Setting Permissions

```java
// Set permissions
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setPermissions(Collections.singletonList("geolocation")));

// Grant permissions for specific origin
context.setPermissions(
    Collections.singletonList("geolocation"),
    new BrowserContext.SetPermissionsOptions()
        .setOrigin("https://example.com"));

// Clear permissions
context.clearPermissions();
```

### Permission Examples

```java
// Example: Test location-based feature
public void testLocationFeature() {
    // Create context with geolocation
    BrowserContext context = browser.newContext(
        new Browser.NewContextOptions()
            .setGeolocation(new Geolocation(40.7128, -74.0060))
            .setPermissions(Collections.singletonList("geolocation")));
    
    Page page = context.newPage();
    page.navigate("https://example.com");
    
    // Test location feature
    page.click("button.get-location");
    page.waitForSelector(".location-display");
    
    String location = page.locator(".location-display").textContent();
    Assertions.assertTrue(location.contains("New York"));
}

// Example: Test notification permission
public void testNotificationPermission() {
    // Create context with notification permission
    BrowserContext context = browser.newContext(
        new Browser.NewContextOptions()
            .setPermissions(Collections.singletonList("notifications")));
    
    Page page = context.newPage();
    page.navigate("https://example.com");
    
    // Test notification
    page.click("button.enable-notifications");
    page.waitForSelector(".notification-enabled");
}
```

## Device Emulation

### Built-in Devices

```java
// Emulate iPhone
BrowserContext context = browser.newContext(
    playwright.devices().get("iPhone 12"));

// Emulate iPad
BrowserContext context = browser.newContext(
    playwright.devices().get("iPad Pro"));

// Emulate Android
BrowserContext context = browser.newContext(
    playwright.devices().get("Pixel 5"));
```

### Custom Device Emulation

```java
// Custom device emulation
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(375, 667)  // iPhone size
        .setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)")
        .setDeviceScaleFactor(2.0)
        .setIsMobile(true)
        .setHasTouch(true));
```

### Device Emulation Examples

```java
// Example: Test mobile viewport
public void testMobileView() {
    // Create mobile context
    BrowserContext context = browser.newContext(
        playwright.devices().get("iPhone 12"));
    
    Page page = context.newPage();
    page.navigate("https://example.com");
    
    // Verify mobile layout
    String viewport = page.evaluate("() => window.innerWidth + 'x' + window.innerHeight").toString();
    Assertions.assertTrue(viewport.contains("390x844"));  // iPhone 12 viewport
}

// Example: Test responsive design
public void testResponsiveDesign() {
    // Test desktop
    BrowserContext desktopContext = browser.newContext(
        new Browser.NewContextOptions()
            .setViewportSize(1920, 1080));
    Page desktopPage = desktopContext.newPage();
    desktopPage.navigate("https://example.com");
    // Verify desktop layout
    
    // Test mobile
    BrowserContext mobileContext = browser.newContext(
        playwright.devices().get("iPhone 12"));
    Page mobilePage = mobileContext.newPage();
    mobilePage.navigate("https://example.com");
    // Verify mobile layout
}
```

## Browser Extensions

### Loading Extensions

```java
// Load extension
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setExtraHTTPHeaders(Map.of("X-Extension", "enabled")));

// Note: Playwright doesn't directly support loading extensions
// Extensions need to be handled through browser launch options
```

### Extension Testing

```java
// Example: Test with extension
public void testWithExtension() {
    // Launch browser with extension
    Browser browser = playwright.chromium().launch(
        new BrowserType.LaunchOptions()
            .setArgs(Arrays.asList(
                "--disable-extensions-except=/path/to/extension",
                "--load-extension=/path/to/extension"
            )));
    
    BrowserContext context = browser.newContext();
    Page page = context.newPage();
    page.navigate("https://example.com");
    
    // Test extension functionality
}
```

## JavaScript Execution

### Evaluate JavaScript

```java
// Execute JavaScript
Object result = page.evaluate("() => document.title");

// Execute with arguments
Object result = page.evaluate("(arg) => arg * 2", 5);

// Execute and return value
String title = page.evaluate("() => document.title").toString();
```

### Evaluate Handle

```java
// Evaluate and get handle
JSHandle handle = page.evaluateHandle("() => document.body");

// Use handle
JSHandle child = handle.evaluateHandle("(element) => element.firstElementChild");
```

### JavaScript Examples

```java
// Example: Get page dimensions
public void getPageDimensions() {
    page.navigate("https://example.com");
    
    // Get viewport dimensions
    Object width = page.evaluate("() => window.innerWidth");
    Object height = page.evaluate("() => window.innerHeight");
    
    System.out.println("Viewport: " + width + "x" + height);
}

// Example: Scroll to element
public void scrollToElement(String selector) {
    page.evaluate("(selector) => {" +
        "  const element = document.querySelector(selector);" +
        "  element.scrollIntoView({ behavior: 'smooth' });" +
        "}", selector);
}

// Example: Get computed styles
public String getComputedStyle(String selector, String property) {
    return page.evaluate("(selector, property) => {" +
        "  const element = document.querySelector(selector);" +
        "  return window.getComputedStyle(element)[property];" +
        "}", selector, property).toString();
}

// Example: Execute async JavaScript
public void executeAsyncScript() {
    page.evaluate("async () => {" +
        "  await new Promise(resolve => setTimeout(resolve, 1000));" +
        "  return 'Done';" +
        "}");
}
```

## Advanced Context Features

### Storage State

```java
// Save storage state
context.storageState(new BrowserContext.StorageStateOptions()
    .setPath(Paths.get("storage-state.json")));

// Load storage state
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setStorageStatePath(Paths.get("storage-state.json")));
```

### Cookies

```java
// Get cookies
List<Cookie> cookies = context.cookies();

// Set cookies
context.addCookies(Collections.singletonList(
    new Cookie("name", "value")
        .setDomain("example.com")
        .setPath("/")
));

// Clear cookies
context.clearCookies();
```

### Local Storage

```java
// Set local storage
page.evaluate("() => localStorage.setItem('key', 'value')");

// Get local storage
String value = page.evaluate("() => localStorage.getItem('key')").toString();

// Clear local storage
page.evaluate("() => localStorage.clear()");
```

## Practical Examples

### Multi-Context Testing

```java
public class MultiContextTest {
    private Browser browser;
    
    public MultiContextTest(Browser browser) {
        this.browser = browser;
    }
    
    public void testMultipleUsers() {
        // Create contexts for different users
        BrowserContext user1Context = browser.newContext();
        BrowserContext user2Context = browser.newContext();
        
        Page user1Page = user1Context.newPage();
        Page user2Page = user2Context.newPage();
        
        // User 1 actions
        user1Page.navigate("https://example.com");
        user1Page.fill("input[name='username']", "user1");
        user1Page.fill("input[name='password']", "pass1");
        user1Page.click("button[type='submit']");
        
        // User 2 actions
        user2Page.navigate("https://example.com");
        user2Page.fill("input[name='username']", "user2");
        user2Page.fill("input[name='password']", "pass2");
        user2Page.click("button[type='submit']");
        
        // Contexts are isolated
    }
}
```

### Device Testing

```java
public class DeviceTest {
    private Browser browser;
    
    public DeviceTest(Browser browser) {
        this.browser = browser;
    }
    
    public void testMobileDevice() {
        // Emulate mobile device
        BrowserContext context = browser.newContext(
            playwright.devices().get("iPhone 12"));
        
        Page page = context.newPage();
        page.navigate("https://example.com");
        
        // Verify mobile layout
        String viewport = page.evaluate("() => window.innerWidth + 'x' + window.innerHeight").toString();
        Assertions.assertTrue(viewport.contains("390x844"));
    }
}
```

### Geolocation Testing

```java
public class GeolocationTest {
    private Browser browser;
    
    public GeolocationTest(Browser browser) {
        this.browser = browser;
    }
    
    public void testLocationFeature() {
        // Create context with geolocation
        BrowserContext context = browser.newContext(
            new Browser.NewContextOptions()
                .setGeolocation(new Geolocation(40.7128, -74.0060))
                .setPermissions(Collections.singletonList("geolocation")));
        
        Page page = context.newPage();
        page.navigate("https://example.com");
        
        // Test location feature
        page.click("button.get-location");
        page.waitForSelector(".location-display");
        
        String location = page.locator(".location-display").textContent();
        Assertions.assertTrue(location.contains("New York"));
    }
}
```

## Best Practices

### 1. Use Contexts for Isolation

```java
// Good - isolated contexts
BrowserContext user1Context = browser.newContext();
BrowserContext user2Context = browser.newContext();

// Avoid - shared context
Page user1Page = page.context().newPage();
Page user2Page = page.context().newPage();  // Shared cookies
```

### 2. Clean Up Contexts

```java
// Good - clean up
@AfterEach
void tearDown() {
    if (context != null) {
        context.close();
    }
}

// Avoid - resource leak
```

### 3. Use Device Emulation for Mobile Testing

```java
// Good - device emulation
BrowserContext context = browser.newContext(
    playwright.devices().get("iPhone 12"));

// Avoid - manual viewport setting
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(375, 667));  // May not match device exactly
```

### 4. Set Permissions Explicitly

```java
// Good - explicit permissions
BrowserContext context = browser.newContext(
    new Browser.NewContextOptions()
        .setPermissions(Collections.singletonList("geolocation")));

// Avoid - relying on default permissions
```

## Key Takeaways

- Browser contexts provide isolation for parallel testing
- Geolocation and permissions enable testing of location-based features
- Device emulation allows testing on different devices
- JavaScript execution enables advanced interactions
- Storage state can be saved and loaded for faster test setup
- Always clean up contexts to avoid resource leaks

## References

- [Playwright Browser Contexts](https://playwright.dev/java/docs/browser-contexts)
- [Playwright Devices](https://playwright.dev/java/docs/emulation)
- [Playwright Geolocation](https://playwright.dev/java/docs/emulation#geolocation)
- [Playwright JavaScript Execution](https://playwright.dev/java/docs/evaluating)

