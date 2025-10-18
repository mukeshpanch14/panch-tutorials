# Real-World Use Cases - Deep Dive

## Overview

Real-world GitHub Actions use cases demonstrate practical automation scenarios that solve common development and operational challenges. This guide covers practical examples from code quality automation to deployment pipelines, showing how to implement these solutions effectively.

## Code Quality and Review Automation

### Automated Linting and Formatting

#### 1. Multi-Language Linting Workflow
```yaml
name: Code Quality Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  lint:
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
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Check code formatting
        run: npm run format:check
      
      - name: Run Prettier
        run: npx prettier --check "src/**/*.{js,ts,json,md}"
  
  python-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black isort
      
      - name: Run flake8
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Check Black formatting
        run: black --check .
      
      - name: Check import sorting
        run: isort --check-only .
```

#### 2. Automated Code Formatting with PR Comments
```yaml
name: Auto Format Code

on:
  pull_request:
    branches: [main]

jobs:
  format-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Check formatting
        id: format-check
        run: |
          if ! npm run format:check; then
            echo "needs-formatting=true" >> $GITHUB_OUTPUT
          else
            echo "needs-formatting=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Comment on PR
        if: steps.format-check.outputs.needs-formatting == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🔧 Code Formatting Required
              
              Your code needs formatting. Please run:
              \`\`\`bash
              npm run format
              \`\`\`
              
              Or use your editor's format-on-save feature.`
            })
```

### Automated Testing and Coverage

#### 1. Comprehensive Test Suite
```yaml
name: Comprehensive Testing

on: [push, pull_request]

jobs:
  unit-tests:
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
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          flags: unittests
          name: codecov-umbrella
  
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
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
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
        run: npm run test:integration
  
  e2e-tests:
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
      
      - name: Build application
        run: npm run build
      
      - name: Start application
        run: |
          npm start &
          sleep 10
      
      - name: Run E2E tests
        run: npm run test:e2e
```

#### 2. Test Coverage Reporting
```yaml
name: Coverage Report

on:
  pull_request:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests with coverage
        run: npm run test:coverage
      
      - name: Generate coverage report
        run: |
          npx nyc report --reporter=html
          npx nyc report --reporter=text-summary
      
      - name: Comment coverage on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const coverage = fs.readFileSync('coverage/coverage-summary.txt', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📊 Test Coverage Report
              
              \`\`\`
              ${coverage}
              \`\`\`
              
              [View detailed coverage report](${context.payload.repository.html_url}/actions/runs/${context.runId})`
            })
```

## Package Publishing and Distribution

### NPM Package Publishing

#### 1. Automated NPM Publishing
```yaml
name: Publish to NPM

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build package
        run: npm run build
      
      - name: Publish to NPM
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            ## Changes in this Release
            
            - Automated release from workflow
            - Version: ${{ github.ref }}
            - Commit: ${{ github.sha }}
          draft: false
          prerelease: false
```

#### 2. Multi-Environment Package Publishing
```yaml
name: Multi-Environment Publishing

on:
  push:
    branches: [main, develop]

jobs:
  publish-staging:
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://npm.pkg.github.com'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build package
        run: npm run build
      
      - name: Publish to GitHub Packages (staging)
        run: npm publish --tag beta
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  
  publish-production:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build package
        run: npm run build
      
      - name: Publish to NPM (production)
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Docker Image Publishing

#### 1. Multi-Architecture Docker Builds
```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ secrets.DOCKER_USERNAME }}/myapp
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

#### 2. Security-Scanned Docker Images
```yaml
name: Secure Docker Build

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: myapp:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest
```

## Deployment Automation

### Static Site Deployment

#### 1. GitHub Pages Deployment
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
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
      
      - name: Build site
        run: npm run build
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### 2. Multi-Environment Static Deployment
```yaml
name: Multi-Environment Deployment

on:
  push:
    branches: [main, develop]

jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
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
      
      - name: Build for staging
        run: |
          npm run build:staging
      
      - name: Deploy to staging
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
          destination_dir: staging
      
      - name: Comment deployment URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 **Staging deployment ready!**
              
              Preview: https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/staging/`
            })
  
  deploy-production:
    if: github.ref == 'refs/heads/main'
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
      
      - name: Build for production
        run: |
          npm run build:production
      
      - name: Deploy to production
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### Cloud Platform Deployment

#### 1. AWS S3 + CloudFront Deployment
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
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
      
      - name: Build application
        run: npm run build
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to S3
        run: |
          aws s3 sync dist/ s3://${{ secrets.S3_BUCKET }} --delete
      
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
      
      - name: Notify deployment
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d '{
              "text": "🚀 Application deployed to AWS",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Deployment Successful*\nRepository: ${{ github.repository }}\nBranch: ${{ github.ref_name }}\nCommit: ${{ github.sha }}"
                  }
                }
              ]
            }'
```

#### 2. Kubernetes Deployment
```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
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
      
      - name: Build application
        run: npm run build
      
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_REGISTRY }}/myapp:${{ github.sha }}
      
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'
      
      - name: Deploy to Kubernetes
        run: |
          # Update image tag in deployment
          sed -i "s|IMAGE_TAG|${{ github.sha }}|g" k8s/deployment.yaml
          
          # Apply deployment
          kubectl apply -f k8s/
          
          # Wait for rollout
          kubectl rollout status deployment/myapp
      
      - name: Verify deployment
        run: |
          kubectl get pods -l app=myapp
          kubectl get services -l app=myapp
```

## Notification and Communication

### Slack Integration

#### 1. Comprehensive Slack Notifications
```yaml
name: Slack Notifications

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, closed, merged]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify on push
        if: github.event_name == 'push'
        uses: 8398a7/action-slack@v3
        with:
          status: success
          channel: '#deployments'
          text: |
            🚀 *Deployment Successful*
            Repository: ${{ github.repository }}
            Branch: ${{ github.ref_name }}
            Commit: ${{ github.sha }}
            Actor: ${{ github.actor }}
          fields: repo,message,commit,author,action,eventName,ref,workflow
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      
      - name: Notify on PR
        if: github.event_name == 'pull_request'
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          channel: '#code-review'
          text: |
            📝 *Pull Request ${{ github.event.action }}*
            Repository: ${{ github.repository }}
            PR: #${{ github.event.number }} - ${{ github.event.pull_request.title }}
            Author: ${{ github.event.pull_request.user.login }}
            URL: ${{ github.event.pull_request.html_url }}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### 2. Team-Specific Notifications
```yaml
name: Team Notifications

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]

jobs:
  notify-teams:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion != 'success' }}
    steps:
      - name: Notify frontend team
        if: contains(github.event.workflow_run.head_commit.message, 'frontend')
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          channel: '#frontend-team'
          text: |
            ⚠️ *Frontend CI Failed*
            Repository: ${{ github.repository }}
            Workflow: ${{ github.event.workflow_run.name }}
            Commit: ${{ github.event.workflow_run.head_sha }}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
      
      - name: Notify backend team
        if: contains(github.event.workflow_run.head_commit.message, 'backend')
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          channel: '#backend-team'
          text: |
            ⚠️ *Backend CI Failed*
            Repository: ${{ github.repository }}
            Workflow: ${{ github.event.workflow_run.name }}
            Commit: ${{ github.event.workflow_run.head_sha }}
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Email Notifications

#### 1. Release Notifications
```yaml
name: Release Notifications

on:
  release:
    types: [published]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send release email
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "🎉 New Release: ${{ github.event.release.tag_name }}"
          body: |
            <h2>New Release Published</h2>
            <p><strong>Version:</strong> ${{ github.event.release.tag_name }}</p>
            <p><strong>Repository:</strong> ${{ github.repository }}</p>
            <p><strong>Release Notes:</strong></p>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
              ${{ github.event.release.body }}
            </div>
            <p><a href="${{ github.event.release.html_url }}">View Release on GitHub</a></p>
          to: ${{ secrets.RELEASE_NOTIFICATION_EMAIL }}
          from: GitHub Actions
          content_type: text/html
```

## Automation and Maintenance

### Dependency Management

#### 1. Automated Dependency Updates
```yaml
name: Dependency Updates

on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM
  workflow_dispatch:

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: Update dependencies
        run: |
          npm update
          npm audit fix
      
      - name: Check for changes
        id: changes
        run: |
          if git diff --quiet package*.json; then
            echo "has-changes=false" >> $GITHUB_OUTPUT
          else
            echo "has-changes=true" >> $GITHUB_OUTPUT
          fi
      
      - name: Create PR
        if: steps.changes.outputs.has-changes == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'chore: update dependencies'
          title: 'Automated dependency updates'
          body: |
            ## Automated Dependency Updates
            
            This PR contains automated dependency updates.
            
            ### Changes
            - Updated npm dependencies
            - Applied security fixes
            
            ### Testing
            - [ ] Run tests locally
            - [ ] Verify application functionality
          branch: automated-dependency-updates
          delete-branch: true
```

#### 2. Security Vulnerability Scanning
```yaml
name: Security Scan

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run npm audit
        run: |
          npm audit --audit-level=moderate --json > audit-results.json
      
      - name: Check for vulnerabilities
        id: audit
        run: |
          VULNERABILITIES=$(jq '.metadata.vulnerabilities.total' audit-results.json)
          if [ "$VULNERABILITIES" -gt 0 ]; then
            echo "has-vulnerabilities=true" >> $GITHUB_OUTPUT
            echo "vulnerability-count=$VULNERABILITIES" >> $GITHUB_OUTPUT
          else
            echo "has-vulnerabilities=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Create security issue
        if: steps.audit.outputs.has-vulnerabilities == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            const vulnerabilities = ${{ steps.audit.outputs.vulnerability-count }};
            
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `🚨 Security Alert: ${vulnerabilities} vulnerabilities detected`,
              body: `## Security Vulnerability Alert
              
              **Vulnerabilities Found:** ${vulnerabilities}
              **Scan Date:** ${new Date().toISOString()}
              
              Please review the audit results and update dependencies as needed.
              
              ### Next Steps
              1. Review the audit results
              2. Update vulnerable dependencies
              3. Test the application
              4. Close this issue when resolved
              
              ### Audit Results
              \`\`\`json
              ${require('fs').readFileSync('audit-results.json', 'utf8')}
              \`\`\``,
              labels: ['security', 'dependencies', 'automated']
            });
```

### Documentation Automation

#### 1. Automated API Documentation
```yaml
name: Generate API Documentation

on:
  push:
    branches: [main]
    paths: ['src/**/*.js', 'docs/**']

jobs:
  generate-docs:
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
      
      - name: Generate API documentation
        run: |
          npx jsdoc src/ -d docs/api
      
      - name: Deploy documentation
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
          destination_dir: api
```

## Key Takeaways

1. **Automate Everything:** Use GitHub Actions to automate repetitive tasks and improve consistency
2. **Quality First:** Implement comprehensive testing and code quality checks
3. **Security Focus:** Include security scanning and vulnerability management
4. **Communication:** Set up proper notifications for team awareness
5. **Documentation:** Automate documentation generation and updates
6. **Monitoring:** Implement monitoring and alerting for deployments
7. **Maintenance:** Automate dependency updates and maintenance tasks

## References

- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Starter workflows](https://github.com/actions/starter-workflows)
- [GitHub Actions examples](https://docs.github.com/en/actions/examples)
- [Community workflows](https://github.com/actions/starter-workflows/tree/main/ci)
