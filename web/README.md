# Web Interface of Package Analysis

## Installation

### Requirements
- Docker
- Django
- requests
- WSL on Windows or Linux

## Usage

```bash
cd Pack-A-Mal/web/package-analysis-web
python manage.py runserver
```

Connect to [127.0.0.1:8000/package-analysis](http://127.0.0.1:8000/package-analysis)

## Demo

### Dashboard
When searching for a package, it will display a list of packages in the Wolfi registry.
![Dashboard](images/dashboard.png)

### Scan Results
After filling in the necessary information: package name, package version, and package ecosystem, the system will run the Pack-A-Mal tool to get the scan reports and display them in the dashboard interface.

The scan results will display: the number of executed commands, the number of accessed files, and the number of system calls.

There are two phases when analyzing a sample: install and execute.
![Results](images/results.png)
