##############################################################################################
#     File Name   :  Realtime_Manager.py
#       Version   :  1.0.0
#       Arthors   :  Yeh Yu-Hao
#
#  Dependencies   :
#
#  Description    :  Manage the Measurement of Realtime EEG
#
#      Details    :  - activation       --> decide realtime measuring state
#                    - measuring        --> keep in measuring state once activated
#                    - reset_start_time --> reset start time once restart realtime measurement
#
# Rev     Arthor   Date          Changes
#--------------------------------------------------------------------------------------------#
# 1.0.0   Yeh      2024/01/02    ---
##############################################################################################
import numpy as np

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
   
   def get_start_time(self):
      return self.reset_start_time
   
   def reset_off(self):
      self.reset_start_time = False

   def set_ratio(self, ratio_list):
      self.ratio_list = ratio_list

   def get_ratio(self) -> np.array:
      return self.ratio_list
         
   def clear_ratio(self):
      self.ratio_list = np.array([[0, 0, 0, "freeze"]])
   
   def is_activated(self):
      return self.activation
   
   def is_measuring(self):
      return self.measuring
   