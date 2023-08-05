import os
import re
import json
import numpy as np
import pandas as pd
import glob
import argparse

def run(path, prob):
    mask_csv = 'mask.csv'
    pred_path = os.path.join(path, '..', 'predict')
    if not os.path.exists(pred_path):
        print("Predict directory not found. ", pred_path)
        return
    print('Probability threshold: {:.0%}'.format(prob))
    print('Sample \t\t\t GT - Labeled, GT - CTC, \t Predicted, Matched')
    for f in os.scandir(path):
        if not f.is_dir():
             continue
        sum = np.array([0, 0])
        # measure ground truth
        for f_csv in glob.iglob(os.path.join(path, f.name, '**', mask_csv), recursive=True):
            df = pd.read_csv(f_csv, index_col='ImageId', dtype={'Label': str})
            if 'Label' not in df.columns:
                df['Label'] = ''
            df = df[['EncodedPixels', 'Label']]
            sum += df[ df['Label'] == 'ctc' ].count().tolist()
        # measure prediction result
        pred = np.array([0, 0])
        for f_csv in glob.iglob(os.path.join(pred_path, f.name, '**', mask_csv), recursive=True):
            df = pd.read_csv(f_csv, index_col='ImageId', dtype={'Label': str})
            if 'Label' not in df.columns:
                df['Label'] = np.NaN
            if 'TumorProb' not in df.columns:
                df['TumorProb'] = 0.
            df.TumorProb.fillna(0, inplace=True)
            df = df[['TumorProb', 'Label']]
            #print(f_csv, df[ df['TumorProb'] >= prob ].count())
            pred += df[ df['TumorProb'] >= prob ].count().tolist()
        # result output
        print('{: <30} \t {} \t {} \t\t\t {} \t {}'.format(f.name, sum[1], sum[0], pred[0], pred[1]))

def main(args=None):
    parser = argparse.ArgumentParser(
        prog='statistics'
    )
    parser.add_argument('path', action='store', help='dataset folder')
    parser.add_argument('-p','--prob', type=float, help='probability threshold')
    args = parser.parse_args(args)

    run(args.path, args.prob)