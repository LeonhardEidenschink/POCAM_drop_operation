#!/usr/bin/env python
import json

if __name__ == "__main__":
    from iceboot.POCAMSession import startPOCAMSession

    outfile_cfg = './parameters_cfg.json'
    with open(outfile_cfg, 'r') as file:
        cfg_values = json.load(file)

    port    = cfg_values['port']
    host    = cfg_values['host']
    to = 20
    
    st = startPOCAMSession(host=host, port=port)
    cur_stat =st.cmd("pcmDrop_stat", timeout=to)
    print(cur_stat)
    if not (cur_stat.split()[1] in ["ARMED", "IDLE"]):
      print('\033[1m\033[93m WARNING! Drop is likely still running, continue? [y / n] \033[0m')
      ans = input()
      if ans.lower() != 'y':
          print('Exiting ...')
          exit()
    print('Transfering files from POCAM')
    allfiles = st.flashLS()
    for f_ in allfiles:
        if f_['Name'].endswith('.pdd'):
            print(f"Getting file {f_['Name']} ...")
            st.flashFileGet(f_['Name'])