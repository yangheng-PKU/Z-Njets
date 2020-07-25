import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class exampleProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	self.out.branch("pass_selection","B");
	self.out.branch("gen_weight","F");
        self.out.branch("z_mass","F");
        self.out.branch("z_pt","F");
	self.out.branch("z_phi","F");
	self.out.branch("ngoodjets","I");
        self.out.branch("ngoodmuons","I");
        self.out.branch("muon_pt","F",lenVar="ngoodmuons");
        self.out.branch("muon_eta","F",lenVar="ngoodmuons");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        '''
	if not (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ or event.HLT_IsoTkMu24 or event.HLT_IsoMu24):
	    self.out.fillBranch("pass_selection",0)
            return True
        '''
	electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        Z = ROOT.TLorentzVector()

	tight_muons = []
	goodmuons_pt = []
        goodmuons_eta = [] 

	if (len(muons)<=1):
		self.out.fillBranch("pass_selection",0)
                return True
	for i in range(0,len(muons)):
            #if (muons[i].eta) < 2.4 and (muons[i].mediumId) and (muons[i].pfIsoId)>=3:
	     if (muons[i].eta) < 2.4 and (muons[i].mediumId):
	        if (muons[i].pt) <= 25:
                    continue
		for j in range(i+1,len(muons)):
  		    #if (muons[j].eta) < 2.4 and (muons[j].mediumId) and (muons[j].pfIsoId)>=3:
	            if (muons[j].eta) < 2.4 and (muons[j].mediumId):
	                if (muons[j].pt) <= 20:
			    continue
		        if (muons[i].charge + muons[j].charge == 0):
			    Z = muons[i].p4() + muons[j].p4()
			    if (Z.M() > 76 and Z.M() < 106):
				self.out.fillBranch("pass_selection",1)
	            		self.out.fillBranch("z_pt",Z.Pt())
				self.out.fillBranch("z_mass",Z.M())
				self.out.fillBranch("z_phi",Z.Phi())
				tight_muons.append(muons[i])            
				tight_muons.append(muons[j])
	
	if len(tight_muons) < 2:
	    self.out.fillBranch("pass_selection",0)
	    return True

        ngoodmuons = 0
        ngoodmuons = len(tight_muons)
	if ngoodmuons != 2:
            print(ngoodmuons)

        goodmuons_pt.append(tight_muons[0].pt)
        goodmuons_pt.append(tight_muons[1].pt)
        goodmuons_eta.append(tight_muons[0].eta)
        goodmuons_eta.append(tight_muons[1].eta)        
        
        self.out.fillBranch("muon_pt",goodmuons_pt)
        self.out.fillBranch("muon_eta",goodmuons_eta)        
       
	if hasattr(event,"Generator_weight"):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:
            self.out.fillBranch("gen_weight",0)
	return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

exampleModuleConstr = lambda : exampleProducer() 
 
