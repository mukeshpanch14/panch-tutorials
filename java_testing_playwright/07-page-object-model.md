# Page Object Model (POM) Pattern - Deep Dive

## Overview

The Page Object Model (POM) is a design pattern that creates an object repository for web UI elements. This pattern improves test maintainability and reduces code duplication by encapsulating page-specific logic.

## What is Page Object Model?

POM is a design pattern where:
- Each web page is represented by a class
- Page elements are defined as properties
- Page interactions are defined as methods
- Tests use page objects instead of direct Playwright calls

## Benefits of POM

1. **Maintainability**: Changes to UI only require updates in one place
2. **Reusability**: Page objects can be reused across multiple tests
3. **Readability**: Tests are more readable and express intent clearly
4. **Separation of Concerns**: UI logic is separated from test logic
5. **Reduced Duplication**: Common actions are defined once

## Basic Page Object

### Simple Page Object

```java
import com.microsoft.playwright.*;

public class LoginPage {
    private final Page page;
    
    // Locators
    private final Locator usernameField;
    private final Locator passwordField;
    private final Locator loginButton;
    private final Locator errorMessage;
    
    public LoginPage(Page page) {
        this.page = page;
        this.usernameField = page.locator("input[name='username']");
        this.passwordField = page.locator("input[name='password']");
        this.loginButton = page.locator("button[type='submit']");
        this.errorMessage = page.locator(".error-message");
    }
    
    // Actions
    public void enterUsername(String username) {
        usernameField.fill(username);
    }
    
    public void enterPassword(String password) {
        passwordField.fill(password);
    }
    
    public void clickLogin() {
        loginButton.click();
    }
    
    public void login(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
    }
    
    // Getters
    public String getErrorMessage() {
        return errorMessage.textContent();
    }
    
    public boolean isErrorMessageVisible() {
        return errorMessage.isVisible();
    }
}
```

### Using Page Object in Test

```java
import org.junit.jupiter.api.*;

public class LoginTest extends BaseTest {
    private LoginPage loginPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        loginPage = new LoginPage(page);
    }
    
    @Test
    void testSuccessfulLogin() {
        page.navigate("https://example.com/login");
        loginPage.login("testuser", "password123");
        page.waitForURL("**/dashboard");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
    
    @Test
    void testInvalidLogin() {
        page.navigate("https://example.com/login");
        loginPage.login("invalid", "wrong");
        Assertions.assertTrue(loginPage.isErrorMessageVisible());
        Assertions.assertTrue(loginPage.getErrorMessage().contains("Invalid"));
    }
}
```

## Advanced Page Object

### Private Locator Methods

```java
public class LoginPage {
    private final Page page;
    
    public LoginPage(Page page) {
        this.page = page;
    }
    
    // Private locator methods
    private Locator usernameField() {
        return page.locator("input[name='username']");
    }
    
    private Locator passwordField() {
        return page.locator("input[name='password']");
    }
    
    private Locator loginButton() {
        return page.locator("button[type='submit']");
    }
    
    private Locator errorMessage() {
        return page.locator(".error-message");
    }
    
    // Public action methods
    public void enterUsername(String username) {
        usernameField().fill(username);
    }
    
    public void enterPassword(String password) {
        passwordField().fill(password);
    }
    
    public void clickLogin() {
        loginButton().click();
    }
    
    public void login(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        clickLogin();
    }
    
    // Public getter methods
    public String getErrorMessage() {
        return errorMessage().textContent();
    }
    
    public boolean isErrorMessageVisible() {
        return errorMessage().isVisible();
    }
}
```

## Base Page Class

### Creating Base Page

```java
import com.microsoft.playwright.*;
import java.nio.file.Paths;

public abstract class BasePage {
    protected final Page page;
    
    public BasePage(Page page) {
        this.page = page;
    }
    
    // Common navigation
    public void navigateTo(String url) {
        page.navigate(url);
    }
    
    public void goBack() {
        page.goBack();
    }
    
    public void goForward() {
        page.goForward();
    }
    
    public void refresh() {
        page.reload();
    }
    
    // Common actions
    public void click(String selector) {
        page.click(selector);
    }
    
    public void fill(String selector, String value) {
        page.fill(selector, value);
    }
    
    // Common getters
    public String getTitle() {
        return page.title();
    }
    
    public String getUrl() {
        return page.url();
    }
    
    // Common utilities
    public void takeScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("target/screenshots/" + name + ".png")));
    }
    
    public void waitForLoad() {
        page.waitForLoadState(LoadState.NETWORKIDLE);
    }
    
    // Wait for URL
    public void waitForUrl(String urlPattern) {
        page.waitForURL(urlPattern);
    }
}
```

### Extending Base Page

```java
public class LoginPage extends BasePage {
    public LoginPage(Page page) {
        super(page);
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
    
    public void login(String username, String password) {
        usernameField().fill(username);
        passwordField().fill(password);
        loginButton().click();
    }
    
    public void navigateToLogin() {
        navigateTo("https://example.com/login");
    }
}
```

## Component-Based Page Objects

### Creating Components

```java
// Component class
public class NavigationComponent {
    private final Page page;
    
    public NavigationComponent(Page page) {
        this.page = page;
    }
    
    private Locator homeLink() {
        return page.locator("a[href='/home']");
    }
    
    private Locator aboutLink() {
        return page.locator("a[href='/about']");
    }
    
    private Locator contactLink() {
        return page.locator("a[href='/contact']");
    }
    
    public void clickHome() {
        homeLink().click();
    }
    
    public void clickAbout() {
        aboutLink().click();
    }
    
    public void clickContact() {
        contactLink().click();
    }
}

// Header component
public class HeaderComponent {
    private final Page page;
    
    public HeaderComponent(Page page) {
        this.page = page;
    }
    
    private Locator logo() {
        return page.locator(".logo");
    }
    
    private Locator searchBox() {
        return page.locator("input[type='search']");
    }
    
    private Locator searchButton() {
        return page.locator("button.search");
    }
    
    public void search(String query) {
        searchBox().fill(query);
        searchButton().click();
    }
}
```

### Using Components in Page Objects

```java
public class HomePage extends BasePage {
    private final NavigationComponent navigation;
    private final HeaderComponent header;
    
    public HomePage(Page page) {
        super(page);
        this.navigation = new NavigationComponent(page);
        this.header = new HeaderComponent(page);
    }
    
    public void navigateToAbout() {
        navigation.clickAbout();
    }
    
    public void search(String query) {
        header.search(query);
    }
}
```

## Page Factory Pattern

### Creating Page Factory

```java
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;

public class PageFactory {
    public static <T extends BasePage> T create(Class<T> pageClass, Page page) {
        try {
            T pageObject = pageClass.getConstructor(Page.class).newInstance(page);
            initializeLocators(pageObject, page);
            return pageObject;
        } catch (Exception e) {
            throw new RuntimeException("Failed to create page object", e);
        }
    }
    
    private static void initializeLocators(Object pageObject, Page page) {
        Field[] fields = pageObject.getClass().getDeclaredFields();
        for (Field field : fields) {
            if (field.isAnnotationPresent(FindBy.class)) {
                field.setAccessible(true);
                try {
                    FindBy findBy = field.getAnnotation(FindBy.class);
                    Locator locator = createLocator(page, findBy);
                    field.set(pageObject, locator);
                } catch (Exception e) {
                    throw new RuntimeException("Failed to initialize locator", e);
                }
            }
        }
    }
    
    private static Locator createLocator(Page page, FindBy findBy) {
        if (!findBy.css().isEmpty()) {
            return page.locator(findBy.css());
        } else if (!findBy.xpath().isEmpty()) {
            return page.locator("xpath=" + findBy.xpath());
        } else if (!findBy.text().isEmpty()) {
            return page.getByText(findBy.text());
        }
        throw new IllegalArgumentException("No locator strategy specified");
    }
}

// Annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface FindBy {
    String css() default "";
    String xpath() default "";
    String text() default "";
}
```

### Using Page Factory

```java
public class LoginPage extends BasePage {
    @FindBy(css = "input[name='username']")
    private Locator usernameField;
    
    @FindBy(css = "input[name='password']")
    private Locator passwordField;
    
    @FindBy(css = "button[type='submit']")
    private Locator loginButton;
    
    public LoginPage(Page page) {
        super(page);
    }
    
    public void login(String username, String password) {
        usernameField.fill(username);
        passwordField.fill(password);
        loginButton.click();
    }
}

// Usage
LoginPage loginPage = PageFactory.create(LoginPage.class, page);
loginPage.login("user", "pass");
```

## Best Practices

### 1. Encapsulation

Keep locators private and expose only necessary methods:

```java
// Good - encapsulated
public class LoginPage {
    private Locator usernameField() {
        return page.locator("input[name='username']");
    }
    
    public void enterUsername(String username) {
        usernameField().fill(username);
    }
}

// Avoid - exposing locators
public class LoginPage {
    public Locator usernameField;
}
```

### 2. Single Responsibility

Each page object should represent a single page:

```java
// Good - single page
public class LoginPage {
    // Login page elements and actions
}

// Avoid - multiple pages
public class LoginAndDashboardPage {
    // Login and dashboard mixed together
}
```

### 3. Meaningful Method Names

Use descriptive method names:

```java
// Good - descriptive
public void login(String username, String password) {
    // Implementation
}

// Avoid - unclear
public void doIt(String u, String p) {
    // Implementation
}
```

### 4. Return Page Objects

Return page objects for method chaining:

```java
public class LoginPage extends BasePage {
    public LoginPage enterUsername(String username) {
        usernameField().fill(username);
        return this;
    }
    
    public LoginPage enterPassword(String password) {
        passwordField().fill(password);
        return this;
    }
    
    public DashboardPage clickLogin() {
        loginButton().click();
        return new DashboardPage(page);
    }
}

// Usage - method chaining
DashboardPage dashboard = loginPage
    .enterUsername("user")
    .enterPassword("pass")
    .clickLogin();
```

### 5. Wait for Navigation

Always wait for navigation after actions:

```java
public DashboardPage login(String username, String password) {
    usernameField().fill(username);
    passwordField().fill(password);
    loginButton().click();
    page.waitForURL("**/dashboard");
    return new DashboardPage(page);
}
```

## Complete Example

### Page Objects

```java
// BasePage
public abstract class BasePage {
    protected final Page page;
    
    public BasePage(Page page) {
        this.page = page;
    }
    
    public void navigateTo(String url) {
        page.navigate(url);
    }
    
    public String getTitle() {
        return page.title();
    }
}

// LoginPage
public class LoginPage extends BasePage {
    public LoginPage(Page page) {
        super(page);
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

// DashboardPage
public class DashboardPage extends BasePage {
    public DashboardPage(Page page) {
        super(page);
    }
    
    private Locator welcomeMessage() {
        return page.locator(".welcome-message");
    }
    
    public String getWelcomeMessage() {
        return welcomeMessage().textContent();
    }
}
```

### Test Using Page Objects

```java
public class LoginTest extends BaseTest {
    private LoginPage loginPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        loginPage = new LoginPage(page);
    }
    
    @Test
    void testSuccessfulLogin() {
        loginPage.navigateTo("https://example.com/login");
        DashboardPage dashboard = loginPage.login("testuser", "password123");
        Assertions.assertTrue(dashboard.getWelcomeMessage().contains("Welcome"));
    }
}
```

## Key Takeaways

- Page Object Model improves test maintainability and readability
- Encapsulate locators and expose only necessary methods
- Use base page classes for common functionality
- Create components for reusable UI elements
- Return page objects for method chaining
- Always wait for navigation after actions
- Keep page objects focused on a single page

## References

- [Page Object Model Pattern](https://playwright.dev/java/docs/pom)
- [Selenium Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Design Patterns in Test Automation](https://www.selenium.dev/documentation/test_practices/)

