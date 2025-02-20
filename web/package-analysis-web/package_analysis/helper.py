import requests
import tempfile
import subprocess
import json
import os
import time
import re




class Helper:

    @staticmethod
    def find_root_path():
                # This command to search the analysis script path in wsl environment
        command_search_analysis_script = "wsl pwd"

        if Helper.is_windows_environment():
            command_search_analysis_script = "wsl pwd"
        else:
            command_search_analysis_script = "pwd"
        output_path = subprocess.run(command_search_analysis_script,
                                      shell=True, check=True, capture_output=True,
                                        text=True).stdout.strip()
        # back two directories to get the root directory of Pack-a-mal
        output_list = output_path.split("/")[:-2]
        root_path = "/".join(output_list)
        return root_path

    @staticmethod
    def find_script_path():
        ''' Find scripts/analysis.sh path in the root directory of Pack-a-mal'''
        root_path = Helper.find_root_path()

        # script path is the root directory of Pack-a-mal + scripts/run_analysis.sh
        script_path = root_path + "/scripts/run_analysis.sh"
        return script_path


    @staticmethod
    def is_windows_environment():
        return os.name == 'nt'
    
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
        # /media/listing-0_UwODAKy.1-r0.apk

        local_path = Helper.find_root_path() + '/web/package-analysis-web' + file_path
        package_name = file_path.split("/")[-1].split("-")[0]
        package_version = file_path.split("/")[-1].split("-")[1].split(".apk")[0]
        return Helper.run_package_analysis(package_name, package_version, "wolfi", local_path=local_path)

        

    @staticmethod
    def run_package_analysis(package_name, package_version, ecosystem, local_path=None):
        print(f" Run Package Name: {package_name}, Package Version: {package_version}, Ecosystem: {ecosystem}")
        # ./scripts/run_analysis.sh -ecosystem wolfi -package fijiwashere -version fijiwashere.0.0.0  -local /path/fijiwashere12323-0.0.0-r0.apk -sandbox-image 'wolfi-apk/dynamic-analysis'   -analysis-command 'analyze_wolfi_apk.py' -mode dynamic -nopull 
        # run the script with the package name, version, ecosystem and the path to the apk
        # the script should return the results of the analysis
        # for now, just print the command to the console

        script_path = Helper.find_script_path()
        if local_path:
            command = f"wsl {script_path} -package {package_name} -version {package_version}  -mode dynamic -local {local_path} -nopull"
            print(command)
        else:
            command = f"wsl {script_path} -package {package_name} -version {package_version}  -mode dynamic -nopull"

        try:
            start_time = time.time()
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            end_time = time.time()
            elapsed_time = (end_time - start_time) 
            print(result.stdout)

            json_file_path = os.path.join("/tmp/results/", package_version + ".json")
            
            if Helper.is_windows_environment():
                read_command = f"wsl cat {json_file_path}"
            else:
                read_command = f"cat {json_file_path}"

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
            reports['time'] = elapsed_time

            # example of the reports to test the frontend
            # reports = {
            #     'packages': {            
            #         'package_name': package_name,
            #         'package_version': package_version,
            #         'ecosystem': ecosystem,
            #     },
            #     'time': 0.0,
            #     'install': {
            #         'num_files': 0,
            #         'num_commands': 0,
            #         'num_network_connections': 0,
            #         'num_system_calls': 0,
            #         'files': {
            #             'read': ['file1.txt', 'file2.txt'],
            #             'write': ['file3.txt'],
            #             'delete': ['file4.txt']
            #         },
            #         'dns': ['example.com', 'test.com'],
            #         'ips': [{'Address': '192.168.1.1', 'Port': 80}],
            #         'commands': ['ls', 'mkdir'],
            #         'syscalls': ['open', 'close']  
            #     },
            #     'execute': {
            #         'num_files': 0,
            #         'num_commands': 0,
            #         'num_network_connections': 0,
            #         'num_system_calls': 0,
            #         'files': {
            #             'read': ['file2.txt', 'file5.txt'],
            #             'write': ['file3.txt', 'file6.txt'],
            #             'delete': ['file4.txt']
            #         },
            #         'dns': ['example.com', 'new.com'],
            #         'ips': [{'Address': '192.168.1.1', 'Port': 80}, {'Address': '10.0.0.1', 'Port': 22}],
            #         'commands': ['mkdir', 'rm'],
            #         'syscalls': ['open', 'close']
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
                'files': {
                    'read': [],
                    'write': [],
                    'delete': [],
                },
                'dns': [],
                'ips': [],
                'commands': [],
                'syscalls': []
            },
            'execute': {
                'num_files': 0,
                'num_commands': 0,
                'num_network_connections': 0,
                'num_system_calls': 0,
                'files': {
                    'read': [],
                    'write': [],
                    'delete': [],
                },
                'dns': [],
                'ips': [],
                'commands': [],
                'syscalls': []
            }
        }
        # generate a report based on the data
        # for now, just print the data to the console
        install_phase = json_data.get('Analysis', {}).get('install', {})

        results['install']['num_files'] = len(install_phase.get('Files') or [])
        results['install']['num_commands'] = len(install_phase.get('Commands') or [])
        results['install']['num_network_connections'] = len(install_phase.get('Sockets') or [])
        # for number of system calls divide by 2 because the system calls are 'enter' and 'exit' 
        # so we need to divide by 2 to get the actual number of system calls
        results['install']['num_system_calls'] = len(install_phase.get('Syscalls') or []) // 2

        for file in install_phase.get('Files', []):
            if file.get('Read'):
                results['install']['files']['read'].append(file.get('Path'))
            if file.get('Write'):
                results['install']['files']['write'].append(file.get('Path'))
            if file.get('Delete'):
                results['install']['files']['delete'].append(file.get('Path'))

        for dns in install_phase.get('DNS', []) or []:
            if dns is not None:
                for query in dns.get('Queries', []):
                    results['install']['dns'].append(query.get('Hostname'))
        
        for socket in install_phase.get('Sockets', []) or []:
            if socket is not None:
                results['install']['ips'].append({
                    'Address': socket.get('Address'), 
                    'Port': socket.get('Port')
                })
        
        for command in install_phase.get('Commands', []) or []:
            if command is not None:
                results['install']['commands'].append(command.get('Command'))

        pattern = re.compile(r'^Exit:\s*([\w]+)')
        for syscall in install_phase.get('Syscalls', []):
            if syscall is not None:
                match = pattern.match(syscall)
                if match:
                    results['install']['syscalls'].append(match.group(1))

        execution_phase = json_data.get('Analysis', {}).get('execute', {})

        results['execute']['num_files'] = len(execution_phase.get('Files', []))
        results['execute']['num_commands'] = len(execution_phase.get('Commands', []))
        results['execute']['num_network_connections'] = len(execution_phase.get('Sockets', []))
        results['execute']['num_system_calls'] = len(execution_phase.get('Syscalls', [])) // 2

        for file in execution_phase.get('Files', []):
            if file.get('Read'):
                results['execute']['files']['read'].append(file.get('Path'))
            if file.get('Write'):
                results['execute']['files']['write'].append(file.get('Path'))

        for dns in execution_phase.get('DNS') or []:
            if dns is not None:
                for query in dns.get('Queries', []):
                    results['execute']['dns'].append(query.get('Hostname'))

        for socket in execution_phase.get('Sockets', []) or []:
            if socket is not None:
                results['execute']['ips'].append({
                    'Address': socket.get('Address'), 
                    'Port': socket.get('Port')
                })
        
        for command in execution_phase.get('Commands', []) or []:
            if command is not None:
                results['execute']['commands'].append(command.get('Command'))
        


        pattern = re.compile(r'^Exit:\s*([\w]+)')
        for syscall in execution_phase.get('Syscalls', []):
            if syscall is not None:
                match = pattern.match(syscall)
                if match:
                    results['execute']['syscalls'].append(match.group(1))
        
        return results
