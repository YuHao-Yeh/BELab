from .Baseline_Manager import Baseline_manager
from .Frames import wndApp
import tkinter as tk
from tkinter import messagebox
import threading as td

class GUI(tk.Tk):
   def __init__(self, *args, **kwargs):
      tk.Tk.__init__(self, *args, **kwargs)
      self.baseline_manager = Baseline_manager()
      self.title("EEG Monitor")
      # self.geometry("350x200+600+250")
      self.event = td.Event()
      self.app = wndApp(self, self.baseline_manager)
   
   def start(self):
      self.thread1 = td.Thread(target=self.app.obtain_new_baseline_data, daemon=True)
      self.thread2 = td.Thread(target=self.app.obtain_new_realtime_data, daemon=True)
      self.thread1.start()
      self.thread2.start()
      self.mainloop()
   
   def set_event(self):
      self.event.set()
   
   def clear_event(self):
      self.event.clear()

   def wait_event(self):
      self.event.wait()

   def Quit(self):
      if messagebox.askyesno(title="Quit", message="Are you sure to leave?"):
         self.app.destroy()
         self.destroy()
      else:
         return
   def leave(self):
      raise SystemExit() 