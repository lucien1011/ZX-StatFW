import glob,os,argparse,subprocess
from CombineAPI.CombineInterface import CombineAPI,CombineOption 

parser = argparse.ArgumentParser()
parser.add_argument("--inputDir",action="store")
parser.add_argument("--selectStr",action="store")
parser.add_argument("--option",action="store",type=str)
parser.add_argument("--pattern",action="store")
parser.add_argument("--method",action="store",default="AsymptoticLimits")

option = parser.parse_args()

inputDir = option.inputDir
pattern = "window*.root" if not option.pattern else option.pattern

api = CombineAPI()
for cardDir in glob.glob(inputDir+"*"+option.selectStr+"*/") if option.selectStr else [inputDir,]:
    print "Running on directory "+cardDir
    wsFilePath = cardDir+cardDir.split("/")[-2]+".root"
    if option.option:
        optionList = option.option.split()
    else:
        optionList = []
    combineOption = CombineOption(cardDir,wsFilePath,option=optionList,verbose=True,method=option.method)
    api.run(combineOption)
