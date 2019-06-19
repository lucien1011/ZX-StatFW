#!/bin/bash

#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/ZXCR_m4l100To170_Nominal/2019-06-18_v1/
#outputDir=DataCard/2019-06-18_v1_ZXCR_m4l100To170/

#inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/ZXCR_m4l130To170_Nominal/2019-06-18_v1_Run2016/
#outputDir=DataCard/ZXCR_m4l130To170_Nominal/2019-06-18_v1_Run2016/
#frPath=/raid/raid7/lucien/AnalysisCode/Higgs/ZXEstimate/Data/FakeRate_Vukasin_190301/fakeRates_2016.root

inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/ZXCR_m4l130To170_Nominal/2019-06-18_v1_Run2018/
outputDir=DataCard/ZXCR_m4l130To170_Nominal/2019-06-18_v1_Run2018/
frPath=/raid/raid7/lucien/AnalysisCode/Higgs/ZXEstimate/Data/FakeRate_Vukasin_190326/FR_WZremoved_18.root

python makeDataCard.py --inputDir ${inputDir} --outputDir ${outputDir} --frPath ${frPath}

python makeWorkspace.py --inputDir ${outputDir} --pattern "*/FakeRate*.txt"

python runCombineTask.py --inputDir ${outputDir} --method FitDiagnostics --selectStr "FakeRate"
