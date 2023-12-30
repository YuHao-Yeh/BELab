class Baseline_manager():
   def __init__(self):
      self.activation = False
      self.measuring = True
      self.data = {
         "drownsiness" : "unknown",
         "relaxation"  : "unknown",
         "alertness"   : "unknown",
         "status"      : "unknown"
      }

   def activate(self):
      self.activation = True
      return self.activation

   def set_baseline(self, _data):
      self.data = _data
   
   def deactivate(self):
      self.measuring, self.activation = False, False
      return self.data
   
   def get_data(self):
      return self.data
   
   def is_activated(self):
      return self.activation
   
   def is_measuring(self):
      return self.measuring
