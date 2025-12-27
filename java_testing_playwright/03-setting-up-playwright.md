# Setting Up Playwright with Java - Deep Dive

## Overview

This module covers setting up a Java project with Playwright, configuring dependencies, installing browsers, and creating your first test. We'll cover both Maven and Gradle build tools.

## Prerequisites

Before setting up Playwright, ensure you have:

- **Java JDK 11 or higher** installed
- **Maven 3.6+** or **Gradle 6.0+** installed
- **IDE** (IntelliJ IDEA, Eclipse, or VS Code) installed
- **Internet connection** for downloading dependencies and browsers

## Maven Setup

### Creating a Maven Project

#### Option 1: Using Maven Archetype

```bash
mvn archetype:generate \
  -DgroupId=com.example \
  -DartifactId=playwright-tests \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false
```

#### Option 2: Manual Project Structure

Create the following directory structure:

```
playwright-tests/
├── pom.xml
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   └── test/
│       └── java/
│           └── com/
│               └── example/
└── target/
```

### Maven pom.xml Configuration

Create or update `pom.xml`:

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
    <packaging>jar</packaging>
    
    <name>Playwright Tests</name>
    <description>Playwright automation tests</description>
    
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <playwright.version>1.40.0</playwright.version>
        <junit.version>5.10.0</junit.version>
    </properties>
    
    <dependencies>
        <!-- Playwright -->
        <dependency>
            <groupId>com.microsoft.playwright</groupId>
            <artifactId>playwright</artifactId>
            <version>${playwright.version}</version>
        </dependency>
        
        <!-- JUnit 5 -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
        
        <!-- TestNG (Alternative) -->
        <dependency>
            <groupId>org.testng</groupId>
            <artifactId>testng</artifactId>
            <version>7.8.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <!-- Maven Compiler Plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                </configuration>
            </plugin>
            
            <!-- Maven Surefire Plugin (JUnit) -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
        </plugins>
    </build>
</project>
```

### Installing Dependencies

```bash
# Download dependencies
mvn clean install

# Or just download dependencies without compiling
mvn dependency:resolve
```

## Gradle Setup

### Creating a Gradle Project

#### Option 1: Using Gradle Init

```bash
gradle init \
  --type java-library \
  --dsl groovy \
  --package com.example \
  --project-name playwright-tests
```

#### Option 2: Manual Project Structure

Create the following directory structure:

```
playwright-tests/
├── build.gradle
├── settings.gradle
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   └── test/
│       └── java/
│           └── com/
│               └── example/
└── build/
```

### Gradle build.gradle Configuration

Create or update `build.gradle`:

```gradle
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    // Playwright
    implementation 'com.microsoft.playwright:playwright:1.40.0'
    
    // JUnit 5
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    
    // TestNG (Alternative)
    testImplementation 'org.testng:testng:7.8.0'
}

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

test {
    useJUnitPlatform()
}
```

### Installing Dependencies

```bash
# Download dependencies
./gradlew build

# Or just download dependencies
./gradlew dependencies
```

## Installing Playwright Browsers

Playwright requires browser binaries to be installed separately. This is done automatically when you first run Playwright, or you can install them manually.

### Automatic Installation

Browsers are automatically installed when you first create a Playwright instance:

```java
import com.microsoft.playwright.*;

public class InstallBrowsers {
    public static void main(String[] args) {
        Playwright playwright = Playwright.create();
        // Browsers will be downloaded automatically on first use
        playwright.close();
    }
}
```

### Manual Installation

You can also install browsers manually using the Playwright CLI:

```bash
# Install all browsers
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install"

# Or using Gradle
./gradlew --console=plain -q --args="install"
```

### Installing Specific Browsers

```bash
# Install Chromium only
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install chromium"

# Install Firefox only
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install firefox"

# Install WebKit only
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install webkit"
```

## Project Structure

### Recommended Structure

```
playwright-tests/
├── pom.xml (or build.gradle)
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   │               ├── pages/
│   │               │   ├── LoginPage.java
│   │               │   └── HomePage.java
│   │               ├── utils/
│   │               │   ├── TestConfig.java
│   │               │   └── TestData.java
│   │               └── base/
│   │                   └── BaseTest.java
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│                   ├── tests/
│                   │   ├── LoginTest.java
│                   │   └── HomeTest.java
│                   └── resources/
│                       ├── test-data.json
│                       └── config.properties
└── target/ (or build/)
```

## IDE Setup

### IntelliJ IDEA

1. **Open Project**
   - File → Open → Select project directory

2. **Configure SDK**
   - File → Project Structure → Project
   - Set Project SDK to Java 11+

3. **Import Maven/Gradle**
   - IntelliJ will automatically detect Maven/Gradle
   - Click "Import Maven Project" or "Import Gradle Project"

4. **Run Configuration**
   - Right-click test class → Run
   - Or create Run Configuration

### Eclipse

1. **Import Project**
   - File → Import → Existing Maven/Gradle Projects

2. **Configure Build Path**
   - Right-click project → Build Path → Configure Build Path
   - Ensure Java 11+ is selected

3. **Run Tests**
   - Right-click test class → Run As → JUnit Test

### VS Code

1. **Install Extensions**
   - Java Extension Pack
   - Test Runner for Java

2. **Open Project**
   - File → Open Folder → Select project directory

3. **Run Tests**
   - Click "Run Test" above test methods

## Creating Your First Test

### Simple Test Example

Create `src/test/java/com/example/FirstTest.java`:

```java
package com.example;

import com.microsoft.playwright.*;
import org.junit.jupiter.api.*;

public class FirstTest {
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
    @DisplayName("Navigate to Playwright website")
    void testNavigate() {
        page.navigate("https://playwright.dev");
        String title = page.title();
        System.out.println("Page title: " + title);
        Assertions.assertTrue(title.contains("Playwright"));
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

## Running Tests

### Maven

```bash
# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=FirstTest

# Run specific test method
mvn test -Dtest=FirstTest#testNavigate

# Run with specific browser
mvn test -Dbrowser=firefox
```

### Gradle

```bash
# Run all tests
./gradlew test

# Run specific test class
./gradlew test --tests FirstTest

# Run specific test method
./gradlew test --tests FirstTest.testNavigate
```

### IDE

- **IntelliJ IDEA**: Right-click test → Run
- **Eclipse**: Right-click test → Run As → JUnit Test
- **VS Code**: Click "Run Test" above test method

## Configuration Files

### Test Configuration

Create `src/test/resources/config.properties`:

```properties
# Browser Configuration
browser=chromium
headless=false
slow.mo=100

# Application URLs
base.url=https://example.com
login.url=https://example.com/login

# Timeouts
default.timeout=30000
navigation.timeout=60000

# Screenshots
screenshot.on.failure=true
screenshot.path=target/screenshots
```

### Reading Configuration

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class TestConfig {
    private static Properties props;
    
    static {
        props = new Properties();
        try {
            props.load(new FileInputStream(
                "src/test/resources/config.properties"
            ));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String getProperty(String key) {
        return props.getProperty(key);
    }
    
    public static String getBaseUrl() {
        return getProperty("base.url");
    }
    
    public static boolean isHeadless() {
        return Boolean.parseBoolean(getProperty("headless"));
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Browsers Not Installed

**Error**: `Executable doesn't exist`

**Solution**:
```bash
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install"
```

#### 2. Java Version Mismatch

**Error**: `UnsupportedClassVersionError`

**Solution**: Ensure Java 11+ is installed and configured

#### 3. Dependency Download Issues

**Error**: `Could not resolve dependencies`

**Solution**: Check internet connection and Maven/Gradle repository settings

#### 4. IDE Not Recognizing Tests

**Solution**: 
- Refresh Maven/Gradle project
- Reimport dependencies
- Check test source directory configuration

## Best Practices

1. **Use Test Base Class**: Create a base test class for common setup
2. **Configuration Management**: Use properties files for configuration
3. **Resource Management**: Always close browsers and contexts
4. **Test Organization**: Organize tests by feature or page
5. **Version Management**: Pin Playwright version in pom.xml/build.gradle

## Key Takeaways

- Maven and Gradle both work well with Playwright
- Browsers are installed automatically on first use
- Proper project structure improves maintainability
- Configuration files centralize test settings
- IDE setup is straightforward with proper SDK configuration

## References

- [Playwright Java Installation](https://playwright.dev/java/docs/intro)
- [Maven Getting Started](https://maven.apache.org/guides/getting-started/)
- [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html)
- [Playwright Maven Repository](https://mvnrepository.com/artifact/com.microsoft.playwright/playwright)
