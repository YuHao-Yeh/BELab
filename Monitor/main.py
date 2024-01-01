##############################################################################################
#     File Name   :  main.py
#       Version   :  1.0.0
#       Arthors   :  Yeh Yu-Hao
#
#  Dependencies   :  GUI.py
#                    Frames.py
#                    EEG_handle.py
#                    Baseline_Manager.py
#                    Realtime_Manager.py
#
#  Description    :  Realtime EEG Measurement of Drownsiness/Relaxation/Alertness Level
#                    Based on Baseline Measurement 
#
#      Details    :  
#
# Rev     Arthor   Date          Changes
#--------------------------------------------------------------------------------------------#
# 1.0.0   Yeh      2024/01/02    ---
##############################################################################################
from package import *
def main():
   root = GUI()
   root.start()
   root.leave()
   print("End")

if __name__ == "__main__":
   main()