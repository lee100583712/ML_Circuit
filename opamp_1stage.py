####################################################################################################
import os
import numpy as np
import matplotlib.pyplot as plt


####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

####################################################################################################

spice_library = SpiceLibrary('./')

####################################################################################################

circuit = Circuit('opamp')
#I tried using other library files, but it doesn't recognizes it
circuit.include(spice_library['nch'])
#circuit.include(spice_library['ptm65nm_pmos'])

circuit.SinusoidalVoltageSource('Vinn', 'inn', circuit.gnd, amplitude=0.2@u_V,frequency=100@u_kHz)
circuit.V('VDD', 6, circuit.gnd, 1.65@u_V)
circuit.V('VSS', 2, circuit.gnd, -1.65@u_V)
circuit.I('Bias', circuit.gnd, 1, 10@u_uA)

#netlist - MOSFET
# ww1 = 40e-6
# ww2 = ww1
# ww3 = 3e-6
# ww4 = ww3
# ww5 = 5e-6
# ww6 = 1e-6
# llen1 = 3e-6
# llen2 = 4e-6

#180n version
ww1 = 180e-9
ww2 = ww1
ww3 = 18e-6
ww4 = ww3
ww5 = 10e-6
ww6 = 1e-6
llen1 = 180e-9
llen2 = 180e-9


M1 = circuit.M('n1', '4', '4', '6', '6', model='pch', l=llen1, w=ww1)
M2 = circuit.M('n2', '5', '4', '6', '6', model='pch', l=llen1, w=ww2)
M3 = circuit.M('n3', '4', 'inn', '3', '3', model='nch', l=llen2, w=ww3)
# M3 = circuit.M('n3', '4', 'inn', '3', '3', model='nch', l=llen2, w=ww3)
M4 = circuit.M('n4', '5', circuit.gnd, '3', '3', model='nch', l=llen2, w=ww4)
M5 = circuit.M('n5', '3', '1', '2', '2', model='nch',l=llen1, w=ww5)
M6 = circuit.M('n6', '1', '1', '2', '2', model='nch', l=llen1, w=ww6)


simulator = circuit.simulator(temperature=25, nominal_temperature=25)
#op = simulator.operating_point()
analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=100@u_GHz, number_of_points=20,  variation='dec')

## Check Mosfet



## plot
mag = 20*np.log10(np.abs(analysis['5']))
plt.semilogx(analysis.frequency,mag)
plt.show()
