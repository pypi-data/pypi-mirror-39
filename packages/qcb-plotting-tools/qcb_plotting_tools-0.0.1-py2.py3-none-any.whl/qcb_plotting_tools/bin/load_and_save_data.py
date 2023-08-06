#!/usr/bin/env python

from pathlib import Path

import pandas as pd
try:
    import datasetdatabase as dsdb
except ModuleNotFoundError:
    raise ImportError("DSDB must be installed in this environment first! "
                      "For further information see https://github.com/AllenCellModeling/datasetdatabase")


# %% LOAD DATASET from Network
# connect to database(prod)
prod = dsdb.DatasetDatabase(config="//allen/aics/assay-dev/Analysis/QCB_database/prod_config.json")

# load features from golgi
ds_meta = prod.get_dataset(name='QCB_drug_cell_meta')
ds_dna_fea = prod.get_dataset(name='QCB_DRUG_DNA_feature')
ds_cell_fea = prod.get_dataset(name='QCB_DRUG_CELL_feature')
ds_gol_fea = prod.get_dataset(name='QCB_DRUG_ST6GAL_feature')
ds_tub_fea = prod.get_dataset(name='QCB_DRUG_TUBA1B_feature')
ds_sec_fea = prod.get_dataset(name='QCB_DRUG_SEC61B_feature')
ds_actb_fea = prod.get_dataset(name='QCB_DRUG_ACTB_feature')
ds_tjp1_fea = prod.get_dataset(name='QCB_DRUG_TJP1_feature')
ds_myo_fea = prod.get_dataset(name='QCB_DRUG_MYH10_feature')
ds_lamp1_fea = prod.get_dataset(name='QCB_DRUG_LAMP1_feature')

# %% Making dataframe with all features and meta data and save to csv

# Concatenate structure features table
# struc_fea = pd.concat(struc_dfs.values(), axis = 0)

struc_fea = pd.concat([ds_gol_fea.ds,
                       ds_tub_fea.ds,
                       ds_sec_fea.ds,
                       ds_actb_fea.ds,
                       ds_tjp1_fea.ds,
                       ds_myo_fea.ds,
                       ds_lamp1_fea.ds], axis=0)

# Inner join between dna and cell features
df_dna_cell_merge = pd.merge(ds_dna_fea.ds,
                             ds_cell_fea.ds,
                             on='cell_id', how='inner')

# Merge with dna/cell/struc_fea
df_allfea_merge = pd.merge(df_dna_cell_merge,
                           struc_fea,
                           on='cell_id', how='inner')

# Merge meta with all features
df_merge = pd.merge(df_allfea_merge,
                    ds_meta.ds,
                    on='cell_id', how='inner')

# Coerce it to dataframe
df = pd.DataFrame(df_merge)

# Save to network
export_dir = Path(r'\\allen\aics\microscopy\Winnie\QCB\Python Scripts\Drug datasets export')

df.to_csv(export_dir / 'df.csv', index=False)
ds_dna_fea.ds.to_csv(export_dir / 'ds_dna_fea.csv', index=False)
ds_cell_fea.ds.to_csv(export_dir / 'ds_cell_fea.csv', index=False)

ds_gol_fea.ds.to_csv(export_dir / 'ds_gol_fea.csv', index=False)
ds_tub_fea.ds.to_csv(export_dir / 'ds_tub_fea.csv', index=False)
ds_sec_fea.ds.to_csv(export_dir / 'ds_sec_fea.csv', index=False)
ds_actb_fea.ds.to_csv(export_dir / 'ds_actb_fea.csv', index=False)
ds_tjp1_fea.ds.to_csv(export_dir / 'ds_tjp1_fea.csv', index=False)
ds_myo_fea.ds.to_csv(export_dir / 'ds_myo_fea.csv', index=False)
ds_lamp1_fea.ds.to_csv(export_dir / 'ds_lamp1_fea.csv', index=False)
