import os
from Feature import Feature
from FeatureExtractor import FeatureExtractor

# Initialization of the main Object
Extractor = FeatureExtractor()

# We needed to have the 105 features of the article published in Sensors "http://mdpi.com/1424-8220/18/1/268"
# So, we must remove the following features.
Extractor.FeatureManagement.Remove(Feature.DC_COMPONENT_TOTAL)
Extractor.FeatureManagement.Remove(Feature.ENERGY_TOTAL)
Extractor.FeatureManagement.Remove(Feature.ENTROPY_TOTAL)

# The Dataset has a 9-DOF containing an Accelerometer 3-axes, a Gyroscope 3-axes and a Magnetometer 3-axes.
Extractor.AddDevice({"name":"Accelerometer",    "tab":["ax","ay","az"]})    # ax, ay, az are the names of the columns for the Accelerometer in the CSV Files
Extractor.AddDevice({"name":"Gyroscope",        "tab":["gx","gy","gz"]})    # gx, gy, gz are the names of the columns for the Gyroscope in the CSV Files
Extractor.AddDevice({"name":"Magnetometer",     "tab":["mx","my","mz"]})    # mx, my, mz are the names of the columns for the Magnetometer in the CSV Files

# If the dataset is not here, download it.
if not os.path.isdir("Datasets/"):
    import subprocess
    def git(*args):
        return subprocess.check_call(['git'] + list(args))
    print("Datasets not detected.")
    print("Downloading ...")
    git("clone", "https://github.com/LIARALab/Datasets.git")
    print("Downloaded.")

raw_folder  = "Datasets/ActivitiesExercisesRecognition/raw/A/"                                  # Path to one exercice of this data
exercice    = "ExoFente"                                                                        # Folder containing the exercice
full_path   = raw_folder+exercice+"/"                                                           # Compilation

print("Running Extractor on \""+full_path+"\"...")
Extractor.ExtractFeaturesFromFolder(full_path,output_file="output.csv",class_added=exercice)    # Running the Extractor on whole folder
print("Finished !")