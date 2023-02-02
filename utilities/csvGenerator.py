import csv
from datetime import datetime

import utilities.watcher as watcher

def similarityResult(botnetUniqueSelection, normalUniqueSelection, botnetRecord, normalRecord, samplingRule, decompositor, similarityResult):
  ctx= 'Export Similarity Result'
  start=watcher.watcherStart(ctx)
  # list of column names 
  field_names = ['CreatedAt', 'botnetUniqueSelection','normalUniqueSelection','botnetRecord','normalRecord','samplingRule', 'decompositor', 'similarityResult']
  # Dictionary
  dict = {
    "CreatedAt": datetime.now(),
    "botnetUniqueSelection": botnetUniqueSelection,
    "normalUniqueSelection": normalUniqueSelection,
    "botnetRecord": botnetRecord,
    "normalRecord": normalRecord,
    "samplingRule": samplingRule,
    "decompositor": decompositor,
    "similarityResult": similarityResult
  }

  with open('data/similarity_results.csv', 'a', newline='') as csv_file:
    dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
    dict_object.writerow(dict)

  watcher.watcherEnd(ctx, start)

def classificationResult(algorithm, decompositor, tn, fp, fn, tp):
  ctx= 'Export Classification Result'
  start=watcher.watcherStart(ctx)
  # list of column names 
  field_names = ['CreatedAt','Algorithm','Decompositor','TN','FP','FN', 'TP']
  # Dictionary
  dict = {
    "CreatedAt": datetime.now(),
    "Algorithm":algorithm,
    "Decompositor":decompositor,
    "TN": tn,
    "FP": fp,
    "FN": fn,
    "TP": tp
  }

  with open('data/classification_results.csv', 'a', newline='') as csv_file:
    dict_object = csv.DictWriter(csv_file, fieldnames=field_names) 
    dict_object.writerow(dict)

  watcher.watcherEnd(ctx, start)