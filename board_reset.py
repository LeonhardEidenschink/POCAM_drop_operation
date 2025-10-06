import sys
import time
import json
import subprocess


outfile_cfg = './parameters_cfg.json'
with open(outfile_cfg, 'r') as file:
    cfg_values = json.load(file)

fh_port  = str(cfg_values['fh_port'])
wp_ad    = str(cfg_values['wp_ad'])
port    = cfg_values['port']
host    = cfg_values['host']



### just to be save if something is still running. Stop and disarm the device
sys.path.insert(0, '/home/leonhard/pocam/pocam_prod_software/date_20251002/STM32Tools/python/')
from iceboot.POCAMSession import startPOCAMSession



st = startPOCAMSession(host=host, port=port)

to=20

try:
    output_stop = st.cmd("pcmDrop_stop", timeout=to)
    if 'ERROR' in output_stop:
        raise
    time.sleep(6)
    #print(output_stop)
except:
    print(output_stop)
    print('Can not stop drop session, because nothing was running')



try:
    output_disarm = st.cmd("pcmDrop_disarm", timeout=to)
    if 'ERROR 2' in output_disarm:
        raise
except:
    print(output_disarm)
    print('Can not disarm POCAM, because it was not armed')


st.toggle_pwm(on=False)
st.toggle_boards(on=False)
st.icmStopCalTrig()

# close port for later excess
st.close()

