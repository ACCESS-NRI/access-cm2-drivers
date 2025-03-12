#!/usr/bin/env python3

# Reformat the data post-processed by um2netcdf4.py to be suitable for the
# ozone redistribution. Metadata has to match file created by iris exactly.

import iris, sys, numpy as np, cftime
from iris.coords import CellMethod

orog = iris.load_cube(sys.argv[1], 'fld_s00i033')
rho = iris.load_cube(sys.argv[1], 'fld_s00i253')
trop = iris.load_cube(sys.argv[1], 'fld_s30i453')

for v in [rho, trop, orog]:
    # Remove these extra attributes (history can prevent concatenation)
    v.attributes = {}
    for cname in ('latitude', 'longitude'):
        v.coord(cname).coord_system = iris.coord_systems.GeogCS(6371229.0)
        v.coord(cname).points = v.coord(cname).points.astype(np.float32)
        v.coord(cname).attributes = {}
        v.coord(cname).long_name = None

trop.standard_name = 'tropopause_altitude'
# Sets the um_stash_source attribute in netCDF file
trop.attributes['STASH'] = iris.fileformats.pp.STASH(1,30,453)
trop.cell_methods = (CellMethod("mean", "time"),)

rho.attributes['STASH'] = iris.fileformats.pp.STASH(1,0,253)
rho.cell_methods = (CellMethod("mean", "time"),)

# Add level height coordinate, settings values to exactly match iris
level_height_bounds = np.array([
0.0, 19.9999985,
19.9999985, 53.333335,
53.333335, 100.000035,
100.000035, 160.00000500000002,
160.00000500000002, 233.33333000000002,
233.33333000000002, 320.00001000000003,
320.00001000000003, 419.99996000000004,
419.99996000000004, 533.33335,
533.33335, 659.999925,
659.999925, 799.9999399999999,
799.9999399999999, 953.33365,
953.33365, 1119.99995,
1119.99995, 1300.0002,
1300.0002, 1493.3335499999998,
1493.3335499999998, 1700.0,
1700.0, 1919.99955,
1919.99955, 2153.33305,
2153.33305, 2399.9996499999997,
2399.9996499999997, 2659.99935,
2659.99935, 2933.333,
2933.333, 3219.9997500000004,
3219.9997500000004, 3519.9996,
3519.9996, 3833.3334,
3833.3334, 4160.0003,
4160.0003, 4499.99945,
4499.99945, 4853.3334,
4853.3334, 5219.9996,
5219.9996, 5599.999750000001,
5599.999750000001, 5993.333,
5993.333, 6399.99935,
6399.99935, 6819.99965,
6819.99965, 7253.33305,
7253.33305, 7699.99955,
7699.99955, 8160.000849999999,
8160.000849999999, 8633.3395,
8633.3395, 9120.007000000001,
9120.007000000001, 9620.0195,
9620.0195, 10133.3685,
10133.3685, 10660.0795,
10660.0795, 11200.161000000002,
11200.161000000002, 11753.6385,
11753.6385, 12320.546,
12320.546, 12900.934500000001,
12900.934500000001, 13494.8805,
13494.8805, 14102.477499999999,
14102.477499999999, 14723.878499999999,
14723.878499999999, 15359.236499999999,
15359.236499999999, 16008.815,
16008.815, 16672.903,
16672.903, 17351.899999999998,
17351.899999999998, 18046.2905,
18046.2905, 18756.7035,
18756.7035, 19483.887,
19483.887, 20228.775999999998,
20228.775999999998, 20992.5265,
20992.5265, 21776.506999999998,
21776.506999999998, 22582.392,
22582.392, 23412.162,
23412.162, 24268.18,
24268.18, 25153.2255,
25153.2255, 26070.588,
26070.588, 27024.109500000002,
27024.109500000002, 28018.261,
28018.261, 29058.227499999997,
29058.227499999997, 30150.018500000002,
30150.018500000002, 31300.536,
31300.536, 32517.7105,
32517.7105, 33810.5945,
33810.5945, 35189.524,
35189.524, 36666.2375,
36666.2375, 38254.029,
38254.029, 39967.9265,
39967.9265, 41824.853500000005,
41824.853500000005, 43843.833,
43843.833, 46046.2085,
46046.2085, 48455.831000000006,
48455.831000000006, 51099.348,
51099.348, 54006.4245,
54006.4245, 57210.015,
57210.015, 60746.7035,
60746.7035, 64656.9585,
64656.9585, 68985.524,
68985.524, 73781.768,
73781.768, 79100.014,
79100.014, 85000.0 ])
level_height_bounds.shape = (85,2)
level_height = iris.coords.AuxCoord.from_coord(rho.coord('atmosphere_hybrid_height_coordinate'))
level_height.var_name = 'rho_level_height'
level_height.standard_name = 'atmosphere_hybrid_height_coordinate'
if 'comments' in level_height.attributes:
    del level_height.attributes['comments']
level_height.long_name = 'level_height'
level_height.bounds = level_height_bounds
vertical_dim = rho.coord_dims('atmosphere_hybrid_height_coordinate')
rho.remove_coord('atmosphere_hybrid_height_coordinate')
rho.add_aux_coord(level_height, vertical_dim)
# Taken from an iris file
sigmavals = np.array([
0.9988703178378605, 0.9958609543494445, 0.9913554222771422,
0.9853639339748554, 0.977900121158012, 0.9689809882708184,
0.9586269847325276, 0.9468619365874433, 0.9337130937430719,
0.9192110832746528, 0.90338992880522, 0.8862871957632836,
0.8679436981974601, 0.8484036126834742, 0.8277146998624683,
0.805927948677273, 0.7830980129368152, 0.7592826066381502,
0.734543106256622, 0.7089441261204913, 0.6825538502965935,
0.6554437841102416, 0.6276888378402183, 0.5993673267187785,
0.5705608258278599, 0.5413546836062403, 0.5118373560028198,
0.4821007782808077, 0.45224022606434383, 0.42235445103577796,
0.3925457306224956, 0.3629194976628622, 0.33358477504338374,
0.3046538751669476, 0.27624257600277374, 0.24847010878557452,
0.22145873782379283, 0.19533420936946502, 0.17022603408794018,
0.14626603165340443, 0.12359046416974817, 0.1023385248809107,
0.08265210444029283, 0.0646774270996039, 0.04856467862905003,
0.03446767795496172, 0.022545399339137694, 0.012962170141052493,
0.005889128229205224, 0.0015053213577387798, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0])
sbounds = np.array([
1.0, 0.9977412750867046,
0.9977412750867046, 0.99398240804637,
0.99398240804637, 0.9887319086991806,
0.9887319086991806, 0.9820017053048774,
0.9820017053048774, 0.9738071111315476,
0.9738071111315476, 0.9641668541070583,
0.9641668541070583, 0.9531030766200717,
0.9531030766200717, 0.9406412979502162,
0.9406412979502162, 0.9268104892015255,
0.9268104892015255, 0.9116429706682841,
0.9116429706682841, 0.8951744686401991,
0.8951744686401991, 0.8774442595747195,
0.8774442595747195, 0.8584947620210737,
0.8584947620210737, 0.8383720345959034,
0.8383720345959034, 0.8171254499928189,
0.8171254499928189, 0.7948077858589021,
0.7948077858589021, 0.771475140430401,
0.771475140430401, 0.7471871883028769,
0.7471871883028769, 0.7220069222008947,
0.7220069222008947, 0.6960006596711161,
0.6960006596711161, 0.6692382865878034,
0.6692382865878034, 0.6417930107530044,
0.6417930107530044, 0.6137413696750177,
0.6137413696750177, 0.5851634598555833,
0.5851634598555833, 0.5561427758035619,
0.5561427758035619, 0.5267659304639668,
0.5267659304639668, 0.4971233715112597,
0.4971233715112597, 0.46730859939624103,
0.46730859939624103, 0.43741872674124527,
0.43741872674124527, 0.40755420141022863,
0.40755420141022863, 0.3778188171815414,
0.3778188171815414, 0.3483198955684122,
0.3483198955684122, 0.3191680995122804,
0.3191680995122804, 0.2904773933738275,
0.2904773933738275, 0.26236511781852073,
0.26236511781852073, 0.234952656271582,
0.234952656271582, 0.20836341927290566,
0.20836341927290566, 0.18272562255024646,
0.18272562255024646, 0.15816925054760358,
0.15816925054760358, 0.1348287514696936,
0.1348287514696936, 0.11284146808862441,
0.11284146808862441, 0.0923482445245987,
0.0923482445245987, 0.07349334516402808,
0.07349334516402808, 0.056424577994753276,
0.056424577994753276, 0.04129402833172342,
0.04129402833172342, 0.028257655095849585,
0.028257655095849585, 0.017477468116064616,
0.017477468116064616, 0.009120471203004651,
0.009120471203004651, 0.0033616981617406966,
0.0033616981617406966, 0.00038481840982484077,
0.00038481840982484077, 0.0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ])
sbounds.shape = (85,2)
sigma = iris.coords.AuxCoord(sigmavals, units="1")
sigma.var_name = 'sigma_rho'
sigma.standard_name = None
sigma.long_name = 'sigma'
sigma.bounds = sbounds
rho.add_aux_coord(sigma, vertical_dim)

model_level_number = iris.coords.DimCoord(np.arange(1,86,dtype=np.int32),
        standard_name="model_level_number", units="1")
model_level_number.attributes["positive"] = "up"
model_level_number.var_name = 'model_rho_level_number'
rho.add_dim_coord(model_level_number, vertical_dim)

# Change lat, lon to 64 bit variables to match those created by um2netcdf_iris.py
trop.coord('latitude').points = trop.coord('latitude').points.astype(np.float64)
trop.coord('longitude').points = trop.coord('longitude').points.astype(np.float64)
rho.coord('latitude').points = rho.coord('latitude').points.astype(np.float64)
rho.coord('longitude').points = rho.coord('longitude').points.astype(np.float64)
trop.coord('latitude').guess_bounds()
trop.coord('longitude').guess_bounds()
rho.coord('latitude').guess_bounds()
rho.coord('longitude').guess_bounds()

# Save orog as surface_altitude, making attributes match those from iris
orog.coord('latitude').points = trop.coord('latitude').points.astype(np.float64)
orog.coord('longitude').points = orog.coord('longitude').points.astype(np.float64)
orog.coord('latitude').guess_bounds()
orog.coord('longitude').guess_bounds()
orog.var_name = 'surface_altitude'
orog = orog[0]
orog.long_name = None
orog.cell_methods = None
orog.grid_mapping = None
orog.attributes['um_stash_source'] = "m01s00i033"

# Time bounds
time = trop.coord('time')
date = time.units.num2date(time.points[0])

# Set bounds for this month
d0 = cftime.DatetimeProlepticGregorian(date.year, date.month, 1, 0, 0, 0)
if date.month < 12:
    endmonth = date.month + 1
    endyear = date.year
else:
    endmonth = 1
    endyear = date.year + 1
d1 = cftime.DatetimeProlepticGregorian(endyear, endmonth, 1, 0, 0, 0)

tbounds = np.empty([1,2],float)
tbounds[0,0] = time.units.date2num(d0)
tbounds[0,1] = time.units.date2num(d1)

trop.coord('time').bounds = tbounds
rho.coord('time').bounds = tbounds


with iris.fileformats.netcdf.Saver(sys.argv[2], 'NETCDF4') as sman:
    sman.write(trop)
    sman.write(rho)
    sman.write(orog)
    # Need these to match the iris file
    sman.update_global_attributes({'Conventions':'CF-1.6',
                                   'source':'Data from Met Office Unified Model',
                                   'um_version':'10.6'})
