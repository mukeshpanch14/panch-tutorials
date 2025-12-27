# Advanced Locator Strategies - Deep Dive

## Overview

This module covers advanced locator strategies in Playwright, including CSS selectors, XPath, text-based locators, chaining, and best practices for reliable element identification.

## CSS Selectors

### Basic CSS Selectors

```java
// Element selector
Locator element = page.locator("div");

// ID selector
Locator element = page.locator("#myId");

// Class selector
Locator element = page.locator(".myClass");

// Attribute selector
Locator element = page.locator("[data-testid='submit']");

// Multiple classes
Locator element = page.locator(".btn.primary.large");
```

### Advanced CSS Selectors

```java
// Descendant selector
Locator element = page.locator("div.container button");

// Child selector
Locator element = page.locator("div > button");

// Adjacent sibling
Locator element = page.locator("h1 + p");

// General sibling
Locator element = page.locator("h1 ~ p");

// Pseudo-classes
Locator element = page.locator("button:hover");
Locator element = page.locator("input:focus");
Locator element = page.locator("li:first-child");
Locator element = page.locator("li:last-child");
Locator element = page.locator("li:nth-child(2)");

// Not selector
Locator element = page.locator("button:not(.disabled)");

// Contains text
Locator element = page.locator("div:has-text('Hello')");
```

### CSS Selector Best Practices

```java
// Good - specific and stable
page.locator("[data-testid='submit-button']");

// Good - semantic selector
page.locator("button[type='submit']");

// Avoid - too generic
page.locator("button");

// Avoid - fragile (depends on structure)
page.locator("div > div > div > button");
```

## XPath Selectors

### Basic XPath

```java
// Element selector
Locator element = page.locator("xpath=//button");

// Absolute path
Locator element = page.locator("xpath=/html/body/div/button");

// Relative path
Locator element = page.locator("xpath=//div//button");

// Attribute selector
Locator element = page.locator("xpath=//button[@type='submit']");

// Text content
Locator element = page.locator("xpath=//button[text()='Submit']");

// Contains text
Locator element = page.locator("xpath=//button[contains(text(), 'Submit')]");
```

### Advanced XPath

```java
// Multiple attributes
Locator element = page.locator("xpath=//button[@type='submit' and @class='primary']");

// Parent element
Locator element = page.locator("xpath=//button[@type='submit']/parent::div");

// Following sibling
Locator element = page.locator("xpath=//h1/following-sibling::p");

// Preceding sibling
Locator element = page.locator("xpath=//p/preceding-sibling::h1");

// Ancestor
Locator element = page.locator("xpath=//button/ancestor::div[@class='container']");

// Position
Locator element = page.locator("xpath=//li[1]");  // First
Locator element = page.locator("xpath=//li[last()]");  // Last
Locator element = page.locator("xpath=//li[position()>2]");  // After second
```

### XPath Best Practices

```java
// Good - relative and specific
page.locator("xpath=//button[@data-testid='submit']");

// Good - text-based
page.locator("xpath=//button[contains(text(), 'Submit')]");

// Avoid - absolute path (fragile)
page.locator("xpath=/html/body/div[2]/div[3]/button[1]");

// Avoid - position-based (fragile)
page.locator("xpath=//div[3]/button[2]");
```

## Text-Based Locators

### GetByText

```java
// Exact text match
Locator element = page.getByText("Submit");

// Partial text match
Locator element = page.getByText("Submit", 
    new Page.GetByTextOptions().setExact(false));

// Case-insensitive
Locator element = page.getByText("submit", 
    new Page.GetByTextOptions().setExact(false));
```

### GetByLabel

```java
// By label text
Locator element = page.getByLabel("Username");

// By label with options
Locator element = page.getByLabel("Username", 
    new Page.GetByLabelOptions().setExact(false));
```

### GetByPlaceholder

```java
// By placeholder text
Locator element = page.getByPlaceholder("Enter username");

// Partial match
Locator element = page.getByPlaceholder("username", 
    new Page.GetByPlaceholderOptions().setExact(false));
```

### GetByRole

```java
// By role
Locator button = page.getByRole(AriaRole.BUTTON);

// By role and name
Locator button = page.getByRole(AriaRole.BUTTON, 
    new Page.GetByRoleOptions().setName("Submit"));

// By role and options
Locator button = page.getByRole(AriaRole.BUTTON, 
    new Page.GetByRoleOptions()
        .setName("Submit")
        .setExact(false));

// Common roles
page.getByRole(AriaRole.BUTTON);
page.getByRole(AriaRole.LINK);
page.getByRole(AriaRole.TEXTBOX);
page.getByRole(AriaRole.CHECKBOX);
page.getByRole(AriaRole.RADIO);
page.getByRole(AriaRole.HEADING);
```

### GetByAltText

```java
// By alt text
Locator image = page.getByAltText("Logo");

// Partial match
Locator image = page.getByAltText("logo", 
    new Page.GetByAltTextOptions().setExact(false));
```

### GetByTitle

```java
// By title attribute
Locator element = page.getByTitle("Tooltip text");

// Partial match
Locator element = page.getByTitle("tooltip", 
    new Page.GetByTitleOptions().setExact(false));
```

## Chaining Locators

### Basic Chaining

```java
// Chain locators
Locator element = page.locator("div.container")
    .locator("button")
    .getByText("Submit");

// Filter and chain
Locator element = page.locator("button")
    .filter(new Locator.FilterOptions().setHasText("Submit"))
    .first();
```

### Advanced Chaining

```java
// Chain with filters
Locator element = page.locator("div")
    .filter(new Locator.FilterOptions().setHasText("Container"))
    .locator("button")
    .filter(new Locator.FilterOptions().setHasText("Submit"));

// Chain with position
Locator element = page.locator("li")
    .first()
    .locator("button");

Locator element = page.locator("li")
    .last()
    .locator("button");

Locator element = page.locator("li")
    .nth(2)
    .locator("button");
```

## Custom Locators

### Data Attributes

```java
// Data-testid (recommended)
Locator element = page.locator("[data-testid='submit-button']");

// Custom data attributes
Locator element = page.locator("[data-qa='login-form']");
Locator element = page.locator("[data-cy='submit-btn']");
```

### Custom Attributes

```java
// Custom attribute
Locator element = page.locator("[custom-attr='value']");

// Multiple attributes
Locator element = page.locator("[data-testid='submit'][type='button']");
```

## Locator Best Practices

### 1. Prefer Text-Based Locators

```java
// Good - text-based locator
page.getByText("Submit").click();

// Avoid - fragile CSS selector
page.click("button.btn-primary:nth-child(2)");
```

### 2. Use Data Attributes

```java
// Good - stable selector
page.locator("[data-testid='submit-button']").click();

// Avoid - class-based selector (can change)
page.locator(".btn-submit").click();
```

### 3. Use Role-Based Locators

```java
// Good - semantic and accessible
page.getByRole(AriaRole.BUTTON, 
    new Page.GetByRoleOptions().setName("Submit")).click();

// Avoid - generic selector
page.click("button");
```

### 4. Avoid Position-Based Selectors

```java
// Avoid - fragile
page.locator("div > div:nth-child(2) > button");

// Good - use data attributes or text
page.locator("[data-testid='submit-button']");
```

### 5. Use Specific Selectors

```java
// Good - specific
page.locator("button[type='submit'][data-testid='submit']");

// Avoid - too generic
page.locator("button");
```

### 6. Store Locators in Variables

```java
// Good - reusable
Locator submitButton = page.locator("[data-testid='submit-button']");
submitButton.click();
submitButton.isVisible();

// Avoid - repeated selector
page.click("[data-testid='submit-button']");
page.locator("[data-testid='submit-button']").isVisible();
```

## Locator Strategies Comparison

| Strategy | Pros | Cons | When to Use |
|----------|------|------|-------------|
| **CSS Selectors** | Fast, familiar | Can be fragile | Simple, stable elements |
| **XPath** | Powerful, flexible | Can be complex | Complex DOM structures |
| **Text-Based** | User-friendly, stable | May match multiple elements | User-visible elements |
| **Role-Based** | Semantic, accessible | Limited to ARIA roles | Accessible elements |
| **Data Attributes** | Most stable | Requires code changes | Critical elements |

## Practical Examples

### Login Form

```java
public class LoginPage {
    private final Page page;
    
    public LoginPage(Page page) {
        this.page = page;
    }
    
    // Using data attributes (most stable)
    public Locator usernameField() {
        return page.locator("[data-testid='username']");
    }
    
    // Using label (semantic)
    public Locator passwordField() {
        return page.getByLabel("Password");
    }
    
    // Using role (accessible)
    public Locator submitButton() {
        return page.getByRole(AriaRole.BUTTON, 
            new Page.GetByRoleOptions().setName("Login"));
    }
    
    public void login(String username, String password) {
        usernameField().fill(username);
        passwordField().fill(password);
        submitButton().click();
    }
}
```

### Dynamic Content

```java
// Wait for element with specific text
public void waitForElementWithText(String text) {
    page.waitForSelector("text=" + text, 
        new Page.WaitForSelectorOptions()
            .setState(WaitForSelectorState.VISIBLE));
}

// Find element in specific container
public Locator findInContainer(String containerSelector, String elementText) {
    return page.locator(containerSelector)
        .getByText(elementText);
}
```

### Complex Selectors

```java
// Find button in specific section
public Locator findButtonInSection(String sectionText, String buttonText) {
    return page.locator("section")
        .filter(new Locator.FilterOptions().setHasText(sectionText))
        .getByRole(AriaRole.BUTTON, 
            new Page.GetByRoleOptions().setName(buttonText));
}

// Find element by multiple criteria
public Locator findElement(String text, String role, String dataTestId) {
    return page.locator("[data-testid='" + dataTestId + "']")
        .filter(new Locator.FilterOptions().setHasText(text))
        .filter(new Locator.FilterOptions().setHas(page.getByRole(AriaRole.valueOf(role))));
}
```

## Key Takeaways

- Text-based locators are more maintainable than CSS selectors
- Data attributes provide the most stable selectors
- Role-based locators improve accessibility and semantics
- Avoid position-based selectors (nth-child, etc.)
- Chain locators for complex element identification
- Store locators in variables for reuse and readability
- Use specific selectors to avoid matching multiple elements

## References

- [Playwright Locators Guide](https://playwright.dev/java/docs/locators)
- [Best Practices for Locators](https://playwright.dev/java/docs/best-practices)
- [CSS Selectors Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [XPath Reference](https://developer.mozilla.org/en-US/docs/Web/XPath)
