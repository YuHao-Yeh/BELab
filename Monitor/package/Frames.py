from .EEG_handle import State
from .Baseline_Manager import Baseline_manager
from .Realtime_Manager import Realtime_manager
from .GUI import GUI
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
from math import log2
from IPython.display import display

IMAGE_SCALE = 2

class wndApp(tk.Frame):
   to_measure_arr = ['drownsiness', 'relaxation', 'alertness', 'status']
   def __init__(self, 
                master=GUI|None, 
                baseline_manager=Baseline_manager|None,
                realtime_manager=Realtime_manager|None, 
                graph_path="graph.png"):
      self.wnd = master
      super().__init__(master)
      self.pack(anchor="center", side="top")

      self.baseline_manager = baseline_manager  # Baseline Manage
      self.realtime_manager = realtime_manager  # Realtime Manage
      self.name_var = tk.StringVar()            # Subject info
      self.name_var.set('')
      self.graph_path = graph_path              # Graph
      self.running_frames = list()              # Record running frames

      self.style_init()
      self.create_frame1()
   
   def style_init(self):
      self.style = ttk.Style()
      self.style.configure('Measure.TButton',font=("Courier", 8), foreground="green", borderwidth=5)
      self.style.map("Measure.TButton", 
                     foreground = [("active", "!disabled", "black"), ("!active", "disabled", "gray")], 
                     background=[("active", "blue")])

   def create_frame1(self):
      self.clear_frames()
      self.wnd.geometry("350x200+600+250")
      self.widget1 = tk.Frame(self)
      self.widget1.pack()
      self.running_frames.append(self.widget1)

      # Name
      tk.Label(self.widget1, text='Name: ', height=4).grid(row=0, column=0)
      self.name_ent = tk.Entry(self.widget1, font=('Arial', 14))
      self.name_ent.bind("<Return>", (lambda event: self.reply(name=self.name_ent.get())))
      self.name_ent.grid(row=0, column=1, sticky=tk.W, ipadx=10)
      self.name_ent.focus_set()

      # Submit Name
      self.submit = ttk.Button(self.widget1, text='Send', width=20, command=lambda: [self.reply(self.name_ent.get()), self.create_frame2])
      self.submit.grid(row=1, column=0, columnspan=2, ipadx=10, pady=(15, 0))
 
      # Enter Baseline
      self.baseline_ent = ttk.Button(self.widget1, text="Start measuring baseline...", width=20, command=lambda: [self.reply(self.name_ent.get()), self.create_frame2])
      self.baseline_ent.grid(row=2, column=0, columnspan=2, ipadx=10)

      # Quit
      self.quit = ttk.Button(self.widget1, text="Quit", command=self.Quit, width=20)
      self.quit.grid(row=11, column=0, columnspan=2, ipadx=10)

   def create_frame2(self):
      self.clear_frames()
      self.wnd.geometry("500x500+530+150")
      self.widget2 = tk.Frame(self)
      self.widget2.pack()
      self.running_frames.append(self.widget2)

      # Frame Title & Subject Name
      self.create_widgets(self.widget2)

      # Baseline
      self.baseline_fr = tk.LabelFrame(self.widget2, text="Baseline", padx=5, pady=2, width=400, font=("Courier", 12), fg="purple")
      self.baseline_fr.grid(row=2, columnspan=3, ipadx=50, pady=(0, 20))
      self.running_frames.append(self.baseline_fr)
      self.baselines = dict(zip(self.to_measure_arr,
                                [(tk.Label(self.baseline_fr, text=f"{x}:", font=("Courier", 10), pady=2), 
                                  tk.Label(self.baseline_fr, text="unknown", font=("Courier", 10), pady=2)
                                 ) for x in self.to_measure_arr
                                ]))
      cnt = 0
      for i in self.baselines.values():
         i[0].grid(row=cnt, column=0, sticky=tk.E, padx=(90, 10))
         i[1].grid(row=cnt, column=1, sticky=tk.W)
         cnt += 1

      self.baseline_start = ttk.Button(self.baseline_fr, 
                                       text="Start", 
                                       style="Measure.TButton",
                                       command=self.activate_baseline_measurement, 
                                       width=10)
      self.baseline_toggle = ttk.Button(self.baseline_fr, 
                                        text="Finish",
                                        style="Measure.TButton",
                                        state="disabled",
                                        command=self.deactivate_baseline_measurement, 
                                        width=10)
      self.baseline_start.grid(row=cnt, column=0, columnspan=2, pady=(10, 10))
      self.baseline_toggle.grid(row=cnt, column=1, columnspan=2)

      # Back
      self.back = ttk.Button(self.widget2, text="Previous Page", command=self.create_frame1, width=20)
      self.back.grid(row=3, column=1)

      # Start Measurement
      self.realtime_toggle = ttk.Button(self.widget2, 
                                    text="Start measuring data...", 
                                    command=self.create_frame3, 
                                    width=20)
      self.realtime_toggle.grid(row=4, column=1)

      # Quit
      self.quit = ttk.Button(self.widget2, text="Quit", command=self.Quit, width=20)
      self.quit.grid(row=5, column=1)
   
   def create_frame3(self):
      self.check_baseline()
      self.clear_frames()
      self.wnd.geometry("600x800+500+0")  
      self.widget3 = tk.Frame(self)
      self.widget3.pack()
      self.running_frames.append(self.widget3)

      # Frame Title & Subject Name
      self.create_widgets(self.widget3)

      # Baseline
      self.baseline_fr = tk.LabelFrame(self.widget3, text="Baseline", padx=5, pady=2, font=("Courier", 12), fg="purple")
      self.baseline_fr.grid(row=2, columnspan=3, ipadx=50, pady=(0, 10))
      self.running_frames.append(self.baseline_fr)
      self.baselines = dict(zip(self.to_measure_arr,
                                [(tk.Label(self.baseline_fr, text=f"{x}:", font=("Courier", 10), pady=2),
                                  tk.Label(self.baseline_fr, text=self.baseline_data[x], font=("Courier", 10), pady=2)
                                  ) for x in self.baseline_data
                                ]))
      cnt = 0
      for i in self.baselines.values():
         i[0].grid(row=cnt, column=0, sticky=tk.E, padx=(120, 10))
         i[1].grid(row=cnt, column=1, sticky=tk.W)
         cnt += 1

      # Data
      self.realtime_fr = tk.LabelFrame(self.widget3, text="Data", padx=5, font=("Courier", 12), fg="purple")
      self.realtime_fr.grid(row=3, columnspan=3, ipadx=50, pady=(0, 10))
      self.running_frames.append(self.realtime_fr)
      self.texts, cnt = {}, 0
      for i in self.to_measure_arr:
         self.texts[i] = (tk.Label(self.realtime_fr, text=f"{i}:", font=("Courier", 10), pady=2),
                          tk.Label(self.realtime_fr, text=f"unknown", font=("Courier", 10), pady=2))
         self.texts[i][0].grid(row=cnt, column=0, sticky=tk.E, padx=(80, 10))
         self.texts[i][1].grid(row=cnt, column=1, sticky=tk.W)
         cnt += 1

      self.realtime_start = ttk.Button(self.widget3, 
                                       text="Start", 
                                       style="Measure.TButton",
                                       command=self.activate_realtime_measurement, 
                                       width=10)
      self.realtime_stop = ttk.Button(self.widget3, 
                                      text="Stop", 
                                      style="Measure.TButton",
                                      state="disabled",
                                      command=self.stop_realtime_measurement,
                                      width=10)
      self.realtime_toggle = ttk.Button(self.widget3, 
                                        text="Finish",
                                        style="Measure.TButton",
                                        state="disabled",
                                        command=self.deactivate_realtime_measurement, 
                                        width=10)
      self.realtime_start.grid(row=4, column=0, pady=(5, 10))
      self.realtime_stop.grid(row=4, column=1)
      self.realtime_toggle.grid(row=4, column=2)

      # Image
      self.graph_fr = tk.LabelFrame(self.widget3, text="Graph", padx=5, pady=2, font=("Courier", 12), fg="purple")
      self.graph_fr.grid(row=5, columnspan=3, pady=(0, 20))
      self.running_frames.append(self.graph_fr)
      try:
         self.graph_img = tk.PhotoImage(file=self.graph_path).subsample(IMAGE_SCALE)
         self.graph = tk.Label(self.graph_fr, image=self.graph_img, pady=2)
      except:
         self.graph = tk.Label(self.graph_fr, text="image not available", pady=2)
      self.graph.grid(row=1, columnspan=3)
      
      # Save
      self.save = ttk.Button(self.widget3, text="Save Ratio Index", command=self.save_ratio_index)
      self.save.grid(row=6, column=1)
      # Back
      self.back = ttk.Button(self.widget3, text="Previous page", command=self.create_frame2)
      self.back.grid(row=10, column=1)
      # Quit
      self.quit = ttk.Button(self.widget3, text="Quit", command=self.Quit)
      self.quit.grid(row=11, column=1)
   
   def clear_frames(self):
      for f in self.running_frames:
         f.destroy()
      self.running_frames.clear()

   def reply(self, name):
      if name == "":
         if self.name_var.get() == "":
            messagebox.showinfo(title="Reply", message="Please enter a name!")
         else:
            self.create_frame2()
      else:
         self.name_var.set(name)
         self.name_ent.delete(0, tk.END)
         self.create_frame2()

   def create_widgets(self, frame:tk.Frame):
      self.title = tk.Label(frame, text="EEG 心智狀態監測儀", font=("Courier", 30), fg="blue", pady=5)
      self.title.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=(20, 0))
      self.name = tk.Label(frame, text=' '.join(["Name:", self.name_var.get()]), font=("Courier", 18), pady=5)
      self.name.grid(row=1, column=0, columnspan=3, pady=(5, 5))

   def activate_baseline_measurement(self):
      if self.baseline_start["state"] == "disabled":
         return
      self.baseline_manager.activate()
      self.baseline_start.config(state="disabled")
      self.baseline_toggle.config(state="enable", text="Finish")
      for x in self.baselines.values():
         x[1].config(text="measuring...")

   def deactivate_baseline_measurement(self):
      if self.baseline_toggle["state"] == "disabled":
         return
      self.baseline_toggle.config(state="disabled", text="已結束")
      self.baseline_start.config(state="enable", text="Restart")
      self.set_baseline(self.baseline_manager.deactivate())
      # messagebox.showinfo(title="Info", message="End Baseline Measurement")
   
   def set_baseline(self, baseline_data:dict):
      self.baseline_data = baseline_data
      for i in baseline_data:
         self.baselines[i][0].grid(padx=(120, 10))
         self.baselines[i][1].config(text=baseline_data[i])

   def check_baseline(self):
      if self.baseline_manager.is_measuring():
         self.deactivate_baseline_measurement()

   def activate_realtime_measurement(self):
      if self.realtime_start["state"] == "disabled":
         return
      self.wnd.set_event()
      self.realtime_manager.activate()
      if self.realtime_start["text"] == "Restart":
         self.realtime_manager.clear_ratio()
      self.realtime_start.config(state="disabled")
      self.realtime_toggle.config(state="enable", text="Finish")
      self.realtime_stop.config(state="enable", text="Stop")

   def stop_realtime_measurement(self):
      if self.realtime_toggle["state"] == "disabled":
         return
      self.realtime_manager.stop()
      self.realtime_toggle.config(state="enable")
      self.realtime_stop.config(state="disabled")
      self.realtime_start.config(state="enable", text="Continue")

   def deactivate_realtime_measurement(self):
      if self.realtime_toggle["state"] == "disabled":
         return
      self.realtime_manager.deactivate()
      self.realtime_toggle.config(state="disabled", text="已結束量測")
      self.realtime_stop.config(state="disabled")
      self.realtime_start.config(state="enable", text="Restart")
   
   def update_labels(self, datas:dict):
        for i in datas:
            self.texts[i][1]["text"] = datas[i]
   
   def update_graph(self):
      self.graph_img = tk.PhotoImage(file=self.graph_path).subsample(IMAGE_SCALE)
      self.graph.configure(image=self.graph_img)

   def save_ratio_index(self):
      self.deactivate_realtime_measurement()
      filepath = askstring(title="Save Ratio Index", prompt="Filename:")
      base = tuple([self.baseline_data.get(self.to_measure_arr[i]) for i in range(3)])
      with open(filepath, 'w') as file:
         file.write(''.join(["Subject Name: ", self.name_var.get(), '\n']))
         file.write(''.join(["Baseline: ", ','.join(base),'\n']))
         for row in self.realtime_manager.get_ratio():
            file.write(''.join([','.join(row), '\n']))
         file.close()


   def obtain_new_baseline_data(self):
      """Baseline"""
      # i2c = busio.I2C(board.SCL, board.SDA)
      # ads = ADS.ADS1115(i2c, gain=1, data_rate = 250)
      # channel = AnalogIn(ads, ADS.P0)

      start = time.time()
      fs_base = 350
      data, i = np.zeros((300*fs_base, 2)), 0
      while self.baseline_manager.is_measuring():
         if i >= 300*fs_base: i = 0
         if self.baseline_manager.is_activated():
            # data[i], i = [time.time() - start, channel.voltage], i + 1
            data[i], i = [time.time() - start, np.random.randn(1)[0]], i + 1
      data = data[~np.all(data == 0, axis=1)]
      source = State(sig=data[:, 1], fs=(data.shape[0]/data[-1:, 0] - data[0, 0]))
      base = source.Get_RI()
      self.baseline_manager.set_baseline({'drownsiness': str(np.round(base[0], 2)), 'relaxation': str(np.round(base[1], 2)), 'alertness': str(np.round(base[2], 2)), 'status':str('Done')})
      self.set_baseline({'drownsiness': str(np.round(base[0], 2)), 'relaxation': str(np.round(base[1], 2)), 'alertness': str(np.round(base[2], 2)), 'status':str('Done')})

   def obtain_new_realtime_data(self):
      """Realtime"""
      self.wnd.wait_event()
      self.wnd.clear_event()
      
      # i2c = busio.I2C(board.SCL, board.SDA)
      # ads = ADS.ADS1115(i2c, gain=1, data_rate = 250)
      # channel = AnalogIn(ads, ADS.P0)

      start, fs_base, span_unit, span, i = time.time(), 350, 4, 4, 0
      data = np.zeros(((span_unit+1)*fs_base, 2))
      while self.realtime_manager.is_measuring():
         if self.realtime_manager.get_start_time():
            start, span = time.time(), span_unit
            self.realtime_manager.reset_off()

         if i >= (span_unit+1)*fs_base: i = 0
         if self.realtime_manager.is_activated():
            curr = time.time() - start
            # data[i], i = [curr, channel.voltage], i + 1
            data[i], i = [curr, np.random.randn(1)[0]], i + 1
            
            if curr > span:
               with ThreadPoolExecutor(max_workers=5) as executor:
                  executor.submit(self.handle_data, data, i, span_unit)
                  data, i = np.zeros(((span_unit+1)*fs_base, 2)), 0
                  span += span_unit

   def handle_data(self, data:np.zeros, cnt:int, span_unit:int):
      data = data[~np.all(data == 0, axis=1)]
      source = State(sig=data[:cnt, 1], fs=(len(data) >> int(log2(span_unit))))
      ratio = source.Get_RI()
      base = tuple([eval(self.baseline_data.get(self.to_measure_arr[i])) for i in range(3)])
      status = source.mental_status(ratio[0], ratio[1], ratio[2], base[0], base[1], base[2])
      self.update_labels({'drownsiness': str(np.round(ratio[0], 2)), 
                          'relaxation': str(np.round(ratio[1], 2)), 
                          'alertness': str(np.round(ratio[2], 2)), 
                          'status': status
                         })
      self.realtime_manager.set_ratio(np.vstack((self.realtime_manager.get_ratio(), 
                                                 [np.round(ratio[0], 2), np.round(ratio[1], 2), np.round(ratio[2], 2), status]
                                                )))
      data = np.array(self.realtime_manager.get_ratio()[:, :3], dtype=float)
      for i in range(data.shape[0]):
         for j in range(data.shape[1]):
            data[i, j] = np.round(data[i][j]/base[j], 2)
      source.PlotRI(ratio=data)
      with ThreadPoolExecutor(max_workers=5) as executor:
         executor.submit(self.update_graph)
      
   def Quit(self):
      if messagebox.askyesno(title="Quit", message="Are you sure to leave?"):
         self.destroy()
         self.wnd.Quit()
      else:
         return