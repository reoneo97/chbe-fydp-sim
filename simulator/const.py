const_R = 8.314  # Ideal Gas Constant

palm_acid_wt = 256.43  # g/mol
palm_acid_density = 852  # kg/m3

palm_acid_cap = 93593.  # Max number of kmol to reactor
palm_acid_cap_mol = 9.3593 * 10**7  # Max number of mols to reactor

ipa_density = 786
ipa_wt = 60.1

ipp_density = 852
ipp_wt = 298.511

ptsa_density = 1240
ptsa_wt = 172.2
ptsa_cost_per_g = 22500/1000/1000

zna_particle_size = 32e-6
zna_surface_area = 89.97  # m^2g^-1
zna_pore_diameter = 2.578e-9

# Energy Balance

k_e = 0.1399e-3 * 100   # Average Thermal Conductivity for Solution
h_heater = 4*60  # Overall heat transfer coefficient kJ/min/m^2 K

# Costs
ipa_cost = 3  # USD/kg
ipp_cost = 475  # USD/kg

lps_cost = 5.56e-3  # USD/kg
lps_cost_gj = 4.54  # $/GJ
mps_cost_gj = 4.77  # $/GJ
rw_cost = 0.185e-3  # USD/kg


jacket_reactor_a = 53000
jacket_reactor_b = 28000
jacket_reactor_n = 0.8

# Calculate Temperature after mixing
feed_1_mass_flow = 2712
feed_1_cp = 2.204
feed_1_temp = 45

feed_5_mass_flow = 18810
feed_5_cp = 2.132
feed_5_temp = 30.07

ipa_cp = 4507.5

feed_viscosity = 1.507e-4


# Pressure Drop
rough_cast_iron = 0.25e-3
rough_galv_iron = 0.15e-3
rough_steel = 0.046e-3
