import pandas as pd
from tools.app import current_dir, output_dir


def call():

    curated = pd.read_csv('{}/data/interaction_curated.csv'.format(current_dir))
    protein = pd.read_csv('{}/data/protein.csv'.format(current_dir))

    curated_proteins = list(set(curated['multidata_name_1'].tolist() + curated['multidata_name_2'].tolist()))

    def filter_curated(protein):
        if protein in curated_proteins:
            return True
        return False


    proteins_in_curated = protein[protein['uniprot'].apply(filter_curated)]


    proteins_in_curated.to_csv('{}/AUX_proteins_in_curated.csv'.format(output_dir), index=False)




