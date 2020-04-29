import os
import subprocess

base_config_path = os.path.expanduser('~')
base_config_path = os.path.join(base_config_path, 'settings')
base_config_path = os.path.join(base_config_path, 'base_config.yml')
        
cmd = "dmoj-autoconf 1>" + base_config_path + " 2>/dev/null" 
subprocess.call(cmd, shell=True)