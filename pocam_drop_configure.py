#!/usr/bin/env python


import sys
import time
import cfg_func
import json

if __name__ == "__main__":
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

    from iceboot.POCAMSession import startPOCAMSession

    st = startPOCAMSession(host=host, port=port)
    # check if icm was rebooted into correct firmware version
    icm_fwversion = st.icmFWVersion()
    if icm_fwversion < 0x1700:
        print('ERROR:  ICM FPGA has wrong firmware version booted. \n' \
        'Reboot ICM FPGA to version: 0x1700 then start configure script again. \n')
        raise RuntimeError("ICM Firmware Version must be 0x1700")
    
    cur_stat = st.cmd("pcmDrop_stat", timeout=to)
    LID = cur_stat.split("LID = ")[1].split(",")[0]
    MCU_flash = cur_stat.split("flash = ")[1].split(" \r\n")[0]
    if not cur_stat.split()[1] == "IDLE":
        print('\033[1m\033[91m\nERROR:  Device is not in IDLE state. POCAM drop was configured or started!\n\033[0m')
        print(cur_stat)
        raise RuntimeError("Drop op. status must be IDLE")

    if not LID == "1":
        print('\033[1m\033[91m\nERROR:  LID interlock not enabled. Enable LID before configuring! \n\033[0m')
        raise RuntimeError("LID interlock must be enabled")

    if not MCU_flash == "1":
        print(MCU_flash)
        print('\033[1m\033[91m\nERROR:  MCU flash not enabled. Reset device before configuring. \n\033[0m')
        raise RuntimeError("MCU flash must be enabled")
    ## Resetting POCAM and ICM FIFOs
    st.toggle_boards(on=False)
    st.toggle_pwm(on=False)
    st.icmStopCalTrig()
    time.sleep(0.2)
    st.toggle_boards(on=True)
    st.toggle_pwm(on=True)
    st.icmReadCalTrigFIFO()
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

    ###
    time.sleep(3)
    print( st.cmd("pcmDrop_stat", timeout=20))
    ###
    # close port for later excess
    st.close()