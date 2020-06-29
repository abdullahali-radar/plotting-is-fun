# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 13:01:49 2020

@author: Weather Radar Team
"""

import wradlib as wrl
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

radarFile='D:/project_webprogramming/wxradarexplore/radarDataExtraction/data/YOG201711271250.mvol'
f = wrl.util.get_wradlib_data_file(radarFile)
data, metadata = wrl.io.read_gamic_hdf5(f)

az=metadata['SCAN1']['az'] # mengekstrak data azimuth disetiap elevasi
r=metadata['SCAN1']['r'] # mengekstrak data range disetiap elevasi
elevation=float('{0:.1f}'.format(metadata['SCAN1']['elevation'])) # ekstrak data elevasi
ppiData=data['SCAN1']['Z']['data'] # mengekstrak data radar
ppiData[ppiData<5]=np.nan
timeSweep=datetime.strptime(str(metadata['SCAN1']['Time']),"b'%Y-%m-%dT%H:%M:%S.%fZ'")

# # PPI 
# fig = plt.figure(figsize=(10,8))
# cgax, pm = wrl.vis.plot_ppi(ppiData, r=r, az=az, fig=fig, proj='cg',
#                             vmin=5,
#                             vmax=50,
#                             cmap='gist_ncar')

# caax = cgax.parasites[0]
# t = plt.title('YOG {} UTC PPI Elev-{}$^\circ$'.format(timeSweep.strftime("%Y-%m-%d %H:%M"),elevation),fontweight="bold")
# t.set_y(1.05)
# cbar = plt.gcf().colorbar(pm, pad=0.075)
# caax.set_xlabel('x_range [km]')
# caax.set_ylabel('y_range [km]')
# plt.text(1.0, 1.05, 'azimuth', transform=caax.transAxes, va='bottom',
#         ha='right')
# cbar.set_label('reflectivity [dBZ]')
# plt.savefig('PPI.png',bbox_inches='tight',dpi=200,pad_inches=0.1)

# Sector PPI
azimuthStart=90. # start azimnuth dalam derajat
azimuthStop=180. # stop azimuth dalam derajat
rangeStart=50000. # range start dalam meter
rangeStop=250000. # range stop dalam meter
indexAziStart=abs(az-azimuthStart).argmin()
indexAziStop=abs(az-azimuthStop).argmin()
indexRangeStart=abs(r-rangeStart).argmin()
indexRangeStop=abs(r-rangeStop).argmin()

sectorPPIData=ppiData[indexAziStart:indexAziStop, indexRangeStart:indexRangeStop]
sectorPPIAzi=az[indexAziStart:indexAziStop]
sectorPPIRange=r[indexRangeStart:indexRangeStop]

cg={'angular_spacing': 30.}
fig = plt.figure(figsize=(10,8))
clevsZ = [5,10,15,20,25,30,35,40,45,50,55,60,65,70]
cgax, pm = wrl.vis.plot_ppi(sectorPPIData,
                            r=sectorPPIRange, az=sectorPPIAzi,
                            fig=fig, proj=cg, rf=1e3,
                            infer_intervals=True,
                            vmin=5,
                            vmax=50,
                            cmap='gist_ncar'
                            )
caax = cgax.parasites[0]
t = plt.title('YOG {}\nSector PPI Elev-{}$^\circ$ (Azi {}$^\circ$ - {}$^\circ$)'.format(timeSweep.strftime("%Y-%m-%d %H:%M"),elevation,az[indexAziStart],az[indexAziStop]),fontweight="bold")
t.set_y(1.05)
cbar = plt.gcf().colorbar(pm, pad=0.075)
caax.set_xlabel('x_range [km]')
caax.set_ylabel('y_range [km]')
plt.text(1.0, 1.05, 'azimuth', transform=caax.transAxes, va='bottom',
        ha='right')
cbar.set_label('reflectivity [dBZ]')

# add floating axis
cgax.axis["lat"] = cgax.new_floating_axis(0,135)
cgax.axis["lat"].set_ticklabel_direction('-')
cgax.axis["lat"].label.set_text("range [km]")
cgax.axis["lat"].label.set_rotation(0)
cgax.axis["lat"].label.set_pad(10)
# plt.savefig('02/{}'.format(timeSweep.strftime("%H%M")),bbox_inches='tight',dpi=200,pad_inches=0.1)
# plt.close()

