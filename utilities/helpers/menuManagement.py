import time
import os
import glob

# import utilities.mongoDb as mongo
import utilities.data as dl
import src.similarityMeasurement as sim

def dumpFunct():
  print('success')

listMenu =[
  {
    'title': 'SimilarityMeasurement',
    'functionName': sim.similarityMeasurement
  }
]

def validateInput(input):
  try:
    input = int(input)-1
    isValid = True
  except ValueError:
    isValid = False
  return isValid, input

def getListDatasetMenu():
  os.system("clear")
  x=1
  print("\n\n------------------------------------------")
  print("\t| List Available Datasets |")
  print("------------------------------------------\n")
  for dataset in dl.listAvailableDatasets:
    print(str(x)+". "+dataset['name'])
    x += 1
  print("\n------------------------------------------")
  choose = input("Choose one dataset: ")
  isValid, choose = validateInput(choose)
  if(isValid == False or choose >= len(dl.listAvailableDatasets)):
    print("This Option Does Not Exist, Bring You Back to Main Menu!")
    time.sleep(3) # adding 3 seconds time delay
    os.system("clear")
    mainMenu() #call menu again
  return choose

def getListDatasetDetailMenu(datasetIndex):
  os.system("clear")
  chooseDataset = dl.listAvailableDatasets[datasetIndex]
  listSubDataset = list(chooseDataset['list'].keys())
  x=1
  print("\n\n------------------------------------------")
  print("\t| List Sub Dataset on "+chooseDataset['name']+" |")
  print("------------------------------------------\n")
  for subDataset in listSubDataset:
    print(str(x)+". "+subDataset)
    x += 1
  print("\n------------------------------------------")
  choose = input("Choose one subDataset: ")
  isValid, choose = validateInput(choose)
  if(isValid == False or choose >= len(listSubDataset)):
    print("This Option Does Not Exist, Bring You Back to Main Menu!")
    time.sleep(3) # adding 3 seconds time delay
    os.system("clear")
    mainMenu() #call menu again
  return choose+1

def banner():
  x=1
  print("\n\n================================================================")
  print("======| Dimentional Reduction on Botnet Data |=============")
  print("================================================================\n")
  print("Main Menu: ")
  for menu in listMenu:
    print(str(x)+". "+menu['title'])
    x += 1
  print("\n================================================================")

def execute(menuIndex):
  isValid, menuIndex = validateInput(menuIndex)
  if(isValid and menuIndex < len(listMenu)):
    print("============| Processing Menu: "+str(menuIndex+1)+". "+listMenu[menuIndex]['title']+" |========================\n")
    listMenu[menuIndex]['functionName']()

    print("\n\t\t"+listMenu[menuIndex]['title']+" Process Success...")
    print("\tback to menu...")
  else:
    print("This Menu Does Not Exist, Please Try Another Input!")
    time.sleep(3) # adding 3 seconds time delay
    os.system("clear")
    mainMenu() #call menu again

def mainMenu():
  banner()
  # choose = input("Enter Menu: ")
  choose = 1
  execute(choose)