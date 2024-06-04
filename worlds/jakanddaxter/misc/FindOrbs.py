import os
import glob
import json

folder_path = "D:\\Applications\\Games\\OpenGOAL\\active\\jak1\\data\\decompiler_out\\jak1\\entities"
files = glob.glob(os.path.join(folder_path, "*.json"))

for f in files:
    print(f)
    with open(f, 'r') as file:
        j = json.load(file)
        for actor in j:
            if "crate" in actor["etype"]:
                if "crate-type" in actor["lump"]:
                    if "'steel" in actor["lump"]["crate-type"]:
                        if 5 == actor["lump"]["eco-info"][0]:
                            print(str(actor["aid"])
                                  + " steel crate + "
                                  + str(actor["lump"]["eco-info"][1]))
            if "orb-cache-top" in actor["etype"]:
                print(str(actor["aid"])
                      + " orb cache + "
                      + str(actor["lump"]["orb-cache-count"]))
            if "gnawer" in actor["etype"]:
                if "extra-count" in actor["lump"]:
                    if 5 == actor["lump"]["extra-count"][0]:
                        print(str(actor["aid"])
                              + " gnawer + "
                              + str(actor["lump"]["extra-count"][1]))
            if "plant-boss" in actor["etype"]:
                if "extra-count" in actor["lump"]:
                    if 5 == actor["lump"]["extra-count"][0]:
                        print(str(actor["aid"])
                              + " plant boss + "
                              + str(actor["lump"]["extra-count"][1]))
            if "money" in actor["etype"]:
                print(str(actor["aid"]) + " orb")
