# Autodock Vina and Quickdock
The following README.md describes the process for making use of this autodock vina wrapper. Described below is all the information needed to install the necessary files, prepare the Protein and Ligand files for use, and run the script.

## Environment and Requirements
### Create a conda environment with necessary dependencies and activate it:
```
$ conda create -n advina -c conda-forge -c python=3.7 openbabel=2.4.1 rdkit=2020.03 numpy psutil joblib
$ conda activate advina
```
### Install AutoDock Vina and QuickVina
#### Debian/Ubuntu:
##### Install with apt:
```
$ sudo apt install autodock-vina
```
##### Run with:
```
$ vina --help
```

#### Arch:
##### Clone and build package:
```
$ git clone https://aur.archlinux.org/autodock-vina.git
$ cd  autodock-vina/
$ makepkg -si
```

##### Or install with a package helper:
```
$ yay autodock-vina
```

##### Run with:
```
$ vina --help
```

#### Alternatively make use of Linux Binaries:
##### Download and extract binaries:
```
$ curl http://vina.scripps.edu/download/autodock_vina_1_1_2_linux_x86.tgz
$ tar xzvf autodock_vina_1_1_2_linux_x86.tgz
```
##### Run with:
```
$ ./autodock_vina_1_1_2_linux_x86/bin/vina --help
```

##### Optionally move binaries or add autodock_vina_1_1_2_linux_x86/bin/ to $PATH and run with:
```
$ vina --help
```

#### Download QuickVina Binaries:
##### Download binaries
Located at:
https://qvina.github.io/

##### Set permissions, run and optionally add to path or local bin
```
$ chmod u+x qvina2.1
$ qvina2.1 --help
$ cp qvina2.1 ~/.local/bin/
```

## Protein and Ligand prep
In order to make use of Autodock Vina, protein and ligand files need to be properly prepared. I've included the prepared 6rqu.pdbqt for the CAIX protein converted from the PDB file located at:
https://www.rcsb.org/structure/6rqu

Note that the autodocktools on Debian/Ubuntu and similar repositories is outdated and will likely not run out-of-the-box. This is because it makes use of many depreccated packages, particularly numpy=1.8, PIL (replaced with pillow) for Image and Imagefilter, et cetera. This makes use of Python2.7 which is no longer supported.

For the purposes of ligand prep, this should not be a problem as we can use the .py scripts directly, but to prepare the protein files or run the GUI you will need the entire package on the http://mgltools.scripps.edu website.

### Install AutoDockTools for Ligand/Protein Prep
#### Debian/Ubuntu
```
$ sudo apt install autodocktools
```

#### Arch
##### Clone and build package:
```
$ git clone https://aur.archlinux.org/mgltools-bin.git
$ cd mgltools-bin
$ makepkg -si
```

##### Or install with a package helper:
```
$ yay mgltools-bin
```

#### Alternatively, make use of tar.gz package or install on windows
Package is located at:
http://mgltools.scripps.edu/downloads

### Protein Prep
This will require a working GUI for autodocktools and the protein pdb file. It may be easier to run this on Windows or using the complete package included the dependencies as many dependencies are deprecated.
 
#### 1. Run autodocktools
Run using the bash command
```
$ autodocktools
```
or run the .exe on Windows.

#### 2. Download the Protein file from pdb
Visit and search for the protein at:
https://www.rcsb.org/

For example with the 6RQU CAIX protein:
https://www.rcsb.org/structure/6rqu

Click:
Download Files > PDB FOrmat

#### 3. Load the pdb
Either drag and drop into autodocktools, or load from Files dropdown.

#### 4. Delete water molecules, add hydrogen, and add charges
##### Delete Water molecules
Click:
Edit > Delete Water
##### Add Hydrogen
Click:
Edit > Hydrogens > Add > Check "Polar Only" > OK
##### Add Charges
Click:
Edit > Charges > Add Kollman Charges > OK
#### 5. Save molecule pdbqt
Under the ADT4.2 bar, Click:
Grid > Macromolecule > Choose > Select the protein, e.g. 6rqu > Select Molecule > OK > Save

With this, protein prep is complete.

### Establish Folder Layout
```
├── protein_files
│   ├── 6rqu.pdbqt
├── ligand_files
│   ├── ZINC000019364242.pdbqt
│   ├── ...
├── output
│   ├── ZINC000019364242_out.pdbqt
│   ├── ...
├── config
│   ├── ZINC000019364242.conf
│   ├── ...
├── log
│   ├── ZINC000019364242_log.txt
│   ├── ...
├── ...
├── *.py
└── README.md
```

The root folder should contain a ./protein_files/, ./ligand_files/, ./output/, the python scripts and this README.md.

### Import and run
```
>> from advina import adock
```
Example input:
```
>> adock('./protein_files/6rqu.pdbqt','O=C([O-])CN(CCN(CC(=O)[O-])CC(=O)[O-])CC(=O)[O-]','ZINC000019364242')
>> adock('./protein_files/6rqu.pdbqt','O=C([O-])CN(CCN(CC(=O)[O-])CC(=O)[O-])CC(=O)[O-]','ZINC000019364242',0.0,0.0,0.0,25,25,25)
>> adock('./protein_files/6rqu.pdbqt','O=C([O-])CN(CCN(CC(=O)[O-])CC(=O)[O-])CC(=O)[O-]','ZINC000019364242',vina='qvina2.1')
```

Input parameters are as follows:
```
adock(receptor_input,
        smiles,
        ligand_name,
        center_x=9.879,
        center_y=-13.774,
        center_z=7.012,
        size_x=60,
        size_y=60,
        size_z=60,
        vina='vina',
        seed=None,
        cpu=1,
        lig_dir = './ligand_files/',
        out_dir = './output/',
        log_dir = './log/',
        conf_dir = './config/'):
```
-receptor_input defines input file path for the target protein (required)

-smiles defines the 2d smiles structure (required)

-ligand_name defines the output filename for a given ligand input (required)

-center_x/y/z defines the starting coordinates (default X: 9.879, Y: -13.774, Z: 7.012)

-size_x/y/z defines the search space around the starting coordinates (default X: 60, Y: 60, Z: 60)

-vina defines the software being used called through bash, either the executable on $PATH or the full path to the executable location (default provided)

-seed defines the seed used for random generation, (default: None)

-cpu defines the number of cpus (default: 1)

-lig_dir defines directory for generated ligand .pdbqt files

-out_dir defines output directory for generated results

-log_dir defines directory for docking logs

-conf_dir defines directory for configuration used for a given ligand file
