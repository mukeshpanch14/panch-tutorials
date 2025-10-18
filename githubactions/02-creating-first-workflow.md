# Creating Your First Workflow - Deep Dive

## Overview

Creating your first GitHub Actions workflow involves understanding the proper file structure, workflow syntax, and how to debug issues when they arise. This guide walks you through the complete process from creation to troubleshooting.

## File Structure and Conventions

### Directory Structure
```
your-repository/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── security.yml
├── src/
├── tests/
└── README.md
```

### Naming Conventions
- Use descriptive names: `ci.yml`, `deploy-production.yml`
- Use kebab-case for multi-word names: `security-scan.yml`
- Group related workflows: `deploy-staging.yml`, `deploy-production.yml`

## Workflow Structure Breakdown

### Basic Workflow Template
```yaml
name: Workflow Name
on: [trigger-events]
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Step name
        run: command
```

### Required Components

#### 1. Workflow Name
```yaml
name: CI Pipeline
# or
name: Deploy to Production
```

#### 2. Trigger Events
```yaml
# Single event
on: push

# Multiple events
on: [push, pull_request]

# Specific branches
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
```

#### 3. Jobs Definition
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test
```

## Step-by-Step Workflow Creation

### Step 1: Create the Workflows Directory
```bash
mkdir -p .github/workflows
```

### Step 2: Create Your First Workflow File
Create `ci.yml` in `.github/workflows/`:

```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Run linting
        run: npm run lint
```

### Step 3: Commit and Push
```bash
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
git push origin main
```

## Viewing and Debugging Workflows

### GitHub UI Navigation

#### 1. Accessing Workflow Runs
- Go to your repository on GitHub
- Click the "Actions" tab
- Select your workflow from the left sidebar
- Click on a specific run to view details

#### 2. Understanding the Workflow Run Page
- **Status indicators:** Green (success), Red (failure), Yellow (in progress)
- **Job details:** Expand each job to see individual steps
- **Logs:** Click on any step to view detailed logs
- **Artifacts:** Download build outputs or test results

#### 3. Workflow Run Information
```yaml
# Accessible in workflow context
${{ github.run_id }}          # Unique run ID
${{ github.run_number }}      # Sequential run number
${{ github.actor }}           # User who triggered the workflow
${{ github.repository }}      # Repository name
${{ github.ref }}             # Branch or tag ref
```

### Debugging Techniques

#### 1. Enable Debug Logging
Add to your workflow or set as repository secret:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

#### 2. Add Debug Steps
```yaml
- name: Debug information
  run: |
    echo "Repository: ${{ github.repository }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
    echo "Event: ${{ github.event_name }}"
    echo "Working directory: $(pwd)"
    echo "Files in directory:"
    ls -la
```

#### 3. Conditional Steps for Debugging
```yaml
- name: Debug on failure
  if: failure()
  run: |
    echo "Workflow failed. Debug information:"
    echo "Last command exit code: $?"
    # Add specific debug commands
```

## Common Workflow Patterns

### Pattern 1: Multi-Job Workflow
```yaml
name: Full CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build application
        run: npm run build
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy
        run: echo "Deploying to production"
```

### Pattern 2: Matrix Strategy
```yaml
name: Test Matrix

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js ${{ matrix.node-version }} on ${{ matrix.os }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - name: Run tests
        run: npm test
```

### Pattern 3: Environment-Specific Deployment
```yaml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to ${{ github.ref == 'refs/heads/main' && 'Production' || 'Staging' }}
        run: |
          if [ "${{ github.ref }}" = "refs/heads/main" ]; then
            echo "Deploying to production"
          else
            echo "Deploying to staging"
          fi
```

## Troubleshooting Common Issues

### Issue 1: Workflow Not Triggering
**Symptoms:** Workflow doesn't run when expected
**Solutions:**
- Check file location: Must be in `.github/workflows/`
- Verify YAML syntax: Use a YAML validator
- Check trigger conditions: Ensure branch names match exactly
- Verify file extension: Must be `.yml` or `.yaml`

### Issue 2: Permission Denied Errors
**Symptoms:** Steps fail with permission errors
**Solutions:**
```yaml
# Add permissions to workflow
permissions:
  contents: read
  actions: read
  checks: write
```

### Issue 3: Step Timeout
**Symptoms:** Steps fail after 6 hours (default timeout)
**Solutions:**
```yaml
# Set job timeout
jobs:
  long-running-job:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - name: Long running task
        run: your-command
```

### Issue 4: Environment Variables Not Available
**Symptoms:** Variables undefined in steps
**Solutions:**
```yaml
# Define at workflow level
env:
  NODE_ENV: production

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      BUILD_NUMBER: ${{ github.run_number }}
    steps:
      - name: Use environment variable
        run: echo "Environment: $NODE_ENV, Build: $BUILD_NUMBER"
```

## Best Practices

### 1. Use Actions from Official Sources
```yaml
# Good - Official GitHub actions
- uses: actions/checkout@v4
- uses: actions/setup-node@v4

# Avoid - Third-party actions without verification
- uses: some-user/action@v1
```

### 2. Pin Action Versions
```yaml
# Good - Specific version
- uses: actions/checkout@v4.1.1

# Acceptable - Major version
- uses: actions/checkout@v4

# Avoid - Latest or master
- uses: actions/checkout@master
```

### 3. Use Meaningful Step Names
```yaml
# Good
- name: Install production dependencies
  run: npm ci --only=production

# Avoid
- name: Install
  run: npm ci
```

### 4. Handle Failures Gracefully
```yaml
- name: Run tests
  run: npm test
  continue-on-error: true

- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: test-results/
```

## Practical Examples

### Example 1: Node.js Application CI
```yaml
name: Node.js CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Generate coverage report
        run: npm run test:coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
```

### Example 2: Python Application CI
```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linting
        run: |
          flake8 .
          black --check .
      
      - name: Run tests
        run: pytest --cov=src tests/
```

## Key Takeaways

1. **Start Simple:** Begin with basic workflows and add complexity gradually
2. **Test Locally:** Use tools like `act` to test workflows before pushing
3. **Monitor Usage:** Keep track of GitHub Actions minutes consumption
4. **Use Official Actions:** Prefer actions from the GitHub organization
5. **Document Your Workflows:** Add comments explaining complex logic

## References

- [Quickstart for GitHub Actions](https://docs.github.com/en/actions/quickstart)
- [About workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)
- [Managing workflow runs](https://docs.github.com/en/actions/managing-workflow-runs)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
