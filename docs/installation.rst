Installation
============

Requires Python 3.12+.

Use :doc:`compatibility` if you need help deciding whether to start with the
umbrella package or install one sibling library directly.

Install from PyPI:

.. code-block:: bash

   pip install design-research

Optional extras let you opt into sibling-library features from the umbrella
package without switching package names. For example:

.. code-block:: bash

   pip install "design-research[agents_openai]"
   pip install "design-research[problems_all,analysis_all]"
   pip install "design-research[kitchen_sink]"

Editable local install for contributors:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   make dev
