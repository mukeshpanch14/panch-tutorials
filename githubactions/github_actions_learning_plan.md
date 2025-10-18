# 🚀 GitHub Actions Learning Plan for Developers

A structured, developer-focused guide to mastering **GitHub Actions** — from fundamentals to advanced CI/CD automation. Each section includes learning objectives, key concepts, practical hints, and official resources for deeper exploration.

---

## 🧭 1. Introduction & Fundamentals

**🎯 Objective:**  
Understand what GitHub Actions is, how workflows are structured, and the basic building blocks of automation.

**💡 Key Concepts:**
- Core components: *Workflows*, *Jobs*, *Steps*, *Actions*, and *Runners*.
- Common triggers: `push`, `pull_request`, `schedule`, `workflow_dispatch`.
- YAML structure: indentation, syntax, and environment variables.

**🧩 Example:**
```yaml
name: Hello World
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello, GitHub Actions!"
```

**🔗 References:**
- [Understanding GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)
- [Workflow syntax reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

**📘 Deep Dive:** [View detailed guide](./01-introduction-fundamentals.md)

---

## ⚙️ 2. Creating Your First Workflow

**🎯 Objective:**  
Learn to create and run your first workflow inside a repository.

**💡 Key Concepts:**
- Folder convention: `.github/workflows/`
- Structure: `name`, `on`, `jobs`, `steps`
- Viewing and debugging workflow runs in GitHub UI.

**🧩 Example:**
```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

**🔗 References:**
- [Quickstart: GitHub Actions](https://docs.github.com/en/actions/quickstart)
- [About workflows](https://docs.github.com/en/actions/using-workflows/about-workflows)

**📘 Deep Dive:** [View detailed guide](./02-creating-first-workflow.md)

---

## 🧱 3. Working with Actions

**🎯 Objective:**  
Use prebuilt actions and create your own custom actions.

**💡 Key Concepts:**
- Using Marketplace actions.
- Creating **custom actions**:
  - JavaScript or Docker-based.
  - Defining `action.yml` metadata (inputs/outputs).
- Publishing reusable actions.

**🧩 Example:**
```yaml
- name: Checkout code
  uses: actions/checkout@v4
```

**🔗 References:**
- [About custom actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions)
- [JavaScript Actions](https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action)
- [Docker Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)

**📘 Deep Dive:** [View detailed guide](./03-working-with-actions.md)

---

## 🚀 4. CI/CD Implementation

**🎯 Objective:**  
Automate build, test, and deploy workflows for continuous integration and delivery.

**💡 Key Concepts:**
- **CI:** Run tests, lint, and build automatically.
- **CD:** Deploy applications to environments.
- **Matrix builds:** Multiple OS/language versions.
- **Artifacts:** Sharing build outputs between jobs.

**🧩 Example:**
```yaml
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run build
```

**🔗 References:**
- [Building and testing with CI](https://docs.github.com/en/actions/automating-builds-and-tests)
- [Deploying with GitHub Actions](https://docs.github.com/en/actions/deployment/about-deployments)

**📘 Deep Dive:** [View detailed guide](./04-cicd-implementation.md)

---

## 🔒 5. Secrets & Security

**🎯 Objective:**  
Protect credentials and secure your automation environment.

**💡 Key Concepts:**
- Using `secrets.GITHUB_TOKEN` and repository secrets.
- Masking secrets and managing permissions.
- Pinning actions to commit SHAs.

**🧩 Example:**
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
steps:
  - run: curl -H "Authorization: Bearer $API_KEY" https://example.com
```

**🔗 References:**
- [Encrypted secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Security hardening guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

**📘 Deep Dive:** [View detailed guide](./05-secrets-security.md)

---

## 🧠 6. Advanced Topics

**🎯 Objective:**  
Learn reusable, optimized, and scalable workflow design.

**💡 Key Concepts:**
- **Reusable workflows:** via `workflow_call`.
- **Composite actions:** encapsulate common tasks.
- **Caching & Artifacts:** improve performance.
- **Matrix strategy:** parallel testing.
- **Self-hosted runners:** customization.

**🧩 Example:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [18, 20]
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

**🔗 References:**
- [Reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
- [Caching dependencies](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)

**📘 Deep Dive:** [View detailed guide](./06-advanced-topics.md)

---

## 🪄 7. Monitoring & Debugging

**🎯 Objective:**  
Understand how to analyze and troubleshoot workflows.

**💡 Key Concepts:**
- Enable debug logging: `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG`.
- Workflow logs and annotations.
- `continue-on-error` and re-running jobs.

**🔗 References:**
- [Debugging workflows](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/debugging-workflows)
- [Managing workflow runs](https://docs.github.com/en/actions/managing-workflow-runs)

**📘 Deep Dive:** [View detailed guide](./07-monitoring-debugging.md)

---

## 🧰 8. Real-World Use Cases

**🎯 Objective:**  
Explore automation scenarios for real projects.

**💡 Examples:**
- Auto-lint and comment on PRs.
- Publish npm or Docker packages.
- Deploy static sites to GitHub Pages.
- Send Slack or Teams notifications.
- Automate versioning and changelog generation.

**🔗 References:**
- [Starter workflows](https://github.com/actions/starter-workflows)
- [Marketplace examples](https://github.com/marketplace?type=actions)

**📘 Deep Dive:** [View detailed guide](./08-real-world-use-cases.md)

---

## 🏛️ 9. Governance & Best Practices

**🎯 Objective:**  
Maintain scalable and enterprise-ready workflow management.

**💡 Key Concepts:**
- Naming conventions and folder organization.
- Centralized workflow libraries.
- Review and approval patterns.
- Version control for reusable workflows.

**🔗 References:**
- [Workflow naming best practices](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#naming-your-workflow)
- [Reusable workflows in enterprise](https://docs.github.com/en/enterprise-cloud@latest/actions/using-workflows/reusing-workflows)

**📘 Deep Dive:** [View detailed guide](./09-governance-best-practices.md)

---

## 🧩 10. Capstone Projects (Hands-on)

**🎯 Objective:**  
Apply learned concepts through practical projects.

**💡 Projects:**
1. **CI/CD Pipeline for Node.js app** — build, test, and deploy automatically.
2. **Reusable action for dependency updates** — automate PR creation.
3. **Terraform deployment** — infrastructure automation.
4. **ETL Scheduling** — automate data pipeline triggers.

**🔗 References:**
- [GitHub Actions Learning Path](https://docs.github.com/en/actions/learn-github-actions)
- [Starter workflows repository](https://github.com/actions/starter-workflows)

---

### ✅ Next Steps
You can use this guide as a self-paced learning roadmap or training material. For best results:
- Follow the order of topics.
- Try each concept hands-on in a personal repo.
- Gradually design reusable CI/CD pipelines with real-world examples.

---

**Author:** Deloitte Developer Enablement  
**Version:** v1.0  
**Last Updated:** October 2025

