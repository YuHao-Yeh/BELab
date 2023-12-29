##############################################################################################
#     File Name   :  EEG2.py
#       Version   :
#       Arthors   :  Yeh Yu-Hao
#
#  Dependencies   :
#
#  Description    :  
#
#      Details    :  
#
# Rev     Arthor   Date          Changes
#--------------------------------------------------------------------------------------------#
# 1.0.0   Yeh      ----/--/--    ---
##############################################################################################
#%%
import csv
import scipy.io
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from IPython.display import display
import numpy as np
import pandas as pd
from dataclasses import dataclass, field

@dataclass
class EEG_Signal:
   name : str      = field(default=str())
   data : np.array = field(default_factory=np.array)

@dataclass
class State:
   sig   : EEG_Signal = field(default_factory=EEG_Signal(name="EEG",   data=np.array))
   alpha : EEG_Signal = field(default_factory=EEG_Signal(name="Alpha", data=np.array))
   beta  : EEG_Signal = field(default_factory=EEG_Signal(name="Beta",  data=np.array))
   delta : EEG_Signal = field(default_factory=EEG_Signal(name="Delta", data=np.array))
   theta : EEG_Signal = field(default_factory=EEG_Signal(name="Theta", data=np.array))

   falpha : EEG_Signal = field(init=False)
   fbeta  : EEG_Signal = field(init=False)
   fdelta : EEG_Signal = field(init=False)
   ftheta : EEG_Signal = field(init=False)

   N  : int = field(init=False)
   fs : int = field(init=False)

   def __post_init__(self):
      self.N = 5
      self.fs = 200
      self.BF(N=self.N, fs=self.fs)

   
   def BF(self, N=int(5), fs=int(200)):
      """
      Butterwirth Filter
      """
      sos = signal.butter(N=N, Wn=[8, 12], btype="bp", fs=fs, output="sos")
      # self.falpha = EEG_Signal(name="Alpha", data=signal.sosfilt(sos, self.sig.data))
      self.falpha = EEG_Signal(name=self.alpha.name, data=signal.sosfilt(sos, self.sig.data))

      sos = signal.butter(N=N, Wn=[13], btype="hp", fs=fs, output="sos")
      # self.fbeta = EEG_Signal(name="Beta", data=signal.sosfilt(sos, self.sig.data))
      self.fbeta = EEG_Signal(name=self.beta.name, data=signal.sosfilt(sos, self.sig.data))
      
      sos = signal.butter(N=N, Wn=[4], btype="lp", fs=fs, output="sos")
      # self.fdelta = EEG_Signal(name="Delta", data=signal.sosfilt(sos, self.sig.data))
      self.fdelta = EEG_Signal(name=self.delta.name, data=signal.sosfilt(sos, self.sig.data))
      
      sos = signal.butter(N=N, Wn=[4, 7], btype="bp", fs=fs, output="sos")
      # self.ftheta = EEG_Signal(name="Theta", data=signal.sosfilt(sos, self.sig.data))
      self.ftheta = EEG_Signal(name=self.theta.name, data=signal.sosfilt(sos, self.sig.data))

def reject_outliers(data, m=2):
   return data[abs(data - np.mean(data)) < m * np.std(data)]

subject_num = 4
num_level = 3
num_problem = 20
interval = [0, 3, 5, 9]
# interval = [0, 3]
Ratio_Index = ['Drownsiness', 'Relaxation', 'Alertness']

dataset = ["".join(["l", str(l), "_", str(t), "s_", str(num_problem)]) for l in range(1, num_level+1) for t in interval]
csvname = ["".join(["../data/subject4/", x, ".csv"]) for x in dataset]
matname = ["".join(["../data/subject4/eeg_", x,".mat"]) for x in dataset]
# matname = ["".join(["./data/test3/data_", x.replace("20", "L03"),".mat"]) for x in dataset]

test = pd.DataFrame(data=None, columns=pd.MultiIndex.from_product([dataset, Ratio_Index], names=['test number', 'Ratio Index']))
test.index.name = 'Problem id'
fs, fo = 200, 5
# fs, fo = 11, 5

#----------------------------------------------------------------------#
# Baseline - mat
#----------------------------------------------------------------------#
matf = scipy.io.loadmat("../data/subject4/eeg_baseline.mat")
sig   = EEG_Signal(name=str(matf["labels"][0]).capitalize(), data=matf["data"][:, 0])
# alpha = EEG_Signal(name=str(matf["labels"][1]).capitalize(), data=matf["data"][:, 1])
# beta  = EEG_Signal(name=str(matf["labels"][2]).capitalize(), data=matf["data"][:, 2])
# delta = EEG_Signal(name=str(matf["labels"][3]).capitalize(), data=matf["data"][:, 3])
# theta = EEG_Signal(name=str(matf["labels"][4]).capitalize(), data=matf["data"][:, 4])
alpha = EEG_Signal(name=str("Alpha").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
beta  = EEG_Signal(name=str("Beta").capitalize(),  data=np.zeros((len(matf["data"][:, 0]), 1)))
delta = EEG_Signal(name=str("Delta").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
theta = EEG_Signal(name=str("Theta").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
source = State(sig=sig, alpha=alpha, beta=beta, delta=delta, theta=theta)
sum = source.falpha.data[0:3*60*fs] + source.fbeta.data[0:3*60*fs] + source.ftheta.data[0:3*60*fs]
#----------------------------------------------------------------------#
# Baseline - csv
#----------------------------------------------------------------------#
# csvf = pd.read_csv("./data/test3/data_baseline.csv")
# csvf.columns = [x.replace(" ", "") for x in csvf.columns]
# source = State(sig=EEG_Signal(name="Signal", data=csvf["Voltage"]))
# sum = source.falpha.data + source.fbeta.data + source.ftheta.data

a, b, t = np.mean(reject_outliers(np.abs(source.falpha.data[0:3*60*fs]/sum))), np.mean(reject_outliers(np.abs(source.fbeta.data[0:3*60*fs]/sum))), np.mean(reject_outliers(np.abs(source.ftheta.data[0:3*60*fs]/sum)))
drownsiness, relaxation, alertness = (a + b)/t, t/a, b/a
baseline = (drownsiness, relaxation, alertness)
print(baseline)
# plt.plot(sum)

#----------------------------------------------------------------------#
# Test
#----------------------------------------------------------------------#
for i in range(num_level*len(interval)):
   # Record
   csvf = pd.read_csv(csvname[i], sep=",", header=2, nrows=num_problem+1)
   csvf.columns = [x.replace(" ", "") for x in csvf.columns]
   #----------------------------------------------------------------------#
   # Signal - mat
   #----------------------------------------------------------------------#
   matf = scipy.io.loadmat(matname[i])
   sig   = EEG_Signal(name=str(matf["labels"][0]).capitalize(), data=matf["data"][:, 0])
   # alpha = EEG_Signal(name=str(matf["labels"][1]).capitalize(), data=matf["data"][:, 1])
   # beta  = EEG_Signal(name=str(matf["labels"][2]).capitalize(), data=matf["data"][:, 2])
   # delta = EEG_Signal(name=str(matf["labels"][3]).capitalize(), data=matf["data"][:, 3])
   # theta = EEG_Signal(name=str(matf["labels"][4]).capitalize(), data=matf["data"][:, 4])
   alpha = EEG_Signal(name=str("Alpha").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
   beta  = EEG_Signal(name=str("Beta").capitalize(),  data=np.zeros((len(matf["data"][:, 0]), 1)))
   delta = EEG_Signal(name=str("Delta").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
   theta = EEG_Signal(name=str("Theta").capitalize(), data=np.zeros((len(matf["data"][:, 0]), 1)))
   source = State(sig=sig, alpha=alpha, beta=beta, delta=delta, theta=theta)
   
   #----------------------------------------------------------------------#
   # Signal - csv
   #----------------------------------------------------------------------#
   # csvf2 = pd.read_csv(matname[i], sep=",")
   # csvf2.columns = [x.replace(" ", "") for x in csvf.columns]

   for n in range(num_problem+1):
      if n == num_problem : start, end = int(csvf['timeEndAt'].iloc[0]*fs), int(csvf['timeEndAt'][n]*fs)
      else                : start, end = int(csvf['timeEndAt'].iloc[n]*fs), int(csvf['timeEndAt'][n+1]*fs)
      sum = source.falpha.data[start:end] + source.fbeta.data[start:end] + source.ftheta.data[start:end]
      a = np.mean(reject_outliers(np.abs(source.falpha.data[start:end]/sum)))
      b = np.mean(reject_outliers(np.abs(source.fbeta.data[start:end]/sum)))
      t = np.mean(reject_outliers(np.abs(source.ftheta.data[start:end]/sum)))
      drownsiness, relaxation, alertness = (a + b)/t, t/a, b/a
      if n == num_problem : test.loc['avg', (dataset[i], Ratio_Index)] = drownsiness, relaxation, alertness
      else                : test.loc[n+1, (dataset[i], Ratio_Index)] = drownsiness, relaxation, alertness
   
# Figure 1: ratio index on different time limit and test level
fig, axs = plt.subplots(nrows=num_level*len(interval), ncols=1, sharex=True, sharey=True, figsize=(10, 20))
for i in range(num_level*len(interval)):
   axs[i].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Drownsiness')], label="Drownsiness")
   axs[i].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Relaxation')], label="Relaxation")
   axs[i].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Alertness')], label="Alertness")
   axs[i].set_title(dataset[i])
fig.legend(labels=Ratio_Index)

# Figure 2: ratio index on different time limit and test level
fig2, axs2 = plt.subplots(nrows=num_level*len(interval), ncols=len(Ratio_Index), sharex=True, sharey=True, figsize=(10, 20))
for i in range(num_level*len(interval)):
   axs2[i, 0].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Drownsiness')], label="Drownsiness")
   axs2[i, 0].plot(range(num_problem), [baseline[0]]*num_problem, color='r')
   axs2[i, 0].set_title(dataset[i] + "Drownsiness")
   axs2[i, 1].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Relaxation')], label="Relaxation")
   axs2[i, 1].plot(range(num_problem), [baseline[1]]*num_problem, color='r')
   axs2[i, 1].set_title(dataset[i] + "Relaxation")
   axs2[i, 2].plot(range(num_problem), test.loc[:num_problem, (dataset[i], 'Alertness')], label="Alertness")
   axs2[i, 2].plot(range(num_problem), [baseline[2]]*num_problem, color='r')
   axs2[i, 2].set_title(dataset[i] + "Alertness")
fig2.legend(labels=Ratio_Index)

# Figure 3: ratio index based on different time limit
avg = np.zeros((len(Ratio_Index), num_level, len(interval)))
for i in range(num_level*len(interval)):
   avg[0, int(i%num_level), int(i%len(interval))] = test.loc["avg" ,(dataset[i], 'Drownsiness')]
   avg[1, int(i%num_level), int(i%len(interval))] = test.loc["avg" ,(dataset[i], 'Relaxation')]
   avg[2, int(i%num_level), int(i%len(interval))] = test.loc["avg" ,(dataset[i], 'Alertness')]

fig3, axs3 = plt.subplots(nrows=1, ncols=len(Ratio_Index), sharex=True, sharey=True, figsize=(10, 5))
for i in range(len(Ratio_Index)):
   for j in range(num_level):
      axs3[i].plot(interval, avg[i][j]/baseline[i], label=''.join(["Level ", str(j + 1)]))
   # axs3[i].plot(interval, [baseline[i]]*len(interval), label="baseline")
   axs3[i].set_title(Ratio_Index[i])
   axs3[i].xlabel = "Time(s)"
   axs3[i].ylabel = "Ratio"
fig3.legend(labels=[' '.join(["Level", str(x)]) for x in range(num_level)])

# Figure 4: ratio index based on different test level
fig4, axs4 = plt.subplots(nrows=1, ncols=len(Ratio_Index), sharex=True, sharey=True, figsize=(10, 5))
for i in range(len(Ratio_Index)):
   for j in range(len(interval)):
      # axs4[i].plot(np.linspace(1, num_level, num=num_level), avg[i].T[j], label=''.join([str(interval[j]),"s"]))
      axs4[i].plot(["1", "2", "3"], avg[i].T[j]/baseline[i], label=''.join([str(interval[j]),"s"]))
   # axs4[i].plot(np.linspace(1, num_level, num=num_level), [baseline[i]]*num_level, label="baseline")
   # axs4[i].plot(["1", "2", "3"], [baseline[i]]*num_level, label="baseline")
   axs4[i].set_title(Ratio_Index[i])
fig4.legend(labels=[''.join([str(x), "s"]) for x in interval])

# Figure 5: ratio index based on different time
fig5, axs5 = plt.subplots(nrows=num_level, ncols=len(Ratio_Index), sharex=True, sharey=False, figsize=(10, 5))
for i in range(len(Ratio_Index)):
   for j in range(num_level):
      for k in range(len(interval)):
         axs5[i, j].plot(range(num_problem), test.loc[:num_problem, (dataset[j*len(interval)+k], Ratio_Index[i])], label=interval[k])
      axs5[i, j].set_title(''.join(["L", str(j+1), " ", Ratio_Index[i]]))
      axs5[i, j].xlabel = "# of Problem"
      axs5[i, j].ylabel = "Ratio Index"
fig5.legend(labels=[''.join([str(x), "s"]) for x in interval])

