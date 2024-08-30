from worlds.kh1.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("KH1Client", exception_logger="Client")
    launch()
