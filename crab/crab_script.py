#!/usr/bin/env python
import os

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleFilterModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *

p=PostProcessor(".",inputFiles(),"",modules=[countHistogramsModule(),exampleModuleConstr(),exampleFilterModule()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis(),outputbranchsel="output_branch_sel.txt")
p.run()

print "DONE"

