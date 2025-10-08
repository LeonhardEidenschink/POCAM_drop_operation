import sys
import time
import cfg_func
import json

# importing configure scripts of values that might change
outfile_cfg = './parameters_cfg.json'
with open(outfile_cfg, 'r') as file:
    cfg_values = json.load(file)

port    = cfg_values['port']
nph     = cfg_values['nphotons']
host    = cfg_values['host']
ntrig   = cfg_values['ntrig']
rep_rate = cfg_values['rep_rate']

to = 20


sys.path.insert(0, '/home/leonhard/pocam/pocam_prod_software/date_20251002/STM32Tools/python/')
from iceboot.POCAMSession import startPOCAMSession


st = startPOCAMSession(host=host, port=port)

# check if icm was rebooted into correct firmware version
icm_fwversion = str(hex(st.icmFWVersion()))
if not icm_fwversion =='0x1700':
    print('ERROR:  ICM FPGA has wrong firmware version booted. \n' \
    'Reboot ICM FPGA to version: 0x1700 then start configure script again. \n')
    raise ValueError("ICM Firmware Version must be 0x1700")


st.toggle_boards(on=False)
st.toggle_pwm(on=False)
st.icmStopCalTrig()
time.sleep(0.2)
st.toggle_boards(on=True)
st.toggle_pwm(on=True)
st.icmReadCalTrigFIFO()
cur_stat = st.cmd("pcmDrop_stat", timeout=to).split()
if not cur_stat[1] == "IDLE":
    print('\nERROR:  Device is not in IDLE state. Reset device before configuring. \n')
    raise ValueError("drop op. status must be IDLE")


if not cur_stat[5] == "1,":
    print('\nERROR:  LID interlock not enabled. Reset device before configuring. \n')
    raise ValueError("LID interlock must be enabled")


if not cur_stat[8] == "1":
    print('\nERROR:  MCU flash not enabled. Reset device before configuring. \n')
    raise ValueError("MCU flash must be enabled")



time.sleep(0.2)


# getting fpga IDs for comparison check
mmb_id = st.mainboardID()
ib_id = st.cfg_id('ib').split(' ')[2]
dbm_id = st.cfg_id('dbm').split(' ')[2]
dbs_id = st.cfg_id('dbs').split(' ')[2]



# checking if IDs match with database and getting right pwm values for kapu driver
c = cfg_func.config(mmb_id, nph)
c.check_ids(ib_id=ib_id, dbm_id=dbm_id, dbs_id=dbs_id)
pwm_m, pwm_s = c.get_pwms()



## Setting flasher HV
st.pwm('kapu1', pwm_m)
st.pwm('kapu2', pwm_s)
####
st.pwm('sipm1', 58000)
st.pwm('sipm2', 58000)
### pulse properties
st.set_pulserSettings('3', enable = False, tpulse=20, period=1000)
### setting Kapustinsky 405 nm default
st.cmd("1 8 1 pcmKapu_set", timeout=to)
st.cmd("2 8 2 pcmKapu_set", timeout=to)

## setting PD properties
st.cmd("3 $3e80 4 pcmPD_ADC_set", timeout=to) # time window and 
st.cmd("1 1 18000 1 pcmPD_pwr_set", timeout=to)
st.cmd("2 1 18000 1 pcmPD_pwr_set", timeout=to)
## setting SiPM
st.cmd("1 1 1 pcmSiPM_set", timeout=to)
st.cmd("2 2 1 pcmSiPM_set", timeout=to)
###
st.cmd("3 0 26600 pcmTDCthr_set", timeout=to)
st.cmd("3 1 1000 pcmTDCthr_set", timeout=to)
st.cmd("3 2 2000 pcmTDCthr_set", timeout=to)
print(st.info_pwm())
####
from datetime import datetime , timezone
prefix = "pdrop_"+datetime.now(timezone.utc).strftime("%m%d_%H%M_")
st.cmd('s" {:s}" pcmDrop_prefix'.format(prefix), timeout=to)

arm_string = str(ntrig) + ' ' + str(rep_rate) + ' pcmDrop_arm'
print(st.cmd(f"{arm_string}", timeout=to))

from time import time_ns

###
time.sleep(3)
print( st.cmd("pcmDrop_stat", timeout=20))
###


# close port for later excess
st.close()