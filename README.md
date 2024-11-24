# GalaxyDock-DL (linux only)
GalaxyDock-DL is a protein-ligand docking method which utilizes Conformational Space Annealing(CSA) as a sampling algorithm and deep learning-based scoring functions.

## Installation Guide (linux only)
1. Install [Anaconda](https://www.anaconda.com/products/individual) if you have not installed it yet.<br/>
2. Install [UCSF Chimera](https://www.cgl.ucsf.edu/chimera/download.html) if you have not installed it yet.<br/>
3. Intallation can be done by running below commands in terminal from main directory location. After git clone, below commands should be run in terminal from main directory location.<br/>
4. Clone this Git repository<br/>

```bash
$ git clone git@github.com:seoklab/colab_gd_dl.git
```

Below commands should be run in terminal from main directory location.<br/>

5. Install torch geometric files. (you can ignore errors) <br/>
```bash
$ pip install torch_geometric
$ pip install torch_scatter
```

6. Install source files (gd_dl)<br/>

```bash
$ pip install -e .
```

When you use GalaxyDock-DL, please make sure you activate the enviroment in terminal first ("conda activate gd_dl").<br/>

## Usage (linux only)
Below commands should be run in terminal from main directory location.<br/>
We recommend checking src/gd_dl/path_setting.py if you want to change path settings.<br/>

### Running docking
Run docking for a single ligand mol2 file and a protein receptor file without the ligand. (A center coordinate of a docking box (22.5 angstrom^3) is usually set to a coordinate of cognate ligand's geometric center for docking box to include a binding site.)<br/>

Random seeds were set to zero, but you can modify random seeds by adding argument
```bash
--random_seed <random_seed value>
```

Default output directory is set to current working directory, but you can modify random seeds by adding argument
```bash
--out_dir <location of output directory>
```

You can change length of docking box by adding argument
```bash
--box_size <box size value in angstrom>
```

```bash
$ python scripts/run_gd_dl.py -p <path to protein receptor file(.pdb)> -l <path to ligand file(.mol2)> -x <center x coordinate of a docking box> -y <center y coordinate of a docking box> -z <center z coordinate of a docking box>
```

Example for 3rsx

```bash
$ python scripts/run_gd_dl.py -p ./example/3rsx/3rsx_protein.pdb -l example/output_dir/charged_ligand.mol2 -x 69.637 -y 49.989 -z 10.160 --out_dir example/output_dir/
```

If you want to run docking in terminal from a different directory, you can use bash command with '-d <location of main directory>' below<br/>
```bash
$ python scripts/run_gd_dl_from_other_directory -d <Path to main directory> -p <path to protein receptor file(.pdb)> -l <path to ligand file(.mol2)> -x <center x coordinate of a docking box> -y <center y coordinate of a docking box> -z <center z coordinate of a docking box>
```

### Output files
- `GalaxyDock_fb.mol2`: Contains the final output ligand poses, sorted by total score.
- `GalaxyDock_fb.E.info`: Provides the scores of the final output ligand poses in the final bank, sorted by total score.

For `GalaxyDock_fb.E.info`:
- The second column (Energy) shows the ranking scores of output poses inferred by neural network scoring functions.
- You can ignore the values in the l_RMSD column, as they only represent RMSD calculated by the Hungarian algorithm between processed input ligand poses and output ligand poses.
- You can also ignore the other columns, which correspond to the values of GalaxyDock BP2 Score energy components multiplied by their weights (ATDK_E: AutoDock Energy, INT_E: AutoDock intra-ligand energy, DS_E: Drug Score, HM_E: Hydrophobic interaction, PLP: PLP score).

GalaxyDock_ib.mol2: Initial ligand conformations in the first bank<br/>
box.pdb: Representation of docking box<br/>
GalaxyDock_cl.mol2: clustered final output ligand poses sorted by total score<br/>

Other output files are used during initialization or sampling and not important after docking is finished.<br/>

You can view ligand conformations directly using UCSF chimera<br/>
For example,
```bash
$ chimera GalaxyDock_fb.mol2
```

or you can view ligand conformations and protein receptor
```bash
$ chimera GalaxyDock_fb.mol2 <path to protein receptor file(.pdb)>
```

# Citation

If you utilize this code or the models in your research, please cite the following paper:
```
@article{lee2024galaxydock,
  title={GalaxyDock-DL: Protein--Ligand Docking by Global Optimization and Neural Network Energy},
  author={Lee, Changsoo and Won, Jonghun and Ryu, Seongok and Yang, Jinsol and Jung, Nuri and Park, Hahnbeom and Seok, Chaok},
  journal={Journal of Chemical Theory and Computation},
  year={2024},
  publisher={ACS Publications}
}
```

# License

All code is licensed under the MIT license. The weights of the neural networks are licensed under the CC BY-NC 4.0 license.
