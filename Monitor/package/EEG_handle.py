import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class State:
   falpha      : np.array
   fbeta       : np.array
   ftheta      : np.array
   fsum        : np.array
   drownsiness : float
   relaxation  : float
   alertness   : float
   status_dict = {0:"freeze", 1:"alert", 2:"relax", 3:"aware", 4:"drowsy", 5:"nervous", 6:"sleepy", 7:"full"}
   # (drowiness, relaxation, alertness)
   # +++ full
   # -++ aware
   # +-+ nervous
   # --+ alert
   # ++- sleepy
   # -+- relax
   # +-- drowsy
   # --- freeze

   def __init__(self, sig:np.array, fs:int(300)):
      self.sig = sig
      self.N = 5
      self.fs = fs
      self.BF(N=self.N, fs=self.fs)
      self.RI()
   
   def BF(self, N=int(5), fs=int(350)):
      """
      Butterwirth Filter
      """
      sos = signal.butter(N=N, Wn=[8, 12], btype="bp", fs=fs, output="sos")
      self.falpha = signal.sosfilt(sos, self.sig)

      sos = signal.butter(N=N, Wn=[13, 30], btype="bp", fs=fs, output="sos")
      self.fbeta = signal.sosfilt(sos, self.sig)
            
      sos = signal.butter(N=N, Wn=[4, 7], btype="bp", fs=fs, output="sos")
      self.ftheta = signal.sosfilt(sos, self.sig)

      self.fsum = np.abs(self.falpha) + np.abs(self.fbeta) + np.abs(self.ftheta)
      
   def reject_outliers(self, data, m=2):
      return data[abs(data - np.mean(data)) < m * np.std(data)]

   def RI(self) -> tuple([float, float, float]):
      try:
         a, b, t = np.mean(self.reject_outliers(np.abs(self.falpha/self.fsum))), \
                   np.mean(self.reject_outliers(np.abs(self.fbeta /self.fsum))), \
                   np.mean(self.reject_outliers(np.abs(self.ftheta/self.fsum)))
      except ZeroDivisionError as ze:
         print(self.falpha, self.fsum)
         a, b, t = 0, 0, 0
      except Exception as e:
         a, b, t = 0, 0, 0
      self.drownsiness, self.relaxation, self.alertness = (a + b)/t, t/a, b/a

   def mental_status(self, drownsiness, relaxation, alertness, base_dr=float(0), base_re=float(0), base_aw=float(0)):
      status = list()
      if drownsiness > base_dr : status.append("1")  # drownsiness
      else                     : status.append("0")
      if relaxation > base_re  : status.append("1")  # relaxation
      else                     : status.append("0")
      if alertness > base_aw   : status.append("1")  # alertness
      else                     : status.append("0")
      return self.status_dict[int(''.join(status), 2)]
   
   def Get_RI(self) -> np.array([float, float, float]):
      return np.array([self.drownsiness, self.relaxation, self.alertness])
   
   def PlotRI(self, ratio:np.array):
       plt.figure()
       plt.plot(np.arange(len(ratio))*4, ratio[:, 0], label='Drownsiness')
       plt.plot(np.arange(len(ratio))*4, ratio[:, 1], label='Relaxation')
       plt.plot(np.arange(len(ratio))*4, ratio[:, 2], label='Alertness')
       plt.xlabel("Time(s)")
       plt.ylabel("Ratio")
       plt.legend()
       plt.savefig("./graph.png")