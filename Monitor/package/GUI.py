##############################################################################################
#     File Name   :  GUI.py
#       Version   :  1.0.0
#       Arthors   :  Yeh Yu-Hao
#
#  Dependencies   :  Frames.py
#                    Baseline_Manager.py
#                    Realtime_Manager.py
#
#  Description    :  GUI of EEG Monitor for Measurement of Baseline and Realtime 
#                    Drownsiness/Relaxation/Alertness Level
#
#      Details    :  - eventb  --> activate obatin_baseline_data if start button is pressed
#                    - eventr  --> activate obatin_realtime_data if start button is pressed
#                    - thread1 --> run obatin_baseline_data function
#                    - thread2 --> run obatin_realtime_data function
#
# Rev     Arthor   Date          Changes
#--------------------------------------------------------------------------------------------#
# 1.0.0   Yeh      2024/01/02    ---
##############################################################################################
from .Baseline_Manager import Baseline_manager
from .Realtime_Manager import Realtime_manager
# from .Frames import wndApp
from . import Frames
import tkinter as tk
import threading as td

class GUI(tk.Tk):
   def __init__(self, *args, **kwargs):
      tk.Tk.__init__(self, *args, **kwargs)
      self.baseline_manager = Baseline_manager()
      self.realtime_manager = Realtime_manager()
      self.title("EEG Monitor")
      # self.geometry("350x200+600+250")
      self.eventb = td.Event()
      self.eventr = td.Event()
      
      self.app = Frames.wndApp(self, self.baseline_manager, self.realtime_manager)
   
   def start(self):
      self.thread1 = td.Thread(target=self.app.obtain_new_baseline_data, daemon=True)
      self.thread2 = td.Thread(target=self.app.obtain_new_realtime_data, daemon=True)
      self.thread1.start()
      self.thread2.start()
      self.mainloop()
   
   def set_event(self, c):
      if c == 'b' : self.eventb.set()
      else        : self.eventr.set()
   
   def clear_event(self, c):
      if c == 'b' : self.eventb.clear()
      else        : self.eventr.clear()

   def wait_event(self, c):
      if c == 'b' : self.eventb.wait()
      else        : self.eventr.wait()

   def Quit(self):
      self.destroy()
      
   def leave(self):
      raise SystemExit() 