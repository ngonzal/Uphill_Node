# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:06:28 2023

@author: nrg4

Initial class definitions for the Rigol spectrum analyzer DSA 3000
"""

import pyvisa
import time
import numpy as np


def converter(x): return float(x) if (x[0] != '#') else float(x[11:])

class Rigol_SA(pyvisa.resources.TCPIPInstrument):
    def __init__(self, *args, **kwargs):
        super(Rigol_SA, self).__init__(*args, **kwargs)
    
    def IDquery (self):
        return self.query('*IDN?')
    
    def initialize (self, channel):
        self.write(':CALCulate:MARKer{}:FCOunt:STATe ON'.format(channel))
        print(self.query(":CALCulate:MARKer{}:FCOunt:STATe?".format(channel)))
    
    def get_freq (self, reps):
        list = []
        for x in range(reps):
            freq = self.query(':CALCulate:MARKer1:FCOunt:X?')
            list.append(float(freq))
            time.sleep(.001)
        return list

class Agilent_Scope(pyvisa.resources.TCPIPInstrument):
    def __init__(self, *args, **kwargs):
        super(Agilent_Scope, self).__init__(*args, **kwargs)

    def set_vert_div(self, channel, div):
        """
        Set the vertical divisions on a channel of the device

        Parameters
        ----------
        div : int
        a vertical division in volts, 8 volts, as 8 for example. 

        channel : int
        channel on the scope on which the divisions should be set

        Returns
        -------
        none

        """
        print("changing vertical divisions on channel {} to".format(
            channel), div, "volts")
        div = div*8
        self.write(':CHANnel{a}:RANGe {b}'.format(a=channel, b=div))
        # return self.query('*OPC?')

    def set_time_div(self, div):
        """
        Set the vertical divisions on a channel of the device

        Parameters
        ----------
        div : int
        a horizontal division in seconds, 8 seconds, as 8 for example. 

        Returns
        -------
        none

        """
        print("changing horizontal divisions to", div, "seconds")
        self.write(':TIMebase:RANGe {}'.format(div))
        # return self.query('*OPC?')

    def get_data(self, index=1):
        """
        retrieve data for a specific channel of the oscilloscope

        Parameters
        ----------
        index : int, optional
            Channel number to retrive the data from. The default is 1.

        Returns
        -------
        xy_data : numpy array
            Returns the X and Y data times, and voltages from a given channel
            in a 2 D numpy array. Units are seconds vs time. 

        """
        # print(instr.query(":WAVeform:FORMat?"))
        self.write(':WAVeform:POINts:MODE RAW')
        self.write(":WAVeform:SOURce CHANnel{}".format(index))
        self.write('DIGITIZE CHAN{}'.format(index))
        self.write(':WAVeform:POINts 500') #set how many points we want from scope trace
        self.write(":WAVeform:FORMat ASCii")
        data = self.query_ascii_values(
            ":WAVeform:DATA?", converter=converter, container=np.array)
        # print(data)
        preamble = self.query(":WAVeform:PREamble?").split(',')
        # print(preamble)
        x = np.add(np.linspace(
            0, len(data)*float(preamble[4]), len(data)), float(preamble[5]))
        xy_data = np.stack([x, data], axis=1)
        return xy_data
