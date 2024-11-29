import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
from pathlib import Path

def main():
    output_energy_file = Path(sys.argv[1])
    output_rmsd_file = Path(sys.argv[2])
    
    energy_array = np.array([float(line.split()[1]) for line in output_energy_file.read_text().splitlines()
                             if not line.startswith('!') and not line.startswith('Bank')],
                          dtype=np.float64)
    rmsd_array = np.array([float(line.split()[-1]) for line in output_rmsd_file.read_text().splitlines()],
                          dtype=np.float64)
    
    
    font_size = 10
    
    sns.set_style("whitegrid")
    sns.set_theme(rc={'figure.figsize':(16,16)})
    sns.set_theme(font_scale = 3.0)
    
    rmsd_range = list(range(round(rmsd_array.max())+1))
    
    ax = sns.scatterplot(x=rmsd_array, y=energy_array, s=1000)
    plt.xticks(fontsize=font_size*2.5, fontweight='bold')
    plt.yticks(fontsize=font_size*2.5, fontweight='bold')
    plt.xlabel('RMSD', fontsize=font_size*4.0, labelpad=font_size*2, fontweight='bold')
    plt.ylabel('Score', fontsize=font_size*4.0, labelpad=font_size*2, fontweight='bold')
    
    ax.axvline(2.0, linestyle='--', color='k')
    ax.spines['bottom'].set_color('k')
    ax.spines['top'].set_color('k') 
    ax.spines['right'].set_color('k')
    ax.spines['left'].set_color('k')
    ax.set_xticks(np.array(rmsd_range))
        
    plt.show()
    
if __name__ == '__main__':
    main()