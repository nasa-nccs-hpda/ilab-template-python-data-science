import os
import re
import datasets
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st
import streamlit.components.v1 as components
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
import rioxarray as rxr
import xarray as xr
import pandas as pd
from glob import glob
from pathlib import Path
from datetime import datetime
from huggingface_hub import snapshot_download, hf_hub_download

# define dataset url
DATASET_URL = 'jordancaraballo/alaska-wildfire-occurrence'
EPSG = 3338

# Grab the dataset from Hugging Face
#cgl_dataset_dir = snapshot_download(repo_id=DATASET_URL, allow_patterns="*.tif", repo_type='dataset')
#cgl_filename = glob(os.path.join(cgl_dataset_dir, 'alaskan-tundra-lightning-forecast_latest.tif'))[0]

cgl_filename = hf_hub_download(
    repo_id=DATASET_URL, 
    filename='alaskan-tundra-lightning-forecast_latest.tif', 
    repo_type="dataset")

#print(cgl_dataset_dir)

# Open the filename from the forecast
cgl_ds = rxr.open_rasterio(cgl_filename)

# Rename bands with timestamps
cgl_ds['band'] = cgl_ds.attrs['DATES'].replace("'", "").strip('][').split(', ')

# Generate visualization
fig = plt.figure()
ax = plt.axes(projection=ccrs.epsg(EPSG))
ax.coastlines()

# Generate merge with cartipy
mesh = cgl_ds.isel(band=0).plot.pcolormesh(
    ax=ax, transform=ccrs.epsg(EPSG), animated=True,cmap='seismic', vmin=0, vmax=1)

# Define update function
def update_mesh(t):
    ax.set_title("time = %s"%t)
    mesh.set_array(cgl_ds.sel(band=t).values.ravel())
    return mesh,

# Generate animation function
animation = FuncAnimation(
    fig, update_mesh, frames=cgl_ds.band.values, interval=600)
animation_js = animation.to_jshtml()

# Adding autoplay
click_on_play = """document.querySelector('.anim-buttons button[title="Play"]').click();"""

## Search for the creation of the animation within the jshtml file created by matplotlib
pattern = re.compile(r"(setTimeout.*?;)(.*?})", re.MULTILINE | re.DOTALL)

## Insert the JS line right below that
animation_js = pattern.sub(rf"\1 \n {click_on_play} \2", animation_js)

# Plot text and animation on streamlit page
st.title("Alpha Version - Alaskan Tundra 10-day Lightning Forecast")
st.markdown(
    "Cloud to ground lightning 10-day lightning forecast for the Alaskan tundra. " +
    "This is still work in progress and under development.")
components.html(animation_js, height=1000)
