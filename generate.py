import os
import shutil
import subprocess
from pathlib import Path
TARGET_FOLDER = "../PQClean-Saber/crypto_kem/"

params = [
    {'name': 'lightsaber', 'def' : ['Saber_type=1']},
    {'name': 'saber', 'def' : ['Saber_type=2']},
] 

for param in params:
    parameterSet = param['name']
    pqcleanDir = f"{TARGET_FOLDER}/{parameterSet}/clean/"

    # delete old files    
    if Path(pqcleanDir).exists():
        shutil.rmtree(pqcleanDir)
    os.makedirs(pqcleanDir)

    nmspc = "PQCLEAN_"+parameterSet.upper().replace("-", "")+"_CLEAN"
    for f in os.listdir(f"saber"):
        # copy over common source files
        shutil.copyfile(f"saber/{f}", f"{pqcleanDir}/{f}")

        # namespace source files
        cmd = f"sed -i 's/PQCLEAN_NAMESPACE/{nmspc}/g' {pqcleanDir}/{f}"
        subprocess.call(cmd, shell=True)

        # remove preprocessor conditionals 
        cmd = f"unifdef -m " + " ".join(["-D"+d for d in param['def']]) + f" {pqcleanDir}/{f}" 
        print(cmd)
        subprocess.call(cmd, shell=True)
    # copy over param specific files 
    for f in os.listdir(f"params/{parameterSet}"):
        shutil.copyfile(f"params/{parameterSet}/{f}", f"{pqcleanDir}/{f}")


    # copy over Makefiles 
    for f in os.listdir(f"make"):
        shutil.copyfile(f"make/{f}", f"{pqcleanDir}/{f}")

        # replace lib name
        cmd = f"sed -i 's/SCHEME_NAME/{parameterSet}/g' {pqcleanDir}/{f}"
        subprocess.call(cmd, shell=True)
    
    # run astyle to fix formatting due to namespace 
    cmd = f"astyle --project {pqcleanDir}/*.[ch]"    
    subprocess.call(cmd, shell=True)
