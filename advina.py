def adock(receptor_name,
        ligand_name,
        center_x=9.879,
        center_y=-13.774,
        center_z=7.012,
        size_x=60,
        size_y=60,
        size_z=60,
        vina='vina'
        seed=None
        cpu=1):

    #Imports
    import os
    import subprocess
    import psutil
    import re

    timeout_duration = 600

    pro_dir = './protein_files/'
    lig_dir = './ligand_files/'
    out_dir = './output/'
    log_dir = './log/'
    conf_dir = './config/'

    protein = pro_dir + receptor_name + '.pdbqt'
    ligand = lig_dir + ligand_name + '.pdbqt'
    output = out_dir + ligand_name + '_out.pdbqt'
    config = conf_dir + ligand_name + '.conf'
    log = log_dir + ligand_name + '_log.txt'

    #Dock
    if os.path.isfile(ligand):
        if not os.path.isfile(output):
            #Create conf files
            conf = 'receptor = ' + protein + '\n' +\
                    'ligand = ' + ligand + '\n' + \
                    'center_x = ' + str(center_x) + '\n' + \
                    'center_y = ' + str(center_y) + '\n' + \
                    'center_z = ' + str(center_z) + '\n' + \
                    'size_x = ' + str(size_x) + '\n' + \
                    'size_y = ' + str(size_y) + '\n' + \
                    'size_z = ' + str(size_z) + '\n' + \
                    'out = ' + output + '\n' + \
                    'seed = ' + str(seed) + '\n' + \
                    'cpu = ' + str(cpu)
            
            #mkdir for output, conf files and logs
            os.makedirs(out_dir, exist_ok=True)
            os.makedirs(conf_dir, exist_ok=True)
            os.makedirs(log_dir, exist_ok=True)
            
            with open(config, 'w') as f:
                f.write(conf)
            with subprocess.Popen('' + vina + \
                    ' --config ' + config + \
                    ' --log ' + log + \
                    ' > /dev/null 2>&1', \
                    shell=True, start_new_session=True) as proc:
                try:
                    proc.wait(timeout=timeout_duration)
                except subprocess.TimeoutExpired:
                    p = psutil.Process(proc.pid)
                    p.terminate()

        result = None
        try:
            score = float("inf")
            with open(output, 'r') as f:
                for line in f.readlines():
                    if "REMARK VINA RESULT" in line:
                        new_score = re.findall(r'([-+]?[0-9]*\.?[0-9]+)', line)[0]
                        score = min(score, float(new_score))
                result = score
        except FileNotFoundError:
            result = None
        
    else:
        result = None

    return (result)
