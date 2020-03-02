#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
##soon to be deprecated
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
##new way of using jme uncertainty
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

from  exampleModule import *
from  exampleFilterModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *

##Function parameters
##(isMC=True, dataYear=2016, runPeriod="B", jesUncert="Total", redojec=False, jetType = "AK4PFchs", noGroom=False)
##All other parameters will be set in the helper module

jmeCorrections = createJMECorrector(True, "2016", "B", "Total", True, "AK4PFchs", False)

fnames=["/nfs/dust/cms/user/hengyang/nanoAOD/03F12777-8E13-C84E-85BA-3D92F2A24C7E.root"]

#fnames=["/eos/cms/store/mc/RunIISummer16NanoAODv5/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7_ext2-v1/120000/FF69DF6E-2494-F543-95BF-F919B911CD23.root"]

#p=PostProcessor(".",fnames,"Jet_pt>150","",[jetmetUncertainties2016(),exampleModuleConstr()],provenance=True)

p=PostProcessor(".",fnames,"","",[countHistogramsModule(),jmeCorrections(),exampleModuleConstr(),exampleFilterModule()],maxEntries=30000,provenance=True,outputbranchsel="output_branch_sel.txt")
p.run()
