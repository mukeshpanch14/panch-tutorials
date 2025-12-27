# File Operations and Downloads - Deep Dive

## Overview

This module covers handling file uploads, downloads, screenshots, and PDF generation in Playwright. These operations are essential for testing file-based features and capturing test evidence.

## File Uploads

### Basic File Upload

```java
// Upload single file
page.setInputFiles("input[type='file']", Paths.get("path/to/file.pdf"));

// Upload with options
page.setInputFiles("input[type='file']", 
    new Page.SetInputFilesOptions()
        .setFiles(Paths.get("path/to/file.pdf")));
```

### Multiple File Upload

```java
// Upload multiple files
page.setInputFiles("input[type='file']", 
    new Path[] {
        Paths.get("path/to/file1.pdf"),
        Paths.get("path/to/file2.pdf"),
        Paths.get("path/to/file3.pdf")
    });
```

### File Upload Examples

```java
// Example: Upload profile picture
public void uploadProfilePicture(String filePath) {
    page.navigate("https://example.com/profile");
    page.setInputFiles("input[type='file']", Paths.get(filePath));
    page.click("button[type='submit']");
    page.waitForSelector(".success-message");
}

// Example: Upload multiple documents
public void uploadDocuments(String[] filePaths) {
    page.navigate("https://example.com/upload");
    Path[] paths = Arrays.stream(filePaths)
        .map(Paths::get)
        .toArray(Path[]::new);
    page.setInputFiles("input[type='file']", paths);
    page.click("button[type='submit']");
}

// Example: Clear file input
public void clearFileInput() {
    page.setInputFiles("input[type='file']", new Path[0]);
}
```

## File Downloads

### Basic File Download

```java
// Wait for download
Download download = page.waitForDownload(() -> {
    page.click("a.download-link");
});

// Save downloaded file
download.saveAs(Paths.get("downloaded-file.pdf"));

// Get download information
String url = download.url();
String suggestedFilename = download.suggestedFilename();
String path = download.path().toString();
```

### Download Examples

```java
// Example: Download file
public void downloadFile(String downloadLinkSelector, String savePath) {
    Download download = page.waitForDownload(() -> {
        page.click(downloadLinkSelector);
    });
    
    download.saveAs(Paths.get(savePath));
    
    // Verify file exists
    Assertions.assertTrue(Files.exists(Paths.get(savePath)));
}

// Example: Download and verify
public void downloadAndVerify(String downloadLinkSelector) {
    Download download = page.waitForDownload(() -> {
        page.click(downloadLinkSelector);
    });
    
    String filename = download.suggestedFilename();
    Path savePath = Paths.get("downloads/" + filename);
    download.saveAs(savePath);
    
    // Verify file
    Assertions.assertTrue(Files.exists(savePath));
    Assertions.assertTrue(Files.size(savePath) > 0);
}

// Example: Download with timeout
public void downloadWithTimeout(String downloadLinkSelector, int timeout) {
    Download download = page.waitForDownload(
        new Page.WaitForDownloadOptions().setTimeout(timeout),
        () -> {
            page.click(downloadLinkSelector);
        }
    );
    
    download.saveAs(Paths.get("downloaded-file.pdf"));
}
```

### Download Event Handling

```java
// Listen to download events
page.onDownload(download -> {
    System.out.println("Download started: " + download.suggestedFilename());
    System.out.println("Download URL: " + download.url());
    
    // Save download
    download.saveAs(Paths.get("downloads/" + download.suggestedFilename()));
});
```

## Screenshots

### Full Page Screenshots

```java
// Full page screenshot
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("screenshot.png")));

// Full page screenshot with options
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("screenshot.png"))
    .setFullPage(true)
    .setQuality(90));
```

### Element Screenshots

```java
// Screenshot of specific element
page.locator(".element").screenshot(
    new Locator.ScreenshotOptions()
        .setPath(Paths.get("element-screenshot.png")));

// Screenshot with options
page.locator(".element").screenshot(
    new Locator.ScreenshotOptions()
        .setPath(Paths.get("element-screenshot.png"))
        .setQuality(90));
```

### Screenshot Examples

```java
// Example: Take screenshot on failure
public void takeScreenshotOnFailure(String testName) {
    try {
        // Test code
        page.click("button");
    } catch (Exception e) {
        // Take screenshot on failure
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("screenshots/" + testName + "-failure.png"))
            .setFullPage(true));
        throw e;
    }
}

// Example: Screenshot helper
public class ScreenshotHelper {
    private Page page;
    
    public ScreenshotHelper(Page page) {
        this.page = page;
    }
    
    public void takeScreenshot(String name) {
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("screenshots/" + name + ".png"))
            .setFullPage(true));
    }
    
    public void takeElementScreenshot(String selector, String name) {
        page.locator(selector).screenshot(
            new Locator.ScreenshotOptions()
                .setPath(Paths.get("screenshots/" + name + ".png")));
    }
}
```

## PDF Generation

### Generate PDF from Page

```java
// Generate PDF
page.pdf(new Page.PdfOptions()
    .setPath(Paths.get("page.pdf"))
    .setFormat("A4")
    .setPrintBackground(true));

// PDF with options
page.pdf(new Page.PdfOptions()
    .setPath(Paths.get("page.pdf"))
    .setFormat("A4")
    .setPrintBackground(true)
    .setMargin(new PdfOptions.Margin()
        .setTop("1cm")
        .setRight("1cm")
        .setBottom("1cm")
        .setLeft("1cm")));
```

### PDF Examples

```java
// Example: Generate PDF
public void generatePdf(String url, String outputPath) {
    page.navigate(url);
    page.waitForLoadState(LoadState.NETWORKIDLE);
    page.pdf(new Page.PdfOptions()
        .setPath(Paths.get(outputPath))
        .setFormat("A4")
        .setPrintBackground(true));
}

// Example: PDF helper
public class PdfHelper {
    private Page page;
    
    public PdfHelper(Page page) {
        this.page = page;
    }
    
    public void generatePdf(String outputPath) {
        page.pdf(new Page.PdfOptions()
            .setPath(Paths.get(outputPath))
            .setFormat("A4")
            .setPrintBackground(true));
    }
    
    public void generatePdfWithMargins(String outputPath) {
        page.pdf(new Page.PdfOptions()
            .setPath(Paths.get(outputPath))
            .setFormat("A4")
            .setPrintBackground(true)
            .setMargin(new PdfOptions.Margin()
                .setTop("1cm")
                .setRight("1cm")
                .setBottom("1cm")
                .setLeft("1cm")));
    }
}
```

## File System Operations

### Reading Files

```java
import java.nio.file.Files;
import java.nio.file.Paths;

// Read file content
String content = Files.readString(Paths.get("path/to/file.txt"));

// Read file as bytes
byte[] bytes = Files.readAllBytes(Paths.get("path/to/file.pdf"));

// Read file line by line
List<String> lines = Files.readAllLines(Paths.get("path/to/file.txt"));
```

### Writing Files

```java
// Write string to file
Files.writeString(Paths.get("path/to/file.txt"), "content");

// Write bytes to file
Files.write(Paths.get("path/to/file.pdf"), bytes);

// Write lines to file
Files.write(Paths.get("path/to/file.txt"), lines);
```

### File System Examples

```java
// Example: Read test data from file
public String readTestData(String filePath) {
    try {
        return Files.readString(Paths.get(filePath));
    } catch (IOException e) {
        throw new RuntimeException("Failed to read file: " + filePath, e);
    }
}

// Example: Write test results to file
public void writeTestResults(String results) {
    try {
        Files.writeString(Paths.get("test-results.txt"), results);
    } catch (IOException e) {
        throw new RuntimeException("Failed to write file", e);
    }
}
```

## Practical Examples

### File Upload Test

```java
public class FileUploadTest extends BaseTest {
    @Test
    void testFileUpload() {
        // Navigate to upload page
        page.navigate("https://example.com/upload");
        
        // Upload file
        page.setInputFiles("input[type='file']", 
            Paths.get("test-data/sample.pdf"));
        
        // Submit form
        page.click("button[type='submit']");
        
        // Wait for success message
        page.waitForSelector(".success-message");
        
        // Verify upload
        String message = page.locator(".success-message").textContent();
        Assertions.assertTrue(message.contains("Upload successful"));
    }
    
    @Test
    void testMultipleFileUpload() {
        // Navigate to upload page
        page.navigate("https://example.com/upload");
        
        // Upload multiple files
        page.setInputFiles("input[type='file']", 
            new Path[] {
                Paths.get("test-data/file1.pdf"),
                Paths.get("test-data/file2.pdf"),
                Paths.get("test-data/file3.pdf")
            });
        
        // Submit form
        page.click("button[type='submit']");
        
        // Verify uploads
        int fileCount = page.locator(".uploaded-file").count();
        Assertions.assertEquals(3, fileCount);
    }
}
```

### File Download Test

```java
public class FileDownloadTest extends BaseTest {
    @Test
    void testFileDownload() {
        // Navigate to download page
        page.navigate("https://example.com/download");
        
        // Download file
        Download download = page.waitForDownload(() -> {
            page.click("a.download-link");
        });
        
        // Save file
        String filename = download.suggestedFilename();
        Path savePath = Paths.get("downloads/" + filename);
        download.saveAs(savePath);
        
        // Verify file exists
        Assertions.assertTrue(Files.exists(savePath));
        Assertions.assertTrue(Files.size(savePath) > 0);
    }
}
```

### Screenshot Test

```java
public class ScreenshotTest extends BaseTest {
    @Test
    void testScreenshot() {
        // Navigate to page
        page.navigate("https://example.com");
        
        // Take full page screenshot
        page.screenshot(new Page.ScreenshotOptions()
            .setPath(Paths.get("screenshots/full-page.png"))
            .setFullPage(true));
        
        // Take element screenshot
        page.locator(".header").screenshot(
            new Locator.ScreenshotOptions()
                .setPath(Paths.get("screenshots/header.png")));
        
        // Verify screenshots exist
        Assertions.assertTrue(Files.exists(Paths.get("screenshots/full-page.png")));
        Assertions.assertTrue(Files.exists(Paths.get("screenshots/header.png")));
    }
}
```

### PDF Generation Test

```java
public class PdfTest extends BaseTest {
    @Test
    void testPdfGeneration() {
        // Navigate to page
        page.navigate("https://example.com");
        page.waitForLoadState(LoadState.NETWORKIDLE);
        
        // Generate PDF
        page.pdf(new Page.PdfOptions()
            .setPath(Paths.get("pdfs/page.pdf"))
            .setFormat("A4")
            .setPrintBackground(true));
        
        // Verify PDF exists
        Assertions.assertTrue(Files.exists(Paths.get("pdfs/page.pdf")));
    }
}
```

## Best Practices

### 1. Organize File Paths

```java
// Good - organized paths
private static final String SCREENSHOTS_DIR = "screenshots/";
private static final String DOWNLOADS_DIR = "downloads/";
private static final String PDFS_DIR = "pdfs/";

// Avoid - hardcoded paths
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("screenshot.png")));
```

### 2. Create Directories

```java
// Good - create directories if they don't exist
Path screenshotsDir = Paths.get("screenshots");
if (!Files.exists(screenshotsDir)) {
    Files.createDirectories(screenshotsDir);
}

// Avoid - assume directories exist
```

### 3. Use Descriptive Filenames

```java
// Good - descriptive filenames
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("screenshots/login-test-failure.png")));

// Avoid - generic filenames
page.screenshot(new Page.ScreenshotOptions()
    .setPath(Paths.get("screenshot.png")));
```

### 4. Clean Up Files

```java
// Good - clean up test files
@AfterEach
void tearDown() {
    // Clean up downloaded files
    try {
        Files.deleteIfExists(Paths.get("downloads/test-file.pdf"));
    } catch (IOException e) {
        // Handle error
    }
}
```

### 5. Verify File Operations

```java
// Good - verify file operations
Download download = page.waitForDownload(() -> {
    page.click("a.download-link");
});
download.saveAs(Paths.get("downloaded-file.pdf"));
Assertions.assertTrue(Files.exists(Paths.get("downloaded-file.pdf")));

// Avoid - no verification
download.saveAs(Paths.get("downloaded-file.pdf"));
```

## Key Takeaways

- File uploads support single and multiple files
- File downloads require waiting for download events
- Screenshots can capture full pages or specific elements
- PDF generation creates printable documents from pages
- File system operations enable reading and writing test data
- Always verify file operations and clean up test files
- Organize file paths and use descriptive filenames

## References

- [Playwright File Operations](https://playwright.dev/java/docs/downloads)
- [Playwright Screenshots](https://playwright.dev/java/docs/screenshots)
- [Playwright PDF Generation](https://playwright.dev/java/docs/pdf)
- [Java NIO File Operations](https://docs.oracle.com/javase/tutorial/essential/io/fileio.html)

