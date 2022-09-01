import os
import logging
import shutil
from pathlib import Path
from emi import Merx, Epitome

class remove(Merx):
    def __init__(this, name="Remove"):
        super().__init__(name)

        this.transactionSucceeded = True
        this.rollbackSucceeded = True

    # Required Merx method. See that class for details.
    def Transaction(this):
        for tome in this.tomes:
            logging.info(f"Removing {tome}...")
            epitome = this.executor.GetTome(tome, download=False)
            if (epitome is None or epitome.installed_at is None or not len(epitome.installed_at)):
                logging.debug(f"Nothing to remove for {tome}")
                continue

            toRemove = epitome.installed_at.split(';')
            for thing in toRemove:
                logging.debug(f"REMOVING: {thing}")
                thing = Path(thing)
                if (not thing.exists()):
                    logging.debug(f"Could not find {str(thing)}")
                    #That's okay. that might be why we're rolling back ;)
                    continue
                if (thing.is_dir()):
                    shutil.rmtree(thing)
                else:
                    thing.unlink()
                logging.debug(f"Removed {str(thing)}")
                #TODO: error checking
                
            epitome.installed_at = ""
            this.catalog.add(epitome)

    # Required Merx method. See that class for details.
    def DidTransactionSucceed(this):
        return this.transactionSucceeded

    # Required Merx method. See that class for details.
    def Rollback(this):
        #TODO: Implement this...
        super().Rollback()

    # Required Merx method. See that class for details.
    def DidRollbackSucceed(this):
        return this.rollbackSucceeded