import requests
import tempfile
import subprocess
import json
import os

class Helper:


    script_path = "/mnt/d/HocTap/projectDrVuDucLy/tools/Pack-A-Mal/scripts/run_analysis.sh"

    @staticmethod
    def fetch_package_list():
        urls = [
            "https://apk.dag.dev/https/packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX",
            "https://apk.dag.dev/https/packages.cgr.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX",
            "https://apk.dag.dev/https/packages.cgr.dev/extras/x86_64/APKINDEX.tar.gz/APKINDEX"
        ]
        package_list = []
        for url in urls:
            response = requests.get(url)
            package_list.extend(response.text.splitlines())
        return package_list
    
    @staticmethod
    def search_apk(package_name):
        raw_package_list = Helper.fetch_package_list()
        package_repo_names = [pkg.replace('.apk', '') for pkg in raw_package_list]

        package_repo_names = sorted(package_repo_names, key=lambda x: (x, len(x)))

        for package in package_repo_names:
            if package.startswith(package_name):
                return Helper.download_apk(package)
        
        raise ValueError(f'apk {package_name} not found in wolfi registry.')

    @staticmethod     
    def download_apk(package_repo_name):
        arch = "x86_64"
        package_url = f"https://packages.wolfi.dev/os/{arch}/{package_repo_name}.apk"
        # download the apk and save to temporary location and return the location of the apk
        try:
            response = requests.get(package_url)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".apk") as temp_file:
                temp_file.write(response.content)
                return temp_file.name
            print(f"Failed to download APK: {e}")
            raise
        except IOError as e:
            print(f"Failed to write APK to file: {e}")
            raise

    @staticmethod       
    def get_wolfis_packages():
        packages =  Helper.fetch_package_list()

        data = {'packages': packages}
        return data
    
    @staticmethod
    def handle_uploaded_file(file_path):
        package_name = file_path.split("\\")[-1].removesuffix(".apk")
        package_version = package_name
        return Helper.run_package_analysis(package_name, package_version, "wolfi", file_path)

        

    @staticmethod
    def run_package_analysis(package_name, package_version, ecosystem, local_path=None):
        print(f" Run Package Name: {package_name}, Package Version: {package_version}, Ecosystem: {ecosystem}")
        # ./scripts/run_analysis.sh -ecosystem wolfi -package fijiwashere -version fijiwashere.0.0.0  -local /path/fijiwashere12323-0.0.0-r0.apk -sandbox-image 'wolfi-apk/dynamic-analysis'   -analysis-command 'analyze_wolfi_apk.py' -mode dynamic -nopull 
        # run the script with the package name, version, ecosystem and the path to the apk
        # the script should return the results of the analysis
        # for now, just print the command to the console
        if local_path:
            command = f"wsl {Helper.script_path} -package {package_name} -version {package_version}  -mode dynamic -local {local_path} -nopull"
            print(command)
        else:
            command = f"wsl {Helper.script_path} -package {package_name} -version {package_version}  -mode dynamic -nopull"

        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)

            json_file_path = os.path.join("/tmp/results/" ,  package_version + ".json")
            read_command = f"wsl cat {json_file_path}"
            json_result = subprocess.run(read_command, shell=True,
                                        check=True, capture_output=True,
                                        text=True, encoding='utf-8')
            json_data = json.loads(json_result.stdout)
            reports = Report.generate_report(json_data)
            
            reports['packages'] = {
                'package_name': package_name,
                'package_version': package_version,
                'ecosystem': ecosystem,
            }
            # reports = {

            #     'packages': {
            #         'package_name': "curl",
            #         'package_version': "7.77.0",
            #         'ecosystem': "wolfis",
            #     }, 
            #     'install': {
            #         'num_files': 0,
            #         'num_commands': 0,
            #         'num_network_connections': 0,
            #         'num_system_calls': 0,
            #     },
            #     'execute': {
            #         'num_files': 0,
            #         'num_commands': 0,
            #         'num_network_connections': 0,
            #         'num_system_calls': 0,
            #     }
            # }
    
            return reports
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the analysis: {e.stderr}")
            raise





class Report:

    @staticmethod
    def generate_report(json_data):
        results = {

            'install': {
                'num_files': 0,
                'num_commands': 0,
                'num_network_connections': 0,
                'num_system_calls': 0,
            },
            'execute': {
                'num_files': 0,
                'num_commands': 0,
                'num_network_connections': 0,
                'num_system_calls': 0,
            }
        }
        # generate a report based on the data
        # for now, just print the data to the console
        install_phase = json_data['Analysis']['install']

        results['install']['num_files'] = len(install_phase['Files'])
        results['install']['num_commands'] = len(install_phase['Commands'])
        results['install']['num_network_connections'] = len(install_phase['Sockets'])
        results['install']['num_system_calls'] = len(install_phase['Syscalls'])

        execution_phase = json_data['Analysis']['execute']

        results['execute']['num_files'] = len(execution_phase['Files'])
        results['execute']['num_commands'] = len(execution_phase['Commands'])
        results['execute']['num_network_connections'] = len(execution_phase['Sockets'])
        results['execute']['num_system_calls'] = len(execution_phase['Syscalls'])

        # print(results)
        return results
