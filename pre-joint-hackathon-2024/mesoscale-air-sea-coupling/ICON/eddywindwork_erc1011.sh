#!/bin/bash
###SBATCH --account=uo0122
###SBATCH --job-name=windwork
###SBATCH --partition=compute
###SBATCH --nodes=1
###SBATCH --mem=0
###SBATCH --output=windwork.run.%j.o
###SBATCH --error=windwork.run.%j.o
###SBATCH --exclusive
###SBATCH --time=01:30:00
###SBATCH --mail-type=END
###SBATCH --mail-user=dian.putrasahan@mpimet.mpg.de
##if [ -z "$1" ] ; then
##    echo "invalid number of parameters: need year"
##    exit 1      #exit out of program
##fi
##if [ -z "$2" ] ; then
##    echo "invalid number of parameters: need month"
##    exit 1      #exit out of program
##fi
##
##yyyy=$1
##mm=$2

#smdeg=3
smdeg=2

expid=erc1011
catdir=/work/bm1344/k203123/icon-mpim/ec1-5/experiments/${expid}/scripts
catalog=${catdir}/${expid}.json
#catdir=/home/m/m300466/EERIE/intake
#catalog=${catdir}/${expid}_200201-200812.json

#outdir=/work/mh0287/m300466/EERIE/${expid}
outdir=/work/bm1344/k203123/reg25/${expid}

#test -d ${outdir} || mkdir -p ${outdir}
#cd ${outdir}
## provide intake find files
##test -f find_files || ln -s /home/k/k203123/Quickplots/find_files .
#test -f find_files || ln -s /home/m/m300466/pyfuncs/find_files .

#varname='Wind_Speed_10m'
#namevar='WSP'
namevarx1='TAUX'
varnamex1='atmos_fluxes_stress_xw'
namevary1='TAUY'
varnamey1='atmos_fluxes_stress_yw'
#namevarxy='TAUmag'
namevarx2='Uocn'
varnamex2='u'
namevary2='Vocn'
varnamey2='v'
#namevarxy='ocnUVmag'
namevarxy='windwork'

test -d ${outdir}/${namevarxy} || mkdir -p ${outdir}/${namevarxy}
#test -d ${outdir}/${namevarxy}/dm || mkdir -p ${outdir}/${namevarxy}/dm
test -d ${outdir}/${namevarxy}/sm${smdeg}deg || mkdir -p ${outdir}/${namevarxy}/sm${smdeg}deg

echo '======================================='

#varfile=`./find_files --catalog_file=${catalog} ${varname} ${expid} --level_type=2d --frequency=1day --time_range 2002-01-02 2002-02-01T23 `

for yyyy in $(seq 2002 2008); 
do
  daterng=${yyyy}'0101-'${yyyy}'1231'
  for mm in $(seq 1 12);
  do
    if [ $mm -lt 10 ]; then mm='0'$mm; else mm=$mm; fi 
###    smvarx1file=${outdir}/${varnamex1}/${smdeg}deg/${expid}_${varnamex1}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc
###    smvary1file=${outdir}/${varnamey1}/${smdeg}deg/${expid}_${varnamey1}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc
###    smvarx2file=${outdir}/${varnamex2}/${smdeg}deg/${expid}_${varnamex2}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc
###    smvary2file=${outdir}/${varnamey2}/${smdeg}deg/${expid}_${varnamey2}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc
###    cdo -chname,${varnamex1},windwork -add -mul -select,name=${varnamex1} [ ${smvarx1file} ] -select,name=${varnamex2},levidx=1 [ ${smvarx2file} ] -mul -select,name=${varnamey1} [ ${smvary1file} ] -select,name=${varnamey2},levidx=1 [ ${smvary2file} ] ${outdir}/${namevarxy}/sm${smdeg}deg/${expid}_${namevarxy}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc
###    cdo -sub -select,year=${yyyy},month=${mm} [ ${outdir}/${namevarxy}/${expid}_${namevarxy}_dm_${daterng}_IFS25.nc ] ${outdir}/${namevarxy}/sm${smdeg}deg/${expid}_${namevarxy}_dm_${yyyy}${mm}_IFS25_sm${smdeg}deg.nc ${outdir}/${namevarxy}/sm${smdeg}deg/${expid}_${namevarxy}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg.nc
    hpvarx1file=${outdir}/${varnamex1}/${smdeg}deg/${expid}_${varnamex1}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg.nc
    hpvary1file=${outdir}/${varnamey1}/${smdeg}deg/${expid}_${varnamey1}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg.nc
    hpvarx2file=${outdir}/${varnamex2}/${smdeg}deg/${expid}_${varnamex2}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg.nc
    hpvary2file=${outdir}/${varnamey2}/${smdeg}deg/${expid}_${varnamey2}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg.nc
    cdo -chname,${varnamex1},windwork -add -mul -select,name=${varnamex1} [ ${hpvarx1file} ] -select,name=${varnamex2},levidx=1 [ ${hpvarx2file} ] -mul -select,name=${varnamey1} [ ${hpvary1file} ] -select,name=${varnamey2},levidx=1 [ ${hpvary2file} ] ${outdir}/${namevarxy}/sm${smdeg}deg/${expid}_${namevarxy}_dm_${yyyy}${mm}_IFS25_hp${smdeg}deg_eddy.nc
  done
done

