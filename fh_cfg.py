import sys
import time
import json
import subprocess


outfile_cfg = './parameters_cfg.json'
with open(outfile_cfg, 'r') as file:
    cfg_values = json.load(file)

fh_port  = str(cfg_values['fh_port'])
wp_ad    = str(cfg_values['wp_ad'])



fh_server_path = '/home/leonhard/pocam/pocam_prod_software/date_20251002/fh_server'

wire_pair_on = subprocess.run('python '+fh_server_path+'/scripts/wp_on.py -p' + fh_port, shell=True)

#icm_reset = subprocess.run('python '+fh_server_path+'/scripts/icm_reset.py -w'+wp_ad+' -p' + fh_port, shell=True)

mcu_reset = subprocess.run('python '+fh_server_path+'/scripts/mcu_reset.py -w'+wp_ad+' -p' + fh_port, shell=True)

fpga_reboot = subprocess.run('python '+fh_server_path+'/scripts/icm_fpga_reboot.py -w'+wp_ad+' -i2 -p' + fh_port, shell=True)

lid_enable = subprocess.run('python '+fh_server_path+'/scripts/lid_enable.py -w'+wp_ad+' -p' + fh_port, shell=True)

mcu_flash_enable = subprocess.run('python '+fh_server_path+'/scripts/mcu_flash_enable.py -w'+wp_ad+' -p' + fh_port, shell=True)
