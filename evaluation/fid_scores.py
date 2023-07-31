#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 12:30:52 2023

@author: tomas
"""

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from matplotlib import rcParams

# %% GANformer
fig, ax = plt.subplots(1, 1, figsize=(12, 7))

rcParams.update({'font.size': 20})

for fi in [f'ganformer_{i}_fid.jsonl' for i in ['cropped', 'padding']]:
    with open(fi) as f:
        raw = [json.loads(i.strip()) for i in f.readlines()]
    
    fid = [i["results"]['fid1k'] if 'fid1k' in i["results"] else i["results"]['fid50k'] for i in raw]
    snapshot = [int(i["snapshot_pkl"].strip('.pkl').split('-')[-1]) for i in raw]
    
    if 'padding' in fi:
        fid = fid[1:]
        snapshot = snapshot[1:]
        label = 'Front padded'
    else:
        label = 'Front cropped'
    
    print(fi)
    print('Min Fid: ', np.min(fid))
    print('Snapshot: ', snapshot[np.argmin(fid)])

    ax.plot(snapshot, fid, label=label)

ax.legend()

ax.grid(which = "major", linewidth=1)
ax.grid(which = "minor", linewidth=0.2)
ax.minorticks_on()

ax.set_xlabel('Step')
ax.set_ylabel('FID Score')

fig.tight_layout()
plt.savefig('images/ganformer_fid.png', dpi=200)

# %% StyleGAN
groups = [
    [[f'stylegan_front_{i}_fid.jsonl' for i in ['cropped', 'padded']], 'front'],
    [[f'stylegan_{i}_cropped_fid.jsonl' for i in ['front', 'mix', 'side', 'upper', 'lower']], 'mix']
]


for g in groups:
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    
    rcParams.update({'font.size': 20})
    
    for fi in g[0]:
        with open(fi) as f:
            raw = [json.loads(i.strip()) for i in f.readlines() if i != '\n']
        
        fid = [i["results"]['fid50k_full'] for i in raw]
        snapshot = [int(i["snapshot_pkl"].strip('.pkl').split('-')[-1]) for i in raw]
        
        label = ' '.join(fi.split('_')[1:3]).capitalize()
    
        ax.plot(snapshot, fid, label=label)
        
        print(f'{fi}\tMin FID: {np.round(np.min(fid), 2)}\tSnapshot: {snapshot[np.argmin(fid)]}')
    
    ax.legend()
    
    ax.grid(which = "major", linewidth=1)
    ax.grid(which = "minor", linewidth=0.2)
    ax.minorticks_on()
    
    ax.set_xlabel('Step')
    ax.set_ylabel('FID Score')
    
    fig.tight_layout()
    plt.savefig(f'images/stylegan_fid_{g[1]}.png', dpi=200)

# %% ProGAN
fig, main_ax = plt.subplots(1, 7, figsize=(16, 7))
rcParams.update({'font.size': 20})

for t in ['cropped', 'padded']:

    depths = []
    epochs = []
    fids = []

    with open(f'progan_{t}_fid') as f:    
        lines = f.readlines()
        
        for i in range(len(lines) // 7):
            meta_idx = 7 * i
            fid_idx = 7 * i + 6
            
            meta = lines[meta_idx]
            fid = lines[fid_idx]
            
            _, depth, _, epoch = meta.strip().strip('.bin').split('/')[-1].split('_')
            fid_score = fid.strip().split(':')[1].strip()
            
            depths.append(int(depth))
            epochs.append(int(epoch))
            fids.append(float(fid_score))
    
    df = pd.DataFrame({'depth': depths, 'epoch': epochs, 'fid': fids}).sort_values(by=['depth', 'epoch'])
    
    
    
    for i in range(2, 9):
        temp = df.query(f'depth == {i}')
        ax = main_ax[i - 2]
        ax.plot(temp.epoch, temp.fid, label=f'Front {t}')
        
        ax.set_ylim(0, np.max(df.fid) + 10)
        
        if i > 2:
            ax.set_yticks([])
            ax.set_yticklabels([])
            
        ax.set_xlabel(f'{2**i}x{2**i}')
        
        ax.set_xticks([10, 20, 30, 40])
    
    print(f'Type: {t}\tMin FID: {np.min(df.fid)}\tEpoch: {df.epoch[np.argmin(df.fid)]}\tDepth: {df.depth[np.argmin(df.fid)]}')

for i in range(7):
    main_ax[i].grid()

main_ax[0].grid(axis='y')

plt.legend(loc='lower right')
    
main_ax[0].set_ylabel('FID Score')

fig.text(0.5, 0, 'Epoch', ha='center')

plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig('images/progan_fid.png', dpi=200)