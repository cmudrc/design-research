Workshop Setup and Preflight
============================

Complete this setup before **AI Experiments in Engineering Design: A Tutorial
on the Design Research Open-Source Ecosystem** at IDETC-CIE 2026 on Sunday,
August 23.

Before Sunday
-------------

Install `Python 3.12 <https://www.python.org/downloads/>`_, open a terminal, and
run the block for your operating system.

On macOS or Linux:

.. code-block:: bash

   python3.12 -c "from urllib.request import urlretrieve; urlretrieve('https://cmudrc.github.io/design-research/_static/idetc2026-design-research-setup.zip', 'idetc2026-design-research-setup.zip')"
   python3.12 -m zipfile -e idetc2026-design-research-setup.zip .
   cd idetc2026-design-research-setup
   python3.12 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python preflight.py

On Windows PowerShell:

.. code-block:: powershell

   py -3.12 -c "from urllib.request import urlretrieve; urlretrieve('https://cmudrc.github.io/design-research/_static/idetc2026-design-research-setup.zip', 'idetc2026-design-research-setup.zip')"
   py -3.12 -m zipfile -e idetc2026-design-research-setup.zip .
   Set-Location idetc2026-design-research-setup
   py -3.12 -m venv .venv
   .venv\Scripts\python -m pip install --upgrade pip
   .venv\Scripts\python -m pip install -r requirements.txt
   .venv\Scripts\python preflight.py

A successful check ends with ``Preflight passed. You are ready for the
tutorial.`` Keep the ``idetc2026-design-research-setup`` folder. The activity
notebooks will be provided separately at the tutorial.
