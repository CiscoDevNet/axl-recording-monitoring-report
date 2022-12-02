# axl-recording-monitoring-report

## Overview

This sample uses the [AXL SOAP API](https://developer.cisco.com/site/axl/) to query a target CUCM for details about the recording/monitoring capabilities of supported devices, then produces a simple markdown report similar to the [Unified CM Silent Monitoring/Recording Supported Device Matrix](https://developer.cisco.com/site/uc-manager-sip/documents/supported/).

Example output from CUCM v14 is included, see [supported_list.md](supported_list.md)

## Requirements

This project was built using Visual Studio Code, and tested with:

* Ubuntu 22.04
* Python 3.10

## Getting started

* From a terminal, clone this repository:

  ```
  git clone https://github.com/CiscoDevNet/axl-recording-monitoring-report
  cd axl-recording-monitoring-report
  ```

* (Optional) Create/activate a Python virtual environment named `venv`:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

* Install needed dependency packages:

    ```bash
    pip install -r requirements.txt
    ```

* Rename `.env.example` to `.env`, and edit it to specify your CUCM address and AXL user credentials.

* Open the directory in Visual Studio Code, select the **Run and Debug** tab, and click the green "Start Debugging" button (or press `F5`.)

  Or, to run from the terminal:

  ```
  python report.py
  ```

The report output will be written to `supported_list.md`
