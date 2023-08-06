Introduction
============

Parsim is a tool for working with parameterized simulation models.
The primary objective is to facilitate quality assurance of simulation projects.
The tool supports a scripted and automated workflow, where verified and validated simulation models
are parameterized, so that they can be altered/modified in well-defined ways and reused with minimal user invention.
All events are logged on several levels, to support traceability, project documentation and quality control.

Parsim provides basic functionality for generating studies based on common design-of experiments
(DOE) methods, for example using factorial designs, response surface methods or random sampling,
like Monte Carlo or Latin Hypercube.

Parsim can also be used as an interface to the Dakota library; Dakota is run as a subprocess,
generating cases from a Parsim model template.

How it works
============

Once a prototype simulation case has been developed, a corresponding simulation
:term:`model template` is created by collecting all simulation input files, data
files and scripts into a :term:`template directory`. The text files in a model
template can then be parameterized by replacing numerical values, or text
strings with macro names. Parsim uses the pyexpander macro processing library, which
supports embedding of arbitrarly complex Python code in the template files.
This can be used for advanced parameterization needs, for example to compute data
tables from functions, generate graphs for reports, generate content in loops or
conditionals, etc.

When a simulation case is created, the model template directory is recursively
replicated to create a :term:`case` directory. Parsim operations can also be carried
out on a :term:`study`, containing multiple cases. A study is a directory containing
multiple case directories.

You operate on your cases (either individually or on all cases of a study at once)
by executing scripts written to perform specific tasks, e.g.
meshing operations, starting a simulation, or post-processing of results.

Your simulation project lives in a Parsim :term:`project` directory, which holds all
cases and studies of the project. The project directory holds Parsim
configuration settings and logs project events, like creation of cases and
studies, serious errors, change of configuration settings, etc.

Summary of features:

* Flexible and full-featured support for parameterization of text-based simulation models.
* Cases and parameter studies kept together in projects.
* Scripted workflow can be applied to individual cases as well as to large parameter studies.
* Logging and error handling, for traceability and project documentation.
* Support for many common design-of-experiments (DOE) methods.
* Can be used as an interface to the Dakota library, for complex uncertainty quantification and optimization tasks.
* Based on Python (works with both Python 2 and 3).
* One simple workflow for any kind of simulation application.
* Platform independent: Works in both Linux, Windows and MacOS environments.
* Simple installation from public Python repositories (install with pip, in any Python installation).
* Available under open-source license (GNU Public License v. 3)


Installation
============

Parsim is available at the `PyPI, the Python Package Index <https://pypi.python.org/pypi>`_.
It is installed in your ordinary Python environment using the pip installer.

The Parsim installation requires and automatically installs the
Python library `pyexpander <http://pyexpander.sourceforge.net>`_,
which is used for macro and parameter expansion (parameterization of input files).

The DOE (Design of Experiments) functionality is optional. This is because
it requires the Python packages `NumPy <http://www.numpy.org/>`_
and `SciPy <https://www.scipy.org/>`_, which may be difficult to install correctly.

Installation without DOE support
................................

To install Parsim without DOE support, ::

    pip install parsim

Installation with DOE support
.............................

It is recommended to first make a clean and fully functional installation
of the NumPy and SciPy libraries.
The best way to do this depends on which Python distribution you use.
The `anaconda Python distribution <https://www.continuum.io/downloads>`_
is highly recommended. It works well on both Windows and Linux.
In an anaconda distribution, you simply install the conda packages for NumPy and SciPy.
They are usually installed by default.

The DOE functionality is provided by the
`pyDOE <https://pythonhosted.org/pyDOE/>`_ library.
Once NumPy and SciPy are in place, you install parsim with DOE support: ::

    pip install parsim[doe]

This will install also the pyDOE package, which in turn will check for NumPy and SciPy.

Documentation
=============

The Parsim documentation is hosted at `ReadTheDocs <https://parsim.readthedocs.io>`_.

Author
======

Parsim was developed by Ola Widlund, `RISE Research Institutes of Sweden <https://www.ri.se/en>`_, to
provide basic and generic functionality for uncertainty quantification
and quality assurance of parameterized simulation models.

Licensing
=========

Parsim is licensed under the GNU Public License, GPL, version 3 or later.
Copyright belongs to `RISE Research Institutes of Sweden AB <https://www.ri.se/en>`_.

Source code and reporting of issues
===================================

The source code is hosted at `GitLab.com <https://gitlab.com/olwi/psm>`_.
Here you can also report issues and suggest improvements.
