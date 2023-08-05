#-*- coding: utf-8 -*-

from yandex.Translater import Translater
import yandex
import os
import unittest

class TestYandexTranslater(unittest.TestCase):

    def test_ins(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        print('test_ins -> Ok.')

    def test_empty_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)

        try:
            tr.set_key('')
        except yandex.Translater.TranslaterApiKey:
            print('test_empty_api_key -> Ok.')

    def test_empty_text(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        try:
            tr.set_text('')
        except yandex.Translater.TranslaterText:
            print('test_empty_text -> Ok.')

    def test_empty_from_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        
        try:
            tr.set_from_lang('')
        except yandex.Translater.TranslaterLang:
            print('test_empty_from_lang -> Ok.')

    def test_empty_to_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        
        try:
            tr.set_to_lang('')
        except yandex.Translater.TranslaterLang:
            print('test_empty_to_lang -> Ok.')

    def test_forbiden_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        tr.set_key('IaMiNvAlIdKeY')
        tr.set_text('Hello Yandex')
        tr.set_from_lang('en')
        tr.set_to_lang('ru')

        try:
            result = tr.translate()
        except yandex.Translater.TranslaterError:
            print('test_forbiden_api_key -> Ok.')

    def test_blocked_api_key(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)

        blocked_key = os.environ.get('YANDEX_BLOCKED_KEY', False)

        if not blocked_key:
            print('no test for blocked_api_key -> Ok.')

        else:
            tr.set_key(blocked_key)
            tr.set_text('Hello Yandex')
            tr.set_from_lang('en')
            tr.set_to_lang('ru')

            try:
                result = tr.translate()
            except (yandex.Translater.TranslaterBlockedKey, yandex.Translater.TranslaterError):
                print('test_blocked_api_key -> Ok.')

    def test_valid_api_key(self):    
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        key = os.environ.get('YANDEX_KEY', False)
        
        if not key:
            print('no test for valid_api_key -> Ok.')
        
        else:
            try:
                tr.set_key(key)
                tr.set_text('Hello Yandex')
                tr.set_from_lang('en')
                tr.set_to_lang('ru')
                result = tr.translate()
                self.assertEqual(type(result), str)
                self.assertEqual(result, 'Здравствуйте Яндекса')
                print('test_valid_api_key -> Ok.')
            except (yandex.Translater.TranslaterBlockedKey, yandex.Translater.TranslaterError):
                print('test_valid_api_key -> NoK.')

    def test_get_langs(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        key = os.environ.get('YANDEX_KEY', False)

        if not key:
            print('no test for get_langs -> Ok.')

        else:
            try:
                tr.set_key(key)
                result = tr.get_langs()
                self.assertEqual(isinstance(result, list), True)
                print('test_get_langs -> Ok.')
            except (yandex.Translater.TranslaterBlockedKey, yandex.Translater.TranslaterError):
                print('test_get_langs -> NoK.')

    def test_detect_lang(self):
        tr = Translater()
        self.assertEqual(type(tr), Translater)
        key = os.environ.get('YANDEX_KEY', False)

        if not key:
            print('no test for detect_lang -> Ok.')
        
        else:
            try:
                tr.set_key(key)
                tr.set_hint('en','ru','ar')
                tr.set_text('Привет Мир')
                result = tr.detect_lang()
                self.assertEqual(isinstance(result, str), True)
                self.assertEqual(result, 'ru')
                print('test_detect_lang -> Ok.')
            except (yandex.Translater.TranslaterBlockedKey, yandex.Translater.TranslaterError):
                print('test_detect_lang -> NoK.')

if __name__ == '__main__':
        unittest.main()

