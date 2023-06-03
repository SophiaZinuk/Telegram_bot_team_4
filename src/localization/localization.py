from localization.language import Language
import json


class Localization:

    def __init__(self, lang: Language) -> None:
        self._init_lang(lang)

    def _init_lang(self, lang: Language):
        if lang is None:
            self._read_localization_file('localization/lang/ua.json')
        else:
            self._read_localization_file('localization/lang/' + lang + '.json')

    def _read_localization_file(self, path: str):
        with open(path, mode='r') as file:
            self.lang = json.load(file)
