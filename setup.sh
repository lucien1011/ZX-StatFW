export PYTHONPATH=${PYTHONPATH}:${PWD}/
export PATH=${PATH}:${PWD}/bin/

export BASE_PATH=${PWD}

cd /home/lucien/Higgs/DarkZ/Combine/CMSSW_8_1_0/src/ 
eval `scramv1 runtime -sh`
cd -
