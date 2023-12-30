import numpy as np
import IPython.display as display

class Realtime_manager():
   def __init__(self) -> None:
      self.activation = False
      self.measuring = True
      self.reset_start_time = False
      self.ratio_list = np.array([[0, 0, 0, "freeze"]])
   
   def activate(self):
      self.activation, self.measuring = True, True
      return self.activation
   
   def stop(self):
      self.activation, self.measuring, self.reset_start_time = False, True, False
   
   def deactivate(self):
      self.activation, self.measuring, self.reset_start_time = False, True, True
   
   def reset_off(self):
      self.reset_start_time = False

   def get_start_time(self):
      return self.reset_start_time
   
   def is_activated(self):
      return self.activation
   
   def is_measuring(self):
      return self.measuring
   
   def clear_ratio(self):
      self.ratio_list = np.array([[0, 0, 0, "freeze"]])
   
   def set_ratio(self, ratio_list):
      self.ratio_list = ratio_list

   def get_ratio(self) -> np.array:
      return self.ratio_list
         