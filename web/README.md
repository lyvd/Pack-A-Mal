# Web Interface of Package Analysis

## Installation

### Requirements
- Django
- requests
- wsl on window or Linux os



### some intersting code
    [package-analysis scripts/analysis.sh](https://github.com/lyvd/Pack-A-Mal/blob/9ded033989132e563c63edb4414f1cf6fa0cc3aa/web/package-analysis-web/package_analysis/helper.py#L10)

## Usage

```bash
cd Pack-A-Mal\web\package-analysis-web
python manage.py runserver
```

Connect to [127.0.0.1:8000/package-analysis](http://127.0.0.1:8000/package-analysis)

## demo

Dash board when searching a package, it will display a list of package in wolfi registry
![alt text](images/dashboard.png)


The scan results will display: number of executed command, number of access files, number of system  
![alt text](images/results.png)