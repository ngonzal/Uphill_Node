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
instr=rm.open_resource("TCPIP::169.254.34.26::INSTR", resource_pyclass=AO.Rigol_SA)

#Check connection
#query = AO.Rigol_SA.IDquery(instr)
#print(query)

#Set up peak table thresholds
out = AO.Rigol_SA.peak_setup(instr)
#print(out)

#Collect frequencies, amplitude, and time
num_steps = 430000
freq, amp, t = AO.Rigol_SA.peak_table_read(instr, num_steps)

#print(freq)

#%%
#Plotting
#t = np.linspace(1, num_steps*0.01, num_steps)
"""
plt.plot(t, freq)
plt.plot(t, amp)
plt.ylabel('Frequency (MHz)')
plt.xlabel('Time (s)')
"""
#%%
#Save to CSV
np.savetxt('2hfreq.txt',freq,delimiter=',')
np.savetxt('2hamp.txt',amp,delimiter=',')
np.savetxt('2htime.txt',t,delimiter=',')



instr.close()
rm.close()