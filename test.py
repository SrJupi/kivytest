from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from threading import Thread
import evdev
from evdev import InputDevice, categorize, ecodes, list_devices

class MyApp(App):
    def build(self):
        # Create the layout
        layout = BoxLayout(orientation='vertical')

        # Create a label to display key press events
        self.label = Label(text="Press any key on the Bluetooth device", size_hint=(1, 0.8))

        # Create the Button
        button = Button(text='Press me', size_hint=(1, 0.2))

        # Bind the button press and release events to their respective methods
        button.bind(on_press=self.on_button_press)
        button.bind(on_release=self.on_button_release)

        # Add the label and button to the layout
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout

    def on_button_press(self, instance):
        # This method is called when the button is pressed
        self.label.text = 'Button pressed'

    def on_button_release(self, instance):
        # This method is called when the button is released
        self.label.text = 'Button not pressed'

    def detect_input_device(self):
        # Enumerate all input devices
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            # Check if the device supports EV_KEY (keyboard-like events)
            if ecodes.EV_KEY in device.capabilities():
                # You can add more filtering based on device properties if needed
                return device.path
        return None

    def start_evdev_thread(self):
        device_path = self.detect_input_device()
        if not device_path:
            print("No suitable input device found.")
            return

        print(f"Using input device: {device_path}")
        device = InputDevice(device_path)
        loop_list = device.read_loop()
        for event in loop_list:
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                # Update label text from evdev thread
                if key_event.scancode == 201:  # pause
                    self.update_label_from_thread('Pause pressed')
                elif key_event.scancode == 200:  # play
                    self.update_label_from_thread('Play pressed')

    def update_label_from_thread(self, text):
        # Schedule label update on the main thread
        self.label.text = text

    def on_start(self):
        # Start the evdev thread
        print("Start Thread")
        evdev_thread = Thread(target=self.start_evdev_thread)
        evdev_thread.start()

if __name__ == '__main__':
    MyApp().run()
