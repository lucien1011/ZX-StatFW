#!/bin/bash

inputDir=/raid/raid7/lucien/Higgs/DarkZ/ParaInput/ZXCR_m4l100To170_Nominal/2019-06-18_v1/

python makeDataCard.py --inputDir ${inputDir} --outputDir DataCard/2019-06-18_v1_ZXCR_m4l100To170/

python makeWorkspace.py --inputDir DataCard/2019-06-18_v1_ZXCR_m4l100To170/FakeRateDC/ --pattern "FakeRate*.txt"

python runCombineTask.py --inputDir DataCard/2019-06-18_v1_ZXCR_m4l100To170/ --method FitDiagnostics --selectStr "FakeRate"
