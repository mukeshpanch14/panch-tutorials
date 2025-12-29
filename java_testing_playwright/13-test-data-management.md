# Test Data Management - Deep Dive

## Overview

This module covers strategies for managing test data in Playwright tests, including data sources (JSON, CSV, Excel, databases), data-driven testing, test fixtures, random data generation, and data cleanup.

## Test Data Sources

### JSON Files

#### Reading JSON Data

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;

// JSON structure
// {
//   "users": [
//     {"username": "user1", "password": "pass1"},
//     {"username": "user2", "password": "pass2"}
//   ]
// }

// Read JSON file
ObjectMapper mapper = new ObjectMapper();
TestData data = mapper.readValue(new File("test-data.json"), TestData.class);

// Use data
for (User user : data.getUsers()) {
    page.fill("input[name='username']", user.getUsername());
    page.fill("input[name='password']", user.getPassword());
    page.click("button[type='submit']");
}
```

#### JSON Data Class

```java
public class TestData {
    private List<User> users;
    
    public List<User> getUsers() {
        return users;
    }
    
    public void setUsers(List<User> users) {
        this.users = users;
    }
}

public class User {
    private String username;
    private String password;
    
    public String getUsername() {
        return username;
    }
    
    public void setUsername(String username) {
        this.username = username;
    }
    
    public String getPassword() {
        return password;
    }
    
    public void setPassword(String password) {
        this.password = password;
    }
}
```

### CSV Files

#### Reading CSV Data

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

// CSV structure
// username,password
// user1,pass1
// user2,pass2

public List<User> readCsvData(String filePath) throws IOException {
    List<User> users = new ArrayList<>();
    BufferedReader reader = new BufferedReader(new FileReader(filePath));
    String line;
    boolean firstLine = true;
    
    while ((line = reader.readLine()) != null) {
        if (firstLine) {
            firstLine = false;
            continue;  // Skip header
        }
        String[] values = line.split(",");
        User user = new User();
        user.setUsername(values[0]);
        user.setPassword(values[1]);
        users.add(user);
    }
    
    reader.close();
    return users;
}
```

### Excel Files

#### Reading Excel Data

```java
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import java.io.FileInputStream;
import java.io.IOException;

public List<User> readExcelData(String filePath) throws IOException {
    List<User> users = new ArrayList<>();
    FileInputStream fis = new FileInputStream(filePath);
    Workbook workbook = new XSSFWorkbook(fis);
    Sheet sheet = workbook.getSheetAt(0);
    
    for (int i = 1; i <= sheet.getLastRowNum(); i++) {
        Row row = sheet.getRow(i);
        User user = new User();
        user.setUsername(row.getCell(0).getStringCellValue());
        user.setPassword(row.getCell(1).getStringCellValue());
        users.add(user);
    }
    
    workbook.close();
    fis.close();
    return users;
}
```

### Database

#### Database Connection

```java
import java.sql.*;

public class DatabaseHelper {
    private Connection connection;
    
    public DatabaseHelper(String url, String username, String password) throws SQLException {
        connection = DriverManager.getConnection(url, username, password);
    }
    
    public List<User> getUsers() throws SQLException {
        List<User> users = new ArrayList<>();
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery("SELECT username, password FROM users");
        
        while (rs.next()) {
            User user = new User();
            user.setUsername(rs.getString("username"));
            user.setPassword(rs.getString("password"));
            users.add(user);
        }
        
        rs.close();
        stmt.close();
        return users;
    }
    
    public void close() throws SQLException {
        if (connection != null) {
            connection.close();
        }
    }
}
```

## Data-Driven Testing

### JUnit 5 Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.CsvFileSource;

// Value source
@ParameterizedTest
@ValueSource(strings = {"user1", "user2", "user3"})
void testLoginWithUsers(String username) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", "password");
    page.click("button[type='submit']");
    Assertions.assertTrue(page.url().contains("dashboard"));
}

// CSV source
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

// CSV file source
@ParameterizedTest
@CsvFileSource(resources = "/test-data.csv", numLinesToSkip = 1)
void testLoginFromCsv(String username, String password) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", password);
    page.click("button[type='submit']");
    Assertions.assertTrue(page.url().contains("dashboard"));
}
```

### TestNG Data Providers

```java
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

@DataProvider(name = "loginCredentials")
public Object[][] loginCredentials() {
    return new Object[][] {
        {"user1", "pass1"},
        {"user2", "pass2"},
        {"user3", "pass3"}
    };
}

@Test(dataProvider = "loginCredentials")
public void testLogin(String username, String password) {
    page.navigate("https://example.com/login");
    page.fill("input[name='username']", username);
    page.fill("input[name='password']", password);
    page.click("button[type='submit']");
    Assert.assertTrue(page.url().contains("dashboard"));
}
```

## Test Fixtures

### Setup and Teardown Data

```java
public class TestFixture {
    private Page page;
    
    public TestFixture(Page page) {
        this.page = page;
    }
    
    public void setupTestData() {
        // Create test data via API
        APIRequestContext requestContext = playwright.request().newContext();
        requestContext.post("https://api.example.com/users",
            new APIRequestContext.PostOptions()
                .setData("{\"username\": \"testuser\", \"email\": \"test@example.com\"}")
                .setHeader("Content-Type", "application/json"));
    }
    
    public void teardownTestData() {
        // Clean up test data via API
        APIRequestContext requestContext = playwright.request().newContext();
        requestContext.delete("https://api.example.com/users/testuser");
    }
}
```

### Using Fixtures

```java
public class LoginTest extends BaseTest {
    private TestFixture fixture;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        fixture = new TestFixture(page);
        fixture.setupTestData();
    }
    
    @AfterEach
    void tearDown() {
        fixture.teardownTestData();
        super.tearDown();
    }
    
    @Test
    void testLogin() {
        // Test implementation
    }
}
```

## Random Data Generation

### Java Faker

#### Setup

Add dependency to `pom.xml`:

```xml
<dependency>
    <groupId>com.github.javafaker</groupId>
    <artifactId>javafaker</artifactId>
    <version>1.0.2</version>
</dependency>
```

#### Using Faker

```java
import com.github.javafaker.Faker;

Faker faker = new Faker();

// Generate random data
String firstName = faker.name().firstName();
String lastName = faker.name().lastName();
String email = faker.internet().emailAddress();
String phoneNumber = faker.phoneNumber().phoneNumber();
String address = faker.address().fullAddress();
String city = faker.address().city();
String country = faker.address().country();
String zipCode = faker.address().zipCode();
```

#### Faker Examples

```java
public class RandomDataGenerator {
    private Faker faker;
    
    public RandomDataGenerator() {
        this.faker = new Faker();
    }
    
    public User generateUser() {
        User user = new User();
        user.setUsername(faker.name().username());
        user.setEmail(faker.internet().emailAddress());
        user.setFirstName(faker.name().firstName());
        user.setLastName(faker.name().lastName());
        user.setPhoneNumber(faker.phoneNumber().phoneNumber());
        user.setAddress(faker.address().fullAddress());
        return user;
    }
    
    public String generateEmail() {
        return faker.internet().emailAddress();
    }
    
    public String generatePassword() {
        return faker.internet().password(8, 16, true, true, true);
    }
}
```

## Data Cleanup

### API Cleanup

```java
public class DataCleanup {
    private APIRequestContext requestContext;
    
    public DataCleanup(Playwright playwright) {
        this.requestContext = playwright.request().newContext();
    }
    
    public void cleanupUser(String username) {
        requestContext.delete("https://api.example.com/users/" + username);
    }
    
    public void cleanupAllTestUsers() {
        // Get all test users
        APIResponse response = requestContext.get("https://api.example.com/users?prefix=test_");
        JSONArray users = response.json().getJSONArray("users");
        
        // Delete each user
        for (int i = 0; i < users.length(); i++) {
            String username = users.getJSONObject(i).getString("username");
            cleanupUser(username);
        }
    }
}
```

### Database Cleanup

```java
public class DatabaseCleanup {
    private Connection connection;
    
    public DatabaseCleanup(Connection connection) {
        this.connection = connection;
    }
    
    public void cleanupTestData() throws SQLException {
        Statement stmt = connection.createStatement();
        stmt.executeUpdate("DELETE FROM users WHERE username LIKE 'test_%'");
        stmt.close();
    }
    
    public void cleanupUser(String username) throws SQLException {
        PreparedStatement pstmt = connection.prepareStatement("DELETE FROM users WHERE username = ?");
        pstmt.setString(1, username);
        pstmt.executeUpdate();
        pstmt.close();
    }
}
```

## Practical Examples

### Data-Driven Login Test

```java
public class DataDrivenLoginTest extends BaseTest {
    private List<User> testUsers;
    
    @BeforeAll
    static void setUpAll() {
        super.setUpAll();
        // Load test data
        ObjectMapper mapper = new ObjectMapper();
        try {
            TestData data = mapper.readValue(new File("test-data.json"), TestData.class);
            testUsers = data.getUsers();
        } catch (IOException e) {
            throw new RuntimeException("Failed to load test data", e);
        }
    }
    
    @ParameterizedTest
    @MethodSource("getTestUsers")
    void testLoginWithData(User user) {
        page.navigate("https://example.com/login");
        page.fill("input[name='username']", user.getUsername());
        page.fill("input[name='password']", user.getPassword());
        page.click("button[type='submit']");
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
    
    static Stream<Arguments> getTestUsers() {
        return testUsers.stream()
            .map(user -> Arguments.of(user));
    }
}
```

### Random Data Test

```java
public class RandomDataTest extends BaseTest {
    private RandomDataGenerator dataGenerator;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        dataGenerator = new RandomDataGenerator();
    }
    
    @Test
    void testRegistrationWithRandomData() {
        User user = dataGenerator.generateUser();
        
        page.navigate("https://example.com/register");
        page.fill("input[name='username']", user.getUsername());
        page.fill("input[name='email']", user.getEmail());
        page.fill("input[name='firstName']", user.getFirstName());
        page.fill("input[name='lastName']", user.getLastName());
        page.fill("input[name='phoneNumber']", user.getPhoneNumber());
        page.fill("input[name='address']", user.getAddress());
        page.click("button[type='submit']");
        
        Assertions.assertTrue(page.url().contains("dashboard"));
    }
}
```

### Test Fixture Example

```java
public class FixtureTest extends BaseTest {
    private TestFixture fixture;
    private DataCleanup cleanup;
    
    @BeforeEach
    void setUp() {
        super.setUp();
        fixture = new TestFixture(page);
        cleanup = new DataCleanup(playwright);
        fixture.setupTestData();
    }
    
    @AfterEach
    void tearDown() {
        cleanup.cleanupAllTestUsers();
        super.tearDown();
    }
    
    @Test
    void testWithFixture() {
        // Test implementation
    }
}
```

## Best Practices

### 1. Separate Test Data from Code

```java
// Good - external data file
ObjectMapper mapper = new ObjectMapper();
TestData data = mapper.readValue(new File("test-data.json"), TestData.class);

// Avoid - hardcoded data
User user = new User();
user.setUsername("user1");
user.setPassword("pass1");
```

### 2. Use Data Providers

```java
// Good - data provider
@ParameterizedTest
@CsvFileSource(resources = "/test-data.csv")
void testLogin(String username, String password) {
    // Test implementation
}

// Avoid - repeated test methods
@Test
void testLogin1() { /* ... */ }
@Test
void testLogin2() { /* ... */ }
```

### 3. Generate Unique Test Data

```java
// Good - unique data
String username = "test_" + System.currentTimeMillis();

// Avoid - fixed data
String username = "testuser";  // May cause conflicts
```

### 4. Clean Up Test Data

```java
// Good - cleanup
@AfterEach
void tearDown() {
    cleanup.cleanupTestData();
    super.tearDown();
}

// Avoid - data accumulation
// Test data remains in system
```

### 5. Use Fixtures for Setup

```java
// Good - fixture
@BeforeEach
void setUp() {
    fixture.setupTestData();
}

// Avoid - setup in each test
@Test
void test1() {
    setupTestData();
    // Test implementation
}
```

## Key Takeaways

- Use external data sources (JSON, CSV, Excel) for test data
- Implement data-driven testing with parameterized tests
- Use test fixtures for setup and teardown
- Generate random data for unique test scenarios
- Always clean up test data after tests
- Separate test data from test code
- Use data providers for multiple test scenarios

## References

- [JUnit 5 Parameterized Tests](https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests)
- [TestNG Data Providers](https://testng.org/doc/documentation-main.html#parameters-dataproviders)
- [Java Faker](https://github.com/DiUS/java-faker)
- [Jackson JSON](https://github.com/FasterXML/jackson)

