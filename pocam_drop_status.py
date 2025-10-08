#!/usr/bin/env python

import sys
import time
import json


if __name__ == "__main__":
    from iceboot.POCAMSession import startPOCAMSession

    outfile_cfg = './parameters_cfg.json'
    with open(outfile_cfg, 'r') as file:
        cfg_values = json.load(file)
    port    = cfg_values['port']
    host    = cfg_values['host']

    st = startPOCAMSession(host=host, port=port)
    to = 20
    output = st.cmd("pcmDrop_stat", timeout=to)
    print("======== POCAM drop status ========")
    LID = output.split("LID = ")[1].split(",")[0]
    MCU_flash = output.split("flash = ")[1].split("\n")[0]
    if LID != "1":
        print("\033[1m\033[91mERROR! LID interlock disabled! \033[0m")
    if MCU_flash != "1":
        print("\033[1m\033[91mERROR! MCU flash interlock disabled! \033[0m")
    if output.split()[0] == "OK" and LID == "1" and MCU_flash == "1":
        print("\033[1m\033[92mPOCAM drop status OK ("+output.split()[1]+")\033[0m ")
    elif output.split()[0] == "OK":
        print("\033[1m\033[93mWARNING! Status OK, but interlocks disabled!  \033[0m")
    else : 
        RuntimeError("ERROR! POCAM drop status NOT OK!")
    if output.split()[1] in ["IDLE", "ARMED"]:
        print("\033[1m\033[93mWARNING! DROP IS INACTIVE! \033[0m")

    print(output)
    print("------------- Voltages ------------")
    st.info_pwr()
    st.info_pwm()
    print("----------  Environment ---------")
    print("\tT =", st.readPressureSensorTemperature(), "C")
    print("\tP =", st.readPressure(), "hPa")
    print("---------- Files on flash ---------")
    for f_ in st.flashLS():
        print(f"\t{f_}")
    st.close()