Installation
============

``design-research`` requires Python 3.12 or newer. Start with the published
umbrella package when you want the complete package family and its shared
namespace.

Install The Published Package
-----------------------------

Create an isolated environment, then install from PyPI:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install design-research

On Windows, activate the same environment with
``.venv\Scripts\activate``. See :doc:`vscode_start` for interpreter selection
and platform-specific activation commands.

The base install resolves the exact Problems, Agents, Experiments, and Analysis
versions recorded in :doc:`compatibility`. That matrix is the combination
tested by this umbrella release; it is not a compatibility promise for
unlisted component versions.

Component Packages And Extras
-----------------------------

Install a component directly when you need only that package or one of its
optional backends. Optional runtime dependencies are defined and documented by
the package that uses them:

- `Problems documentation <https://cmudrc.github.io/design-research-problems/>`__
- `Agents documentation and provider extras <https://cmudrc.github.io/design-research-agents/dependencies_and_extras.html>`__
- `Experiments documentation <https://cmudrc.github.io/design-research-experiments/>`__
- `Analysis documentation <https://cmudrc.github.io/design-research-analysis/>`__

Repository Development
----------------------

For a source checkout, install the umbrella contributor toolchain:

.. code-block:: bash

   git clone https://github.com/cmudrc/design-research.git
   cd design-research
   python -m venv .venv
   source .venv/bin/activate
   make dev

Maintainer workflows target Python ``3.12`` from ``.python-version``. Continue
to :doc:`quickstart` for the installed-package smoke step and repository
validation commands.
