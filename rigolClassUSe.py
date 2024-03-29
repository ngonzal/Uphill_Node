# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29  2024

@author: nathan gonzalez

Initial class definitions for the Rigol spectrum analyzer DSA 3000
"""


import pyvisa
import numpy as np
from matplotlib import pyplot as plt
import rigolClassObjects as AO

#Set up Spectrum Analyzer
rm=pyvisa.ResourceManager()
#print(rm.list_resources())

instr=rm.open_resource("TCPIP::169.254.163.226::INSTR", resource_pyclass=AO.Rigol_SA)

query = AO.Rigol_SA.IDquery(instr)
#print(query)

AO.Rigol_SA.initialize(instr, 1)
num_steps = 1
ask = AO.Rigol_SA.get_freq(instr, num_steps)

#Plotting
time = np.linspace(1, num_steps*0.5, num_steps)
plt.plot(time, ask)
plt.ylabel('Frequency (MHz)')
plt.xlabel('Time (s)')

#Save to CSV
np.savetxt('one_minute.txt',ask,delimiter=',')



instr.close()
rm.close()