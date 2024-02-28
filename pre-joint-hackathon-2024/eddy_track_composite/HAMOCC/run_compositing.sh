#!/bin/sh

##ocean variables
declare -a varnamearr=("to" "so" "mlotst" "Wind_Speed_10m" "sea_level_pressure" "atmos_fluxes_HeatFlux_Latent" "atmos_fluxes_HeatFlux_Sensible" "atmos_fluxes_FrshFlux_Precipitation")
#hamocc variables
#declare -a varnamearr=("co2flux" "o2flux" "pco2" "coex90" "NPP" "dissic" "dissoc" "phyp" "phydiaz" "det" "talk" "no3" "po4" "o2" "delcar" "delsil")
#declare -a varnamearr=("calex90" "opex90" "wpoc" "remin" "hi")

#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} cyclonic AR; done
#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} anticyclonic AR; done
#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} cyclonic LC; done
#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} anticyclonic LC; done
#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} cyclonic NB; done
#for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} anticyclonic NB; done
for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} cyclonic SO; done
for varname in "${varnamearr[@]}"; do sbatch compositefields_hamocc.job ${varname} anticyclonic SO; done



#declare -a rgnarr=("AR" "LC" "NB" "SO") 
#declare -a rgnarr=("AR" "LC" "NB") 
#declare -a rgnarr=("SO") 

##hamocc variables
#varname=co2flux
#varname=o2flux
#varname=pco2
#varname=coex90
#varname=NPP
#varname=dissic
#varname=dissoc
#varname=phyp
#varname=phydiaz
#varname=det
#varname=talk
#varname=no3
#varname=po4
#varname=o2
#varname=delcar
#varname=delsil


##ocean variables
#varname=to
#varname=so
#varname=mlotst
#varname=Wind_Speed_10m
#varname=sea_level_pressure
#varname=atmos_fluxes_HeatFlux_Latent
#varname=atmos_fluxes_HeatFlux_Sensible
#varname=atmos_fluxes_FrshFlux_Precipitation

#for rgn in "${rgnarr[@]}"; do sbatch compositefields_hamocc.job ${varname} cyclonic ${rgn}; done
#for rgn in "${rgnarr[@]}"; do sbatch compositefields_hamocc.job ${varname} anticyclonic ${rgn}; done

