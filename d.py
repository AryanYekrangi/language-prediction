from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

# FONTS
from kivy.core.text import LabelBase
LabelBase.register(name="ArialUnicodeMS",
                   fn_regular="_fonts/arial-unicode-ms.ttf")

# UM
from language_model import Text
from language_model import UnigramModel
from predictor_model import LanguagePredictor

class FirstWindow(Screen):
    def press(self):
        fhand = open(file='current_text.txt', mode='r', encoding='utf-8')
        if len(fhand.read()) == 0:
            test_text = self.ids.name_input.text
            fhand = open(file='current_text.txt', mode='w', encoding='utf-8')
            fhand.write(test_text)
            fhand.close()
        else:
            test_text = fhand.read()
        
        if len(test_text) == 0:
            pass
        else:
            # prediction on saved file
            prediction = MODEL.predict_language(Text(filename='current_text.txt', language='english', percentage=1))
            prediction = list(prediction.items())[0][0]
        #self.ids.name_label.text = prediction
            try:
                exec(f"self.ids.{self.previous_prediction}_label.background_color = [0, 0, 0, 0]")
            except AttributeError:
                pass
            self.previous_prediction = prediction
            exec(f"self.ids.{prediction}_label.background_color = [0, 0, 1, 1]")
        open(file='current_text.txt', mode='w', encoding='utf-8').close()
        
class SecondWindow(Screen):
    def select(self, *args):
        try:
            filename = args[1][0]
            with open(filename, encoding='utf-8') as f:
                text = f.read()
            self.text_input.text = text
        except:
            pass

    def copy_texts(self):
        pass
        test_text = self.ids.text_input.text
        #fhand = open(file='current_text.txt', mode='w', encoding='utf-8')
        #fhand.write(test_text)
        self.manager.get_screen('first').ids.name_input.text = test_text
        #fhand.close()
        
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('new_window.kv')

class MyLayout(Widget):
    pass

class AwesomeApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    open(file='current_text.txt', mode='w', encoding='utf-8').close()
    MODEL = LanguagePredictor()
    AwesomeApp().run()
