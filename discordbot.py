from googletrans import Translator

translator = Translator()

japanese = translator.translate('おはようございます。')
print(japanese.text)
#>> Good morning.
