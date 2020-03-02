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
	self.out.branch("jet_id","I",lenVar="ngoodjets");
	self.out.branch("jet_pt","F",lenVar="ngoodjets");
	self.out.branch("jet_phi","F",lenVar="ngoodjets");
	self.out.branch("dphi_zjet","F",lenVar="ngoodjets");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ or event.HLT_IsoTkMu24 or event.HLT_IsoMu24):
	    self.out.fillBranch("pass_selection",0)
            return True
        '''
	if hasattr(event,"Generator_weight"):
	    self.out.fillBranch("gen_weight",event.Generator_weight)
	else:
            self.out.fillBranch("gen_weight",0)
	'''
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

	ngoodjets = 0
        goodjets_pt = []
	goodjets_id = []
	goodjets_phi = []
	goodjets_dphi_zjet = []

	for k in range(0,len(jets)):
            #print(4)
	    if abs(jets[k].eta) > 2.4:
                continue
            #print(5) 
	    if jets[k].pt < 30:
		continue
	    #print(6)
	    if not (jets[k].jetId & 1):
		continue
	    #print(7)
	    pass_lepton_dr_cut = True

	    for i in range(0,len(tight_muons)):
		if deltaR(muons[tight_muons[i]].eta,muons[tight_muons[i]].phi,jets[k].eta,jets[k].phi) < 0.4:
	            pass_lepton_dr_cut = False

	    if not pass_lepton_dr_cut:
		continue

            ngoodjets += 1
            goodjets_pt.append(jets[k].pt)
	    goodjets_id.append(jets[k].jetId)
	    goodjets_phi.append(jets[k].phi)	    
	    goodjets_dphi_zjet.append(deltaPhi(Z.Phi(),jets[k].phi))            

        if ngoodjets != len(goodjets_pt):
            print(error)

	self.out.fillBranch("ngoodjets",ngoodjets)
        self.out.fillBranch("jet_pt",goodjets_pt)
	self.out.fillBranch("jet_id",goodjets_id)
	self.out.fillBranch("jet_phi",goodjets_phi)
	self.out.fillBranch("dphi_zjet",goodjets_dphi_zjet)
	'''
	if(njet!=0):
	    print(njet)
        '''
	if hasattr(event,"Generator_weight"):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:
            self.out.fillBranch("gen_weight",0)
	return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

exampleModuleConstr = lambda : exampleProducer() 
 
