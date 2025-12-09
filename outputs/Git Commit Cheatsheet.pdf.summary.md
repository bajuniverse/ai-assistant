Here is a summary of the content in clear bullet points:

**Git Commit Types**

* `feat`: Add new feature or functionality
* `fix`: Solve a problem or bug
* `docs`: Write or update explanations
* `style`: Change code look/format without affecting functionality
* `refactor`: Rewrite code for clarity or efficiency without changing results
* `test`: Write or adjust tests
* `chore`: Perform routine updates or maintenance
* `perf`: Optimize code for speed or efficiency
* `build`: Change how the project is built or packaged
* `config`: Update configuration files

**When to Use Each Type**

* `feat` and `BREAKING CHANGE` for significant changes that affect functionality
* `revert` when a previous commit broke something and needs to be undone
* `merge` when combining branches together
* `hotfix` for urgent fixes in production
* `security`, `ui`, and `ux` for non-functional changes that improve appearance or user experience
* `env`, `db`, and `deps` for configuration, database, or dependency changes

**Categories**

* Libraries: Update ESLint rules, change settings files
* Infrastructure: Update docker-compose, cloud/servers/network/containers
* Release: Tag new app version or release notes
* Analytics: Add tracking/metrics (e.g. Google), logs, events, metrics
* i18n: Add translations (e.g. Spanish), multi-language support
* a11y: Improve accessibility (e.g. contrast on buttons)
* Content: Update static content (e.g. homepage text)
* Prototype: Experimental changes or temporary proof-of-concept
* Spike: Research or exploration (try out tools, not final code)
* WIP: Work in progress (not finished, avoid pushing to main)

**Practical Tips**

* Use present tense when writing commit messages
* Keep title short, 50 characters or less
* Add details to body if needed, especially for complex commits