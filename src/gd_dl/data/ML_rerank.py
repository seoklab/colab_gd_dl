import os
import time

import argparse
import torch

from gd_dl.rerank_model import Rerank_model
from gd_dl.data.ML_inference import load_files, calculate_energy

READOUT = 'mean'

device = torch.device('cpu')

torch.set_num_threads(1)
#torch.set_num_interop_threads(1)

REP_DIST = 1.5
N_NODE = 29

model_1_feature_dict = {'dist_cutoff' : 5.0,
 'bucket' : torch.tensor([1.5,1.9,2.3,2.7,3.1,3.5,4.0,4.5,5.0]),
  'n_edge': 17,'zip':1}
model_2_feature_dict = {'dist_cutoff' : 6.0,
 'bucket' : torch.tensor([1.5,1.9,2.3,2.7,3.1,3.5,4.0,4.5,5.0,5.5,6.0]),
  'n_edge': 19,'zip':2}

def calc_e(args):
    pre_ML_fn = args.infile_pre_ML
    mol_fn = os.path.join(args.mol2_prefix+'.mol2')
    rerank_model = args.load_model

    fn_sampling_model = rerank_model.replace('rerank_model.pt','sampling_model.pt')
    fn_rerank_model = rerank_model

    fn_sampling_model_list = [fn_sampling_model, fn_sampling_model[:-3] + '_0.pt', fn_sampling_model[:-3] + '_1.pt']
    
    sampling_model_list = []
    
    for fn_model_i in fn_sampling_model_list:      
        tmp_model = Rerank_model(node_dim_hidden=64,
                                 edge_dim_hidden=32,
                                 readout=READOUT,
                                 ligand_only=True).to(device)
        checkpoint = torch.load(fn_model_i, map_location=device, weights_only=True)
        tmp_model.load_state_dict(checkpoint['model_state_dict'])
        tmp_model.eval()
        
        sampling_model_list.append(tmp_model)
    
    rerank_model = Rerank_model(node_dim_hidden=64,
                                edge_dim_hidden=32,
                                edge_dim_in=model_2_feature_dict['n_edge'],
                                readout=READOUT,ligand_only=True).to(device)

    checkpoint = torch.load(fn_rerank_model, map_location=device, weights_only=True)
    rerank_model.load_state_dict(checkpoint['model_state_dict'])
    rerank_model.eval()

    all_zip, coord_l = load_files(pre_ML_fn, mol_fn)

    with torch.no_grad():
        energy = 0.0
        for model_i in sampling_model_list:
            energy += calculate_energy(all_zip, coord_l, model_i, model_1_feature_dict)
        
        energy += calculate_energy(all_zip, coord_l, rerank_model, model_2_feature_dict)

        energy /= len(fn_sampling_model_list) + 1

    out_fn = os.path.join(args.mol2_prefix+'.mol2.th1')
    with open(out_fn, 'w') as f:
        for energy_ in energy:
            f.write('%10.3f\n'%(energy_))

    print('%s is working!'%mol_fn)

    return

def main(args):
    st = time.time()
    calc_e(args)
    et = time.time()
    print ("Time for inference:", round(et-st, 2), " (s)")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile_pre_ML', type=str, required=True,
                                            help='torch_file_for_ML')
    parser.add_argument('--mol2_prefix', type=str, required=True,
                                            help='Prefix of a mol2 file')
    parser.add_argument('--load_model', type=str, required=True,
                                            help='saved_model')
    args = parser.parse_args()

    main(args)
