import os
import csv
import glob
import json

for fp in glob.iglob(os.path.join('**', 'meta.json'), recursive=True):
    with open(fp) as f:
        data = json.load(f)
    
    if 'centroid' in data and len(data['centroid']):
        centroid = np.array(data['centroid'], dtype=object)
        if centroid.shape[1] == 3:
            continue
        data['centroid'] = []

    with open(fp, 'w') as f:
        json.dump(data, f)
