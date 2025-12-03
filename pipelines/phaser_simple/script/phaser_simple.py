try:
    import ccp4mg
    import mmdb2 as mmdb
except:
    print('FAILED CCP4ModelData imported ccp4mg')
import mmut

from pipelines.phaser_pipeline.script import phaser_pipeline
from core.CCP4PluginScript import CPluginScript

class phaser_simple(phaser_pipeline.phaser_pipeline):
    TASKNAME = 'phaser_simple'                                  # Task name - should be same as class name

    ERROR_CODES = {
        301: {'description': 'Exception in createEnsembleElements'},
        302: {'description': 'Exception setting up search model ensemble'},
        303: {'description': 'Exception setting up fixed structure ensemble'},
    }

    def process(self):
        print("[DEBUG phaser_simple.process] called")
        self.createEnsembleElements()
        print("[DEBUG phaser_simple.process] Ensemble elements created")
        super(phaser_simple,self).process()
        
    def checkInputData(self):
        print("[DEBUG phaser_simple.checkInputData] called")
        invalidFiles = super(phaser_simple,self).checkInputData()
        print(f"[DEBUG phaser_simple.checkInputData] invalidFiles: {invalidFiles}")
        if (not self.container.inputData.INPUT_FIXED) and ('XYZIN_FIXED' in invalidFiles):
            invalidFiles.remove('XYZIN_FIXED')
        print(f"[DEBUG phaser_simple.checkInputData] returning invalidFiles: {invalidFiles}")
        return invalidFiles

    def createEnsembleElements(self):
        try:
            from core.CCP4ModelData import CPdbDataFile, CAtomSelection, CPdbEnsembleItem
            elements = self.container.inputData.ENSEMBLES
            #Before removing all elements from this list, I have to set its listMinLength to 0
            print(f"[DEBUG phaser_simple.createEnsembleElements] elements before clearing: {elements}")
            self.container.inputData.ENSEMBLES.setQualifiers({'listMinLength':0})
            print(f"[DEBUG phaser_simple.createEnsembleElements] listMinLength set to 0")
            while len(elements) > 0: elements.remove(elements[-1])
            print(f"[DEBUG phaser_simple.createEnsembleElements] elements after clearing: {elements}")
            self.container.inputData.ENSEMBLES.append(self.container.inputData.ENSEMBLES.makeItem())
            print(f"[DEBUG phaser_simple.createEnsembleElements] elements after appending new item: {elements}")
            ensemble = self.container.inputData.ENSEMBLES[-1]
            print(f"[DEBUG phaser_simple.createEnsembleElements] ensemble: {ensemble}")
            ensemble.number.set(self.container.inputData.NCOPIES)
            print(f"[DEBUG phaser_simple.createEnsembleElements] ensemble.number set to {self.container.inputData.NCOPIES}")
            ensemble.label.set('SearchModel')
            print(f"[DEBUG phaser_simple.createEnsembleElements] ensemble.label set to 'SearchModel'")
            elements = ensemble.pdbItemList
            print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItemList elements: {elements}")
            while len(elements) > 1: elements.remove(elements[-1])
            while len(elements) < 1: elements.append(elements.makeItem())
            print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItemList elements after removing extras: {elements}")
            pdbItem = elements[-1]
            print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem: {pdbItem}")
            pdbItem.structure.set(self.container.inputData.XYZIN)
            print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem.structure set to {self.container.inputData.XYZIN}")
            if self.container.inputData.ID_RMS == 'ID':
                print(f"[DEBUG phaser_simple.createEnsembleElements] ID_RMS is 'ID', setting identity_to_target to {self.container.inputData.SEARCHSEQUENCEIDENTITY}")
                pdbItem.identity_to_target.set(self.container.inputData.SEARCHSEQUENCEIDENTITY)
                print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem.identity_to_target set")
            elif self.container.inputData.ID_RMS == 'RMS':
                print(f"[DEBUG phaser_simple.createEnsembleElements] ID_RMS is 'RMS', setting rms_to_target to {self.container.inputData.SEARCHRMS}")
                pdbItem.rms_to_target.set(self.container.inputData.SEARCHRMS)
                print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem.rms_to_target set")
            else:
                print(f"[DEBUG phaser_simple.createEnsembleElements] ID_RMS is neither 'ID' nor 'RMS', setting both identity_to_target and rms_to_target to None")
                pdbItem.identity_to_target.set(None)
                print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem.identity_to_target set to None")
                pdbItem.rms_to_target.set(None)
                print(f"[DEBUG phaser_simple.createEnsembleElements] pdbItem.rms_to_target set to None")
        except Exception as e:
            self.appendErrorReport(302, 'Exception setting up search model ensemble: ' + str(e))
            self.reportStatus(CPluginScript.FAILED)
            raise

        try:
            if self.container.inputData.INPUT_FIXED.isSet() and self.container.inputData.INPUT_FIXED and self.container.inputData.XYZIN_FIXED.isSet():
                self.container.inputData.ENSEMBLES.append(self.container.inputData.ENSEMBLES.makeItem())
                ensemble = self.container.inputData.ENSEMBLES[-1]
                ensemble.number.set(0)
                ensemble.label.set('KnownStructure')
                elements = ensemble.pdbItemList
                while len(elements) > 1: elements.remove(elements[-1])
                pdbItem = elements[-1]
                pdbItem.structure.set(self.container.inputData.XYZIN_FIXED)
                if self.container.inputData.FIXED_ID_RMS == 'ID':
                    pdbItem.identity_to_target.set(self.container.inputData.FIXEDSEQUENCEIDENTITY)

                elif self.container.inputData.FIXED_ID_RMS == 'RMS':
                    pdbItem.rms_to_target.set(self.container.inputData.FIXEDRMS)

                self.container.inputData.FIXENSEMBLES.append(self.container.inputData.FIXENSEMBLES.makeItem())
                self.container.inputData.FIXENSEMBLES[-1].set('KnownStructure')
        except Exception as e:
            self.appendErrorReport(303, 'Exception setting up fixed structure ensemble: ' + str(e))
            self.reportStatus(CPluginScript.FAILED)
            raise

        print(f"[DEBUG phaser_simple.createEnsembleElements] Finished creating ensemble elements: {self.container.inputData.ENSEMBLES}")