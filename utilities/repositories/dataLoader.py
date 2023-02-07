import csv
import pandas as pd
import numpy as np

from datetime import datetime
from scapy.all import rdpcap, PcapReader, IP

from utilities.helpers.watcher import *
from utilities.helpers.common import *

def pcap(pcapFile):
  ctx=pcapFile+' Dataset Loader'
  start = watcherStart(ctx)
  
  packets = PcapReader(pcapFile)
  # Create a list of dictionaries, where each dictionary represents a single packet

  with open("collections/example.binetflow", "w") as f:
    for packet in packets:
      ip_header = packet.getlayer(IP)
      if(ip_header):
        # Get the IP addresses and port numbers for the source and destination
        src_ip = getattr(ip_header, 'src', '')
        dst_ip = getattr(ip_header, 'dst', '')
        src_port = getattr(ip_header, 'sport', '')
        dst_port = getattr(ip_header, 'dport', '')
        proto = getattr(ip_header, 'proto', '')
        startTime = datetime.fromtimestamp(packet.time)

        # Write the Binetflow record to the file
        f.write("{},{},{},{},{},{}\n".format(startTime, src_ip, src_port, dst_ip, dst_port, proto))

  return 0
  packetList = []
  f = open('collections/pcap.csv', 'w')
  for packet in packets:
    # packetDict = {}
    # packetDict["source"] = packet[0].src
    # packetDict["destination"] = packet[0].dst
    # packetDict["protocol"] = packet[0].proto if packet.proto else ''
    # packetList.append(packetDict)
    packetList.append(packet)
    writer = csv.writer(f)
    writer.writerow(packet)
    if(len(packetList)==1000):
    #   # Convert the list of dictionaries into a pandas DataFrame
    #   raw_df = pd.DataFrame(packetList)
    #   with open('collections/pcap.csv', 'a', newline='') as csv_file:
    #     dict_object = csv.DictWriter(csv_file,fieldnames=[]) 
    #     dict_object.writerow(dict)
      break

  watcherEnd(ctx, start)
  # return raw_df

def binetflow(dataset, scenario, stringDataset=''):
  ctx=stringDataset.upper()+' '+scenario+' Dataset Loader'
  start = watcherStart(ctx)

  fileName = dataset[scenario] #load dataset
  raw_df=pd.read_csv(fileName)

  watcherEnd(ctx, start)
  return raw_df

def splitDataFrameWithProportion(dataFrame, trainProportion=defaultTrainProportion):
  ctx='Split Data Frame With Proportion'
  start= watcherStart(ctx)

  normal_df=dataFrame[dataFrame['ActivityLabel'].isin([0])] #create new normal custom dataframe
  bot_df=dataFrame[dataFrame['ActivityLabel'].isin([1])] #create a new data frame for bots

  msk_normal = np.random.rand(len(normal_df)) < trainProportion #get random 20% from normal
  msk_bot = np.random.rand(len(bot_df)) < trainProportion #get random 20% from bot

  #split normal dataset
  normal_dfTrain = normal_df[msk_normal]
  normal_dfTest = normal_df[~msk_normal]

  #split normal dataset
  bot_dfTrain = bot_df[msk_bot]
  bot_dfTest = bot_df[~msk_bot]
  
  #combine dataTest and dataTrain
  train = pd.concat([normal_dfTrain, bot_dfTrain])
  test = pd.concat([normal_dfTest, bot_dfTest])

  watcherEnd(ctx, start)
  return train, test

#only take samples for training, testing with all data
def splitTestAllDataframe(dataFrame, trainProportion=defaultTrainProportion):
  ctx='Split Test All Dataframe'
  start= watcherStart(ctx)

  normal_df=dataFrame[dataFrame['ActivityLabel'].isin([0])] #create new normal custom dataframe
  bot_df=dataFrame[dataFrame['ActivityLabel'].isin([1])] #create a new data frame for bots

  msk_normal = np.random.rand(len(normal_df)) < trainProportion #get random 20% from normal
  msk_bot = np.random.rand(len(bot_df)) < trainProportion #get random 20% from bot

  #split normal dataset
  normal_dfTrain = normal_df[msk_normal]

  #split normal dataset
  bot_dfTrain = bot_df[msk_bot]
  
  #combine dataTest and dataTrain
  train = pd.concat([normal_dfTrain, bot_dfTrain])
  test = dataFrame

  watcherEnd(ctx, start)
  return train, test
