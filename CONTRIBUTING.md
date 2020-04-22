# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Get Started!
Ready to contribute? Here's how to set up twitter_analysis_tools for local development.

1. Fork the `twitter-analysis-tools` repo on GitHub.

2. Clone your fork locally:

    ```bash
    git clone git@github.com:{your_name_here}/twitter-analysis-tools.git
    ```

3. Install the project in editable mode. (It is also recommended to work in a virtualenv or anaconda environment):

    ```bash
    $ cd twitter-analysis-tools/
    $ pip install -e .[dev]
    ```

4. Create a branch for local development:

    ```bash
    $ git checkout -b {your_development_type}/short-description
    ```

    Ex: feature/read-tiff-files or bugfix/handle-file-not-found

    Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linting and
   tests, including testing other Python versions with make:

    ```bash
    $ tox -e lint
    ```


6. Commit your changes and push your branch to GitHub:

    ```bash
    $ git add .
    $ git commit -m "Resolves gh-###. Your detailed description of your changes."
    $ git push origin {your_development_type}/short-description
    ```

7. Submit a pull request through the GitHub website.

## Deploying

A reminder for the maintainers on how to deploy a release. If you have not already created accounts on [test.pypi.org](https://test.pypi.org/) and [pypi.org](https://pypi.org/), do that first.
Make sure all your changes are committed.

Make sure you have added API tokens for [test.pypi.org](https://test.pypi.org/) and [pypi.org](https://pypi.org/) as secrets called `test_pypi_password` and `pypi_password` in your GitHub repository. See the "Saving credentials on GitHub" section of [this guide](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#saving-credentials-on-github) for instructions on this.

Then run:
```bash
$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags
```

Next, on GitHub, create a release from the version tag you have just created.

This will release a new package version on Git + GitHub and publish to PyPI.
