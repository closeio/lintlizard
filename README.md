# LintLizard

LintLizard helps maintaining great and consistent code quality across all Python-based projects at Close, making it easy to install and run exact same versions of code checking tools with a single command.

(Interested in working on projects like this? [Close](http://close.com) is looking for [great engineers](http://jobs.close.com) to join our team)

# Recommended usage

Set up dependabot. See example in this repo in `.github/dependabot.yml`

Make a separate `requirements_lint.txt` that contains `lintlizard==0.0.3` (with the latest release version).

Configure individual linters. Use `setup.cfg` and `pyproject.toml` from this repo as examples.

In your CI system, have a separate job that executes something like this:

```
pip install -r requirements_lint.txt
lintlizard
```

# Combining requirements

If LintLizard's requirements intersect with your production, use pip's constraints feature:

```
pip install -c your_requirements.txt -r requirements_lint.txt
```
