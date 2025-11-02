# Working with Actions - Deep Dive

## Overview

Actions are the building blocks of GitHub Actions workflows. They are reusable units of code that perform specific tasks, from checking out code to deploying applications. Understanding how to use existing actions and create custom ones is essential for effective workflow automation.

## Understanding Actions

### What Are Actions?
Actions are portable units of code that can be:
- **JavaScript actions:** Run directly on the runner using Node.js
- **Docker actions:** Run in a Docker container
- **Composite actions:** Combine multiple run steps into a single action

### Action Types Comparison

| Type | Use Case | Performance | Dependencies |
|------|----------|-------------|--------------|
| JavaScript | Simple tasks, file operations | Fast | Node.js only |
| Docker | Complex environments, specific tools | Slower startup | Full container |
| Composite | Combining multiple steps | Fast | Any available tools |

## Using Marketplace Actions

### Finding Quality Actions

#### 1. Official GitHub Actions
Always prefer actions from the `actions` organization:
```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
- uses: actions/upload-artifact@v4
```

#### 2. Verified Actions
Look for actions with:
- High star count and recent updates
- Clear documentation and examples
- Active maintenance and community support
- Proper versioning (not using `@master`)

#### 3. Action Marketplace Search
- Use specific keywords: "node", "docker", "deploy"
- Filter by category: CI, Deployment, Utilities
- Check the "Verified creator" badge

### Using Actions Effectively

#### Basic Usage
```yaml
- name: Checkout code
  uses: actions/checkout@v4

- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

#### Advanced Usage with Inputs
```yaml
- name: Deploy to AWS
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Upload to S3
  uses: aws-actions/amazon-s3-deploy@v1
  with:
    args: --delete --follow-symlinks
    file: ./dist
    bucket: my-bucket
    destination: my-app
```

#### Using Action Outputs
```yaml
- name: Get version
  id: get_version
  uses: actions/github-script@v7
  with:
    script: |
      const version = require('./package.json').version;
      return { version };

- name: Use version
  run: echo "Version is ${{ steps.get_version.outputs.version }}"
```

## Creating Custom Actions

### JavaScript Actions

#### 1. Action Structure
```
my-action/
├── action.yml
├── index.js
├── package.json
└── README.md
```

#### 2. Action Metadata (action.yml)
```yaml
name: 'My Custom Action'
description: 'A custom action that does something useful'
inputs:
  input1:
    description: 'First input parameter'
    required: true
  input2:
    description: 'Second input parameter'
    required: false
    default: 'default-value'
outputs:
  output1:
    description: 'First output value'
runs:
  using: 'node20'
  main: 'index.js'
```

#### 3. Action Implementation (index.js)
```javascript
const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // Get inputs
    const input1 = core.getInput('input1');
    const input2 = core.getInput('input2');
    
    // Process inputs
    const result = processInputs(input1, input2);
    
    // Set outputs
    core.setOutput('output1', result);
    
    // Log information
    core.info(`Processed: ${input1} with ${input2}`);
    
  } catch (error) {
    core.setFailed(error.message);
  }
}

function processInputs(input1, input2) {
  // Your custom logic here
  return `${input1}-${input2}`;
}

run();
```

#### 4. Package Configuration (package.json)
```json
{
  "name": "my-custom-action",
  "version": "1.0.0",
  "description": "A custom GitHub Action",
  "main": "index.js",
  "dependencies": {
    "@actions/core": "^1.10.0",
    "@actions/github": "^6.0.0"
  }
}
```

### Docker Actions

#### 1. Docker Action Structure
```
docker-action/
├── action.yml
├── Dockerfile
└── entrypoint.sh
```

#### 2. Action Metadata for Docker
```yaml
name: 'Docker Action'
description: 'A custom Docker-based action'
inputs:
  input1:
    description: 'Input parameter'
    required: true
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.input1 }}
```

#### 3. Dockerfile
```dockerfile
FROM alpine:3.18

# Install required tools
RUN apk add --no-cache curl jq

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
```

#### 4. Entrypoint Script
```bash
#!/bin/sh

# Get input
INPUT1=$1

# Process input
echo "Processing: $INPUT1"

# Perform action
curl -s "https://api.example.com/process" \
  -H "Content-Type: application/json" \
  -d "{\"input\": \"$INPUT1\"}" \
  | jq -r '.result'
```

### Composite Actions

#### 1. Composite Action Structure
```
composite-action/
├── action.yml
└── README.md
```

#### 2. Composite Action Metadata
```yaml
name: 'Composite Action'
description: 'Combines multiple steps into one action'
inputs:
  node-version:
    description: 'Node.js version to use'
    required: true
    default: '20'
outputs:
  node-version:
    description: 'The Node.js version that was set up'
    value: ${{ steps.setup-node.outputs.node-version }}
runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      id: setup-node
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    
    - name: Install dependencies
      shell: bash
      run: npm ci
    
    - name: Run tests
      shell: bash
      run: npm test
```

## Publishing Reusable Actions

### Publishing to GitHub

#### 1. Create a New Repository
- Repository name: `action-name`
- Make it public for marketplace visibility
- Add appropriate topics and description

#### 2. Version Your Action
```bash
# Create a tag for versioning
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### 3. Publish to Marketplace
- Go to your repository on GitHub
- Click "Actions" tab
- Click "Draft a release"
- Fill in release details
- Check "Publish this Action to the GitHub Marketplace"

### Using Your Published Action
```yaml
- name: Use my custom action
  uses: your-username/action-name@v1.0.0
  with:
    input1: 'value'
```

## Best Practices for Actions

### 1. Input Validation
```javascript
const input1 = core.getInput('input1');
if (!input1) {
  core.setFailed('input1 is required');
  return;
}
```

### 2. Error Handling
```javascript
try {
  // Action logic
} catch (error) {
  core.setFailed(`Action failed: ${error.message}`);
}
```

### 3. Proper Logging
```javascript
core.info('Starting action...');
core.debug('Debug information');
core.warning('Warning message');
core.error('Error message');
```

### 4. Security Considerations
- Never log sensitive inputs
- Use secrets for credentials
- Pin dependencies to specific versions
- Scan for vulnerabilities

## Common Pitfalls

### 1. Not Pinning Action Versions
```yaml
# Bad
- uses: actions/checkout@master

# Good
- uses: actions/checkout@v4.1.1
```

### 2. Missing Required Inputs
```yaml
# Bad - missing required input
- uses: actions/setup-node@v4

# Good
- uses: actions/setup-node@v4
  with:
    node-version: '20'
```

### 3. Not Handling Action Failures
```yaml
# Bad - workflow continues on failure
- name: Run tests
  uses: my-action@v1
  continue-on-error: true

# Good - handle failures explicitly
- name: Run tests
  uses: my-action@v1

- name: Upload results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: results/
```

## Practical Examples

### Example 1: Custom JavaScript Action
```yaml
# action.yml
name: 'Generate Release Notes'
description: 'Generates release notes from commits'
inputs:
  from-tag:
    description: 'Previous tag'
    required: true
  to-tag:
    description: 'Current tag'
    required: true
outputs:
  release-notes:
    description: 'Generated release notes'
runs:
  using: 'node20'
  main: 'index.js'
```

```javascript
// index.js
const core = require('@actions/core');
const { execSync } = require('child_process');

async function run() {
  try {
    const fromTag = core.getInput('from-tag');
    const toTag = core.getInput('to-tag');
    
    // Get commits between tags
    const commits = execSync(
      `git log ${fromTag}..${toTag} --oneline --pretty=format:"- %s"`
    ).toString();
    
    const releaseNotes = `## Changes from ${fromTag} to ${toTag}\n\n${commits}`;
    
    core.setOutput('release-notes', releaseNotes);
    core.info('Release notes generated successfully');
    
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
```

### Example 2: Custom Docker Action
```yaml
# action.yml
name: 'Security Scan'
description: 'Runs security scan on code'
inputs:
  path:
    description: 'Path to scan'
    required: true
    default: '.'
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.path }}
```

```dockerfile
FROM alpine:3.18

RUN apk add --no-cache \
    git \
    npm \
    python3 \
    py3-pip

# Install security tools
RUN pip3 install bandit safety

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/sh
# entrypoint.sh

SCAN_PATH=$1

echo "Running security scan on: $SCAN_PATH"

# Run bandit for Python security issues
if [ -f "$SCAN_PATH/requirements.txt" ]; then
  echo "Scanning Python dependencies..."
  bandit -r "$SCAN_PATH" || true
  safety check -r "$SCAN_PATH/requirements.txt" || true
fi

# Run npm audit for Node.js
if [ -f "$SCAN_PATH/package.json" ]; then
  echo "Scanning Node.js dependencies..."
  cd "$SCAN_PATH" && npm audit || true
fi

echo "Security scan completed"
```

### Example 3: Composite Action for Testing
```yaml
# action.yml
name: 'Test Suite'
description: 'Runs comprehensive test suite'
inputs:
  test-command:
    description: 'Test command to run'
    required: true
    default: 'npm test'
  coverage-threshold:
    description: 'Coverage threshold percentage'
    required: false
    default: '80'
runs:
  using: 'composite'
  steps:
    - name: Install dependencies
      shell: bash
      run: npm ci
    
    - name: Run linting
      shell: bash
      run: npm run lint
    
    - name: Run tests
      shell: bash
      run: ${{ inputs.test-command }}
    
    - name: Check coverage
      shell: bash
      run: |
        COVERAGE=$(npm run test:coverage -- --coverageReporters=text-summary | grep -o '[0-9]*\.[0-9]*%' | head -1 | sed 's/%//')
        if (( $(echo "$COVERAGE < ${{ inputs.coverage-threshold }}" | bc -l) )); then
          echo "Coverage $COVERAGE% is below threshold ${{ inputs.coverage-threshold }}%"
          exit 1
        fi
        echo "Coverage $COVERAGE% meets threshold ${{ inputs.coverage-threshold }}%"
```

## Key Takeaways

1. **Use Official Actions:** Prefer actions from the `actions` organization
2. **Pin Versions:** Always use specific versions, never `@master`
3. **Validate Inputs:** Check required inputs and provide meaningful error messages
4. **Handle Errors:** Implement proper error handling and logging
5. **Security First:** Never expose sensitive data in logs or outputs
6. **Document Well:** Provide clear documentation and examples
7. **Test Thoroughly:** Test your actions in various scenarios

## References

- [About custom actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions)
- [Creating a JavaScript action](https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action)
- [Creating a Docker container action](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
- [Creating a composite action](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [Publishing actions in GitHub Marketplace](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace)

