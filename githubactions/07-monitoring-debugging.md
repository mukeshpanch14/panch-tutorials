# Monitoring & Debugging - Deep Dive

## Overview

Effective monitoring and debugging are crucial for maintaining reliable CI/CD pipelines. GitHub Actions provides comprehensive tools for analyzing workflow performance, troubleshooting issues, and implementing monitoring strategies. This guide covers everything from basic debugging techniques to advanced monitoring solutions.

## Debug Logging and Troubleshooting

### Enabling Debug Logging

#### 1. Repository-Level Debug Logging
```yaml
# Enable debug logging for all workflows
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

jobs:
  debug-job:
    runs-on: ubuntu-latest
    steps:
      - name: Debug step
        run: echo "This will show detailed debug information"
```

#### 2. Workflow-Level Debug Logging
```yaml
name: Debug Workflow

on: [push]

env:
  ACTIONS_STEP_DEBUG: true

jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Debug information
        run: |
          echo "=== Debug Information ==="
          echo "Runner OS: $RUNNER_OS"
          echo "Runner Architecture: $RUNNER_ARCH"
          echo "Runner Name: $RUNNER_NAME"
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Ref: $GITHUB_REF"
          echo "Event: $GITHUB_EVENT_NAME"
          echo "Actor: $GITHUB_ACTOR"
          echo "Workflow: $GITHUB_WORKFLOW"
          echo "Job: $GITHUB_JOB"
          echo "Run ID: $GITHUB_RUN_ID"
          echo "Run Number: $GITHUB_RUN_NUMBER"
```

#### 3. Step-Level Debug Logging
```yaml
- name: Debug specific step
  env:
    ACTIONS_STEP_DEBUG: true
  run: |
    echo "Debug information for this step"
    # Your commands here
```

### Understanding Workflow Logs

#### 1. Log Structure
```
Workflow Run
├── Job 1
│   ├── Step 1: Checkout code
│   ├── Step 2: Setup environment
│   └── Step 3: Run tests
├── Job 2
│   ├── Step 1: Build application
│   └── Step 2: Deploy
└── Job 3
    └── Step 1: Cleanup
```

#### 2. Log Analysis Techniques
```yaml
- name: Analyze logs
  run: |
    echo "=== Workflow Context ==="
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Head Ref: ${{ github.head_ref }}"
    echo "Base Ref: ${{ github.base_ref }}"
    
    echo "=== Environment Variables ==="
    env | sort
    
    echo "=== File System ==="
    pwd
    ls -la
    
    echo "=== Process Information ==="
    ps aux
```

### Common Debugging Patterns

#### 1. Conditional Debugging
```yaml
- name: Debug on failure
  if: failure()
  run: |
    echo "=== Failure Debug Information ==="
    echo "Last command exit code: $?"
    echo "Current directory: $(pwd)"
    echo "Environment variables:"
    env | grep -E "(GITHUB|RUNNER|ACTIONS)"
    
    echo "=== File contents ==="
    find . -name "*.log" -exec echo "=== {} ===" \; -exec cat {} \;
```

#### 2. Debug with Artifacts
```yaml
- name: Collect debug information
  if: always()
  run: |
    mkdir -p debug-info
    
    # Collect system information
    uname -a > debug-info/system.txt
    df -h > debug-info/disk.txt
    free -h > debug-info/memory.txt
    
    # Collect process information
    ps aux > debug-info/processes.txt
    
    # Collect environment
    env > debug-info/environment.txt
    
    # Collect logs
    find . -name "*.log" -exec cp {} debug-info/ \;

- name: Upload debug artifacts
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: debug-info-${{ github.run_id }}
    path: debug-info/
    retention-days: 30
```

#### 3. Interactive Debugging
```yaml
- name: Interactive debugging
  run: |
    echo "Starting interactive debugging session"
    echo "Available commands:"
    echo "  - ls: List files"
    echo "  - cat <file>: Show file contents"
    echo "  - env: Show environment variables"
    echo "  - ps: Show processes"
    
    # Create a debug script
    cat > debug.sh << 'EOF'
    #!/bin/bash
    while true; do
      read -p "debug> " cmd
      case $cmd in
        ls) ls -la ;;
        env) env | sort ;;
        ps) ps aux ;;
        exit) break ;;
        *) echo "Unknown command: $cmd" ;;
      esac
    done
    EOF
    
    chmod +x debug.sh
    # Note: This won't work in non-interactive environments
    # Use for local testing with act
```

## Workflow Annotations and Notifications

### Creating Workflow Annotations

#### 1. Basic Annotations
```yaml
- name: Create annotations
  run: |
    echo "::notice title=Build Started::Starting build process"
    echo "::warning title=Deprecated API::Using deprecated API endpoint"
    echo "::error title=Build Failed::Build process failed"
    echo "::debug::Debug information here"
```

#### 2. Advanced Annotations
```yaml
- name: Create detailed annotations
  run: |
    # Notice with file and line information
    echo "::notice file=src/app.js,line=10,col=5::Consider using const instead of var"
    
    # Warning with title and message
    echo "::warning title=Security Warning,file=package.json::Outdated dependency detected"
    
    # Error with custom properties
    echo "::error title=Test Failure,file=tests/unit.test.js,line=25::Test case failed: expected 5, got 3"
    
    # Debug with multiline message
    echo "::debug::" << EOF
    Debug information:
    - Node version: $(node --version)
    - NPM version: $(npm --version)
    - Current directory: $(pwd)
    EOF
```

#### 3. Conditional Annotations
```yaml
- name: Conditional annotations
  run: |
    if [ "${{ github.ref }}" = "refs/heads/main" ]; then
      echo "::notice title=Production Build::Building for production environment"
    else
      echo "::notice title=Development Build::Building for development environment"
    fi
    
    # Check test results
    if [ -f "test-results.json" ]; then
      TEST_COUNT=$(jq '.tests | length' test-results.json)
      PASSED_COUNT=$(jq '.tests | map(select(.status == "passed")) | length' test-results.json)
      
      if [ "$PASSED_COUNT" -eq "$TEST_COUNT" ]; then
        echo "::notice title=All Tests Passed::$PASSED_COUNT/$TEST_COUNT tests passed"
      else
        echo "::warning title=Some Tests Failed::$PASSED_COUNT/$TEST_COUNT tests passed"
      fi
    fi
```

### Notification Systems

#### 1. Slack Notifications
```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ci-cd'
    text: |
      Workflow failed: ${{ github.workflow }}
      Repository: ${{ github.repository }}
      Branch: ${{ github.ref_name }}
      Actor: ${{ github.actor }}
      Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### 2. Email Notifications
```yaml
- name: Send email notification
  if: always()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "Workflow ${{ job.status }}: ${{ github.workflow }}"
    body: |
      Workflow: ${{ github.workflow }}
      Status: ${{ job.status }}
      Repository: ${{ github.repository }}
      Branch: ${{ github.ref_name }}
      Actor: ${{ github.actor }}
      Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
    to: ${{ secrets.NOTIFICATION_EMAIL }}
```

#### 3. Custom Webhook Notifications
```yaml
- name: Send webhook notification
  if: always()
  run: |
    curl -X POST "${{ secrets.WEBHOOK_URL }}" \
      -H "Content-Type: application/json" \
      -d '{
        "workflow": "${{ github.workflow }}",
        "status": "${{ job.status }}",
        "repository": "${{ github.repository }}",
        "branch": "${{ github.ref_name }}",
        "actor": "${{ github.actor }}",
        "run_id": "${{ github.run_id }}",
        "run_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}",
        "timestamp": "'$(date -u -Iseconds)'"
      }'
```

## Performance Monitoring

### Workflow Performance Metrics

#### 1. Timing Measurements
```yaml
- name: Measure execution time
  run: |
    start_time=$(date +%s)
    
    # Your commands here
    npm ci
    npm test
    npm run build
    
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    echo "::notice title=Performance::Total execution time: ${duration}s"
    
    # Log to file for analysis
    echo "$(date -u -Iseconds),${{ github.workflow }},${{ github.job }},${duration}" >> performance.log
```

#### 2. Resource Usage Monitoring
```yaml
- name: Monitor resource usage
  run: |
    # Monitor during execution
    (
      while true; do
        echo "$(date -u -Iseconds),$(ps -o pid,ppid,cmd,%mem,%cpu --no-headers -C node | wc -l),$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}'),$(df -h . | awk 'NR==2{print $5}' | sed 's/%//')" >> resource-usage.log
        sleep 10
      done
    ) &
    
    MONITOR_PID=$!
    
    # Your main commands
    npm ci
    npm test
    
    # Stop monitoring
    kill $MONITOR_PID
    
    # Upload resource usage data
    echo "::notice title=Resource Usage::Check resource-usage.log for details"
```

#### 3. Performance Regression Detection
```yaml
- name: Detect performance regression
  run: |
    # Get current performance metrics
    CURRENT_TIME=$(npm run test:performance --silent | grep "Total time" | awk '{print $3}')
    
    # Get baseline from previous run (stored as artifact)
    if [ -f "baseline-time.txt" ]; then
      BASELINE_TIME=$(cat baseline-time.txt)
      THRESHOLD=1.2  # 20% increase threshold
      
      if (( $(echo "$CURRENT_TIME > $BASELINE_TIME * $THRESHOLD" | bc -l) )); then
        echo "::warning title=Performance Regression::Current time: ${CURRENT_TIME}s, Baseline: ${BASELINE_TIME}s"
      else
        echo "::notice title=Performance OK::Current time: ${CURRENT_TIME}s, Baseline: ${BASELINE_TIME}s"
      fi
    fi
    
    # Store current time as new baseline
    echo "$CURRENT_TIME" > baseline-time.txt
```

### Workflow Optimization

#### 1. Parallel Job Optimization
```yaml
# Before: Sequential jobs
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test
  
  lint:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Run linting
        run: npm run lint
  
  build:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build

# After: Parallel jobs
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: npm test
  
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Run linting
        run: npm run lint
  
  build:
    needs: [test, lint]
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build
```

#### 2. Caching Optimization
```yaml
- name: Optimize caching
  run: |
    # Check cache hit rate
    if [ -d "node_modules" ]; then
      echo "::notice title=Cache Hit::Dependencies loaded from cache"
    else
      echo "::notice title=Cache Miss::Installing dependencies from scratch"
    fi
    
    # Measure installation time
    start_time=$(date +%s)
    npm ci
    end_time=$(date +%s)
    install_time=$((end_time - start_time))
    
    echo "::notice title=Installation Time::${install_time}s"
```

## Error Handling and Recovery

### Advanced Error Handling

#### 1. Retry Mechanisms
```yaml
- name: Retry on failure
  run: |
    max_attempts=3
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
      echo "Attempt $attempt of $max_attempts"
      
      if npm test; then
        echo "Tests passed on attempt $attempt"
        break
      else
        echo "Tests failed on attempt $attempt"
        if [ $attempt -eq $max_attempts ]; then
          echo "All attempts failed"
          exit 1
        fi
        attempt=$((attempt + 1))
        sleep 10
      fi
    done
```

#### 2. Graceful Degradation
```yaml
- name: Graceful degradation
  run: |
    # Try primary method
    if npm run test:full; then
      echo "::notice title=Full Tests Passed::All tests completed successfully"
    else
      echo "::warning title=Full Tests Failed::Falling back to quick tests"
      
      # Fallback to quick tests
      if npm run test:quick; then
        echo "::notice title=Quick Tests Passed::Quick tests completed successfully"
      else
        echo "::error title=All Tests Failed::Both full and quick tests failed"
        exit 1
      fi
    fi
```

#### 3. Conditional Recovery
```yaml
- name: Conditional recovery
  run: |
    # Try to recover from common issues
    if ! npm ci; then
      echo "::warning title=NPM CI Failed::Trying npm install instead"
      rm -rf node_modules package-lock.json
      npm install
    fi
    
    if ! npm test; then
      echo "::warning title=Tests Failed::Checking for flaky tests"
      # Retry individual test files
      for test_file in tests/*.test.js; do
        if ! npm test -- "$test_file"; then
          echo "::error title=Test File Failed::$test_file failed consistently"
        fi
      done
    fi
```

### Workflow Recovery Patterns

#### 1. Automatic Rollback
```yaml
- name: Deploy with rollback
  run: |
    # Deploy new version
    if deploy.sh; then
      echo "::notice title=Deployment Successful::New version deployed"
      
      # Wait and verify
      sleep 30
      if health-check.sh; then
        echo "::notice title=Health Check Passed::Deployment verified"
      else
        echo "::error title=Health Check Failed::Rolling back"
        rollback.sh
        exit 1
      fi
    else
      echo "::error title=Deployment Failed::Deployment aborted"
      exit 1
    fi
```

#### 2. State Recovery
```yaml
- name: Recover workflow state
  run: |
    # Check for previous state
    if [ -f "workflow-state.json" ]; then
      echo "::notice title=State Recovery::Found previous workflow state"
      
      LAST_STEP=$(jq -r '.last_step' workflow-state.json)
      echo "Resuming from step: $LAST_STEP"
      
      # Resume from last successful step
      case $LAST_STEP in
        "test")
          echo "Resuming from test step"
          npm test
          ;;
        "build")
          echo "Resuming from build step"
          npm run build
          ;;
        *)
          echo "Starting from beginning"
          ;;
      esac
    fi
    
    # Update state
    echo '{"last_step": "test", "timestamp": "'$(date -u -Iseconds)'"}' > workflow-state.json
```

## Monitoring Dashboards

### Custom Monitoring Solutions

#### 1. Workflow Metrics Collection
```yaml
- name: Collect workflow metrics
  if: always()
  run: |
    # Collect comprehensive metrics
    cat > metrics.json << EOF
    {
      "workflow": "${{ github.workflow }}",
      "job": "${{ github.job }}",
      "status": "${{ job.status }}",
      "started_at": "${{ job.started_at }}",
      "completed_at": "${{ job.completed_at }}",
      "runner": "${{ runner.os }}",
      "repository": "${{ github.repository }}",
      "ref": "${{ github.ref }}",
      "actor": "${{ github.actor }}",
      "run_id": "${{ github.run_id }}",
      "run_number": "${{ github.run_number }}",
      "event": "${{ github.event_name }}",
      "duration": "${{ job.duration }}"
    }
    EOF
    
    # Send to monitoring service
    curl -X POST "${{ secrets.MONITORING_ENDPOINT }}" \
      -H "Content-Type: application/json" \
      -d @metrics.json
```

#### 2. Performance Trend Analysis
```yaml
- name: Analyze performance trends
  run: |
    # Get historical data
    curl -s "${{ secrets.MONITORING_ENDPOINT }}/metrics?workflow=${{ github.workflow }}&days=7" > historical-data.json
    
    # Analyze trends
    CURRENT_DURATION="${{ job.duration }}"
    AVG_DURATION=$(jq -r '.average_duration' historical-data.json)
    
    if (( $(echo "$CURRENT_DURATION > $AVG_DURATION * 1.5" | bc -l) )); then
      echo "::warning title=Performance Degradation::Current duration ($CURRENT_DURATION) is 50% higher than average ($AVG_DURATION)"
    fi
```

## Practical Examples

### Example 1: Comprehensive Monitoring Workflow
```yaml
name: Comprehensive Monitoring

on: [push, pull_request]

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup monitoring
        run: |
          echo "::notice title=Monitoring Started::Comprehensive monitoring enabled"
          echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
          echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV
      
      - name: Collect system information
        run: |
          echo "=== System Information ==="
          uname -a
          cat /etc/os-release
          df -h
          free -h
          nproc
      
      - name: Monitor resource usage
        run: |
          # Start resource monitoring
          (
            while true; do
              echo "$(date -u -Iseconds),$(ps aux | wc -l),$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}'),$(df -h . | awk 'NR==2{print $5}' | sed 's/%//')" >> resource-monitor.log
              sleep 5
            done
          ) &
          echo $! > monitor.pid
      
      - name: Run tests with monitoring
        run: |
          start_time=$(date +%s)
          
          # Run tests
          npm ci
          npm test
          
          end_time=$(date +%s)
          duration=$((end_time - start_time))
          
          echo "::notice title=Test Duration::Tests completed in ${duration}s"
      
      - name: Stop monitoring
        if: always()
        run: |
          if [ -f "monitor.pid" ]; then
            kill $(cat monitor.pid) 2>/dev/null || true
            rm -f monitor.pid
          fi
      
      - name: Upload monitoring data
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: monitoring-data-${{ github.run_id }}
          path: |
            resource-monitor.log
            metrics.json
          retention-days: 30
      
      - name: Send monitoring report
        if: always()
        run: |
          # Create monitoring report
          cat > monitoring-report.md << EOF
          # Workflow Monitoring Report
          
          **Workflow:** ${{ github.workflow }}
          **Status:** ${{ job.status }}
          **Duration:** ${{ job.duration }}
          **Repository:** ${{ github.repository }}
          **Branch:** ${{ github.ref_name }}
          **Actor:** ${{ github.actor }}
          
          ## Resource Usage
          \`\`\`
          $(cat resource-monitor.log | tail -10)
          \`\`\`
          
          ## System Information
          - OS: $(uname -s)
          - Architecture: $(uname -m)
          - CPU Cores: $(nproc)
          - Memory: $(free -h | awk 'NR==2{print $2}')
          - Disk: $(df -h . | awk 'NR==2{print $2}')
          EOF
          
          # Send report
          curl -X POST "${{ secrets.MONITORING_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"$(cat monitoring-report.md | sed 's/"/\\"/g' | tr '\n' '\\n')\"}"
```

### Example 2: Error Recovery Workflow
```yaml
name: Error Recovery Workflow

on: [push]

jobs:
  resilient-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Deploy with error recovery
        run: |
          set -e
          
          # Function to handle errors
          error_handler() {
            echo "::error title=Deployment Error::Error occurred at line $1"
            echo "Attempting recovery..."
            
            # Try to rollback
            if [ -f "rollback.sh" ]; then
              ./rollback.sh
            fi
            
            # Send notification
            curl -X POST "${{ secrets.ERROR_WEBHOOK }}" \
              -H "Content-Type: application/json" \
              -d '{"text": "Deployment failed and rollback attempted"}'
          }
          
          # Set error trap
          trap 'error_handler $LINENO' ERR
          
          # Deploy steps
          echo "::notice title=Deployment Started::Beginning deployment process"
          
          # Step 1: Build
          npm ci
          npm run build
          echo "::notice title=Build Complete::Application built successfully"
          
          # Step 2: Test
          npm test
          echo "::notice title=Tests Passed::All tests completed successfully"
          
          # Step 3: Deploy
          ./deploy.sh
          echo "::notice title=Deployment Complete::Application deployed successfully"
          
          # Step 4: Verify
          sleep 30
          if ./health-check.sh; then
            echo "::notice title=Health Check Passed::Deployment verified"
          else
            echo "::error title=Health Check Failed::Deployment verification failed"
            exit 1
          fi
      
      - name: Success notification
        if: success()
        run: |
          curl -X POST "${{ secrets.SUCCESS_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d '{"text": "Deployment completed successfully"}'
```

## Key Takeaways

1. **Enable Debug Logging:** Use `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG` for detailed troubleshooting
2. **Use Annotations:** Create meaningful workflow annotations for better visibility
3. **Implement Monitoring:** Collect metrics and monitor workflow performance
4. **Handle Errors Gracefully:** Implement retry mechanisms and recovery strategies
5. **Set Up Notifications:** Use webhooks and integrations for real-time alerts
6. **Optimize Performance:** Monitor resource usage and optimize workflow execution
7. **Document Issues:** Maintain detailed logs and artifacts for post-mortem analysis

## References

- [Debugging workflows](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/debugging-workflows)
- [Managing workflow runs](https://docs.github.com/en/actions/managing-workflow-runs)
- [Workflow run logs](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/viewing-workflow-run-logs)
- [Using workflow annotations](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions)
- [Monitoring and troubleshooting workflows](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows)
