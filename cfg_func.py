import json
import numpy as np



class config:

    def __init__(self,mmb_id,nphotons):

        self.mmb_id = mmb_id

        outfile = './cfg_pwm_KAPU405_IDs.json'

        with open(outfile, 'r') as file:
            library = json.load(file)

        self.data = library[self.mmb_id]
        self.nphotons = float(nphotons)

    def check_ids(self, ib_id, dbm_id, dbs_id):

        ib_id_match = self.data['ib_id']
        dbm_id_match = self.data['dbm_id']
        dbs_id_match = self.data['dbs_id']

        if ib_id_match == ib_id:
            print('Interface_Board_ID matches')
        else:
            print('\033[1m\033[93mWARNING: Interface_Board_ID DO NOT matches\033[0m')

        if dbm_id_match == dbm_id:
            print('Master_Digital_Board_ID matches')
        else:
            print('\033[1m\033[93mWARNING: Master_Digital_Board_ID DO NOT matches\033[0m')

        if dbs_id_match == dbs_id:
            print('Slave_Digital_Board_ID matches')
        else:
            print('\033[1m\033[93mWARNING: Slave_Digital_Board_ID DO NOT matches\033[0m')



    def get_pwms(self):

        ideal_ph_per_hem = self.nphotons/2

        drop_mmb_ids = ['7a0000006722d242','3200000067249a42','d000000067339042','1d0000006749e742']


        max_ph_m = self.data['master']['max_ph']
        max_ph_s = self.data['slave']['max_ph']

        ratio_m = ideal_ph_per_hem/max_ph_m
        ratio_s = ideal_ph_per_hem/max_ph_s

        fit_m = self.data['master']['fit_values']
        fit_s = self.data['slave']['fit_values']

        if self.mmb_id in drop_mmb_ids: 
            pwm_m = int(np.round((ratio_m-fit_m[1])/fit_m[0],0))
            pwm_s = int(np.round((ratio_s-fit_s[1])/fit_s[0],0))
            
            print('Drop operation device connected, ideal amount of photons can be reached.')
        else:
            if max_ph_m > max_ph_s:
                max_ph = max_ph_s
                pwm_s = 54000
                pwm_m = int(np.round((max_ph/max_ph_m-fit_m[1])/fit_m[0],0))
            else:
                max_ph = max_ph_m
                pwm_m = 54000
                pwm_s = int(np.round((max_ph/max_ph_s-fit_s[1])/fit_s[0],0))
            
            print('\033[1m\033[93m WARNING! Connected device is NO drop operation device. maximum amount of photons per flash is reduced to: ',np.round(max_ph*2*10**(-9),6),'x10^9\033[0m')
        
        return pwm_m, pwm_s




