import sys
import time
import json
from time import time_ns

sys.path.insert(0, '/home/leonhard/pocam/pocam_prod_software/date_20251002/STM32Tools/python/')
from iceboot.POCAMSession import startPOCAMSession

outfile_cfg = './parameters_cfg.json'
with open(outfile_cfg, 'r') as file:
    cfg_values = json.load(file)

port    = cfg_values['port']
host    = cfg_values['host']


st = startPOCAMSession(host=host, port=port)

to = 20
if st.cmd("pcmDrop_stat", timeout=to).split()[1] == "ARMED":
    ###
    # splitting 64-bit integer into 2 x uint32_t 
    # and then merging on iceboot side into proper uint64 again
    epoch_ns = time_ns()
    epoch_hex = hex(epoch_ns)[2:].zfill(16)
    comm = "${:s} ${:s} pcmDrop_start".format(epoch_hex[0:8], epoch_hex[8:])
    print(st.cmd(comm , timeout=to))
    print("Epoch ns (python):", epoch_ns)
    print("Sleeping to get temperature measurements and some triggers")
    time.sleep(6)
    print( st.cmd("pcmDrop_stat", timeout=20))
    ###
else:
    print('ERROR:  Device is not armed.')
    raise ValueError("drop op. status must be ARMED")



# close port for later excess
st.close()