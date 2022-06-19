# GUI Packages
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
Builder.load_file('update_label.kv')

# UM
from language_model import Text
from language_model import UnigramModel
from predictor_model import LanguagePredictor

class MyLayout(Widget):
    def press(self):
        test_text = self.ids.name_input.text
        fhand = open(file='current_text.txt', mode='w', encoding='utf-8')
        fhand.write(test_text)
        fhand.close()
        
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

class AwesomeApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    MODEL = LanguagePredictor()
    AwesomeApp().run()


# Errors to fix
# 1. devision by hero (when only numbers are entered)
