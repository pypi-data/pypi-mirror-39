#-*- coding: utf-8 -*-

from yandex.Translater import Translater

tr = Translater()

key = 'yandex_key'

tr.set_key(key)

print(' '.join(tr.get_langs()))

