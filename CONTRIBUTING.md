# Contributing guidelines

Welcome! *Duqtools* is an open-source project that aims to work with a wide range of IMAS data for fusion research. If you're trying *duqtools* with your data, your experience, questions, bugs you encountered, and suggestions for improvement are important to the success of the project.

We have a [Code of Conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions with the project.

## Questions, feedback, bugs

Use the search function to see if someone else already ran accross the same issue. Feel free to open a new [issue here](https://github.com/duqtools/duqtools/issues) to ask a question, suggest improvements/new features, or report any bugs that you ran into.

## Submitting changes

Even better than a good bug report is a fix for the bug or the implementation of a new feature. We welcome any contributions that help improve the code.

When contributing to this repository, please first discuss the change you wish to make via an [issue](https://github.com/duqtools/duqtools/issues) with the owners of this repository before making a change.

Contributions can come in the form of:

- Bug fixes
- New features
- Improvement of existing code
- Updates to the documentation
- ... ?

We use the usual GitHub pull-request flow. For more info see [GitHub's own documentation](https://help.github.com/articles/using-pull-requests/).

Typically this means:

1. [Forking](https://docs.github.com/articles/about-forks) the repository and/or make a [new branch](https://docs.github.com/articles/about-branches)
2. Making your changes
3. Make sure that the tests pass and add your own
4. Update the documentation is updated for new features
5. Pushing the code back to Github
6. [Create a new Pull Request](https://help.github.com/articles/creating-a-pull-request/)

One of the code owners will review your code and request changes if needed. Once your changes have been approved, your contributions will become part of *duqtools*. 🎉

## Getting started with development

### Setup

*Duqtools* targets Python 3.7, which is the version available on [eufus](https://wiki.eufus.eu/doku.php).

Clone the repository into the `duqtools` directory:

```console
git clone https://github.com/duqtools/duqtools
```

Install using `virtualenv`:

```console
cd duqtools
python3 -m venv env
source env/bin/activate
python3 -m pip install -e .[develop]
```

Alternatively, install using Conda:

```console
cd duqtools
conda create -n duqtools python=3.7
conda activate duqtools
pip install -e .[develop]
```

### Running tests

Duqtools uses [pytest](https://docs.pytest.org/en/7.1.x/) to run the tests. You can run the tests for yourself using:

```console
pytest
```

To check coverage:

```console
coverage run -m pytest
coverage report  # terminal
coverage html    # html report
```


### Building the documentation

The documentation is written in [markdown](https://www.markdownguide.org/basic-syntax/), and uses [mkdocs](https://www.mkdocs.org/) to generate the pages.

To build the documentation for yourself:

```console
pip install -e .[docs]
mkdocs serve
```

You can find the documentation source in the [docs](https://github.com/duqtools/duqtools/tree/main/docs) directory.
If you are adding new pages, make sure to update the listing in the [`mkdocs.yml`](https://github.com/duqtools/duqtools/blob/main/mkdocs.yml) under the `nav` entry.

### Making a release

The versioning scheme we use is [SemVer](http://semver.org/).

1. Bump the version (`major`/`minor`/`patch` as needed)

```console
bumpversion minor
```

2. Make a new [release](https://github.com/duqtools/duqtools/releases). The [upload to pypi](https://github.com/duqtools/duqtools/actions/workflows/publish.yaml) is triggered when a release is published.
