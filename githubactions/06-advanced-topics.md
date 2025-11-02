# Advanced Topics - Deep Dive

## Overview

Advanced GitHub Actions features enable you to create sophisticated, reusable, and optimized workflows. This guide covers reusable workflows, composite actions, caching strategies, matrix builds, and self-hosted runners for enterprise-scale automation.

## Reusable Workflows

### Understanding Reusable Workflows
Reusable workflows allow you to define a workflow once and use it across multiple repositories or trigger it from other workflows. This promotes consistency and reduces duplication.

### Creating Reusable Workflows

#### 1. Basic Reusable Workflow
```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version to use'
        required: true
        type: string
      test-command:
        description: 'Test command to run'
        required: false
        type: string
        default: 'npm test'
    outputs:
      test-results:
        description: 'Test results artifact name'
        value: ${{ jobs.test.outputs.artifact-name }}

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      artifact-name: ${{ steps.upload.outputs.artifact-name }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ inputs.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: ${{ inputs.test-command }}
      
      - name: Upload test results
        id: upload
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ github.run_id }}
          path: test-results/
```

#### 2. Calling Reusable Workflows
```yaml
# .github/workflows/main-ci.yml
name: Main CI

on: [push, pull_request]

jobs:
  frontend-ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '20'
      test-command: 'npm run test:frontend'
  
  backend-ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '18'
      test-command: 'npm run test:backend'
  
  integration-tests:
    needs: [frontend-ci, backend-ci]
    uses: ./.github/workflows/reusable-ci.yml
    with:
      node-version: '20'
      test-command: 'npm run test:integration'
```

#### 3. Cross-Repository Reusable Workflows
```yaml
# In repository: company/shared-workflows
name: Shared CI

on:
  workflow_call:
    inputs:
      node-version:
        description: 'Node.js version'
        required: true
        type: string
    secrets:
      npm-token:
        description: 'NPM token for publishing'
        required: false

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          registry-url: 'https://registry.npmjs.org'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Publish to NPM
        if: github.ref == 'refs/heads/main'
        env:
          NODE_AUTH_TOKEN: ${{ secrets.npm-token }}
        run: npm publish
```

```yaml
# In your project repository
name: Project CI

on: [push]

jobs:
  ci:
    uses: company/shared-workflows/.github/workflows/shared-ci.yml@main
    with:
      node-version: '20'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

### Advanced Reusable Workflow Patterns

#### 1. Conditional Reusable Workflows
```yaml
# .github/workflows/conditional-deploy.yml
name: Conditional Deploy

on:
  workflow_call:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: string
      skip-tests:
        description: 'Skip tests'
        required: false
        type: boolean
        default: false

jobs:
  test:
    if: ${{ !inputs.skip-tests }}
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test
  
  deploy:
    needs: test
    if: always() && (needs.test.result == 'success' || inputs.skip-tests)
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy to ${{ inputs.environment }}
        run: echo "Deploying to ${{ inputs.environment }}"
```

#### 2. Matrix Reusable Workflows
```yaml
# .github/workflows/matrix-test.yml
name: Matrix Test

on:
  workflow_call:
    inputs:
      test-matrix:
        description: 'JSON string of test matrix'
        required: true
        type: string

jobs:
  test:
    runs-on: ${{ fromJson(inputs.test-matrix).os }}
    strategy:
      matrix:
        node-version: ${{ fromJson(inputs.test-matrix).node-versions }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Run tests
        run: npm test
```

## Composite Actions

### Creating Composite Actions
Composite actions combine multiple run steps into a single reusable action.

#### 1. Basic Composite Action
```yaml
# action.yml
name: 'Setup Development Environment'
description: 'Sets up Node.js, installs dependencies, and runs initial setup'
inputs:
  node-version:
    description: 'Node.js version to install'
    required: true
    default: '20'
  install-command:
    description: 'Command to install dependencies'
    required: false
    default: 'npm ci'
  setup-command:
    description: 'Additional setup command'
    required: false
    default: 'npm run setup'

outputs:
  node-version:
    description: 'The Node.js version that was set up'
    value: ${{ steps.setup-node.outputs.node-version }}

runs:
  using: 'composite'
  steps:
    - name: Setup Node.js ${{ inputs.node-version }}
      id: setup-node
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      shell: bash
      run: ${{ inputs.install-command }}
    
    - name: Run setup
      shell: bash
      run: ${{ inputs.setup-command }}
    
    - name: Verify installation
      shell: bash
      run: |
        echo "Node.js version: $(node --version)"
        echo "NPM version: $(npm --version)"
```

#### 2. Using Composite Actions
```yaml
name: Development Workflow

on: [push]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup development environment
        uses: ./.github/actions/setup-dev
        with:
          node-version: '20'
          install-command: 'npm ci'
          setup-command: 'npm run setup:dev'
      
      - name: Use Node.js version
        run: echo "Using Node.js ${{ steps.setup-dev.outputs.node-version }}"
```

### Advanced Composite Action Patterns

#### 1. Database Setup Composite Action
```yaml
# .github/actions/setup-database/action.yml
name: 'Setup Database'
description: 'Sets up and configures database for testing'

inputs:
  database-type:
    description: 'Type of database to setup'
    required: true
    default: 'postgresql'
  database-version:
    description: 'Database version'
    required: false
    default: '15'

outputs:
  connection-string:
    description: 'Database connection string'
    value: ${{ steps.setup.outputs.connection-string }}

runs:
  using: 'composite'
  steps:
    - name: Setup PostgreSQL
      if: inputs.database-type == 'postgresql'
      shell: bash
      run: |
        echo "Setting up PostgreSQL ${{ inputs.database-version }}"
        # PostgreSQL setup logic
    
    - name: Setup MySQL
      if: inputs.database-type == 'mysql'
      shell: bash
      run: |
        echo "Setting up MySQL ${{ inputs.database-version }}"
        # MySQL setup logic
    
    - name: Generate connection string
      id: setup
      shell: bash
      run: |
        if [ "${{ inputs.database-type }}" = "postgresql" ]; then
          echo "connection-string=postgresql://user:pass@localhost:5432/testdb" >> $GITHUB_OUTPUT
        elif [ "${{ inputs.database-type }}" = "mysql" ]; then
          echo "connection-string=mysql://user:pass@localhost:3306/testdb" >> $GITHUB_OUTPUT
        fi
```

## Caching Strategies

### Understanding GitHub Actions Caching
Caching can significantly speed up workflows by storing and reusing dependencies, build artifacts, and other files.

#### 1. Basic Caching
```yaml
- name: Cache Node.js dependencies
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

#### 2. Advanced Caching Patterns
```yaml
- name: Cache with multiple paths
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache/yarn
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/yarn.lock') }}
    restore-keys: |
      ${{ runner.os }}-deps-
      ${{ runner.os }}-
```

#### 3. Conditional Caching
```yaml
- name: Cache build artifacts
  uses: actions/cache@v4
  with:
    path: dist/
    key: ${{ runner.os }}-build-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-build-
  if: github.event_name == 'pull_request'

- name: Cache build artifacts (push)
  uses: actions/cache@v4
  with:
    path: dist/
    key: ${{ runner.os }}-build-${{ github.ref }}
    restore-keys: |
      ${{ runner.os }}-build-
  if: github.event_name == 'push'
```

### Language-Specific Caching

#### 1. Node.js Caching
```yaml
- name: Setup Node.js with cache
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
    cache-dependency-path: 'package-lock.json'
```

#### 2. Python Caching
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Cache Python packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
```

#### 3. Docker Layer Caching
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build Docker image with cache
  uses: docker/build-push-action@v5
  with:
    context: .
    push: false
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Matrix Strategy Deep Dive

### Advanced Matrix Configurations

#### 1. Include and Exclude Patterns
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node-version: [16, 18, 20]
    include:
      - os: ubuntu-latest
        node-version: 20
        test-group: 'integration'
      - os: windows-latest
        node-version: 18
        test-group: 'unit'
    exclude:
      - os: windows-latest
        node-version: 16
      - os: macos-latest
        node-version: 16
```

#### 2. Dynamic Matrix Generation
```yaml
jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Generate matrix
        id: set-matrix
        run: |
          # Generate matrix based on changed files
          CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)
          MATRIX='{"include":[]}'
          
          if echo "$CHANGED_FILES" | grep -q "frontend/"; then
            MATRIX=$(echo "$MATRIX" | jq '.include += [{"component": "frontend", "test-command": "npm run test:frontend"}]')
          fi
          
          if echo "$CHANGED_FILES" | grep -q "backend/"; then
            MATRIX=$(echo "$MATRIX" | jq '.include += [{"component": "backend", "test-command": "npm run test:backend"}]')
          fi
          
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT
  
  test:
    needs: generate-matrix
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    steps:
      - name: Test ${{ matrix.component }}
        run: ${{ matrix.test-command }}
```

#### 3. Matrix with Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - name: Build for Node ${{ matrix.node-version }}
        run: npm run build
  
  test:
    needs: build
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - name: Test for Node ${{ matrix.node-version }}
        run: npm test
```

## Self-Hosted Runners

### Understanding Self-Hosted Runners
Self-hosted runners allow you to run workflows on your own infrastructure, providing more control over the environment and potentially reducing costs.

#### 1. Basic Self-Hosted Runner Setup
```yaml
# .github/workflows/self-hosted-example.yml
name: Self-Hosted Example

on: [push]

jobs:
  build:
    runs-on: self-hosted
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Build on self-hosted runner
        run: |
          echo "Running on self-hosted runner"
          uname -a
          df -h
```

#### 2. Labeled Self-Hosted Runners
```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
    steps:
      - name: Build on labeled runner
        run: echo "Building on Linux x64 runner"
  
  test:
    runs-on: [self-hosted, windows, x64]
    steps:
      - name: Test on Windows runner
        run: echo "Testing on Windows x64 runner"
```

#### 3. Self-Hosted Runner with Custom Software
```yaml
jobs:
  build:
    runs-on: [self-hosted, gpu]
    steps:
      - name: Build with GPU support
        run: |
          echo "Building with GPU acceleration"
          nvidia-smi
          # GPU-specific build commands
```

### Self-Hosted Runner Security

#### 1. Secure Self-Hosted Runner Configuration
```yaml
jobs:
  secure-build:
    runs-on: [self-hosted, secure]
    environment: production
    steps:
      - name: Secure build
        run: |
          echo "Building in secure environment"
          # Secure build process
```

#### 2. Ephemeral Self-Hosted Runners
```yaml
jobs:
  ephemeral-build:
    runs-on: [self-hosted, ephemeral]
    steps:
      - name: Clean environment
        run: |
          # Clean up any previous state
          docker system prune -f
          rm -rf /tmp/*
      
      - name: Build in clean environment
        run: |
          echo "Building in ephemeral environment"
          # Build process
      
      - name: Cleanup after build
        if: always()
        run: |
          # Clean up after build
          docker system prune -f
```

## Advanced Workflow Patterns

### 1. Workflow Dependencies and Orchestration
```yaml
name: Orchestrated Pipeline

on: [push]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      frontend-changed: ${{ steps.changes.outputs.frontend }}
      backend-changed: ${{ steps.changes.outputs.backend }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Detect changes
        id: changes
        run: |
          CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)
          if echo "$CHANGED_FILES" | grep -q "frontend/"; then
            echo "frontend=true" >> $GITHUB_OUTPUT
          else
            echo "frontend=false" >> $GITHUB_OUTPUT
          fi
          
          if echo "$CHANGED_FILES" | grep -q "backend/"; then
            echo "backend=true" >> $GITHUB_OUTPUT
          else
            echo "backend=false" >> $GITHUB_OUTPUT
          fi
  
  frontend-ci:
    needs: detect-changes
    if: needs.detect-changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Frontend CI
        run: echo "Running frontend CI"
  
  backend-ci:
    needs: detect-changes
    if: needs.detect-changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Backend CI
        run: echo "Running backend CI"
  
  integration-tests:
    needs: [frontend-ci, backend-ci]
    if: always() && (needs.frontend-ci.result == 'success' || needs.frontend-ci.result == 'skipped') && (needs.backend-ci.result == 'success' || needs.backend-ci.result == 'skipped')
    runs-on: ubuntu-latest
    steps:
      - name: Integration tests
        run: echo "Running integration tests"
```

### 2. Dynamic Workflow Generation
```yaml
name: Dynamic Workflow

on:
  workflow_dispatch:
    inputs:
      components:
        description: 'Components to test (comma-separated)'
        required: true
        default: 'frontend,backend'

jobs:
  generate-workflow:
    runs-on: ubuntu-latest
    outputs:
      workflow-config: ${{ steps.config.outputs.workflow }}
    steps:
      - name: Generate workflow configuration
        id: config
        run: |
          COMPONENTS="${{ inputs.components }}"
          CONFIG='{"jobs":{}}'
          
          for component in $(echo "$COMPONENTS" | tr ',' ' '); do
            CONFIG=$(echo "$CONFIG" | jq --arg comp "$component" '.jobs[$comp] = {"runs-on": "ubuntu-latest", "steps": [{"name": "Test " + $comp, "run": "echo Testing " + $comp}]}')
          done
          
          echo "workflow=$CONFIG" >> $GITHUB_OUTPUT
  
  execute-workflow:
    needs: generate-workflow
    runs-on: ubuntu-latest
    steps:
      - name: Execute dynamic workflow
        run: |
          echo "Executing workflow:"
          echo '${{ needs.generate-workflow.outputs.workflow-config }}'
```

## Performance Optimization

### 1. Parallel Job Execution
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Lint code
        run: npm run lint
  
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test
  
  security:
    runs-on: ubuntu-latest
    steps:
      - name: Security scan
        run: npm audit
  
  build:
    needs: [lint, test, security]
    runs-on: ubuntu-latest
    steps:
      - name: Build application
        run: npm run build
```

### 2. Conditional Job Execution
```yaml
jobs:
  quick-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Quick lint check
        run: npm run lint:quick
  
  full-tests:
    needs: quick-checks
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Full test suite
        run: npm test
  
  deploy:
    needs: [quick-checks, full-tests]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: npm run deploy
```

## Key Takeaways

1. **Reusable Workflows:** Create once, use everywhere for consistency
2. **Composite Actions:** Combine multiple steps into reusable actions
3. **Smart Caching:** Use caching to speed up workflows significantly
4. **Matrix Strategy:** Test across multiple environments efficiently
5. **Self-Hosted Runners:** Use for specialized environments or cost optimization
6. **Performance First:** Design workflows for speed and efficiency
7. **Security:** Implement proper security practices for all advanced features

## References

- [Reusing workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Creating a composite action](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
- [Caching dependencies to speed up workflows](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Using a matrix strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-strategy)
- [About self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)

