
import ROOT,argparse,sys,os
from collections import OrderedDict

def plotStyle(hist,color=ROOT.kBlue):
    hist.GetYaxis().SetTitle("#frac{#theta - #theta_{0}}{#sigma_{0}}")
    hist.SetLineColor(color)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(1.0)
    hist.SetLineWidth(2)
    hist.GetXaxis().LabelsOption("v")
    hist.SetMaximum(3.)
    hist.SetMinimum(-3.)
    #hist.SetStats(0)
    hist.SetMarkerColor(color)

def makePlot(postFitDict,preFitDict,histName="postFitNuisance",labelFunc=None):
    nNuis = len(postFitDict)
    hist = ROOT.TH1D(histName,"Nuisance parameters",nNuis,0,nNuis)
    iNuis = 1
    for nuisName,nuisTuple in postFitDict.iteritems():
        nuisValue,nuisErr = nuisTuple
        preFitValue,preFitError = preFitDict[nuisName]
        hist.SetBinContent(iNuis,(nuisValue-preFitValue)/preFitError)
        hist.SetBinError(iNuis,nuisErr/preFitError)
        hist.GetXaxis().SetBinLabel(iNuis,nuisName if not labelFunc else labelFunc(nuisName))
        iNuis += 1
    return hist

# __________________________________________________________________________________________________________ ||
parser = argparse.ArgumentParser()

parser.add_argument('--inputPath',action='store')
parser.add_argument('--outputPath',action='store')
parser.add_argument('--verbose',action='store_true')

option = parser.parse_args()

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

# __________________________________________________________________________________________________________ ||
inputFile = ROOT.TFile(option.inputPath,"READ")
nuisDict = OrderedDict()
for fitResultName in ["fit_b","nuisances_prefit_res",]:
    fitResult = inputFile.Get(fitResultName).floatParsFinal()
    nuisDict[fitResultName] = OrderedDict()
    for i in range(fitResult.getSize()):
        nuis = fitResult.at(i)
        nuisName = nuis.GetName()
        if option.verbose: print "Processing ",nuisName
        nuisDict[fitResultName][nuisName] = (nuis.getVal(),nuis.getError())

# __________________________________________________________________________________________________________ ||
#postFitHist = makePlot(nuisDict,"postfit")
#preFitHist = makePlot(nuisDict,"prefit")
#postFitPlot = getGraph(postFitHist,0.)
#preFitPlot = getGraph(preFitHist,0.)
postFitPlot = makePlot(nuisDict["fit_b"],nuisDict["nuisances_prefit_res"],"postfit")
#preFitPlot = makePlot(nuisDict["nuisances_prefit_res"],"prefit")
plotStyle(postFitPlot,color=ROOT.kBlue)
#plotStyle(preFitPlot,color=ROOT.kBlack)
postFitPlot.GetYaxis().SetRangeUser(-3.,3.)
#preFitPlot.GetYaxis().SetRangeUser(-3.,3.)
c = ROOT.TCanvas()
#preFitPlot.SetFillColor(ROOT.kGray)
#preFitPlot.SetMarkerSize(0.001)
#preFitPlot.Draw("E2")
#preFitPlot.GetXaxis().SetLabelSize(0.02)
postFitPlot.GetXaxis().SetLabelSize(0.02)
postFitPlot.Draw("Esame")
c.SetGridx()
c.SetGridy()
c.RedrawAxis('g')
if not os.path.exists(os.path.dirname(os.path.abspath(option.outputPath))):
    os.makedirs(os.path.dirname(os.path.abspath(option.outputPath)))
c.SaveAs(option.outputPath)

# __________________________________________________________________________________________________________ ||
