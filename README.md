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

### Ligand Prep
Ligand prep can be done without the GUI making use of the compiled python script "prepare_ligand4.py".
If installed from repository, you can find it in your /usr/lib/python2.7/dist-packages/AutoDockTools/Utilities24/ folder.

This is assuming you already have mol2 or pdb ligand files with conformers generated. Alternatively, ligand pdbqt files can also be generated from smiles using obabel, more details below.

#### Convert mol2 or pdb to pdbqt
##### Make a folder and copy any .mol2 or .pdb to be converted
```
$ mkdir ./ligand_files/
$ cp /home/usr/dir/{foo.mol2,bar.pdb} ./ligand_files/
```

##### Run the autodocktools python script on all files in the folder with the .mol2 or .pdb extension
```
$ source deactivate
$ find ./ligand_files/ -name "*.mol2" -o -name "*.pdb" | xargs -r -n 1 python2.7 /usr/lib/python2.7/dist-packages/AutoDockTools/Utilities24/prepare_ligand4.py
```

Autodocktools rely on python2.7, so make sure to deactivate the source before preparing your ligand files.
This will convert all files ending in ".mol2" or ".pdb" into ".pdbqt" format required. With this, ligand prep is complete.

#### Alternatively, generate pdbqt from smiles using obabel
##### Convert $SMI using $NAME to $NAME.pdbqt
```
$ obabel -:"$SMI" -O ./ligand_files/$NAME.pdbqt -h --gen3d > /dev/null 2>&1
```

This will run obabel using the SMILES $SMI as input, $NAME.pdbqt as output, -h to add hydrogens, --gen3d to create a 3d model and silence the program errors by redirecting output to /dev/null.

Example use given tranche file CAAAML.smi downloaded from leadlike zinc15 database:
```
smiles zinc_id
0=C{[O...	ZINC000019364242
...
```

You can iterate through each file in the list using:
```
$ dos2unix CAAAML.smi
$ sed 1d CAAAML.smi | while IFS= read -r SMILES NAME
	do
		obabel -:"$SMI" -O ./ligand_files/$NAME.pdbqt -h --gen3d > /dev/null 2>&1
	done
```

Note that the first line used is to convert the tranche file's EOL line ending from dos format to unix.
This will skip the first line (header) of the file, read through each subsequent line of the file and assign the first column as $SMILES and second column as $NAME, and use babel to convert the smiles into a 3d pdbqt file.

#### Note
Alternatively, I can wrap this in python to be called there, but for my workflow I found it easier to prep the protein/ligand files beforehand in bash. Please let me know if there's any changes you'd like to see.

### Establish Folder Layout
```
├── protein_files
│   ├── 6rqu.pdbqt
├── ligand_files
│   ├── A1J.pdbqt
│   ├── ...
├── output
│   ├── A1J_out.pdbqt
│   ├── ...
├── config
│   ├── A1J.conf
│   ├── ...
├── log
│   ├── A1J_log.txt
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

```
>> adock('6rqu','A1J')
>> adock('6rqu','M5C',0.0,0.0,0.0,25,25,25)
>> adock('6rqu','CZ0',vina='qvina2.1')
```

-receptor defines the receptor filename
-ligand defines the ligand filename
-center_x/y/z define the starting coordinates to perform docking, place within protein pocket, default parameters of 9.879/-13.774/7.012 were assigned
-size_x/y/z define the size of the box to dock, default parameters of 60/60/60 were assigned
-vina defines the subprocess which will be run, default parameter of 'vina' was assigned
-seed defines the seed to use for random number generation, default of None
-cpu defines the number of cpu cores, default of 1
