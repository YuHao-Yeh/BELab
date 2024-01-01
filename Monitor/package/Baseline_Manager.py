##############################################################################################
#     File Name   :  Baseline_Manager.py
#       Version   :  1.0.0
#       Arthors   :  Yeh Yu-Hao
#
#  Dependencies   :
#
#  Description    :  Manage the Measurement of Baseline EEG
#
#      Details    :  - activation       --> decide baseline measuring state
#                    - measuring        --> keep in measuring state once activated
#                    - reset_start_time --> reset start time once restart baseline measurement
#                    - set_data         --> calculate ratio index if measurement is done
#
# Rev     Arthor   Date          Changes
#--------------------------------------------------------------------------------------------#
# 1.0.0   Yeh      2024/01/02    ---
##############################################################################################
class Baseline_manager():
   def __init__(self):
      self.activation = False
      self.measuring = True
      self.reset_start_time = False
      self.set_data = False
      self.time = 0.0
      self.data = {
         "drownsiness" : "unknown",
         "relaxation"  : "unknown",
         "alertness"   : "unknown",
         "status"      : "unknown"
      }

   def activate(self):
      self.activation, self.measuring, self.set_data = True, True, False
      return self.activation

   def deactivate(self):
      self.measuring, self.activation, self.reset_start_time, self.set_data = True, False, True, True
      return self.data

   def get_start_time(self):
      return self.reset_start_time
   
   def reset_off(self):
      self.reset_start_time = False
   
   def update_off(self):
      self.set_data = False

   def set_baseline(self, _data):
      self.data = _data
   
   def get_data(self):
      return self.data
   
   def clear_ratio(self):
      self.data = {
         "drownsiness" : "unknown",
         "relaxation"  : "unknown",
         "alertness"   : "unknown",
         "status"      : "unknown"
      }

   def is_activated(self):
      return self.activation
   
   def is_measuring(self):
      return self.measuring

   def update_data(self):
      return self.set_data
