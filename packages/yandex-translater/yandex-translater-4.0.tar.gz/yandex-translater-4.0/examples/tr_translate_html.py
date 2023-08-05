#-*- coding: utf-8 -*-

from yandex.Translater import Translater

tr = Translate()

key = 'yandex_key' 

tr.set_key(key)

tr.set_text_format('html')

tr.set_text('<p>Hello Yandex</p>')

tr.set_from_lang('en')

tr.set_to_lang('fr')

print(tr.translate())