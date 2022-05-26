{ # try
#    this should work interactivly on lxplus
setupATLAS
} || { #    catch
#    this would work in a condor job on lxplus
ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
} || { #    give up
echo "Cannot execute setupATLAS or find atlasLocalSetup.sh"
exit 1
}
#asetup AnalysisBase,21.2.4
asetup AnalysisBase,22.2.67
