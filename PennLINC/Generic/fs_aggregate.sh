#!/bin/bash

#path=`ls -d /cbica/projecst/RBC/PNC_fmriprep/freesurfer/stats/aparc.stats`

#Echo columns into CSV 
echo "SubID, LH_Euler, RH_Euler, Sum_Euler, Avg_Euler, LH_MeanThickness, RH_MeanThickness, Sum_MeanThickness, Avg_MeanThickness, LH_SurfaceArea, RH_SurfaceARea, Sum_SurfaceArea, Avg_SurfaceArea, LH_CortexVolume, RH_CortexVolume, Total_CortexVolume" >> /cbica/projects/RBC/PNC_fmriprep/code/FS_aggregate.csv

#loop through freesurfer subjects 

for i in `ls -d /cbica/projects/RBC/PNC_fmriprep/freesurfer/sub-*/`; do
       subid=`echo $i | cut -d "/" -f 10-11`
done 

for i in `ls -d /cbica/projects/RBC/PNC_fmriprep/freesurfer/sub-*/surf/`; do
	LH_Euler=mris_euler_number -o /cbica/projects/RBC/PNC_fmriprep/code/euler.txt lh.orig.nofix 
	RH_Euler=mris_euler_number -o /cbica/projects/RBC/PNC_fmriprep/code/euler.txt rh.orig.nofix 
	let Sum_Euler=$LH_Euler+$RH_Euler
	let Avg_Euler=$Sum_Euler/2
done 

for i in `ls -d /cbica/projects/RBC/PNC_fmriprep/freesurfer/sub-*/stats/`; do 
	LH_MeanThickness=`grep MeanThickness, $i/rh.aparc.stats | cut -d "," -f 4`
	RH_MeanThickness=`grep MeanThickness, $i/lh.aparc.stats | cut d "," -f 4`
	let Sum_MeanThickness=$LH_MeanThickness+$RH_MeanThickness 
	let Avg_MeanThickness=$Sum_MeanThickness/2
	LH_SurfaceArea=`grep WhiteSurfArea, $i/lh.aparc.stats | cut -d "," -f 4`
	RH_SurfaceArea=`grep WhiteSurfArea, $i/rh.aparc.stats | cut -d "," -f 4`
	let Sum_SurfaceArea=$LH_SurfaceArea+$RH_SurfaceArea
	let Avg_SurfaceArea=$Sum_SurfaceArea/2 
	LH_CortexVolume=`grep lhCortexVol, $i/aseg.stats | cut -d "," -f 4`
	RH_CortexVolume=`grep rhCortexVol, $i/aseg.stats | cut -d "," -f 4`
	Total_CortexVolume=`grep CortexVol, $i/aseg.stats | cut -d "," -f 4`
done 

echo "$subid, $LH_Euler, $RH_Euler, $Sum_Euler, $Avg_Euler, $LH_MeanThickness, $RH_MeanThickness, $Sum_MeanThickness, $Avg_MeanThickness, $LH_SurfaceArea, $RH_SurfaceArea, $Sum_SurfaceArea, $Avg_SurfaceArea, $LH_CortexVolume, $RH_CortexVolume, $Total_CortexVolume" >> /cbica/projects/RBC/PNC_fmriprep/code/FS_aggregate.csv


