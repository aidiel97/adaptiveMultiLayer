import utilities.watcher as watcher
import utilities.menuManagement as menu
import utilities.data as data
import utilities.csvGenerator as generate
import src.preProcessing as pp
import src.classificator as cls

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from utilities.globalConfig import VALIDATION_ITERATION

def randomUnderSampling(decompositor, botnet_df, normal_df, normalUnique=False, botnetUnique=False):
  ctx= 'Random Under Sampling'
  start=watcher.watcherStart(ctx)
  allSimilarity = []
  botnet = botnet_df.DimRedFeature.unique() if botnetUnique==True else botnet_df["DimRedFeature"].to_numpy()
  normal = normal_df.DimRedFeature.unique() if normalUnique==True else normal_df["DimRedFeature"].to_numpy()

  for i in range(VALIDATION_ITERATION):
    normal = np.random.choice(normal, len(botnet)) #undersampling
    similarity = cosine_similarity([botnet], [normal])
    allSimilarity.append(similarity[0])

  generate.similarityResult(botnetUnique, normalUnique, len(botnet), len(normal), ctx, decompositor, round((sum(allSimilarity)/len(allSimilarity))[0], 6))
  watcher.watcherEnd(ctx, start)

def randomOverSampling(decompositor, botnet_df, normal_df, normalUnique=False, botnetUnique=False):
  ctx= 'Random Over Sampling'
  start=watcher.watcherStart(ctx)
  allSimilarity = []
  botnet = botnet_df.DimRedFeature.unique() if botnetUnique==True else botnet_df["DimRedFeature"].to_numpy()
  normal = normal_df.DimRedFeature.unique() if normalUnique==True else normal_df["DimRedFeature"].to_numpy()

  for i in range(VALIDATION_ITERATION):
    botnet = np.random.choice(botnet, len(normal)) #oversampling
    similarity = cosine_similarity([botnet], [normal])
    allSimilarity.append(similarity[0])
  
  generate.similarityResult(botnetUnique, normalUnique, len(botnet), len(normal), ctx, decompositor, round((sum(allSimilarity)/len(allSimilarity))[0], 6))
  watcher.watcherEnd(ctx, start)

def zeroOverSampling(decompositor, botnet_df, normal_df, normalUnique=False, botnetUnique=False):
  ctx= 'Zero Over Sampling'
  start=watcher.watcherStart(ctx)
  botnet = botnet_df.DimRedFeature.unique() if botnetUnique==True else botnet_df["DimRedFeature"].to_numpy()
  normal = normal_df.DimRedFeature.unique() if normalUnique==True else normal_df["DimRedFeature"].to_numpy()

  botnet = np.append(botnet,np.zeros(len(normal)-len(botnet)))
  similarity = cosine_similarity([botnet], [normal])
  
  generate.similarityResult(botnetUnique, normalUnique, len(botnet), len(normal), ctx, decompositor, round(similarity[0][0], 6))
  watcher.watcherEnd(ctx, start)

def runAllRule(decompositor, raw_df):
  raw_df = pp.dimentionalReduction(decompositor, 1, raw_df)
  botnet = raw_df['ActivityLabel'] == 1
  normal = raw_df['ActivityLabel'] == 0
  botnet_df = raw_df[botnet]
  normal_df = raw_df[normal]

  randomUnderSampling(decompositor,botnet_df,normal_df)
  randomUnderSampling(decompositor,botnet_df,normal_df, True)
  randomUnderSampling(decompositor,botnet_df,normal_df, True, True)

  randomOverSampling(decompositor,botnet_df,normal_df)
  randomOverSampling(decompositor,botnet_df,normal_df, True)
  randomOverSampling(decompositor,botnet_df,normal_df, True, True)

  zeroOverSampling(decompositor,botnet_df,normal_df)
  zeroOverSampling(decompositor,botnet_df,normal_df, True)
  zeroOverSampling(decompositor,botnet_df,normal_df, True, True)

def similarityMeasurement():
  # #input
  # datasetIndex = menu.getListDatasetMenu()
  # datasetName = data.listAvailableDatasets[int(datasetIndex)]['list']
  # datasetDetail = menu.getListDatasetDetailMenu(datasetIndex)
  # stringDatasetName = data.listAvailableDatasets[int(datasetIndex)]['shortName']
  # selected = 'scenario'+str(datasetDetail)
  # #input
  ctx= 'Similarity Measurement'
  start=watcher.watcherStart(ctx)

  datasetName = data.ncc2
  selected = 'scenario3'
  stringDatasetName = 'ncc2'

  raw_df = data.loadDataset(datasetName, selected, stringDatasetName)
  raw_df = pp.preProcessing(raw_df)

  # runAllRule('pca',raw_df)
  # runAllRule('svd',raw_df)
  # runAllRule('factorAnalysis',raw_df)
  # runAllRule('FastICA',raw_df)

  #classification
  # cls.executor(raw_df, 'decisionTree')
  # cls.executor(raw_df, 'randomForest')
  # cls.executor(raw_df, 'naiveBayes')
  # cls.executor(raw_df, 'knn')
  # cls.executor(raw_df, 'logisticRegression')

  cls.executor(raw_df, 'decisionTree', 'pca')
  # cls.executor(raw_df, 'randomForest', 'pca')
  # cls.executor(raw_df, 'naiveBayes', 'pca')
  # cls.executor(raw_df, 'knn', 'pca')
  # cls.executor(raw_df, 'logisticRegression', 'pca')

  # cls.executor(raw_df, 'decisionTree', 'svd')
  # cls.executor(raw_df, 'randomForest', 'svd')
  # cls.executor(raw_df, 'naiveBayes', 'svd')
  # cls.executor(raw_df, 'knn', 'svd')
  # cls.executor(raw_df, 'logisticRegression', 'svd')

  # cls.executor(raw_df, 'decisionTree', 'factorAnalysis')
  # cls.executor(raw_df, 'randomForest', 'factorAnalysis')
  # cls.executor(raw_df, 'naiveBayes', 'factorAnalysis')
  # cls.executor(raw_df, 'knn', 'factorAnalysis')
  # cls.executor(raw_df, 'logisticRegression', 'factorAnalysis')

  # cls.executor(raw_df, 'decisionTree', 'FastICA')
  # cls.executor(raw_df, 'randomForest', 'FastICA')
  # cls.executor(raw_df, 'naiveBayes', 'FastICA')
  # cls.executor(raw_df, 'knn', 'FastICA')
  # cls.executor(raw_df, 'logisticRegression', 'FastICA')

  # cls.executor(raw_df, 'svc')

  watcher.watcherEnd(ctx, start)