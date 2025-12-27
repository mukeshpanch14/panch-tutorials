# Java Fundamentals for Testing - Deep Dive

## Overview

Before diving into Playwright automation, it's essential to have a solid foundation in Java programming. This module covers the core Java concepts that are crucial for writing effective test automation code.

## Java Basics

### Classes and Objects

In Java, everything is organized around classes and objects. A class is a blueprint for creating objects.

```java
public class TestBase {
    // Class variables
    private String baseUrl;
    protected WebDriver driver;
    
    // Constructor
    public TestBase() {
        this.baseUrl = "https://example.com";
    }
    
    // Methods
    public void navigateToHome() {
        driver.get(baseUrl);
    }
}
```

### Data Types

Java has two categories of data types:
- **Primitive types**: `int`, `double`, `boolean`, `char`, `byte`, `short`, `long`, `float`
- **Reference types**: Objects, arrays, strings

```java
// Primitive types
int count = 10;
boolean isEnabled = true;
double price = 99.99;

// Reference types
String message = "Hello World";
String[] items = {"item1", "item2", "item3"};
```

### Variables and Scope

Understanding variable scope is crucial for test automation:

```java
public class TestExample {
    // Instance variable
    private String instanceVar = "Instance";
    
    // Class variable (static)
    private static String classVar = "Class";
    
    public void testMethod() {
        // Local variable
        String localVar = "Local";
        
        if (true) {
            // Block variable
            String blockVar = "Block";
        }
    }
}
```

## Object-Oriented Programming

### Inheritance

Inheritance allows a class to inherit properties and methods from another class:

```java
// Base class
public class BaseTest {
    protected Page page;
    
    public void setUp() {
        // Common setup code
    }
    
    public void tearDown() {
        // Common teardown code
    }
}

// Derived class
public class LoginTest extends BaseTest {
    @Override
    public void setUp() {
        super.setUp(); // Call parent setup
        // Additional setup
    }
    
    @Test
    public void testLogin() {
        // Test implementation
    }
}
```

### Polymorphism

Polymorphism allows objects of different types to be accessed through the same interface:

```java
// Interface
public interface WebElement {
    void click();
    void sendKeys(String text);
}

// Implementation
public class Button implements WebElement {
    @Override
    public void click() {
        // Button click implementation
    }
    
    @Override
    public void sendKeys(String text) {
        // Not applicable for button
    }
}
```

### Encapsulation

Encapsulation is the practice of hiding internal details and providing controlled access:

```java
public class TestConfig {
    // Private fields
    private String username;
    private String password;
    
    // Public getters
    public String getUsername() {
        return username;
    }
    
    // Public setters with validation
    public void setUsername(String username) {
        if (username != null && !username.isEmpty()) {
            this.username = username;
        }
    }
}
```

## Collections Framework

### List

Lists are ordered collections that allow duplicate elements:

```java
import java.util.ArrayList;
import java.util.List;

List<String> items = new ArrayList<>();
items.add("item1");
items.add("item2");
items.add("item1"); // Duplicates allowed

// Iterate
for (String item : items) {
    System.out.println(item);
}

// Stream API (Java 8+)
items.stream()
    .filter(item -> item.startsWith("item"))
    .forEach(System.out::println);
```

### Map

Maps store key-value pairs:

```java
import java.util.HashMap;
import java.util.Map;

Map<String, String> testData = new HashMap<>();
testData.put("username", "testuser");
testData.put("password", "testpass");

// Access values
String username = testData.get("username");

// Iterate
for (Map.Entry<String, String> entry : testData.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

### Set

Sets store unique elements:

```java
import java.util.HashSet;
import java.util.Set;

Set<String> uniqueItems = new HashSet<>();
uniqueItems.add("item1");
uniqueItems.add("item2");
uniqueItems.add("item1"); // Duplicate ignored

// Check existence
if (uniqueItems.contains("item1")) {
    System.out.println("Item exists");
}
```

## Exception Handling

### Try-Catch Blocks

Proper exception handling is crucial for robust test automation:

```java
public void performAction() {
    try {
        // Risky code
        page.click("button");
    } catch (TimeoutException e) {
        // Handle timeout
        System.out.println("Element not found: " + e.getMessage());
    } catch (Exception e) {
        // Handle other exceptions
        System.out.println("Unexpected error: " + e.getMessage());
    } finally {
        // Cleanup code (always executes)
        System.out.println("Cleanup performed");
    }
}
```

### Custom Exceptions

Create custom exceptions for specific test scenarios:

```java
// Custom exception
public class ElementNotFoundException extends Exception {
    public ElementNotFoundException(String message) {
        super(message);
    }
    
    public ElementNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }
}

// Usage
public void findElement(String selector) throws ElementNotFoundException {
    if (page.locator(selector).count() == 0) {
        throw new ElementNotFoundException("Element not found: " + selector);
    }
}
```

### Try-With-Resources

Automatically manage resources:

```java
// Automatically closes resources
try (FileInputStream fis = new FileInputStream("config.properties")) {
    Properties props = new Properties();
    props.load(fis);
    // Use properties
} catch (IOException e) {
    e.printStackTrace();
}
```

## Build Tools

### Maven Project Structure

Standard Maven project structure:

```
project-root/
├── pom.xml
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   │               └── Main.java
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│                   └── Test.java
└── target/
```

### Maven Dependencies

Example `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>playwright-tests</artifactId>
    <version>1.0-SNAPSHOT</version>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>com.microsoft.playwright</groupId>
            <artifactId>playwright</artifactId>
            <version>1.40.0</version>
        </dependency>
        
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

### Gradle Setup

Example `build.gradle`:

```gradle
plugins {
    id 'java'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'com.microsoft.playwright:playwright:1.40.0'
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
}

test {
    useJUnitPlatform()
}
```

## Annotations

### Common Test Annotations

```java
import org.junit.jupiter.api.*;

@DisplayName("Login Tests")
public class LoginTest {
    
    @BeforeAll
    static void setUpAll() {
        // Runs once before all tests
    }
    
    @BeforeEach
    void setUp() {
        // Runs before each test
    }
    
    @Test
    @DisplayName("Should login successfully")
    void testLogin() {
        // Test implementation
    }
    
    @AfterEach
    void tearDown() {
        // Runs after each test
    }
    
    @AfterAll
    static void tearDownAll() {
        // Runs once after all tests
    }
}
```

## Lambda Expressions (Java 8+)

Lambda expressions simplify code, especially with collections:

```java
// Traditional approach
List<String> filtered = new ArrayList<>();
for (String item : items) {
    if (item.startsWith("test")) {
        filtered.add(item);
    }
}

// Lambda approach
List<String> filtered = items.stream()
    .filter(item -> item.startsWith("test"))
    .collect(Collectors.toList());
```

## Practical Exercises

1. **Create a TestBase class** with common setup and teardown methods
2. **Implement a configuration reader** using Properties class
3. **Create a data provider** using Map to store test data
4. **Write exception handling** for element not found scenarios
5. **Set up a Maven project** with Playwright and JUnit dependencies

## Key Takeaways

- Java classes and objects form the foundation of test automation
- Collections (List, Map, Set) are essential for managing test data
- Exception handling ensures robust test execution
- Build tools (Maven/Gradle) manage dependencies and project structure
- Understanding OOP principles helps create maintainable test code

## References

- [Java Tutorial](https://docs.oracle.com/javase/tutorial/)
- [Maven Getting Started Guide](https://maven.apache.org/guides/getting-started/)
- [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html)
- [Java Collections Framework](https://docs.oracle.com/javase/tutorial/collections/)
