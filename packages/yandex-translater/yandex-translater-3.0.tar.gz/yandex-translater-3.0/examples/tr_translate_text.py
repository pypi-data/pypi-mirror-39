#-*- coding: utf-8 -*-

from yandex.Translater import Translater

tr = Translater()

key = 'yandex_key' 

tr.set_key(key)

tr.set_text('Hello Yandex')

tr.set_from_lang('en')

tr.set_to_lang('ru')


print(tr.translate())

