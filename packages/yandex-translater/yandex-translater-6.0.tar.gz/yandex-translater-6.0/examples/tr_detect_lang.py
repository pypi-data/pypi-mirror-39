#-*- coding: utf-8 -*-

from yandex.Translater import Translater

tr = Translater()
key = 'yandex_key'

tr.set_key(key)
tr.set_text('Hello Yandex')

print(tr.detect_lang())
