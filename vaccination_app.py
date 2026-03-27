
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from datetime import datetime, timedelta
import os

Window.size = (400, 600)

def get_valid_dates(days=10):
    dates = []
    current = datetime.today() + timedelta(days=1)
    while len(dates) < days:
        if current.weekday() < 5:
            dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    return dates

def get_valid_hours():
    return [f"{h:02d}:00" for h in range(8, 22)]

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.layout.add_widget(Label(text='Email'))
        self.email = TextInput(multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.email)

        self.layout.add_widget(Label(text='Κωδικός'))
        self.password = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        self.layout.add_widget(self.password)

        login_button = Button(text='Σύνδεση', size_hint_y=None, height=50)
        login_button.bind(on_press=self.login)
        self.layout.add_widget(login_button)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.layout.add_widget(self.error_label)

        self.add_widget(self.layout)

    def login(self, instance):
        email = self.email.text
        allowed_domains = ['@gmail.com', '@yahoo.com', '@outlook.com']
        if not all(ord(c) < 128 for c in email + self.password.text):
            self.error_label.text = '⛔ Μόνο αγγλικοί χαρακτήρες επιτρέπονται.'
        elif any(email.endswith(domain) for domain in allowed_domains):
            self.error_label.text = ''
            self.manager.current = 'center_select'
            self.manager.app_data['email'] = email
        else:
            self.error_label.text = '⛔ Μη έγκυρο email. Π.χ. user@gmail.com'

class CenterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text='Επιλέξτε Εμβολιαστικό Κέντρο'))

        centers = ['Αθήνα', 'Θεσσαλονίκη', 'Πάτρα', 'Ηράκλειο']
        for center in centers:
            btn = Button(text=center, size_hint_y=None, height=50)
            btn.bind(on_press=self.select_center)
            layout.add_widget(btn)

        self.add_widget(layout)

    def select_center(self, instance):
        self.manager.app_data['center'] = instance.text
        self.manager.current = 'datetime'

class DateTimeSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.valid_dates = get_valid_dates()
        self.valid_hours = get_valid_hours()

        layout.add_widget(Label(text='Επιλέξτε Ημερομηνία:'))
        self.date_spinner = Spinner(
            text='Επιλέξτε ημερομηνία',
            values=self.valid_dates,
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.date_spinner)

        layout.add_widget(Label(text='Επιλέξτε Ώρα:'))
        self.time_spinner = Spinner(
            text='Επιλέξτε ώρα',
            values=self.valid_hours,
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.time_spinner)

        confirm_btn = Button(text='Επιβεβαίωση Ραντεβού', size_hint_y=None, height=50)
        confirm_btn.bind(on_press=self.confirm)
        layout.add_widget(confirm_btn)

        self.result = Label(text='')
        layout.add_widget(self.result)

        self.add_widget(layout)

    def confirm(self, instance):
        date = self.date_spinner.text
        time = self.time_spinner.text
        if 'Επιλέξτε' in date or 'Επιλέξτε' in time:
            self.result.text = '⛔ Επιλέξτε ημερομηνία και ώρα!'
        else:
            self.result.text = f'✅ Ραντεβού: {date} στις {time}'
            email = self.manager.app_data.get('email', 'anonymous')
            center = self.manager.app_data.get('center', 'Άγνωστο Κέντρο')
            folder = 'bookings'
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"{email.replace('@', '_at_').replace('.', '_')}_{date}_{time.replace(':', '-')}.txt")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Email: {email}\nΗμερομηνία: {date}\nΏρα: {time}\nΚέντρο: {center}")

class VaccinationCenterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text='📋 Ραντεβού προς επιβεβαίωση'))

        self.appts = [
            {'name': 'Γιώργος', 'date': '2025-06-01', 'time': '14:00'},
            {'name': 'Μαρία', 'date': '2025-06-02', 'time': '11:30'}
        ]

        for appt in self.appts:
            btn = Button(text=f"{appt['name']} - {appt['date']} {appt['time']}", size_hint_y=None, height=50)
            btn.bind(on_press=lambda btn, a=appt: self.confirm_appt(btn, a))
            layout.add_widget(btn)

        self.add_widget(layout)

    def confirm_appt(self, button, appt):
        button.text += " ✅ ΕΠΙΒΕΒΑΙΩΘΗΚΕ"
        button.disabled = True

class VaccinationApp(App):
    def build(self):
        sm = ScreenManager()
        sm.app_data = {}
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CenterSelectionScreen(name='center_select'))
        sm.add_widget(DateTimeSelectionScreen(name='datetime'))
        sm.add_widget(VaccinationCenterScreen(name='center'))
        return sm

VaccinationApp().run()