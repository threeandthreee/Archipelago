from worlds.wargroove2.client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("Wargroove2Client", exception_logger="Client")
    launch()