class Baseline_manager():
   def __init__(self):
      self.activation = False
      self.measuring = True
      self.data = {
         "drownsiness" : 1.0,
         "relaxation"  : 1.0,
         "alertness"   : 1.0,
         "status"      : "measuring..."
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
   
   def get_status(self):
      return self.measuring
