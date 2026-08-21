Workshop Setup and Preflight
============================

Complete this one-time setup before attending a Design Research workshop.

Before The Workshop
-------------------

Install `Python 3.12 <https://www.python.org/downloads/>`_, open a terminal, and
run the block for your operating system.

On macOS or Linux:

.. code-block:: bash

   mkdir -p design-research-workshop
   cd design-research-workshop
   curl -fsSLo requirements.txt 'https://cmudrc.github.io/design-research/_static/workshop-requirements.txt'
   curl -fsSLo preflight.py 'https://cmudrc.github.io/design-research/_static/workshop-preflight.py'
   python3.12 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python preflight.py

On Windows PowerShell:

.. code-block:: powershell

   New-Item -ItemType Directory -Force design-research-workshop | Out-Null
   Set-Location design-research-workshop
   curl.exe -fsSLo requirements.txt 'https://cmudrc.github.io/design-research/_static/workshop-requirements.txt'
   curl.exe -fsSLo preflight.py 'https://cmudrc.github.io/design-research/_static/workshop-preflight.py'
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe preflight.py

A successful check ends with ``Preflight passed. You are ready for the
workshop.`` Keep the ``design-research-workshop`` folder. Activity materials
will be provided separately for the workshop.
