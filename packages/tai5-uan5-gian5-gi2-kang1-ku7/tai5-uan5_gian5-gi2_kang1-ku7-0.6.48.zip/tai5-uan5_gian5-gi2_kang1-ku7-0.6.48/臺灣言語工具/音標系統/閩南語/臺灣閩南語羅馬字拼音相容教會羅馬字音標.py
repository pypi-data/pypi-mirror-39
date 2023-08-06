# -*- coding: utf-8 -*-
from 臺灣言語工具.音標系統.閩南語.教會系羅馬音標 import 教會系羅馬音標
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音聲母表
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音韻母表
from 臺灣言語工具.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標聲母表
from 臺灣言語工具.音標系統.閩南語.教會羅馬字音標 import 教會羅馬字音標韻母表


class 臺灣閩南語羅馬字拼音相容教會羅馬字音標(教會系羅馬音標):
    聲母表 = 教會羅馬字音標聲母表 | 臺灣閩南語羅馬字拼音聲母表
    韻母表 = 教會羅馬字音標韻母表 | 臺灣閩南語羅馬字拼音韻母表

    def __init__(self, 音標):
        super(臺灣閩南語羅馬字拼音相容教會羅馬字音標, self).__init__()
        self.分析聲韻調(
            音標.replace('hN', 'Nh')
            .replace('ou', 'oo')
            .replace('ooN', 'onn').replace('oonn', 'onn')
        )

    def 轉換到臺灣閩南語羅馬字拼音(self):
        if self.音標 is None:
            return None
        聲母 = None
        if self.聲 == 'ch':
            聲母 = 'ts'
        elif self.聲 == 'chh':
            聲母 = 'tsh'
        else:
            聲母 = self.聲
        韻母 = None
        if self.韻[:2] == 'oa':
            韻母 = 'ua' + self.韻[2:]
        elif self.韻[:2] == 'oe':
            韻母 = 'ue' + self.韻[2:]
        elif self.韻[:2] == 'ou':
            韻母 = 'oo' + self.韻[2:]
        elif self.韻 == 'ek':
            韻母 = 'ik'
        elif self.韻 == 'eng':
            韻母 = 'ing'
        else:
            韻母 = self.韻
        return self.輕 + self.外來語 + 聲母 + 韻母 + str(self.調)
    # 聲 介 韻 調，韻含元音跟韻尾
