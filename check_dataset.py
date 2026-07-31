import pandas as pd

train = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", nrows=1)
test = pd.read_csv("data/Friday-WorkingHours-Morning.pcap_ISCX.csv", nrows=1)

print("Missing in test:")
print(set(train.columns) - set(test.columns))

print("\nExtra in test:")
print(set(test.columns) - set(train.columns))