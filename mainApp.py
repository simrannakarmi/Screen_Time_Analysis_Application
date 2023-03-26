from time import strftime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from actual_time import Time
import matplotlib.pyplot  as plt
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import threading
import json
import signal
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
# from kivy.factory import Factory
# from kivy.uix.floatlayout import FloatLayout

# # define the custom FlowLayout class
# class FlowLayout(FloatLayout):
#     pass

# register the class with Kivy's Factory
# Factory.register('FlowLayout', cls=FlowLayout)

Window.size = (1000,600)

class Interface(BoxLayout):
    sw_seconds = 0
    sw_started = False

    def on_release(self):
        # super().__init__(**kwargs)
        t=threading.Thread(target=self.threaded_func, daemon=True)
        t.start()

    def threaded_func(self):
        self.start_time()
   
    def start_app(self):       
        self.ids.sm.current = 'timetrack_window'
        
        table = self.ids.table

        with open("my_data.csv", "r") as f:
            # iterate over each row in csv
            for row in f:
                # split the row by comma delimiter
                columns = row.split(",")
                # create a label for each column
                for column in columns:
                    table.add_widget(Label(text=column.strip()))

        Clock.schedule_interval(self.update_time, 0)
        # self.output_display() 

    def show_details(self):
        self.ids.sm.current = "details_window"
        self.plot_detail()
        global detail
        detail = subprocess.Popen(['python', 'csv_store.py'])
        detail.wait()
        detail.send_signal(signal.SIGTERM)

        table = self.ids.table

        with open("my_data.csv", "r") as f:
            # iterate over each row in csv
            for row in f:
                # split the row by comma delimiter
                columns = row.split(",")
                # create a label for each column
                for column in columns:
                    table.add_widget(Label(text=column.strip()))



    def plot_detail(self):
        box = self.ids.box
        obj=Time()
        dataf=obj.total_time()
        labels =dataf['name']
        y_data_seconds = [y.total_seconds() for y in dataf['total_time']]
        values=y_data_seconds
        plt.gcf().autofmt_xdate()
        ax = plt.subplot()
        ax.set_xticklabels(labels, rotation=10, ha='right')
        # print(values)
        plt.bar(labels, values)
        # Add labels and title
        plt.xlabel('Applications')
        plt.ylabel('Usage in seconds')
        plt.title('Screen Time Analysis')
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def start_time(self):
        self.ids.start.text = 'Start'
        self.sw_started = True
        # import timer
        # self.process = subprocess.call("timer.py", shell=True)
        global process
        process = subprocess.Popen(['python', 'timer.py'])
        process.wait()

        # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
        # runpy.run_path("timer.py")
    def stop_time(self):
        self.sw_started = False
        # App.get_running_app().stop()
        # subprocess.terminate()
        process.send_signal(signal.SIGTERM)
        self.ids.sm.current = 'timetrack_window'

        self.ids.show_details_button.disabled = False
        

    def reset(self):
        if self.sw_started:
            self.sw_started = False
        self.sw_seconds = 0

        self.ids.show_details_button.disabled = True

        with open('activities.json', 'w') as f:
        # Write an empty JSON object to the file
            json.dump({}, f)
        

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        hour, rem = divmod(self.sw_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        # part_seconds = seconds * 100 % 100
        self.ids.stopwatch.text = f'{int(hour):02}:{int(minutes):02}:{int(seconds):02}'
        # self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')


class ScreenTime(App):
    pass

ScreenTime().run()