import numpy as np
import os
import pdb
from snr_calculator.genconutils.forminput import MainContainer
from snr_calculator.generate_contour_data import generate_contour_data 

"""
num = 50000
m1 = m2 = np.logspace(5, 10, num)
z = np.logspace(-1,1, num)
st = 1.0
et = 0.0


check2 = snr(m1, m2, z, st, et, chi=0.4, sensitivity_curves=['LPA', 'PL', 'CL'], num_processors=None, num_splits=1000, verbose=10, timer=True)
"""

main = MainContainer(print_output=True)

[main.set_signal_type(sig) for sig in ['all', 'rd']]
main.set_generation_type(num_processors=4, num_splits=100)
main.add_wd_noise(True)
main.output_file_name('testing.txt')
main.set_x_col_name('M_s')
main.set_y_col_name('z')

[main.add_noise_ciurve(curve, noise_type='ASD') for curve in ['PL', 'CL', 'LPA']]

main.set_y_for_grid(1e-2, 1e2, 100, 'log', 'redshift', 'None')
main.set_x_for_grid(1e2, 1e10, 100, 'log', 'total_mass', 'SolarMasses')

main.add_fixed_parameter(0.8, 'mass_ratio', 'None')
main.add_fixed_parameter(0.8, 'spin_1', 'None')
main.add_fixed_parameter(0.8, 'spin_2', 'None')
main.add_fixed_parameter(1.0, 'st', 'Years')
main.add_fixed_parameter(0.0, 'et', 'Years')
main.set_snr_factor(np.sqrt(2.*16./5.))

generate_contour_data(main.return_overall_dictionary())




pdb.set_trace()