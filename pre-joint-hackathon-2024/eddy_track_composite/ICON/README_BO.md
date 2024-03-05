
# _3D Eddy Tracking & Structure Composites Breakout Group_
_Aaron Wienkers_

Full 3D ICON Outputs, *Native* Grid, 2002–2011: 
```
cat['dkrz.disk.model-output']['icon-esm-er']/
   ['eerie-control-1950']['ocean']['native']/
   ['model-level_daily_mean']
```


# Hacking Dependency Path
1. ✅ ID/Track Eddies — referencing 0.25deg SSH
2. ⏹️ Deal with Native Grid: 
	- Option 1:  [composite_tracks.py](https://github.com/eerie-project/EERIE_hackathon_2023/blob/pre-joint-hackathon-2024/pre-joint-hackathon-2024/eddy_track_composite/ICON/composite_tracks.py) by Moritz, after regridding at higher resolution
	- Option 2:  Remain in the native grid (?)
3. ⏹️ Extract 3D boxes around the tracked eddies


# A Few Ideas to Explore...
### 1. How can we visualise the vertical eddy structure meaningfully ?
- 3D Isocontours ?
- Cuts & Slices ?
- Hovmöller along the eddy-track ?
- ...
### 2. Align/scale the Eddy before compositing, e.g. rotate relative to:
1. Direction of the current ?
2. Direction of the eddy motion ?
3. Eddy semi-major axis ?
### 3. Global statistics for Anti/Cyclonic Ir/Regular Eddies: 
- ✅ Currently classified based on surface GS Vorticity (AE/CE)
- ⏹️ Further classify AE & CE into surface & subsurface (mode-water/irregular) eddies
	- i.e. Split based additionally on the sign of the SST anomaly
	- ![[irregular_regular.png]] [Wang, et al. 2019](https://doi.org/10.5194/os-15-1545-2019)
### 4. Induced vertical motions (Ekman & parapycnal) — BGC/Heat
### 5. Other ideas ?

