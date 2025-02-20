# Web Interface for Package Analysis

## Installation

### Requirements
- Docker
- Django
- requests
- WSL (Windows Subsystem for Linux) on Windows or Linux

## Usage

```bash
cd Pack-A-Mal/web/package-analysis-web
```

Create Database to store informations:

```bash
    python manage.py makemigrations
```

Then apply these migrations to our database, run this command:

```bash
    python manage.py migrate
```

Run the server by using this command. 
```bash
python manage.py runserver
```

Access the web interface at [127.0.0.1:8000/package-analysis](http://127.0.0.1:8000/package-analysis)

## Demo

### Dashboard
When searching for a package, a list of packages in the Wolfi registry will be displayed.
![Dashboard](images/dashboard.png)

### Scan Results
After providing the necessary information (package name, version, and ecosystem), the system will run the Pack-A-Mal tool to generate scan reports, which will be displayed on the dashboard.

The scan results include:
- Number of executed commands
- Number of accessed files
- Number of system calls

The analysis consists of two phases: installation and execution.

![Scan Results](images/results.png)

During analysis, a loader will appear.

![Loader](images/loader.png)

### Report Details
Detailed reports include:
- System calls and their counts during sample analysis
- Analysis history, sorted by the latest analysis

![Report Details](images/report_details.png)
![Additional Report Details](images/report_detail2.png)

The system calls list will be categorized by type and count.

![Analysis History](images/history_analysis.png)

Clicking on a report box will display detailed analysis in a pop-up tab.

![Commands Report](images/1_popup_commands_report.png)
![Network Connections](images/2_popup_network_connections.png)
