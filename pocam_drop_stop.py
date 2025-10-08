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
    to=20

    try:
        output_stop = st.cmd("pcmDrop_stop", timeout=to)
        #print(output_stop)
        if 'ERROR' in output_stop:
            raise
        time.sleep(6)
        #print(output_stop)
    except:
        print(output_stop)
        print('Can not stop drop session, because nothing was running')

    # close port for later excess
    st.close()