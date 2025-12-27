# Working with Frames, Windows, and Tabs - Deep Dive

## Overview

This module covers handling complex browser scenarios involving iframes, multiple windows, tabs, and browser contexts in Playwright. Understanding these concepts is essential for testing modern web applications.

## Frames

### What are Frames?

Frames (iframes) are HTML documents embedded within another HTML document. They create isolated document contexts that require special handling.

### Accessing Frames

```java
// Get frame by name
Frame frame = page.frame("frame-name");

// Get frame by URL
Frame frame = page.frameByUrl("**/frame.html");

// Get frame by URL pattern
Frame frame = page.frameByUrl(Pattern.compile(".*frame.*"));

// Get all frames
List<Frame> frames = page.frames();
```

### Interacting with Frames

```java
// Access frame
Frame frame = page.frame("frame-name");

// Interact with frame elements
frame.click("button");
frame.fill("input", "text");
frame.locator(".element").click();

// Get frame content
String content = frame.content();

// Get frame URL
String url = frame.url();
```

### Nested Frames

```java
// Access nested frames
Frame parentFrame = page.frame("parent-frame");
Frame childFrame = parentFrame.childFrames().get(0);

// Interact with nested frame
childFrame.click("button");
```

### Frame Examples

```java
// Example: Login in iframe
public void loginInFrame(String username, String password) {
    // Access frame
    Frame loginFrame = page.frame("login-frame");
    
    // Interact with frame elements
    loginFrame.fill("input[name='username']", username);
    loginFrame.fill("input[name='password']", password);
    loginFrame.click("button[type='submit']");
    
    // Wait for navigation in frame
    loginFrame.waitForURL("**/dashboard");
}

// Example: Switch between frames
public void switchFrames() {
    // Access first frame
    Frame frame1 = page.frame("frame1");
    frame1.click("button");
    
    // Access second frame
    Frame frame2 = page.frame("frame2");
    frame2.fill("input", "text");
}
```

## Windows and Tabs

### What are Windows and Tabs?

Windows and tabs are separate browser contexts that can be opened from the main page. They require special handling to switch between them.

### Handling New Windows

```java
// Wait for new page/window
Page newPage = page.context().waitForPage(() -> {
    page.click("a[target='_blank']");
});

// Wait for new page with options
Page newPage = page.context().waitForPage(
    new BrowserContext.WaitForPageOptions().setTimeout(30000),
    () -> {
        page.click("a[target='_blank']");
    }
);

// Interact with new page
newPage.waitForLoadState();
String title = newPage.title();
newPage.click("button");
```

### Handling Multiple Windows

```java
// Get all pages in context
List<Page> pages = page.context().pages();

// Get current page
Page currentPage = page;

// Get new page
Page newPage = pages.get(pages.size() - 1);

// Switch between pages
newPage.bringToFront();  // Bring to front
currentPage.bringToFront();  // Switch back
```

### Window Examples

```java
// Example: Open link in new tab
public void openLinkInNewTab() {
    // Get initial page count
    int initialPageCount = page.context().pages().size();
    
    // Open link in new tab
    Page newPage = page.context().waitForPage(() -> {
        page.click("a[target='_blank']");
    });
    
    // Wait for new page to load
    newPage.waitForLoadState();
    
    // Interact with new page
    String title = newPage.title();
    System.out.println("New page title: " + title);
    
    // Close new page
    newPage.close();
}

// Example: Switch between windows
public void switchWindows() {
    // Open first window
    Page page1 = page.context().newPage();
    page1.navigate("https://example.com/page1");
    
    // Open second window
    Page page2 = page.context().newPage();
    page2.navigate("https://example.com/page2");
    
    // Switch to first window
    page1.bringToFront();
    page1.click("button");
    
    // Switch to second window
    page2.bringToFront();
    page2.fill("input", "text");
}
```

## Browser Contexts

### What are Browser Contexts?

Browser contexts are isolated browser sessions. Each context has:
- Separate cookies and storage
- Independent browser history
- Isolated JavaScript execution
- Separate network activity

### Creating Contexts

```java
// Create new context
BrowserContext context1 = browser.newContext();

// Create context with options
BrowserContext context2 = browser.newContext(
    new Browser.NewContextOptions()
        .setViewportSize(1920, 1080)
        .setUserAgent("Custom User Agent")
);

// Create page in context
Page page1 = context1.newPage();
Page page2 = context2.newPage();
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
    
    // Each context is isolated - cookies don't interfere
}
```

### Context Management

```java
// Get all contexts
List<BrowserContext> contexts = browser.contexts();

// Get pages in context
List<Page> pages = context.pages();

// Close context
context.close();

// Close all pages in context
for (Page page : context.pages()) {
    page.close();
}
```

## Practical Examples

### Frame Handling

```java
public class FrameTest {
    private Page page;
    
    public FrameTest(Page page) {
        this.page = page;
    }
    
    public void interactWithFrame() {
        // Navigate to page with frame
        page.navigate("https://example.com/page-with-frame");
        
        // Wait for frame to load
        page.waitForSelector("iframe");
        
        // Access frame
        Frame frame = page.frame("frame-name");
        
        // Wait for frame content
        frame.waitForLoadState();
        
        // Interact with frame
        frame.fill("input[name='username']", "testuser");
        frame.fill("input[name='password']", "password");
        frame.click("button[type='submit']");
        
        // Wait for frame navigation
        frame.waitForURL("**/dashboard");
    }
    
    public void handleNestedFrames() {
        // Access parent frame
        Frame parentFrame = page.frame("parent-frame");
        
        // Access child frame
        List<Frame> childFrames = parentFrame.childFrames();
        Frame childFrame = childFrames.get(0);
        
        // Interact with child frame
        childFrame.click("button");
    }
}
```

### Window Handling

```java
public class WindowTest {
    private Page page;
    
    public WindowTest(Page page) {
        this.page = page;
    }
    
    public void handleNewWindow() {
        // Get initial page
        Page initialPage = page;
        
        // Open link in new window
        Page newPage = page.context().waitForPage(() -> {
            page.click("a[target='_blank']");
        });
        
        // Wait for new page to load
        newPage.waitForLoadState();
        
        // Interact with new page
        String title = newPage.title();
        newPage.click("button");
        
        // Switch back to initial page
        initialPage.bringToFront();
        initialPage.click("button");
        
        // Close new page
        newPage.close();
    }
    
    public void handleMultipleWindows() {
        // Open multiple windows
        Page page1 = page.context().newPage();
        page1.navigate("https://example.com/page1");
        
        Page page2 = page.context().newPage();
        page2.navigate("https://example.com/page2");
        
        // Switch between windows
        page1.bringToFront();
        page1.click("button");
        
        page2.bringToFront();
        page2.fill("input", "text");
        
        // Close windows
        page1.close();
        page2.close();
    }
}
```

### Context Handling

```java
public class ContextTest {
    private Browser browser;
    
    public ContextTest(Browser browser) {
        this.browser = browser;
    }
    
    public void testMultipleContexts() {
        // Create context 1
        BrowserContext context1 = browser.newContext();
        Page page1 = context1.newPage();
        page1.navigate("https://example.com");
        page1.fill("input[name='username']", "user1");
        
        // Create context 2
        BrowserContext context2 = browser.newContext();
        Page page2 = context2.newPage();
        page2.navigate("https://example.com");
        page2.fill("input[name='username']", "user2");
        
        // Contexts are isolated - no interference
        String username1 = page1.locator("input[name='username']").inputValue();
        String username2 = page2.locator("input[name='username']").inputValue();
        
        Assertions.assertEquals("user1", username1);
        Assertions.assertEquals("user2", username2);
        
        // Cleanup
        context1.close();
        context2.close();
    }
}
```

## Best Practices

### 1. Wait for Frames

Always wait for frames to load before interacting:

```java
// Good - wait for frame
page.waitForSelector("iframe");
Frame frame = page.frame("frame-name");
frame.waitForLoadState();

// Avoid - immediate access
Frame frame = page.frame("frame-name");
frame.click("button");  // May fail if frame not loaded
```

### 2. Wait for New Windows

Always wait for new windows to open:

```java
// Good - wait for new page
Page newPage = page.context().waitForPage(() -> {
    page.click("a[target='_blank']");
});

// Avoid - immediate access
page.click("a[target='_blank']");
Page newPage = page.context().pages().get(1);  // May not exist yet
```

### 3. Close Resources

Always close contexts and pages:

```java
// Good - cleanup
@AfterEach
void tearDown() {
    for (Page page : context.pages()) {
        page.close();
    }
    context.close();
}

// Avoid - resource leak
// Pages and contexts remain open
```

### 4. Use Contexts for Isolation

Use separate contexts for isolated test scenarios:

```java
// Good - isolated contexts
BrowserContext user1Context = browser.newContext();
BrowserContext user2Context = browser.newContext();

// Avoid - shared context
Page user1Page = page.context().newPage();
Page user2Page = page.context().newPage();  // Shared cookies
```

### 5. Bring Pages to Front

Bring pages to front when switching:

```java
// Good - bring to front
page1.bringToFront();
page1.click("button");

// Avoid - may not be focused
page1.click("button");  // May fail if not focused
```

## Common Patterns

### Frame Helper

```java
public class FrameHelper {
    private Page page;
    
    public FrameHelper(Page page) {
        this.page = page;
    }
    
    public Frame getFrame(String frameName) {
        page.waitForSelector("iframe");
        return page.frame(frameName);
    }
    
    public void interactWithFrame(String frameName, String selector) {
        Frame frame = getFrame(frameName);
        frame.waitForLoadState();
        frame.click(selector);
    }
}
```

### Window Helper

```java
public class WindowHelper {
    private Page page;
    
    public WindowHelper(Page page) {
        this.page = page;
    }
    
    public Page openLinkInNewTab(String selector) {
        Page newPage = page.context().waitForPage(() -> {
            page.click(selector);
        });
        newPage.waitForLoadState();
        return newPage;
    }
    
    public void switchToPage(Page targetPage) {
        targetPage.bringToFront();
    }
}
```

## Key Takeaways

- Frames require special handling to access and interact with
- New windows/tabs must be waited for before interaction
- Browser contexts provide isolation for parallel testing
- Always wait for frames and windows to load
- Close resources properly to avoid leaks
- Use contexts for isolated test scenarios
- Bring pages to front when switching between them

## References

- [Playwright Frames](https://playwright.dev/java/docs/frames)
- [Playwright Browser Contexts](https://playwright.dev/java/docs/browser-contexts)
- [Playwright Pages](https://playwright.dev/java/docs/pages)
- [Multi-page Scenarios](https://playwright.dev/java/docs/multi-pages)

