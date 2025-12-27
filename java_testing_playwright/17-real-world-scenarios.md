# Real-World Test Scenarios - Deep Dive

## Overview

This module covers real-world testing scenarios using Playwright, including e-commerce testing, form validation, authentication flows, API integration, cross-browser testing, and performance testing. These examples demonstrate how to apply Playwright concepts to practical testing situations.

## E-commerce Testing

### Product Search

```java
public class ProductSearchTest extends BaseTest {
    private HomePage homePage;
    private SearchResultsPage searchResultsPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        homePage = new HomePage(page);
        searchResultsPage = new SearchResultsPage(page);
    }
    
    @Test
    void testProductSearch() {
        // Navigate to home page
        homePage.navigate();
        
        // Search for product
        homePage.search("laptop");
        
        // Verify search results
        Assertions.assertTrue(searchResultsPage.hasResults());
        Assertions.assertTrue(searchResultsPage.getResultCount() > 0);
        
        // Verify search term in results
        String firstResult = searchResultsPage.getFirstResultTitle();
        Assertions.assertTrue(firstResult.toLowerCase().contains("laptop"));
    }
    
    @Test
    void testProductSearchWithFilters() {
        homePage.navigate();
        homePage.search("laptop");
        
        // Apply filters
        searchResultsPage.filterByPrice("500-1000");
        searchResultsPage.filterByBrand("Dell");
        
        // Verify filtered results
        Assertions.assertTrue(searchResultsPage.hasResults());
        List<Product> products = searchResultsPage.getProducts();
        products.forEach(product -> {
            Assertions.assertTrue(product.getPrice() >= 500 && product.getPrice() <= 1000);
            Assertions.assertEquals("Dell", product.getBrand());
        });
    }
}
```

### Shopping Cart

```java
public class ShoppingCartTest extends BaseTest {
    private HomePage homePage;
    private ProductPage productPage;
    private CartPage cartPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        homePage = new HomePage(page);
        productPage = new ProductPage(page);
        cartPage = new CartPage(page);
    }
    
    @Test
    void testAddToCart() {
        // Navigate to product
        homePage.navigate();
        homePage.search("laptop");
        homePage.clickFirstResult();
        
        // Add to cart
        productPage.addToCart();
        
        // Verify cart
        cartPage.navigate();
        Assertions.assertTrue(cartPage.hasItems());
        Assertions.assertTrue(cartPage.getItemCount() > 0);
    }
    
    @Test
    void testUpdateCartQuantity() {
        // Add product to cart
        productPage.navigate("product-123");
        productPage.addToCart();
        
        // Update quantity
        cartPage.navigate();
        cartPage.updateQuantity(1, 3);
        
        // Verify quantity updated
        Assertions.assertEquals(3, cartPage.getQuantity(1));
    }
    
    @Test
    void testRemoveFromCart() {
        // Add product to cart
        productPage.navigate("product-123");
        productPage.addToCart();
        
        // Remove from cart
        cartPage.navigate();
        int initialCount = cartPage.getItemCount();
        cartPage.removeItem(1);
        
        // Verify item removed
        Assertions.assertEquals(initialCount - 1, cartPage.getItemCount());
    }
}
```

### Checkout

```java
public class CheckoutTest extends BaseTest {
    private CartPage cartPage;
    private CheckoutPage checkoutPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        cartPage = new CartPage(page);
        checkoutPage = new CheckoutPage(page);
    }
    
    @Test
    void testCheckoutProcess() {
        // Add product to cart
        ProductPage productPage = new ProductPage(page);
        productPage.navigate("product-123");
        productPage.addToCart();
        
        // Proceed to checkout
        cartPage.navigate();
        cartPage.proceedToCheckout();
        
        // Fill shipping information
        checkoutPage.fillShippingInfo(
            "John Doe",
            "123 Main St",
            "New York",
            "NY",
            "10001",
            "United States"
        );
        
        // Fill payment information
        checkoutPage.fillPaymentInfo(
            "4111111111111111",
            "12/25",
            "123"
        );
        
        // Place order
        checkoutPage.placeOrder();
        
        // Verify order confirmation
        Assertions.assertTrue(checkoutPage.isOrderConfirmed());
        String orderNumber = checkoutPage.getOrderNumber();
        Assertions.assertNotNull(orderNumber);
    }
}
```

## Form Validation

### Multi-Step Forms

```java
public class MultiStepFormTest extends BaseTest {
    private RegistrationPage registrationPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        registrationPage = new RegistrationPage(page);
    }
    
    @Test
    void testMultiStepRegistration() {
        registrationPage.navigate();
        
        // Step 1: Personal Information
        registrationPage.fillPersonalInfo(
            "John",
            "Doe",
            "john.doe@example.com",
            "1234567890"
        );
        registrationPage.clickNext();
        
        // Step 2: Address Information
        registrationPage.fillAddressInfo(
            "123 Main St",
            "New York",
            "NY",
            "10001"
        );
        registrationPage.clickNext();
        
        // Step 3: Account Information
        registrationPage.fillAccountInfo(
            "johndoe",
            "Password123!",
            "Password123!"
        );
        registrationPage.submit();
        
        // Verify registration success
        Assertions.assertTrue(registrationPage.isRegistrationSuccessful());
    }
}
```

### Form Validation

```java
public class FormValidationTest extends BaseTest {
    private RegistrationPage registrationPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        registrationPage = new RegistrationPage(page);
    }
    
    @Test
    void testRequiredFieldValidation() {
        registrationPage.navigate();
        registrationPage.submit();
        
        // Verify validation errors
        Assertions.assertTrue(registrationPage.hasValidationError("First name is required"));
        Assertions.assertTrue(registrationPage.hasValidationError("Email is required"));
    }
    
    @Test
    void testEmailFormatValidation() {
        registrationPage.navigate();
        registrationPage.fillEmail("invalid-email");
        registrationPage.submit();
        
        // Verify email validation error
        Assertions.assertTrue(registrationPage.hasValidationError("Invalid email format"));
    }
    
    @Test
    void testPasswordStrengthValidation() {
        registrationPage.navigate();
        registrationPage.fillPassword("weak");
        registrationPage.submit();
        
        // Verify password strength error
        Assertions.assertTrue(registrationPage.hasValidationError("Password must be at least 8 characters"));
    }
}
```

### File Upload

```java
public class FileUploadTest extends BaseTest {
    private FileUploadPage fileUploadPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        fileUploadPage = new FileUploadPage(page);
    }
    
    @Test
    void testFileUpload() {
        fileUploadPage.navigate();
        
        // Upload file
        fileUploadPage.uploadFile(Paths.get("test-data/sample.pdf"));
        
        // Verify upload success
        Assertions.assertTrue(fileUploadPage.isUploadSuccessful());
        String fileName = fileUploadPage.getUploadedFileName();
        Assertions.assertEquals("sample.pdf", fileName);
    }
    
    @Test
    void testMultipleFileUpload() {
        fileUploadPage.navigate();
        
        // Upload multiple files
        fileUploadPage.uploadFiles(new Path[] {
            Paths.get("test-data/file1.pdf"),
            Paths.get("test-data/file2.pdf"),
            Paths.get("test-data/file3.pdf")
        });
        
        // Verify uploads
        Assertions.assertEquals(3, fileUploadPage.getUploadedFileCount());
    }
    
    @Test
    void testFileSizeValidation() {
        fileUploadPage.navigate();
        
        // Upload large file
        fileUploadPage.uploadFile(Paths.get("test-data/large-file.pdf"));
        
        // Verify file size validation error
        Assertions.assertTrue(fileUploadPage.hasValidationError("File size exceeds maximum allowed size"));
    }
}
```

## Authentication Flows

### Login

```java
public class LoginTest extends BaseTest {
    private LoginPage loginPage;
    private DashboardPage dashboardPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        loginPage = new LoginPage(page);
        dashboardPage = new DashboardPage(page);
    }
    
    @Test
    void testSuccessfulLogin() {
        loginPage.navigate();
        dashboardPage = loginPage.login("testuser", "password123");
        
        // Verify login success
        Assertions.assertTrue(dashboardPage.isLoaded());
        Assertions.assertTrue(dashboardPage.getWelcomeMessage().contains("testuser"));
    }
    
    @Test
    void testInvalidCredentials() {
        loginPage.navigate();
        loginPage.login("invalid", "wrong");
        
        // Verify error message
        Assertions.assertTrue(loginPage.hasErrorMessage("Invalid username or password"));
    }
    
    @Test
    void testRememberMe() {
        loginPage.navigate();
        loginPage.loginWithRememberMe("testuser", "password123");
        
        // Close and reopen browser
        context.close();
        context = browser.newContext();
        page = context.newPage();
        
        // Verify still logged in
        loginPage = new LoginPage(page);
        loginPage.navigate();
        Assertions.assertTrue(dashboardPage.isLoaded());
    }
}
```

### Registration

```java
public class RegistrationTest extends BaseTest {
    private RegistrationPage registrationPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        registrationPage = new RegistrationPage(page);
    }
    
    @Test
    void testUserRegistration() {
        registrationPage.navigate();
        
        // Generate unique user data
        String username = "test_" + System.currentTimeMillis();
        String email = username + "@example.com";
        
        // Register user
        registrationPage.register(
            username,
            email,
            "Password123!",
            "John",
            "Doe"
        );
        
        // Verify registration success
        Assertions.assertTrue(registrationPage.isRegistrationSuccessful());
    }
    
    @Test
    void testDuplicateUsername() {
        registrationPage.navigate();
        
        // Try to register with existing username
        registrationPage.register(
            "existinguser",
            "new@example.com",
            "Password123!",
            "John",
            "Doe"
        );
        
        // Verify error message
        Assertions.assertTrue(registrationPage.hasErrorMessage("Username already exists"));
    }
}
```

### Password Reset

```java
public class PasswordResetTest extends BaseTest {
    private PasswordResetPage passwordResetPage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        passwordResetPage = new PasswordResetPage(page);
    }
    
    @Test
    void testPasswordReset() {
        passwordResetPage.navigate();
        
        // Request password reset
        passwordResetPage.requestReset("test@example.com");
        
        // Verify reset email sent message
        Assertions.assertTrue(passwordResetPage.hasMessage("Password reset email sent"));
    }
    
    @Test
    void testPasswordResetWithInvalidEmail() {
        passwordResetPage.navigate();
        
        // Request reset with invalid email
        passwordResetPage.requestReset("invalid-email");
        
        // Verify error message
        Assertions.assertTrue(passwordResetPage.hasErrorMessage("Invalid email address"));
    }
}
```

## API Integration Testing

### Frontend-Backend Validation

```java
public class ApiIntegrationTest extends BaseTest {
    private APIRequestContext apiContext;
    private HomePage homePage;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        apiContext = playwright.request().newContext();
        homePage = new HomePage(page);
    }
    
    @Test
    void testUserCreationViaAPI() {
        // Create user via API
        String username = "test_" + System.currentTimeMillis();
        APIResponse response = apiContext.post("https://api.example.com/users",
            new APIRequestContext.PostOptions()
                .setData("{\"username\": \"" + username + "\", \"email\": \"" + username + "@example.com\"}")
                .setHeader("Content-Type", "application/json"));
        
        Assertions.assertEquals(201, response.status());
        
        // Verify user in UI
        homePage.navigate();
        homePage.searchUser(username);
        Assertions.assertTrue(homePage.isUserDisplayed(username));
    }
    
    @Test
    void testUIUpdatesAfterAPIChange() {
        // Make API change
        apiContext.put("https://api.example.com/users/123",
            new APIRequestContext.PutOptions()
                .setData("{\"status\": \"active\"}")
                .setHeader("Content-Type", "application/json"));
        
        // Refresh page
        homePage.navigate();
        homePage.refresh();
        
        // Verify UI updated
        Assertions.assertTrue(homePage.isUserStatusActive("123"));
    }
}
```

## Cross-Browser Testing

### Browser Compatibility

```java
public class CrossBrowserTest extends BaseTest {
    @ParameterizedTest
    @ValueSource(strings = {"chromium", "firefox", "webkit"})
    void testLoginAcrossBrowsers(String browserType) {
        // Create browser based on type
        BrowserType browserTypeObj = switch (browserType) {
            case "chromium" -> playwright.chromium();
            case "firefox" -> playwright.firefox();
            case "webkit" -> playwright.webkit();
            default -> throw new IllegalArgumentException("Unknown browser: " + browserType);
        };
        
        Browser browser = browserTypeObj.launch();
        BrowserContext context = browser.newContext();
        Page page = context.newPage();
        
        try {
            // Test login
            LoginPage loginPage = new LoginPage(page);
            loginPage.navigate();
            DashboardPage dashboard = loginPage.login("testuser", "password123");
            
            // Verify login success
            Assertions.assertTrue(dashboard.isLoaded());
        } finally {
            context.close();
            browser.close();
        }
    }
}
```

## Performance Testing

### Page Load Time

```java
public class PerformanceTest extends BaseTest {
    @Test
    void testPageLoadTime() {
        long startTime = System.currentTimeMillis();
        
        page.navigate("https://example.com");
        page.waitForLoadState(LoadState.NETWORKIDLE);
        
        long loadTime = System.currentTimeMillis() - startTime;
        
        // Verify load time is acceptable
        Assertions.assertTrue(loadTime < 5000, "Page load time: " + loadTime + "ms");
    }
    
    @Test
    void testResponseTime() {
        // Measure API response time
        long startTime = System.currentTimeMillis();
        
        APIRequestContext apiContext = playwright.request().newContext();
        APIResponse response = apiContext.get("https://api.example.com/users");
        
        long responseTime = System.currentTimeMillis() - startTime;
        
        // Verify response time
        Assertions.assertTrue(responseTime < 1000, "API response time: " + responseTime + "ms");
    }
}
```

## Key Takeaways

- E-commerce testing covers search, cart, and checkout flows
- Form validation ensures proper user input handling
- Authentication flows include login, registration, and password reset
- API integration testing validates frontend-backend consistency
- Cross-browser testing ensures compatibility across browsers
- Performance testing measures page load and response times
- Real-world scenarios require combining multiple Playwright concepts

## References

- [Playwright Examples](https://github.com/microsoft/playwright-java)
- [Playwright Community](https://github.com/microsoft/playwright/discussions)
- [E-commerce Testing](https://playwright.dev/java/docs/test-intro)
- [API Testing](https://playwright.dev/java/docs/api-testing)

