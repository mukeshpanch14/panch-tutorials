# Secrets & Security - Deep Dive

## Overview

Security is paramount in CI/CD pipelines. GitHub Actions provides robust mechanisms for managing secrets, securing workflows, and implementing security best practices. This guide covers everything from basic secret management to advanced security hardening techniques.

## Understanding GitHub Secrets

### Types of Secrets

#### 1. Repository Secrets
- **Scope:** Available to all workflows in a specific repository
- **Access:** Repository administrators can manage
- **Use case:** API keys, database credentials, deployment tokens

#### 2. Environment Secrets
- **Scope:** Available only to workflows using specific environments
- **Access:** Environment-specific permissions
- **Use case:** Environment-specific configurations (staging vs production)

#### 3. Organization Secrets
- **Scope:** Available to all repositories in an organization
- **Access:** Organization administrators
- **Use case:** Shared services, organization-wide API keys

#### 4. GitHub Token (GITHUB_TOKEN)
- **Scope:** Automatically provided for each workflow run
- **Access:** Limited to repository permissions
- **Use case:** Interacting with GitHub API, creating releases, managing issues

### Secret Management Best Practices

#### 1. Principle of Least Privilege
```yaml
# Good - Use environment-specific secrets
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        env:
          API_KEY: ${{ secrets.STAGING_API_KEY }}
        run: deploy-staging.sh

  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: deploy-production.sh
```

#### 2. Secret Rotation
```yaml
# Implement secret rotation in workflows
- name: Rotate API key
  env:
    OLD_API_KEY: ${{ secrets.API_KEY }}
    NEW_API_KEY: ${{ secrets.NEW_API_KEY }}
  run: |
    # Deploy with new key
    deploy-with-key.sh $NEW_API_KEY
    # Verify deployment
    verify-deployment.sh
    # Update secret (requires manual intervention)
    echo "Please update API_KEY secret with NEW_API_KEY value"
```

## Secure Secret Usage Patterns

### Environment Variables
```yaml
name: Secure Deployment

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Deploy with secrets
        env:
          # Never log these values
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_SECRET: ${{ secrets.API_SECRET }}
        run: |
          # Secrets are available as environment variables
          echo "Deploying with secure credentials..."
          # Your deployment script here
```

### Conditional Secret Usage
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        env:
          API_KEY: ${{ secrets.STAGING_API_KEY }}
        run: deploy.sh staging
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: deploy.sh production
```

### Secret Validation
```yaml
- name: Validate secrets
  env:
    REQUIRED_SECRET: ${{ secrets.REQUIRED_SECRET }}
  run: |
    if [ -z "$REQUIRED_SECRET" ]; then
      echo "Error: REQUIRED_SECRET is not set"
      exit 1
    fi
    echo "Secret validation passed"
```

## GitHub Token Security

### Understanding GITHUB_TOKEN Permissions
```yaml
# Default permissions (read-only for contents)
permissions:
  contents: read

# Expanded permissions for specific use cases
permissions:
  contents: read
  issues: write
  pull-requests: write
  statuses: write
  packages: write
```

### Secure GitHub Token Usage
```yaml
name: Secure GitHub Operations

on: [push]

jobs:
  create-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: read
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Create release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: Release v${{ github.run_number }}
          body: |
            Automated release from workflow run ${{ github.run_number }}
          draft: false
          prerelease: false
```

### Personal Access Tokens (PATs)
```yaml
# Use PATs for cross-repository access
- name: Access other repository
  env:
    PAT: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
  run: |
    # Use PAT for cross-repo operations
    git clone https://$PAT@github.com/other-org/other-repo.git
```

## Action Security and Pinning

### Pinning Actions to Commit SHAs
```yaml
# Most secure - pin to specific commit SHA
- name: Checkout code
  uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3

# Good - pin to specific version
- name: Setup Node.js
  uses: actions/setup-node@v4.0.0

# Avoid - using latest or master
- name: Bad practice
  uses: actions/checkout@master
```

### Action Security Verification
```yaml
# Verify action integrity
- name: Verify action
  run: |
    # Check action source and maintainer
    echo "Verifying action: actions/checkout@v4"
    # Add verification logic here
```

### Custom Action Security
```yaml
# Secure custom action usage
- name: Use custom action
  uses: your-org/secure-action@v1.0.0
  with:
    input1: ${{ secrets.SECURE_INPUT }}
```

## Environment Security

### Environment Protection Rules
```yaml
# Environment with protection rules
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: 
      name: production
      url: https://myapp.com
    steps:
      - name: Deploy to production
        run: echo "Deploying to production"
```

### Environment-Specific Secrets
```yaml
# Different secrets per environment
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        env:
          API_URL: https://api-staging.example.com
          API_KEY: ${{ secrets.STAGING_API_KEY }}
        run: deploy.sh

  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        env:
          API_URL: https://api.example.com
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: deploy.sh
```

## Security Hardening Techniques

### Workflow Security Settings
```yaml
name: Secure Workflow

on: [push]

# Restrict workflow to specific branches
jobs:
  secure-job:
    runs-on: ubuntu-latest
    
    # Set job-level permissions
    permissions:
      contents: read
      actions: read
    
    steps:
      - name: Secure step
        run: echo "Secure operation"
```

### Input Validation and Sanitization
```yaml
name: Input Validation

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Validate input
        run: |
          ENV="${{ inputs.environment }}"
          if [[ "$ENV" != "staging" && "$ENV" != "production" ]]; then
            echo "Error: Invalid environment '$ENV'"
            exit 1
          fi
          echo "Valid environment: $ENV"
```

### Secure File Handling
```yaml
- name: Handle sensitive files
  run: |
    # Create temporary file with restricted permissions
    TEMP_FILE=$(mktemp)
    chmod 600 "$TEMP_FILE"
    
    # Write sensitive data
    echo "${{ secrets.SENSITIVE_DATA }}" > "$TEMP_FILE"
    
    # Use the file
    process-sensitive-file.sh "$TEMP_FILE"
    
    # Clean up
    rm -f "$TEMP_FILE"
```

## Common Security Pitfalls

### 1. Logging Secrets
```yaml
# Bad - secrets might be logged
- name: Bad practice
  run: |
    echo "API Key: ${{ secrets.API_KEY }}"
    curl -H "Authorization: Bearer ${{ secrets.API_KEY }}" https://api.example.com

# Good - use environment variables
- name: Good practice
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    curl -H "Authorization: Bearer $API_KEY" https://api.example.com
```

### 2. Using Unpinned Actions
```yaml
# Bad - using latest version
- uses: actions/checkout@master

# Good - pin to specific version
- uses: actions/checkout@v4.1.1
```

### 3. Overly Broad Permissions
```yaml
# Bad - too many permissions
permissions:
  contents: write
  issues: write
  pull-requests: write
  packages: write
  actions: write

# Good - minimal required permissions
permissions:
  contents: read
```

### 4. Hardcoded Credentials
```yaml
# Bad - hardcoded credentials
- name: Bad practice
  run: |
    curl -u "user:password" https://api.example.com

# Good - use secrets
- name: Good practice
  env:
    USERNAME: ${{ secrets.API_USERNAME }}
    PASSWORD: ${{ secrets.API_PASSWORD }}
  run: |
    curl -u "$USERNAME:$PASSWORD" https://api.example.com
```

## Advanced Security Patterns

### Secret Injection at Runtime
```yaml
- name: Inject secrets at runtime
  run: |
    # Create secure configuration file
    cat > config.json << EOF
    {
      "api_key": "${{ secrets.API_KEY }}",
      "database_url": "${{ secrets.DATABASE_URL }}"
    }
    EOF
    
    # Set restrictive permissions
    chmod 600 config.json
    
    # Use configuration
    app --config config.json
    
    # Clean up
    rm -f config.json
```

### Multi-Factor Authentication for Deployments
```yaml
name: Secure Deployment

on:
  workflow_dispatch:
    inputs:
      mfa_token:
        description: 'MFA Token'
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Validate MFA token
        env:
          MFA_TOKEN: ${{ inputs.mfa_token }}
          EXPECTED_TOKEN: ${{ secrets.MFA_SECRET }}
        run: |
          if [ "$MFA_TOKEN" != "$EXPECTED_TOKEN" ]; then
            echo "Invalid MFA token"
            exit 1
          fi
          echo "MFA validation successful"
      
      - name: Deploy
        run: echo "Deploying with valid MFA"
```

### Secret Rotation Workflow
```yaml
name: Secret Rotation

on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly
  workflow_dispatch:

jobs:
  rotate-secrets:
    runs-on: ubuntu-latest
    steps:
      - name: Generate new API key
        id: generate_key
        run: |
          NEW_KEY=$(openssl rand -hex 32)
          echo "new_key=$NEW_KEY" >> $GITHUB_OUTPUT
      
      - name: Update API key
        env:
          NEW_KEY: ${{ steps.generate_key.outputs.new_key }}
          OLD_KEY: ${{ secrets.API_KEY }}
        run: |
          # Update API key in external service
          update-api-key.sh "$NEW_KEY"
          
          # Verify new key works
          verify-api-key.sh "$NEW_KEY"
          
          echo "Please update API_KEY secret with: $NEW_KEY"
          echo "Old key: $OLD_KEY"
```

## Security Monitoring and Auditing

### Workflow Security Logging
```yaml
- name: Security audit log
  run: |
    echo "Workflow: ${{ github.workflow }}"
    echo "Actor: ${{ github.actor }}"
    echo "Repository: ${{ github.repository }}"
    echo "Ref: ${{ github.ref }}"
    echo "Event: ${{ github.event_name }}"
    echo "Timestamp: $(date -u)"
    
    # Log to security monitoring system
    curl -X POST "${{ secrets.SECURITY_WEBHOOK }}" \
      -H "Content-Type: application/json" \
      -d '{
        "workflow": "${{ github.workflow }}",
        "actor": "${{ github.actor }}",
        "repository": "${{ github.repository }}",
        "timestamp": "'$(date -u -Iseconds)'"
      }'
```

### Failed Workflow Notifications
```yaml
- name: Notify on failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '🚨 Security workflow failed. Please investigate immediately.'
      });
```

## Practical Examples

### Example 1: Secure API Deployment
```yaml
name: Secure API Deployment

on:
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run security scan
        run: |
          # Run SAST tools
          npm audit
          # Run dependency check
          npx audit-ci --config audit-ci.json
      
      - name: Upload security report
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: security-report.json
  
  deploy:
    needs: security-scan
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      packages: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Build application
        run: |
          npm ci
          npm run build
      
      - name: Deploy to production
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
          DATABASE_URL: ${{ secrets.PRODUCTION_DATABASE_URL }}
          JWT_SECRET: ${{ secrets.JWT_SECRET }}
        run: |
          # Deploy with secure environment variables
          docker build -t myapp:${{ github.sha }} .
          docker run -d \
            -e API_KEY="$API_KEY" \
            -e DATABASE_URL="$DATABASE_URL" \
            -e JWT_SECRET="$JWT_SECRET" \
            myapp:${{ github.sha }}
      
      - name: Verify deployment
        env:
          API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: |
          # Verify deployment is working
          sleep 30
          curl -H "Authorization: Bearer $API_KEY" \
            https://api.example.com/health
```

### Example 2: Multi-Environment Security
```yaml
name: Multi-Environment Security

on:
  push:
    branches: [develop, main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup environment-specific configuration
        run: |
          if [ "${{ github.ref }}" = "refs/heads/main" ]; then
            echo "ENVIRONMENT=production" >> $GITHUB_ENV
            echo "API_URL=https://api.production.com" >> $GITHUB_ENV
            echo "LOG_LEVEL=warn" >> $GITHUB_ENV
          else
            echo "ENVIRONMENT=staging" >> $GITHUB_ENV
            echo "API_URL=https://api.staging.com" >> $GITHUB_ENV
            echo "LOG_LEVEL=debug" >> $GITHUB_ENV
          fi
      
      - name: Deploy with environment-specific secrets
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          ENCRYPTION_KEY: ${{ secrets.ENCRYPTION_KEY }}
        run: |
          # Create secure configuration
          cat > app-config.json << EOF
          {
            "environment": "${{ env.ENVIRONMENT }}",
            "api_url": "${{ env.API_URL }}",
            "log_level": "${{ env.LOG_LEVEL }}",
            "api_key": "$API_KEY",
            "database_url": "$DATABASE_URL",
            "encryption_key": "$ENCRYPTION_KEY"
          }
          EOF
          
          # Deploy with secure configuration
          deploy-app.sh app-config.json
          
          # Clean up configuration file
          rm -f app-config.json
```

## Key Takeaways

1. **Never Log Secrets:** Always use environment variables for sensitive data
2. **Pin Action Versions:** Use specific versions, never `@master` or `@latest`
3. **Minimal Permissions:** Grant only the permissions needed for each job
4. **Environment Isolation:** Use different secrets for different environments
5. **Regular Rotation:** Implement secret rotation policies
6. **Monitor Access:** Log and monitor secret usage
7. **Validate Inputs:** Always validate and sanitize workflow inputs
8. **Secure Cleanup:** Clean up temporary files containing sensitive data

## References

- [Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Automatic token authentication](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)
- [Using environments for deployment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Keeping your GitHub Actions and workflows secure](https://docs.github.com/en/actions/security-guides/keeping-your-github-actions-and-workflows-secure)
