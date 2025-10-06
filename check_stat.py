import sys
import time
import json

sys.path.insert(0, '/home/leonhard/pocam/pocam_prod_software/date_20251002/STM32Tools/python/')
from iceboot.POCAMSession import startPOCAMSession

outfile_cfg = './parameters_cfg.json'
with open(outfile_cfg, 'r') as file:
    cfg_values = json.load(file)

port    = cfg_values['port']
host    = cfg_values['host']


st = startPOCAMSession(host=host, port=port)

to = 20
output = st.cmd("pcmDrop_stat", timeout=to)
print(output)

st.close()