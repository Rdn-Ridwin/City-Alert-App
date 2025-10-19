from kivy.config import Config

# Set window size and make it non-resizable
Config.set('graphics', 'resizable', '0')  # 0 = False, 1 = True
Config.set('graphics', 'width', '324')    # Window width
Config.set('graphics', 'height', '576')   # Window height

import pickle
import requests
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.garden.mapview import MapView, MapMarker
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
import geocoder
from plyer import gps
from datetime import datetime
import os
from kivy.properties import  StringProperty

HERE_API_KEY = 'U58FLVEk2HlwBB0fTuPg-qx7Skyyu3E-d0niRsFGd48'


# Set the window icon
Window.set_icon('icon.jpg')  # Replace with your icon file name

KV = """
<SignInScreen>:
    canvas.before:
        Rectangle:  # background image
            source: 'CityAlert.png'  # Path to your image
            pos: self.pos  # Position of the image
            size: self.size  # Size of the image

    RelativeLayout:
        # Full Name Label
        Label:
            text: 'Full Name (Required):'
            color: 0, 0, 0, 0.7
            size_hint: 0.476, 0.1
            pos_hint: {'x': 0.1, 'center_y': 0.51}  # Relative positioning

        # TextInput for name
        TextInput:
            background_color: (1, 1, 0, 0)  # Transparent background color
            background_normal: ''  # Removes the normal background image
            foreground_color: (0, 0, 0, 1)  # Text color (black)
            id: name_input
            multiline: False
            size_hint: 0.6, 0.08
            pos_hint: {'x': 0.097, 'y': 0.41}
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 0.6  # Line color (black)
                Line:
                    points: self.x + self.parent.width*0.021, self.y + 15, self.right+self.parent.width*0.17, self.y + 15  # Horizontal line
                    width: 1.2  # Line thickness

        # Phone number label
        Label:
            text: 'Phone Number (required):'
            color: 1, 0, 0, 0.6
            size_hint: 0.45, 0.1
            pos_hint: {'x': 0.15, 'center_y': 0.38}

        # BoxLayout for country code spinner and phone input
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 0.8, 0.08
            pos_hint: {'x': 0.12, 'center_y': 0.3}
            spacing: 10

            Spinner:
                background_color: (1, 1, 1, 0)  # Transparent background color
                background_normal: ''  # Removes the normal background image
                foreground_color: (0, 0, 0, 1)  # Text color (black)
                id: country_code_spinner
                text: '+968 (Oman)'  # Default selected value
                values: ['+1(USA)', '+91(India)', '+968(Oman)', '+44(UK)', '+49(Germany)', '+81(Japan)', '+86(China)', '+33(France)', '+39(Italy)', '+7(Russia)', '+34(Spain)', '+47(Norway)', '+55(Brazil)', '+971(UAE)']
                color: 0, 0, 0, 0.6
                size_hint: 0.5, 1
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.6  # Line color (black)
                    Line:
                        points: self.x -self.parent.width*0.015, self.y, self.right+self.parent.width*0.009, self.y  # Horizontal line
                        width: 1.2  # Line thickness

            # TextInput for phone number
            TextInput:
                background_color: (1, 1, 1, 0)  # Transparent background color
                background_normal: ''  # Removes the normal background image
                foreground_color: (0, 0, 0, 1)  # Text color (black)
                id: phone_input
                multiline: False  # Single-line input
                size_hint: 0.7, 1
                hint_text:'12345678'
                pos_hint: {'x':0.0,'center_y': 0.3}
                input_filter: 'int'  # Restrict input to numbers only

                
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.6  # Line color (black)
                    Line:
                        points: self.x + 5, self.y+self.parent.height*0.2, self.right-self.parent.width*0.08, self.y+self.parent.height*0.2  # Horizontal line
                        width: 1.2  # Line thickness

        # Next button
        Button:
            text: 'Next'
            size_hint: 0.5, 0.1
            pos_hint: {'center_x': 0.5, 'center_y': 0.15}
            on_press: app.switch_to_map()
            background_color: 0, 0, 0, 0  # Make default background transparent
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1  # Set button background color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [20]  # Rounded corners


<MapScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, None
            height: dp(40)
            TextInput:
                id: search_input
                hint_text: 'Search country or location...'
                size_hint: 0.8,1
                multiline: False
            Button:
                text: 'Search'
                size_hint:0.2,1
                on_press: app.search_location(search_input.text)

        MapView:
            id: map_view
            zoom: 5  # Default zoom level
            lat: app.get_lat()  # Initial latitude
            lon: app.get_lon()  # Initial longitude
    RelativeLayout:
        Button:
            text: ""
            size_hint: None, None  # Disable size hint
            size: '50dp','50dp'  # Set absolute size (width, height)
            pos_hint: {'right': 0.97,'y': 0.01}  # Set absolute position (x, y)
            background_color: 0, 0, 0, 0  # Transparent default background
            on_press: app.switch_to_report()
            canvas.before:
                Rectangle:
                    source: 'alert1.png'  # Path to your image file
                    size: self.size
                    pos: self.pos
                    


<Reportscreen>:
    RelativeLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background color
            Rectangle:
                pos: self.pos
                size: self.size
        
        ScrollView:
            do_scroll_y: True  # Enable vertical scrolling
            pos_hint: {'x': 0.0,'top': 0.93875}
            RelativeLayout:
                id: report_content
                size_hint_y: None
                height: 600

                MapView:
                    id: report_map_view
                    zoom: 15
                    lat: 23.66043
                    lon: 58.18732
                    size_hint: 1, 0.3333
                    pos_hint: {'x': 0.0, 'center_y': 0.85}
                Button:
                    text: ""
                    size_hint: None, None  # Disable size hint
                    size: '30dp', '30dp'  # Set absolute size (width, height)
                    pos_hint: {'right': 0.98, 'y': 0.75}  # Position relative to the MapView
                    background_color: 0, 0, 0, 0  # Transparent default background
                    on_press: app.update_current_location()
                    canvas.before:
                        Rectangle:
                            source:'c_location.png'  # Path to your image file
                            size: self.size
                            pos: self.pos    

                TextInput:
                    id: search_input_report
                    hint_text: 'Search country or location...'
                    size_hint: 1,None
                    height: '40dp'
                    multiline: False  
                    pos_hint: {'center_x': 0.5, 'y': 0.65}
                Button:
                    text: ''
                    size_hint: 0.1,0.041
                    pos_hint: {'right': 1.0,'y': 0.65}
                    background_color: 1,1,1, 0  # Transparent default background
                    on_press: app.search_location_report(search_input_report.text)
                    #canvas.before:
                        #Rectangle:
                            #source: 'search.png'  # Path to your image file
                            #size: self.size
                            #pos: self.pos

                    
                Button:
                    text: 'Submit Report'
                    size_hint: None, None
                    size: 320, 45
                    font_size: 20
                    bold: True
                    pos_hint: {'center_x': 0.5, 'y': 0.05}
                    on_press: app.submit_report(),app.switch_to_reportfile()
                    background_color: 0, 0, 0, 0
                    canvas.before:
                        Color:
                            rgba: 1, 0, 0, 1  # Set button background color
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [20]  # Adjust the radius for rounded corners
                

                Button:
                    id: select_case
                    text: 'Select Case'
                    size_hint: 1,0.078125
                    pos_hint: {'center_x': 0.5, 'top': 0.645}
                    on_press: app.switch_to_crimereport()
                    background_color: 1, 0, 0, 1  # Red background
                    color: 1, 1, 1, 1  # White text color

                TextInput:
                    id: report_description
                    hint_text: 'Enter description of the incident'
                    multiline: True
                    size_hint: 1, 0.260
                    pos_hint: {'x': 0.0,'top':0.49 }
                Label:
                    text: app.date()
                    pos_hint: {'center_x': 0.25,'center_y': 0.53}
                    color:0,0,0,1
                Label:
                    text: app.time()
                    pos_hint: {'center_x': 0.75,'center_y': 0.53}
                    color:0,0,0,1
            
        Label:
            text:"Report"
            color: 1, 1, 1, 1  # White text color for contrast
            size_hint: 1,0.0625
            pos_hint: {'x': 0.0,'center_y': 0.97}
            font_size: 24  # Increase font size (adjust as needed)
            bold: True  # Make text bold
            canvas.before:
                Color:
                    rgba: 0.827, 0.184, 0.184, 1  # Red color
                Rectangle:
                    pos: self.pos
                    size: self.size        
        Button:
            text: ''
            font_size: 23
            bold: True
            size_hint: 0.1, 0.05
            pos_hint: {'x': 0,'y': 0.9395}  # Adjusted position to avoid overlap
            on_press: app.switch_to_map()
            background_color: 0, 0, 0, 0  # Transparent background
            color: 1, 1, 1, 1  # Red text color for the 'X'
            canvas.before:
                Rectangle:
                    source: 'back.png'  # Path to your image file
                    size: self.size
                    pos: self.pos

            


<Report>:
    FloatLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background color
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'Report Submitted'
            color: 0, 0, 0, 1  # Black text color
            size_hint: None, None
            size: 300, 50
            pos: 12, 500  # Adjusted position
            font_size: 24  # Increase font size
            bold: True  # Make text bold

        Label:
            text: 'Thank you for reporting!'
            color: 0, 0, 0, 1  # Black text color
            size_hint: None, None
            size: 300, 50
            pos: 12, 460  # Adjusted position
            font_size: 18  # Increase font size

        Button:
            text: 'Back to Map'
            size_hint: None, None
            size: 150, 50
            pos: 85, 20  # Adjusted position
            on_press: app.switch_to_map()
            background_color: 0, 0, 0, 0  # Transparent background
            canvas.before:
                Color:
                    rgba: 1, 0, 0, 1  # Set button background color
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [20]  # Adjust the radius for rounded corners

<CrimeReportScreen>:     
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background color
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'Select the Case:'
            size_hint_y: None
            height: '40dp'
            font_size: 20
            bold: True
            color: 1, 1, 1, 1
            canvas.before:
                Color:
                    rgba: 0.827, 0.184, 0.184, 1  # Red color
                Rectangle:
                    pos: self.pos
                    size: self.size

        ScrollView:
            size_hint: (1, 0.6)  # Take 60% of the screen height and full width
            
            GridLayout:
                id: crime_group  # ID for the group of crime buttons
                cols: 1
                spacing: 0,0  # Use relative spacing (2% of width and height)
                padding: [0.05, 0.05, 0.05, 0.05]  # Padding as 5% of width and height
                size_hint_y: None
                height: self.minimum_height  # Adjust height based on content
                
                ToggleButton:
                    text: 'Burglary'
                    group: 'crime_group'
                    size_hint_y: None
                    color: 0, 0, 0, 1  # Text color
                    height: '40dp'
                    background_color: 1,1,1,1
                    
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Theft'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Vandalism'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Arson'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                
                ToggleButton:
                    text: 'Trespassing'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                    # "Contact Crime"
                ToggleButton:
                    text: 'Assault'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Homicide'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                    # "Other Crimes"
                ToggleButton:
                    text: 'Fraud'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Bribery'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Cybercrime'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Smuggling'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                #    "Missing and Wanted"

                ToggleButton:
                    text: 'Missing Persons'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Wanted Criminals'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                
                ToggleButton:
                    text: 'Abduction'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Kidnapping'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                        # "Accident"
                ToggleButton:
                    text: 'Traffic Acciden'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Workplace Accident'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Industrial Accident'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height: '40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

                ToggleButton:
                    text: 'Slip and Fall'
                    group: 'crime_group'
                    size_hint_y: None
                    color:0,0,0,1
                    background_color: 1,1,1,1
                    height:'40dp'
                    background_normal: ''  # Remove the default background
                    background_down: ''  # Remove default background when pressed                  
                    on_state:
                        self.background_color = (1, 0.5, 0.5, 1) if self.state == 'down' else (1,1,1, 1)  # Change color when pressed down
                    on_press: app.select_crime(self)

        Button:
            text: 'Selected'
            size_hint: (1, 0.05)  # Button takes full width, 10% of screen height
            pos_hint: {'center_x': 0.5}  # Center the button horizontally
            on_press: app.switch_to_report()  # Call app's submit_report method
            background_color: 1, 0, 0, 1  # Red background
            color: 1, 1, 1, 1  # White text color
<CrimePopup>:
    title: "Crime Details"
    size_hint: 0.6, 0.4
    BoxLayout:
        orientation: "vertical"
        Label:
            id: crime_label
            text: root.crime_text
            multiline: True  # allow the text to wrap to multiple lines
        Button:
            text: "Close"
            on_release: root.dismiss()

"""

class SignInScreen(Screen):
    pass

class MapScreen(Screen):
    pass

class Reportscreen(Screen):
    pass

class Report(Screen):
    pass

class CrimeReportScreen(Screen):
    pass
class CrimePopup(Popup):
    crime_text = StringProperty()

    def __init__(self, crime_text, **kwargs):
        self.crime_text = crime_text
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 200)  # initial size
        self.update_size()

    def update_size(self):
        label = self.ids.crime_label
        label.text = self.crime_text
        label.texture_update()
        label.text_size = (self.width - 20, None)  # set the maximum width of the text
        label.height = label.texture_size[1]  # set the height of the label to the height of the texture
        self.height = label.height + 100  # add some padding
            


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.markers = []  # Initialize markers list here
        self.file_path = rf'C:\Users\redbi\Downloads\Project\Project\Userdata\user_data.txt'  # File to store user data

    def build(self):
        self.title = "Crime alert"
        self.icon = "icon.jpg"  # Path to the icon
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SignInScreen(name='sign_in'))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(Reportscreen(name='report'))
        sm.add_widget(Report(name='reportfile'))
        sm.add_widget(CrimeReportScreen(name='crimereport'))

        # Check if user data file exists and is not empty
        if os.path.exists(self.file_path) and os.path.getsize(self.file_path) > 0:
            with open(self.file_path, 'r') as file:
                data = file.read().splitlines()
                if len(data) == 2:  # Check if file contains both name and phone number
                    sm.current = 'map'  # Switch to map screen directly
        else:
            sm.current = 'sign_in'  # Prompt user to sign in

        return sm

    def switch_to_map(self):
        # Check if user is already signed in
        if self.root.current != 'sign_in':
            self.root.current = 'map'
            return

        # Get the text inputs from the SignInScreen
        sign_in_screen = self.root.get_screen('sign_in')
        name = sign_in_screen.ids.name_input.text
        phone = sign_in_screen.ids.phone_input.text

        # Check if both fields are filled
        if not name.strip() or not phone.strip():
            self.show_error("Please fill in both fields.")
        else:
            # Save user data to file
            with open(self.file_path, 'w') as file:
                file.write(name + '\n' + phone)

            self.root.current = 'map'  # Switch to map screen
        self.load_crime_data()

    def switch_to_report(self):
        self.root.current = 'report'

    def switch_to_reportfile(self):
        self.root.current = 'reportfile'
    
    def switch_to_crimereport(self):
        self.root.current = 'crimereport'

    def submit_report(self):
        Rep_scren = self.root.get_screen('report')
        crime_group = self.root.get_screen('crimereport').ids.crime_group.children  # Access the crime buttons
        selected_crime = None
        
        # Find the selected crime button
        for button in crime_group:
            if button.state == 'down':
                selected_crime = button.text
                break

        # Get the description from the TextInput
        description = Rep_scren.ids.report_description.text
        lat=Rep_scren.ids.report_map_view.lat
        lon=Rep_scren.ids.report_map_view.lon
        # Logic for handling the submission
        if selected_crime:
            folder_path = rf'crimereport'  # Folder where files will be saved
            file_path = os.path.join(folder_path, 'crime.txt')
            
            # Write the report to the file
            with open(file_path, 'a') as f:
                f.write(f'\n{[selected_crime,description,lat,lon]}')
            print(f"Report submitted successfully. Saved as {file_path}")
        else:
            print("No crime selected")


    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(0.6, 0.6))
        popup.open()
    
    def search_location_report(self, location):
        if location:
            try:
                # Call the HERE Maps Geocoding API
                geocode_url = f"https://geocode.search.hereapi.com/v1/geocode?q={location}&apiKey={HERE_API_KEY}"
                response = requests.get(geocode_url)
                data = response.json()
                
                if 'items' in data and len(data['items']) > 0:
                    location_data = data['items'][0]['position']
                    lat = location_data['lat']
                    lon = location_data['lng']
                    
                    map_view = self.root.get_screen('report').ids.report_map_view
                    map_view.center_on(lat, lon)
                    map_view.zoom = 15  # Zoom in on the location
                    
                    # Add marker to the map
                    marker = MapMarker(lat=lat, lon=lon)
                    map_view.add_widget(marker)
                else:
                    self.show_error("Location not found.")
            except Exception as e:
                self.show_error(f"Error: {e}")

    def search_location(self, location):
        if location:
            try:
                # Call the HERE Maps Geocoding API
                geocode_url = f"https://geocode.search.hereapi.com/v1/geocode?q={location}&apiKey={HERE_API_KEY}"
                response = requests.get(geocode_url)
                data = response.json()
                
                if 'items' in data and len(data['items']) > 0:
                    location_data = data['items'][0]['position']
                    lat = location_data['lat']
                    lon = location_data['lng']
                    
                    map_view = self.root.get_screen('map').ids.map_view
                    map_view.center_on(lat, lon)
                    map_view.zoom = 15  # Zoom in on the location
                    
                    # Add marker to the map
                    marker = MapMarker(lat=lat, lon=lon)
                    map_view.add_widget(marker)
                else:
                    self.show_error("Location not found.")
            except Exception as e:
                self.show_error(f"Error: {e}")

    def update_location(self, **kwargs):
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if lat and lon:
            map_view = self.root.get_screen('map').ids.map_view
            map_view.center_on(lat, lon)

            # Clear previous markers and add a blinking marker
            map_view.clear_widgets()
            self.blink_marker(map_view, lat, lon)

    def blink_marker(self, map_view, lat, lon):
        # Create a marker
        marker = MapMarker(lat=lat, lon=lon)
        map_view.add_widget(marker)

        def blink():
            while True:
                time.sleep(0.5)
                marker.color = (1, 0, 0, 1)  # Red color
                time.sleep(0.5)
                marker.color = (1, 1, 1, 1)  # White color

        # Start the blinking effect in a separate thread
        threading.Thread(target=blink, daemon=True).start()

    def start_location_tracking(self):
        def run():
            gps.configure(on_location=self.update_location)
            gps.start()

        threading.Thread(target=run).start()
    
    def date(self):
        month=['Jan','Feb','Mar',"Apr",'May','Jun',"Jul",'Aug','Sep',"Oct","Nov","Dec"]
        end={
            '01': 'st', '02': 'nd', '03': 'rd', '04': 'th', '05': 'th', '06': 'th', 
            '07': 'th', '08': 'th', '09': 'th', '10': 'th', '11': 'th', '12': 'th', 
            '13': 'th', '14': 'th', '15': 'th', '16': 'th', '17': 'th', '18': 'th', 
            '19': 'th', '20': 'th', '21': 'st', '22': 'nd', '23': 'rd', '24': 'th', 
            '25': 'th', '26': 'th', '27': 'th', '28': 'th', '29': 'th', '30': 'th', 
            '31': 'st'
            }

        date=datetime.now().strftime('%d')
        monthno=int(datetime.now().strftime('%m'))-1
        return date+end[date]+' '+month[monthno] if int(date)>10 else date[1:]+end[date]+' '+month[monthno]
    
    def time(self):
        now=datetime.now().strftime('%H:%M')
        return now +' AM' if int(now[:2])<13 else str(int(now[:2])-12)+now[2:]+' PM'
    
    def get_lat(self):
        g = geocoder.ip('me')
        return g.latlng[0]
    
    def get_lon(self):
        g = geocoder.ip('me')
        return g.latlng[1]   
    
    def update_current_location(self):
        # Get the current location using geocoder
        g = geocoder.ip('me')
        if g.ok:
            lat, lon = g.latlng
            map_view = self.root.get_screen('report').ids.report_map_view
            map_view.center_on(lat, lon)

            # Set a zoom level (adjust value as needed)
            map_view.zoom = 15  # Change this value to zoom out

            # Check if there's an existing marker and remove it
            if self.markers:
                map_view.remove_widget(self.markers[0])  # Remove the previous marker
                self.markers.clear()  # Clear the marker list

            # Add a new marker for the current location
            marker = MapMarker(lat=lat, lon=lon)
            map_view.add_widget(marker)
            self.markers.append(marker)  # Keep track of the marker

        else:
            self.show_error("Unable to fetch current location.")
        

    def load_crime_data(self):
        file_path=rf"C:\Users\redbi\Downloads\Project\Project\crimereport\crime.txt"
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Convert the string representation of list into a list
                    crime_data = eval(line)  # Unsafe for real-world use; make sure data is sanitized

                    # Extract data from the list: [selected_crime, description, lat, lon]
                    crime_type = crime_data[0]
                    description = crime_data[1]
                    latitude = crime_data[2]
                    longitude = crime_data[3]

                    # Create a MapMarker for the given latitude and longitude
                    marker = MapMarker(lat=latitude, lon=longitude)
                    marker.bind(on_release=lambda marker, ct=crime_type, desc=description: self.show_popup(ct, desc))
                    
                    # Optionally, you can customize the marker's appearance based on the crime type
                    # For example, use different marker colors/icons for different crimes
                    #marker.source = 'marker.png'  # You can customize this with different icons if needed
                    
                    # Add the marker to the map
                    self.root.get_screen('map').ids.map_view.add_marker(marker)

    def show_popup(self, crime_type, description):
        # Create and display a popup with the crime type and description
        popup = CrimePopup(crime_text=f"{crime_type}: {description}")
        popup.open()

    def select_crime(self, instance):
        # Get the text of the selected crime or incident
        selected_crime = instance.text
        # Update the text of the 'Select Case' button
        report_screen = self.root.get_screen('report')
        report_screen.ids.select_case.text = selected_crime

if __name__ == '__main__':
    Builder.load_string(KV)
    MyApp().run()
