import os,copy,math,argparse,ROOT

from CombineStatFW.DataCard import DataCard,CardConfig
from CombineStatFW.Systematic import *
from CombineStatFW.Process import *
from CombineStatFW.Reader import *
from CombineStatFW.Channel import Bin
from CombineStatFW.FileReader import FileReader
from CombineStatFW.RateParameter import RateParameter
from CombineStatFW.BaseObject import BaseObject

from Utils.Hist import getCountAndError,getIntegral
from Utils.mkdir_p import mkdir_p

# ____________________________________________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--outputDir",action="store")
parser.add_argument("--frPath",action="store",default="/home/lucien/AnalysisCode/Higgs/ZXEstimate/Data/FakeRate_Vukasin_190326/FR_WZremoved_17.root")
parser.add_argument("--verbose",action="store_true")

option = parser.parse_args()

# ____________________________________________________________________________________________________________________________________________ ||
# Configurable
inputDir        = option.inputDir
outputDir       = option.outputDir
TFileName       = "StatInput.root"
dataCardName    = "FakeRateDC"
frFilePath      = option.frPath
predCR          = "Data_PredCR_2P2F"

# ____________________________________________________________________________________________________________________________________________ ||
# mass window
data_names = [
        "Data_3P1F",
        ]

bkg_names = [
        "Data_PredCR_2P2F",
        #"WZTo3LNu",
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# bin list
frFile = ROOT.TFile(frFilePath,"READ")
frHistDict = {
        ("Mu","EB"): frFile.Get("Data_FRmu_EB"),
        ("Mu","EE"): frFile.Get("Data_FRmu_EE"),
        ("El","EB"): frFile.Get("Data_FRel_EB"),
        ("El","EE"): frFile.Get("Data_FRel_EE"),
        #("Mu","EB"): frFile.Get("h1D_FRmu_EB"),
        #("Mu","EE"): frFile.Get("h1D_FRmu_EE"),
        #("El","EB"): frFile.Get("h1D_FRel_EB"),
        #("El","EE"): frFile.Get("h1D_FRel_EE"),
        }
binNames = []
for data_name in data_names:
    data_f = ROOT.TFile(os.path.join(option.inputDir,data_name,TFileName),"READ")
    objNames = [ k.GetName() for k in data_f.GetListOfKeys() ]
    for objName in objNames:
        if objName not in binNames: binNames.append(objName)
for bkg_name in bkg_names:
    bkg_f = ROOT.TFile(os.path.join(option.inputDir,bkg_name,TFileName),"READ")
    objNames = [ k.GetName() for k in bkg_f.GetListOfKeys() ]
    for objName in objNames:
        if objName not in binNames: binNames.append(objName)
binList = [
        Bin(binName,inputBinName=binName,signalNames=["Sig",],) for binName in binNames
        if "-Norm" not in binName and "comb" not in binName
        ]

# ____________________________________________________________________________________________________________________________________________ ||
# syst
lnSystReader = LogNormalSystReader()

# ____________________________________________________________________________________________________________________________________________ ||
reader = FileReader()

mkdir_p(os.path.abspath(outputDir))

rateParamDict = {}
fakeRateDict = {}
paramList = []

sel_bin_list = []

for ibin,bin in enumerate(binList):
    if option.verbose: print "-"*20
    if option.verbose: print bin.name
    histName = bin.inputBinName

    # bkg
    for bkgName in bkg_names:
        reader.openFile(inputDir,bkgName,TFileName)
        hist = reader.getObj(bkgName,histName)
        count,error = getIntegral(hist)
        process = Process(bkgName,count if count >= 0. else 1e-12,error)
        bin.processList.append(process)

    # data
    dataCount = 0.
    for sample in data_names:
        reader.openFile(inputDir,sample,TFileName)
        hist = reader.getObj(sample,histName)
        count,error = getIntegral(hist)
        dataCount += count
    error = math.sqrt(dataCount)
    bin.data = Process("data_obs",int(dataCount),error)
 
    bin.systList = []
    #bin.systList.append(
    #        lnNSystematic("DummyStat",bkg_names+["Sig"],lambda syst,procName,anaBin: float(1.002))
    #        )

    if all([process.count == 0. for process in bin.processList]): continue

    sel_bin_list.append(bin)

    # signal
    bin.processList.append(Process("Sig",1e-12,1e-12))

    fs,pTL3,pTL4,etaL3,etaL4 = bin.name.split("_")
    lepCh = fs[-2:]
    fakeRateKeyL3 = "_".join([lepCh,pTL3,etaL3])
    fakeRateKeyL4 = "_".join([lepCh,pTL4,etaL4])
    if fakeRateKeyL3 not in fakeRateDict:
        fakeRateDict[fakeRateKeyL3] = BaseObject(fakeRateKeyL3)
        binNumber = frHistDict[(lepCh,etaL3)].GetXaxis().FindBin(sum(map(float,pTL3.split("-")))/2.)
        fakeRateDict[fakeRateKeyL3].fr_value = frHistDict[(lepCh,etaL3)].GetBinContent(binNumber)
        fakeRateDict[fakeRateKeyL3].fr_error = frHistDict[(lepCh,etaL3)].GetBinError(binNumber)
        #fakeRateDict[fakeRateKeyL3].fr_error = 1.
    if fakeRateKeyL4 not in fakeRateDict:
        fakeRateDict[fakeRateKeyL4] = BaseObject(fakeRateKeyL4)
        binNumber = frHistDict[(lepCh,etaL4)].GetXaxis().FindBin(sum(map(float,pTL4.split("-")))/2.)
        fakeRateDict[fakeRateKeyL4].fr_value = frHistDict[(lepCh,etaL4)].GetBinContent(binNumber)
        fakeRateDict[fakeRateKeyL4].fr_error = frHistDict[(lepCh,etaL4)].GetBinError(binNumber)
        #fakeRateDict[fakeRateKeyL4].fr_error = 1. 
    bin.rateParams.append(RateParameter("Rate_"+bin.name,predCR,"(@0)/(1.-@0)+(@1)/(1.-@1)",fakeRateDict[fakeRateKeyL3].name+","+fakeRateDict[fakeRateKeyL4].name))
    #if fakeRateDict[fakeRateKeyL3].name not in paramList:
    bin.parameterList.append(fakeRateDict[fakeRateKeyL3].name)
    bin.paramDict[fakeRateDict[fakeRateKeyL3].name] = [fakeRateDict[fakeRateKeyL3].name,str(fakeRateDict[fakeRateKeyL3].fr_value),str(fakeRateDict[fakeRateKeyL3].fr_error),"[-5,5]"]
    #if fakeRateDict[fakeRateKeyL4].name not in paramList:
    bin.parameterList.append(fakeRateDict[fakeRateKeyL4].name)
    bin.paramDict[fakeRateDict[fakeRateKeyL4].name] = [fakeRateDict[fakeRateKeyL4].name,str(fakeRateDict[fakeRateKeyL4].fr_value),str(fakeRateDict[fakeRateKeyL4].fr_error),"[-5,5]"]

config = CardConfig(dataCardName)
dataCard = DataCard(config) 
cardDir = outputDir+"/"+dataCard.makeOutFileName("/","")
mkdir_p(cardDir)
dataCard.makeCard(cardDir,sel_bin_list)
reader.end()
