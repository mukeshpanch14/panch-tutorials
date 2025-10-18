# Introduction & Fundamentals - Deep Dive

## Overview

GitHub Actions is a continuous integration and continuous deployment (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. Understanding the fundamental building blocks is crucial for creating effective automation workflows.

## Core Components Explained

### Workflows
A workflow is an automated process that runs one or more jobs. It's defined by a YAML file in your repository's `.github/workflows` directory.

**Key characteristics:**
- Triggered by events (push, pull request, schedule, etc.)
- Can contain multiple jobs that run in parallel or sequence
- Defined using YAML syntax

### Jobs
Jobs are a set of steps that execute on the same runner. Each job runs in a fresh virtual environment.

**Important concepts:**
- Jobs run in parallel by default
- Can have dependencies using `needs` keyword
- Each job runs on a separate runner instance

### Steps
Steps are individual tasks that can run commands or use actions. They execute in order within a job.

**Types of steps:**
- **Run commands:** Execute shell commands
- **Use actions:** Reusable units of code from the marketplace or custom actions

### Actions
Actions are reusable units of code that perform specific tasks. They can be:
- **JavaScript actions:** Run directly on the runner
- **Docker actions:** Run in a Docker container
- **Composite actions:** Combine multiple run steps

### Runners
Runners are servers that execute your workflows. GitHub provides hosted runners, or you can host your own.

**Hosted runners include:**
- Ubuntu Linux, Windows, and macOS
- Various software pre-installed
- 2-core CPU, 7 GB RAM, 14 GB SSD

## Common Triggers Deep Dive

### Push Events
```yaml
on:
  push:
    branches: [ main, develop ]
    paths: [ 'src/**', 'tests/**' ]
    paths-ignore: [ 'docs/**' ]
```

**Use cases:**
- Run tests on every code change
- Deploy to staging environment
- Update documentation

### Pull Request Events
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [ main ]
```

**Use cases:**
- Run tests before merging
- Check code quality
- Generate preview deployments

### Schedule Events
```yaml
on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
```

**Use cases:**
- Run security scans
- Generate reports
- Clean up old resources

### Workflow Dispatch
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
```

**Use cases:**
- Manual deployments
- Emergency rollbacks
- Testing workflows

## YAML Structure Best Practices

### Proper Indentation
```yaml
name: My Workflow
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
```

### Environment Variables
```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      BUILD_NUMBER: ${{ github.run_number }}
    steps:
      - name: Build
        run: npm run build
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

## Common Pitfalls

### 1. Incorrect YAML Indentation
**Problem:** YAML is sensitive to indentation. Mixing tabs and spaces causes failures.
**Solution:** Use 2 spaces consistently for indentation.

### 2. Missing Required Fields
**Problem:** Forgetting required fields like `runs-on` in jobs.
**Solution:** Always include `name`, `on`, `jobs`, and `runs-on` for each job.

### 3. Using Outdated Action Versions
**Problem:** Using `@v1` or `@master` instead of specific versions.
**Solution:** Pin to specific versions like `@v4` for stability.

## Best Practices

### 1. Use Specific Action Versions
```yaml
# Good
- uses: actions/checkout@v4

# Avoid
- uses: actions/checkout@master
```

### 2. Name Your Workflows and Steps
```yaml
name: CI Pipeline
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Install dependencies
        run: npm ci
```

### 3. Use Environment Variables for Configuration
```yaml
env:
  NODE_VERSION: '20'
  TEST_TIMEOUT: '30000'
```

### 4. Organize Workflows by Purpose
- `ci.yml` - Continuous Integration
- `deploy.yml` - Deployment
- `security.yml` - Security scans

## Practical Examples

### Example 1: Basic Node.js CI
```yaml
name: Node.js CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Run linting
      run: npm run lint
```

### Example 2: Multi-Environment Deployment
```yaml
name: Deploy
on:
  push:
    branches: [ main, develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to ${{ github.ref == 'refs/heads/main' && 'Production' || 'Staging' }}
      run: |
        echo "Deploying to ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}"
        # Your deployment commands here
```

## Key Takeaways

1. **Start Simple:** Begin with basic workflows and gradually add complexity
2. **Use Official Actions:** Prefer actions from the GitHub organization
3. **Test Locally:** Use `act` tool to test workflows locally
4. **Monitor Usage:** Keep track of your GitHub Actions minutes
5. **Security First:** Always use secrets for sensitive data

## References

- [Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)
- [Virtual environments for GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
