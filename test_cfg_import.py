import json
import cfg_func
import sys

outfile = './parameters_cfg.json'

with open(outfile, 'r') as file:
    cfg_values = json.load(file)

port    = cfg_values['port']
nph     = cfg_values['nphotons']
host    = cfg_values['host']
ntrig   = cfg_values['ntrig']
rep_rate = cfg_values['rep_rate']


mmb_id = 'e80000006724ab42'

c = cfg_func.config(mmb_id, nph)


arm_string = str(ntrig) + ' ' + str(rep_rate) + ' pcmDrop_arm'

print(f"{arm_string}")


icm_fwversion = '0x1700'
if not icm_fwversion =='0x1700':
    print('ICM FPGA has wrong firmware version booted. \n' \
    'Reboot ICM FPGA to version: 0x1700 then start configure script again.')
    sys.exit()


print('sys.exit() did not work')