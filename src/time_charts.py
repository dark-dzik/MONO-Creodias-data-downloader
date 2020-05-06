import os
import numpy as np
from numpy import cos, sin
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from math import pi
import re
import matplotlib.pyplot as plt

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

# ERUPTION_DIR = os.path.join(DATA_DIR, "Ambrym_2018-12-15")
# lat_volcano = -16.25
# lon_volcano = 168.12
# ERUPTION_DIR = os.path.join(DATA_DIR, "Etna_2018-12-26")
# lat_volcano = 37.734
# lon_volcano = 15.004
# ERUPTION_DIR = os.path.join(DATA_DIR, "Krakatau_2018-12-22")
# lat_volcano = -6.102
# lon_volcano = 105.423
# ERUPTION_DIR = os.path.join(DATA_DIR, "Manam_2019-1-7")
# lat_volcano = -4.1
# lon_volcano = 145.061
# ERUPTION_DIR = os.path.join(DATA_DIR, "Manam_2019-6-28")
# lat_volcano = -4.1
# lon_volcano = 145.061
# ERUPTION_DIR = os.path.join(DATA_DIR, "Sinabung_2019-5-7")
# lat_volcano = 3.17
# lon_volcano = 98.392
# ERUPTION_DIR = os.path.join(DATA_DIR, "Stromboli_2019-7-3")
# lat_volcano = 38.789
# lon_volcano = 15.213
# ERUPTION_DIR = os.path.join(DATA_DIR, "Stromboli_2019-8-28")
# lat_volcano = 38.789
# lon_volcano = 15.213
# ERUPTION_DIR = os.path.join(DATA_DIR, "Taal_2020-1-12")
# lat_volcano = 14.002
# lon_volcano = 120.993
# ERUPTION_DIR = os.path.join(DATA_DIR, "Ulawun_2019-6-26")
# lat_volcano = -5.05
# lon_volcano = 151.33
ERUPTION_DIR = os.path.join(DATA_DIR, "White Island_2019-12-9")
lat_volcano = -37.52
lon_volcano = 177.18


NCs_DIR = os.path.join(ERUPTION_DIR, "unpacked")

# FILE = os.path.join(NCs_DIR, 'Krakatau_2018-12-22_2018-12-23T07:08:56Z.nc')
# Krakatau lat, lon -6.102, 105.423


def tunnel_fast(latvar, lonvar, lat0, lon0):
    '''
    Find closest point in a set of (lat,lon) points to specified point
    latvar - 2D latitude variable from an open netCDF dataset
    lonvar - 2D longitude variable from an open netCDF dataset
    lat0,lon0 - query point
    Returns iy,ix such that the square of the tunnel distance
    between (latval[it,ix],lonval[iy,ix]) and (lat0,lon0)
    is minimum.
    '''
    rad_factor = pi / 180.0  # for trignometry, need angles in radians
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    ny, nx = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    # Compute numpy arrays for all values, no loops
    clat, clon = cos(latvals), cos(lonvals)
    slat, slon = sin(latvals), sin(lonvals)
    delX = cos(lat0_rad) * cos(lon0_rad) - clat * clon
    delY = cos(lat0_rad) * sin(lon0_rad) - clat * slon
    delZ = sin(lat0_rad) - slat
    dist_sq = delX ** 2 + delY ** 2 + delZ ** 2
    minindex_1d = dist_sq.argmin()  # 1D index of minimum element
    iy_min, ix_min = np.unravel_index(minindex_1d, latvals.shape)
    return iy_min, ix_min


def curb_coordinates_area(lat_var, lon_var, lat_centre, lon_centre, lat_range_degrees, lon_range_degrees):
    lat_curbed = np.where(np.abs(lat_var - lat_centre) < lat_range_degrees, lat_var, np.nan)
    lon_curbed = np.where(np.logical_and(np.abs(lon_var - lon_centre) < lon_range_degrees, ~np.isnan(lat_curbed)),
                          lon_var, np.nan)
    # previous lat_curbed does not consider indices of lon_curbed
    lat_curbed = np.where(~np.isnan(lon_curbed), lat_curbed, np.nan)
    return lat_curbed, lon_curbed


date_and_mean_sulfur_tuples = []
for subdir, dirs, files in os.walk(NCs_DIR):
    for file in files:
        if file.endswith('.nc'):
            eruption_datetime = re.search('_(.[^_]*?)T(.[^_]*?)Z', file)
            eruption_datetime = eruption_datetime.group(1) + '\n' + eruption_datetime.group(2)

            file_path = os.path.join(NCs_DIR, file)
            root_group_nc = Dataset(file_path, mode='r+', format='NETCDF4')

            sulfur_total_vcd = np.array(root_group_nc['/PRODUCT/sulfurdioxide_total_vertical_column'])
            # variable from vcd has 3 dims: (time, scanline, ground_pixel),
            # time is always 0, because each file stands for single datetime,
            # hence only 2 dim data array is picked
            sulfur_total_vcd = sulfur_total_vcd[0]
            sulfur_total_vcd = np.float64(sulfur_total_vcd)
            lat_var = np.array(root_group_nc['/PRODUCT/latitude'])
            lat_var = lat_var[0]
            lon_var = np.array(root_group_nc['/PRODUCT/longitude'])
            lon_var = lon_var[0]
            root_group_nc.close()

            lat_curbed, lon_curbed = curb_coordinates_area(lat_var, lon_var, lat_volcano, lon_volcano, 1.0, 2.0)
            sulfur_total_vcd_curbed = np.where(~np.isnan(lon_curbed), sulfur_total_vcd, np.nan)
            mean_sulfur_vcd = np.nanmean(sulfur_total_vcd_curbed)
            date_and_mean_sulfur_tuples.append((eruption_datetime, mean_sulfur_vcd))

date_and_mean_sulfur_tuples.sort(key=lambda tup: tup[0])
dates = [date[0] for date in date_and_mean_sulfur_tuples]
mean_values = [mean_value[1] for mean_value in date_and_mean_sulfur_tuples]
print(date_and_mean_sulfur_tuples)

y_pos = np.arange(len(dates))

plt.bar(y_pos, mean_values, align='center', alpha=0.5)
plt.xticks(y_pos, dates, rotation='vertical')
axes = plt.gca()
axes.set_ylim([0, 0.01])
plt.ylabel('Sulfur Dioxide density [mol per square meter]')
plt.title('Date and time satellite photo was taken')

plt.show()


# rootgrp = Dataset(FILE, 'r+', format='NETCDF4')
# sulfur_total = np.array(rootgrp['/PRODUCT/sulfurdioxide_total_vertical_column'])
# sulfur_total = sulfur_total[0]
# lons = np.array(rootgrp['/PRODUCT/longitude'])
# lons = lons[0]
# lats = np.array(rootgrp['/PRODUCT/latitude'])
# lats = lats[0]
# iy, ix = tunnel_fast(lats, lons, -6.102, 105.423)
#
# print('iy, ix: ', iy, ix)
# print('lat, lon: ', lats[iy, ix], lons[iy, ix])
#
# km_per_lat = km_per_lon_at_equator = 111
# print('lats shape: ', lats.shape)
# print('first scanline: ', lats[0, 0], lats[0, 449])
# print('second scanline: ', lats[277, 0], lats[277, 449])
# print('middle scanline:', lats[138, 0], lats[138, 449])
# print('first diff: ', np.abs(lats[0, 0] - lats[0, 449]))
# print('second diff: ', np.abs(lats[277, 0] - lats[277, 449]))
# print('middle diff:', np.abs(lats[138, 0] - lats[138, 449]))
# print('first diff vertical:', np.abs(lats[0, 0] - lats[277, 0]))
# print('second diff vertical:', np.abs(lats[0, 449] - lats[277, 449]))
# print('first scanline distance: ', np.abs(lats[0, 0] - lats[0, 449]) * km_per_lat)
# print('second scanline distance: ', np.abs(lats[277, 0] - lats[277, 449]) * km_per_lat)
# print('middle scanline distance:', np.abs(lats[138, 0] - lats[138, 449]) * km_per_lat)
# print('first diff vertical distance:', np.abs(lats[0, 0] - lats[277, 0]) * km_per_lat)
# print('second diff vertical distance:', np.abs(lats[0, 449] - lats[277, 449]) * km_per_lat)
# print('************************')
# lats_mask = np.abs(lats - lat_krakatau) < 2.0
# lats_where = np.where(np.abs(lats - lat_krakatau) < 2.0, lats, np.nan)
# lats_where_boolean = np.where(np.abs(lats - lat_krakatau) < 2.0, True, False)
# lats_where_not_nan = np.argwhere(~np.isnan(lats_where))
# print(lats_where)
# # for var in lats_where:
# #     print(var)
# # print(lats[lats_where])
# print('lats shape:', lats.shape)
# print('lats where shape:', lats_where.shape)
# print(np.nanmean(lats_where))
# print(lats_where_not_nan)
# print(np.take(lats, lats_where_not_nan).shape)
# print('************************')
#
# # km_per_lon = cos(lat) * km_per_lon_at_equator
# print('lons shape: ', lons.shape)
# print(lons[0, 0], lons[0, 449])
# print(lons[277, 0], lons[277, 449])
# print('first diff: ', np.abs(lons[0, 0] - lons[0, 449]))
# print('second diff: ', np.abs(lons[277, 0] - lons[277, 449]))
# print('*********************************************')
# lons_where = np.where(np.logical_and(np.abs(lons - lon_krakatau) < 5.0, ~np.isnan(lats_where)), lons, np.nan)
# # print(lons[lats_where])
# print(lons_where)
# print(lons_where.shape)
#
# # print(lons[lons_where])
# # print('lons where shape:', lons[lons_where].shape)
# # print('lats with lons where shape:', lats[lons_where].shape)
# print('*********************************************')
# print('how many not nan in lats_where', np.count_nonzero(~np.isnan(lats_where)))
# print('how many not nan in lons_where', np.count_nonzero(~np.isnan(lons_where)))
# lats_where_considering_lons = np.where(~np.isnan(lons_where), lats, np.nan)
# print('how many not nan in lats_where_considering_lons', np.count_nonzero(~np.isnan(lats_where_considering_lons)))
# lats_indices = np.argwhere(~np.isnan(lats_where_considering_lons))
# lons_indices = np.argwhere(~np.isnan(lons_where))
# print('lats indices', lats_indices)
# print('lons indices', lons_indices)
# print('the same indices?', np.array_equal(lats_indices, lons_indices))
