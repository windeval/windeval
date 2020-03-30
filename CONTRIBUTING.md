# Contributing

Note that most of the following are copies or interpretations of the [scikit-learn#contributing](https://scikit-learn.org/dev/developers/contributing.html#contributing) guide. Feel free to see the more complete original and share your views to improve this adaptation of it.

## Name Convention

For variable names the [CF Standard Name Table (Version 70, 10 December 2019)](http://cfconventions.org/Data/cf-standard-names/70/build/cf-standard-name-table.html) is used.

> Refer to the [Guidelines for Construction of CF Standard Names](http://cfconventions.org/Data/cf-standard-names/docs/guidelines.html) for information on how the names are constructed and interpreted, and how new names could be derived.
>
> **A note about units**
> The canonical units associated with each standard name are usually the SI units for the quantity. [Section 3.3 of the CF conventions](http://cfconventions.org/cf-conventions/cf-conventions.html#standard-name) states: "Unless it is dimensionless, a variable with a standard_name attribute must have units which are physically equivalent (not necessarily identical) to the canonical units, possibly modified by an operation specified by either the standard name modifier ... or by the cell_methods attribute." Furthermore, [Section 1.3 of the CF conventions](http://cfconventions.org/cf-conventions/cf-conventions.html#_overview) states: "The values of the units attributes are character strings that are recognized by UNIDATA's Udunits package [UDUNITS], (with exceptions allowed as discussed in Section 3.1, “Units”)." For example, a variable with the standard name of "air_temperature" may have a units attribute of "degree_Celsius" because Celsius can be converted to Kelvin by Udunits. For the full range of supported units, refer to the [Udunits documentation](https://www.unidata.ucar.edu/software/udunits/udunits-current/doc/udunits/udunits2.html#Database). Refer to the [CF conventions](http://cfconventions.org/cf-conventions/cf-conventions.html) for full details of the units attribute.

## Contributing code

If you wish to contribute to the windeval project you need to

1. First, set up your local repository copy:
    ```bash
    $ git clone git@git.geomar.de:wind-products/windeval.git
    # or use the https path
    # git clone https://git.geomar.de/wind-products/windeval.git
    ```

2. Optional, you may choose to use the Conda environment used during pipeline testing:

    ```bash
    $ wget https://git.geomar.de/wind-products/windeval_docker/blob/master/environment.yml
    $ conda env create --name windeval -f environment.yml
    $ conda activate windeval
    ```

3. Install the development dependencies:

    ```bash
    $ conda install -c conda-forge pytest black flake8
    # or
    # pip install pytest black flake8
    ```

4. Install windeval in editable mode:

    ```bash
    $ cd windeval
    $ python setup.py develop
    # or
    # pip install --editable .
    ```

5. You should now have a working installation of windeval. The next steps now describe the process of modifying code and submitting a merge request:

    Synchronize your master branch with the upstream master branch:

    ```bash
    $ git checkout master
    $ git pull master
    ```

6. Create a feature branch to hold your development changes:

    ```bash
    $ git checkout -b feature/my_feature
    ```

    and start making changes. Always use a feature branch. It’s good practice to never work on the `master` branch!

7. Develop the feature on your feature branch on your computer, using Git to do the version control. When you’re done editing, add changed files using `git add` and then `git commit`:

    ```bash
    $ git add modified_files
    $ git commit
    ```

    to record your changes in Git, then push the changes to your GitLab account with:

    ```bash
    $ git push -u origin feature/my-feature
    ```

8. Follow [these](https://docs.gitlab.com/ee/gitlab-basics/add-merge-request.html) instructions to create a merge request for your feature branch.

It is often helpful to keep your local feature branch synchronized with the latest changes of the main windeval repository:

```
$ git fetch origin master:master
$ git merge master
```

Subsequently, you might need to solve the conflicts. You can refer to the [Git documentation related to resolving merge conflict using the command line](https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/).

*Learning git*:

The [Git documentation](https://git-scm.com/documentation) and [http://try.github.io](http://try.github.io/) are excellent resources to get started with git, and understanding all of the commands shown here.

### Merge requests checklist

1. Give your merge request a helpful title
2. Make sure your code passes the tests
3. Make sure your code is properly commented and documented, and make sure the documentation renders properly.
4. Make sure that your merge request does not add PEP8 violations.
5. Follow the [coding-guidelines](#coding-guidelines) (see below).

You can check for common programming errors with the following tools:

+ Code with a good unittest coverage (at least 80%, better 100%), check with:

   ```bash
   $ pip install pytest pytest-cov
   $ pytest --cov windeval
   ```

## Documentation

Building the documentation requires installing some additional packages:

```bash
$ conda install -c conda-forge sphinx recommonmark sphinx_rtd_theme
# or
# pip install sphinx recommonmark sphinx_rtd_theme
```

To build the documentation, you need to be in the `doc` folder:

```bash
$ cd doc/
```

To generate the documentation:

```bash
$ make clean && make html
```

The documentation will be generated in the `_build/html/` directory.

View the documentation using any browser, e.g. Firefox:

```bash
$ firefox _build/html/index.html
```

### Guidelines for writing documentation

Please see [sciki-learn#guidelines-for-writing-documentation](https://scikit-learn.org/dev/developers/contributing.html#guidelines-for-writing-documentation) or some other resource.

## Coding guidelines

Please see [scikit-learn#coding-guidelines](https://scikit-learn.org/dev/developers/contributing.html#coding-guidelines) or some other resource.

---

In the windeval project Black is chosen as formatting tool using its default settings.

> By using _Black_, you agree to cede control over minutiae of hand-formatting. In return, _Black_ gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.
>
> _Black_ makes code review faster by producing the smallest diffs possible. Blackened code looks the same regardless of the project you're reading. Formatting becomes transparent after a while and you can focus on the content instead.
>
> [(source)](https://black.readthedocs.io/en/stable/)
