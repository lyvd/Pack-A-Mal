#!/usr/bin/env python3
import asyncio
import importlib
import importlib.metadata
import inspect
import os.path
import signal
import subprocess
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
from dataclasses import dataclass
from typing import Optional
from unittest.mock import MagicMock
import requests
import tarfile


APK_EXTENSION = '.apk'

EXECUTION_LOG_PATH = '/execution.log'
EXECUTION_TIMEOUT_SECONDS = 10


@dataclass
class APK:
    """Class for tracking a apk."""

    def __init__(self, is_local_path: bool = False, local_path: Optional[str] = None, package_name: Optional[str] = None):
        self._isLocalPath = is_local_path
        self._local_path = local_path
        self._package_name = package_name

    @property
    def local_path(self) -> Optional[str]:
        return self._local_path
    
    @property
    def package_name(self) -> Optional[str]:
        return self._package_name

    def install_arg(self) -> str:
        if self.local_path:
            return self.local_path
    
    def execute_arg(self) -> str:
        if self.package_name:
            return self.package_name
        
    def is_local_path(self) -> bool:
        return self._isLocalPath


def install(apk):
    """APK install."""
    arg = apk.install_arg()
    print(f"install ARG: {arg}")
    try:
        output = subprocess.check_output(
            (['apk', 'add', '--allow-untrusted', arg]),
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print('Failed to install:')
        print(e.output.decode())
        # Always raise.
        # Install failing is either an interesting issue, or an opportunity to
        # improve the analysis.
        raise
    else:
        print('Install succeeded:')
        print(output.decode())


def execute_apk(apk):
    if not apk.execute_arg().startswith('solana_web3.js'):
        
        if apk.is_local_path():
            folder_execute = '/usr/local/bin/'
            arg = apk.execute_arg()
        else:
            folder_execute = '/usr/bin/'
            apk_path = apk.local_path 

            parent_dir = os.path.dirname(apk_path)
            # Extract the .tar file
            with tarfile.open(apk_path, 'r:gz') as tar:
                tar.extractall(path=parent_dir)

            # List files in /usr/bin and get the filename only
            
            files = os.listdir(os.path.join(parent_dir, 'usr/bin'))
            file_name = files[-1]
            arg = file_name
            if not arg:
                raise FileNotFoundError("No APK file found in /usr/bin")


        """Execute phase for analyzing the apk."""

        
        print(f"execute ARG: {arg}")
        try:
            output = subprocess.check_output(
                ([folder_execute + arg]),
                stderr=subprocess.STDOUT,
                # timeout=EXECUTION_TIMEOUT_SECONDS
            )
        except subprocess.CalledProcessError as e:
            print('Failed to execute:')
            print(e.output.decode())
            raise
        except subprocess.TimeoutExpired:
            print('Execution timed out.')
            raise
        else:
            print('Execution succeeded:')
            print(output.decode())

    else:
    
        js_code = """const { Account } = require('solana-web3.js/lib/index.browser.cjs.js');
                    const crypto = require('crypto');

                    function generateRandomSecretKey() {
                    return crypto.randomBytes(32).toString('hex');
                    }

                    try {
                    // Example usage
                    const randomSecretKey = generateRandomSecretKey();
                    const account = new Account(randomSecretKey);

                    console.log('Public Key:', account._publicKey.toString('hex'));
                    console.log('Secret Key:', account._secretKey.toString('hex'));
                    } catch (error) {
                    console.error('An error occurred:', error.message);
                    }"""
        
        try:
            output = subprocess.check_output(
                (['node', '-e', js_code]),
                stderr=subprocess.STDOUT)
            print('Execution succeeded:')
            print(output.decode())
        except subprocess.CalledProcessError as e:
            print('Failed to executed:')
            print(e.output.decode())
            # Always raise.
            # Install failing is either an interesting issue, or an opportunity to
            # improve the analysis.
            raise

    

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


def search_apk(package_name):
    raw_package_list = fetch_package_list()
    package_repo_names = [pkg.replace('.apk', '') for pkg in raw_package_list]

    package_repo_names = sorted(package_repo_names, key=lambda x: (x, len(x)))

    for package in package_repo_names:
        if package.startswith(package_name):
            return download_apk(package)
        
    raise ValueError(f'apk {package_name} not found in wolfi registry.')
            
def download_apk(package_repo_name):
    arch = "x86_64"
    package_url = f"https://packages.wolfi.dev/os/{arch}/{package_repo_name}.apk"
    # download the apk and save to temporary location and return the location of the apk
    try:
        response = requests.get(package_url)
        response.raise_for_status()
        with open(f"/tmp/{package_repo_name}.apk", "wb") as f:
            f.write(response.content)
        return f"/tmp/{package_repo_name}.apk"
    except requests.RequestException as e:
        print(f"Failed to download APK: {e}")
        raise
    except IOError as e:
        print(f"Failed to write APK to file: {e}")
        raise
    


PHASES = {
    'all': [install, execute_apk],
    'install': [install],
    'execute': [execute_apk],
}


def main() -> int:
    args = list(sys.argv)
    script = args.pop(0)

    if len(args) < 2 or len(args) > 4:
        print(f'Usage: {script} [--local file | --version version] phase package_name')
        return -1

    # Parse the arguments manually to avoid introducing unnecessary dependencies
    # and side effects that add noise to the strace output.
    local_path = None
    is_local_path = False
    if args[0] == '--local':
        args.pop(0)
        local_path = args.pop(0)
        is_local_path = True
    else:
        local_path = search_apk(args[-1])

    

    phase = args.pop(-2)

    

    if phase not in PHASES:
        print(f'Unknown phase {phase} specified.')
        return 1


    package = APK(is_local_path=is_local_path, local_path=local_path, package_name=args[-1])

    # Execute for the specified phase.
    for phase_func in PHASES[phase]:
        phase_func(package)

    return 0


if __name__ == '__main__':
    exit(main())
