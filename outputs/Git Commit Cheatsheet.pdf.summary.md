Here is a concise summary of the content in clear bullet points:

**Git Commit Types**

* `feat`: Add new feature or functionality
* `fix`: Solve a problem or bug
* `docs`: Write or update explanations, README changes, tutorials, or inline comments
* `style`: Change code look or format (not functionality)
* `refactor`: Rewrite code for clarity or efficiency without changing results
* `test`: Write or adjust tests
* `chore`: Perform routine updates or maintenance
* `perf`: Optimize code for speed or efficiency
* `build`: Change how the project is built or packaged
* `config`: Update configuration files
* `ci`: Automate continuous integration/deployment

**Additional Commit Types**

* `revert`: Undo changes that broke things
* `BREAKING CHANGE`: Force others to adjust their code
* `merge`: Combine branches (e.g., dev into main)
* `hotfix`: Urgent fix in production
* `security`: Fix vulnerabilities
* `ui`: Changes to look and feel (not logic)
* `ux`: Improve user experience
* `env`: Environment configuration changes
* `db`: Database changes
* `deps`: Dependency changes (add, update, or remove libraries)

**Categories**

* Libraries: updating ESLint rules and configuration files
* Infrastructure: updating docker-compose and cloud/servers/network/containers
* Release: tagging and preparing new app version or release notes
* Analytics: adding or modifying tracking/metrics
* i18n: adding translations for internationalization
* a11y: improving accessibility features
* Content: updating static content
* Prototype: experimental changes or temporary proof-of-concept
* Spike: research or exploration commit (trying out tools, not final code)
* WIP: work in progress (not finished, avoid pushing to main)

**Practical Tips**

* Use present tense ("add feature", not "added feature")
* Keep title short, 50 characters or less
* Add details in the body if needed
* Make commits clear enough that future you (or teammate) won't be confused