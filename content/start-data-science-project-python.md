Title: How to start a Data Science project in Python
Date: 2017-02-26
Category: Blogs
Summary: A lot of blog posts are written on the complicated Data Science-y stuff but not so many posts talk about the simple stuff.  A simple but very important topic is how to start and structure your projects.  This post gives a few pointers for setting up your projects.
 

A lot of blog posts are written on the complicated Data Science-y stuff but not so many posts talk about the simple stuff.
A simple but very important topic is how to start and structure your projects.
This post gives a few pointers for setting up your projects.


## Project structure

Project structures often organically grow to suit people's needs, leading to different project structures within a team.
You can consider yourself lucky if at some point in time you, or someone in your team, finds an obscure blog post with a somewhat sane structure and enforces it in your team.

Many years ago I stumbled upon [ProjectTemplate for R](http://projecttemplate.net/).
Since then I've tried to get people to use a good project structure.
More recently [DrivenData](https://www.drivendata.org/) released their more generic [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/#cookiecutter-data-science).

The main philosophies of those projects are:

- A consistent and well organized structure allows people to collaborate more easily.
- Your analyses should be reproducible and your structure should enable that.
- A projects starts from raw data that should never be edited; consider raw data immutable and only edit derived sources.


I couldn't help to invent my own project structure and my minimal structure looks something like this (example [here](git@github.com:hgrif/example-project.git)):

```
example_project/
├── data/				<- The original, immutable data dump.       
├── figures/			<- Figures saved by notebooks and scripts.
├── notebooks/			<- Jupyter notebooks.
├── output/				<- Processed data, models, logs, etc.
├── exampleproject/		<- Python package with source code.
│   └── __init__.py		<-- Make the folder a package.
	└── process.py		<-- Example module.
├── tests/				<- Tests for your Python package.
	└── test_process.py	<-- Tests for process.py.
├── environment.yml		<- Virtual environment definition.
├── README.md			<- README with info of the project.
└── setup.py 			<- Install and distribute your module.
```


It mostly follows the other structures: 

- raw data is immutable and goes to `data/`; 
- processed data and derived output goes to different folders like `figures/` and `output/`; 
- notebooks go to `notebooks/`; 
- project info goes in the `README.md`; 
- and the project code goes to a separate folder.

I try to make a full-fledged Python package (plus tests) out of my project structure so that the step between prototyping and production is as small as possible.
The `setup.py` allows me to install the package in a virtual environment and use it in my Notebooks (more on this in a later blog post).

It doesn't really matter which structure you pick, as long as it fits your workflow and you stick with it for a while.
Try to understand the philosophies of the projects and pick the structure that suits your needs.


## Virtual environment

Projects should be independent of each other: you don't want your new experiments to mess up your older work.
We do this partly by putting the files of different projects in different folders but you should also use separate _Python_ environments.

Virtual environments are isolated environments that separate dependencies of different projects and avoid package conflicts.
Each virtual environment has its own packages and its own package versions.
Environment A can have `numpy` version 1.11 and `pandas` version 0.18 while environment B only has `pandas` version 0.17.
I like [conda](https://conda.io/miniconda.html) virtual environments because they're well suited for Data Science (read [here](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/) why).

Create a new [conda]() virtual environment called `example-project` with Python 3.5:

```bash
$ conda install --name example-project python=3.5
```

Make sure your virtual environment is activated (leave out the `source` if you're on Window):

```
$ source activate example-project
```

... and you're now ready to install your favourite packages!

```
$ conda install pandas numpy jupyter scikit-learn
```

When you're switching to a different project, run a `source deactivate` and activate the project's virtual environment.

Once you get the hang of the `activate`-`deactivate`-flow, you'll find that a virtual environments is a lightweight tool to keep your Python environments separated.
By exporting your environment definition file (i.e. all installed packages and their versions) your projects will also be easily reproducible.
If you want a more detailed discussion, check [Tim Hopper's post](http://tdhopper.com/blog/2015/Nov/24/my-python-environment-workflow-with-conda/).


## Git

Every project should have its own Git repository.
Having a repo per project allows you to track the history of a project and maintain complex version dependencies between projects.

Alternatively, you can choose to have one repository with multiple projects, putting all the knowledge in a single place.
The downside is, however, that it often ends up with ugly merge conflicts: Data Scientists are generally not that fluent with Git.
In addition to a lot of Git frustrations, it makes your projects less independent of eachother.

The easiest way to set up Git is by creating a new git repository on your Git host (e.g. [GitHub](https://help.github.com/articles/creating-a-new-repository/) or [GitLab](https://docs.gitlab.com/ee/gitlab-basics/create-project.html)) and cloning that:

```bash
$ git clone https://github.com/hgrif/
```

You can then setup your project structure in this empty folder.

If you followed this guide and already created a folder with some files, first initialize a git repository on your machine:

```bash
$ git init
```

Then create a new git repository on your host, get its link and run:

```bash
$ git remote add origin https://github.com/hgrif/
```

This adds the remote repository with the link `https://github.com/hgrif/` and names it `origin`.
You probably have to push your current `master` branch to `origin`:

```bash
$ git push --set-upstream origin master
```

Now that Git is set up, you can `git add` and `git commit` to your heart's content!



## Tooling

You can get away of some of the repetitive tasks by using some tooling!

The Python package [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) automatically creates project folders based on a template.
You can use existing template like the [Cookiecutter Data Science](https://github.com/drivendata/cookiecutter-data-science) or [mine](https://github.com/hgrif/cookiecutter-ds-python/tree/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D), or invent your own.

The easiest way to use virtual environments is to use an editor like [PyCharm](https://www.jetbrains.com/pycharm/) that supports them.
You can also use [autoenv](https://github.com/kennethreitz/autoenv) or [direnv](https://direnv.net/) to activate a virtual environment and set environment variables if you `cd` into a directory.


## Conclusion

Having a good setup for your Data Science projects makes it easier for other people to work on your projects and makes them more reproducible. 
A good structure, a virtual environment and a git repository are the building blocks of any project.
