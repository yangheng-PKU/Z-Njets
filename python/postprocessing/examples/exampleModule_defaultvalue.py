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
        self.out.branch("z_mass",  "F");
        self.out.branch("z_pt", "F");
	self.out.branch("z_phi","F");
	self.out.branch("jet_id",  "I");
	self.out.branch("jet_pt","F");
	self.out.branch("jet_eta",  "F");
	self.out.branch("njet","I");
	self.out.branch("jet_phi","F");
	self.out.branch("dphi_zjet","F");
	self.out.branch("gen_weight","F");
        self.out.branch("pass_selection",  "B");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ or event.HLT_IsoTkMu24 or event.HLT_IsoMu24):
	    self.out.fillBranch("pass_selection",0)
            return True
	
	electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        Z = ROOT.TLorentzVector()

	tight_muons = []
	
	if (len(muons)<=1):
		self.out.fillBranch("pass_selection",0)
                return True
	for i in range(0,len(muons)):
            if (muons[i].eta) < 2.4 and (muons[i].mediumId) and (muons[i].pfIsoId)>=3:
	        if (muons[i].pt) <= 25:
                    continue
		for j in range(i+1,len(muons)):
  		    if (muons[j].eta) < 2.4 and (muons[j].mediumId) and (muons[j].pfIsoId)>=3:
	                if (muons[j].pt) <= 20:
			    continue
		        if (muons[i].charge + muons[j].charge == 0):
			    Z = muons[i].p4() + muons[j].p4()
			    if (Z.M() > 76 and Z.M() < 106):
				self.out.fillBranch("pass_selection",1)
	            		self.out.fillBranch("z_pt",Z.Pt())
				self.out.fillBranch("z_mass",Z.M())
				self.out.fillBranch("z_phi",Z.Phi())
				tight_muons.append(i)            
				tight_muons.append(j)
				#return True
	
        #print(2)
	if len(tight_muons) < 2:
	    self.out.fillBranch("pass_selection",0)
	    return True
	#print(3)
	njet = 0
	for k in range(0,len(jets)):
            #print(4)
	    if abs(jets[k].eta) > 2.4:
                jets[k].pt = -1000
                jets[k].phi = -1000
                jets[k].jetId = -1000
                continue
            #print(5) 
	    if jets[k].pt < 30:
                jets[k].pt = -1000
                jets[k].phi = -1000
                jets[k].jetId = -1000
		continue
	    #print(6)
	    if not (jets[k].jetId & 1):
                jets[k].pt = -1000
                jets[k].phi = -1000
                jets[k].jetId = -1000
		continue
	    #print(7)
	    pass_lepton_dr_cut = True

	    for i in range(0,len(tight_muons)):
		if deltaR(muons[tight_muons[i]].eta,muons[tight_muons[i]].phi,jets[k].eta,jets[k].phi) < 0.4:
	            pass_lepton_dr_cut = False

	    if not pass_lepton_dr_cut:
                jets[k].pt = -1000
                jets[k].phi = -1000
                jets[k].jetId = -1000
		continue
            njet += 1
	    
	    self.out.fillBranch("jet_pt",jets[k].pt)
	    self.out.fillBranch("jet_id",jets[k].jetId)
	    self.out.fillBranch("jet_phi",jets[k].phi)
	    self.out.fillBranch("dphi_zjet",deltaPhi(Z.Phi(),jets[k].phi))
	
	self.out.fillBranch("njet",njet)
	'''
	if(njet!=0):
	    print(njet)
        '''
	return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

exampleModuleConstr = lambda : exampleProducer() 
 
