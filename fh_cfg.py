#!/usr/bin/env python3

import sys
import time
import json
import subprocess
import os

if __name__ == "__main__":
    outfile_cfg = './parameters_cfg.json'
    with open(outfile_cfg, 'r') as file:
        cfg_values = json.load(file)

    fh_icm_api = cfg_values['fh_icm_api']
    fh_port  = str(cfg_values['fh_port'])
    wp_ad    = str(cfg_values['wp_ad'])
    print("------------- Turning WP ON --------------")
    wire_pair_on = subprocess.run('python3 '+os.path.join(fh_icm_api, "wp_on.py") + ' -p' + fh_port, 
                                  shell=True)
    print("------- Rebooting FPGA to runtime --------")
    fpga_reboot = subprocess.run('python3 '+os.path.join(fh_icm_api, 'icm_fpga_reboot.py')+' -w'+wp_ad+' -i2 -p' + fh_port, 
                                 shell=True)
    print("------------- Doing MCU reset ------------")
    mcu_reset = subprocess.run('python3 '+os.path.join(fh_icm_api, "mcu_reset.py") + ' -p' + fh_port+" -w"+wp_ad, 
                               shell=True)
    print("--------- Enabling LID interlock ---------")
    lid_enable = subprocess.run('python3 '+os.path.join(fh_icm_api, 'lid_enable.py')+' -w'+wp_ad+' -p' + fh_port, 
                                shell=True)
    print("------ Enabling MCU flash interlock ------")

    mcu_flash_enable = subprocess.run('python3 '+os.path.join(fh_icm_api, 'mcu_flash_enable.py')+' -w'+wp_ad+' -p' + fh_port, 
                                      shell=True)
