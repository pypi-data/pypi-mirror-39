﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
import datetime
import math
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextAnnotation import TextAnnotation
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.ner.date.internal.MetaDate import MetaDate
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.date.internal.MetaDateRange import MetaDateRange
from pullenti.ner.core.Termin import Termin
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.AnalyzerData import AnalyzerData
from pullenti.ner.Analyzer import Analyzer
from pullenti.ner.core.internal.EpNerCoreInternalResourceHelper import EpNerCoreInternalResourceHelper
from pullenti.ner.date.internal.DateItemToken import DateItemToken
from pullenti.ner.ReferentToken import ReferentToken

class DateAnalyzer(Analyzer):
    """ Семантический анализатор для дат и диапазонов дат """
    
    class DateAnalizerData(AnalyzerData):
        
        def __init__(self) -> None:
            super().__init__()
            self.__m_hash = dict()
        
        @property
        def referents(self) -> typing.List['Referent']:
            return self.__m_hash.values()
        
        def registerReferent(self, referent : 'Referent') -> 'Referent':
            key = str(referent)
            wrapdr725 = RefOutArgWrapper(None)
            inoutres726 = Utils.tryGetValue(self.__m_hash, key, wrapdr725)
            dr = wrapdr725.value
            if (inoutres726): 
                return dr
            self.__m_hash[key] = referent
            return referent
    
    ANALYZER_NAME = "DATE"
    
    @property
    def name(self) -> str:
        return DateAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Даты"
    
    @property
    def description(self) -> str:
        return "Даты и диапазоны дат"
    
    def clone(self) -> 'Analyzer':
        return DateAnalyzer()
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaDate.GLOBAL_META, MetaDateRange.GLOBAL_META]
    
    @property
    def used_extern_object_types(self) -> typing.List[str]:
        return ["PHONE"]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[MetaDate.DATE_FULL_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("datefull.png")
        res[MetaDate.DATE_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("date.png")
        res[MetaDateRange.DATE_RANGE_IMAGE_ID] = EpNerCoreInternalResourceHelper.getBytes("daterange.png")
        return res
    
    def createReferent(self, type0_ : str) -> 'Referent':
        if (type0_ == DateReferent.OBJ_TYPENAME): 
            return DateReferent()
        if (type0_ == DateRangeReferent.OBJ_TYPENAME): 
            return DateRangeReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 10
    
    def createAnalyzerData(self) -> 'AnalyzerData':
        return DateAnalyzer.DateAnalizerData()
    
    def process(self, kit : 'AnalysisKit') -> None:
        """ Основная функция выделения дат
        
        Args:
            cnt: 
            stage: 
        
        """
        ad = Utils.asObjectOrNull(kit.getAnalyzerData(self), DateAnalyzer.DateAnalizerData)
        t = kit.first_token
        first_pass2831 = True
        while True:
            if first_pass2831: first_pass2831 = False
            else: t = t.next0_
            if (not (t is not None)): break
            pli = DateItemToken.tryAttachList(t, 20)
            if (pli is None or len(pli) == 0): 
                continue
            high = False
            tt = t.previous
            first_pass2832 = True
            while True:
                if first_pass2832: first_pass2832 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.isValue("ДАТА", None) or tt.isValue("DATE", None)): 
                    high = True
                    break
                if (tt.isChar(':') or tt.is_hiphen): 
                    continue
                if (isinstance(tt.getReferent(), DateReferent)): 
                    high = True
                    break
                if (not ((isinstance(tt, TextToken)))): 
                    break
                if (not ((tt.morph.case_.is_genitive))): 
                    break
            rts = self.__tryAttach(pli, high)
            if (rts is not None): 
                dat = None
                hi = None
                i = 0
                while i < len(rts): 
                    rt = rts[i]
                    if (isinstance(rt.referent, DateRangeReferent)): 
                        dr = Utils.asObjectOrNull(rt.referent, DateRangeReferent)
                        if (dr.date_from is not None): 
                            dr.date_from = Utils.asObjectOrNull(ad.registerReferent(dr.date_from), DateReferent)
                        if (dr.date_to is not None): 
                            dr.date_to = Utils.asObjectOrNull(ad.registerReferent(dr.date_to), DateReferent)
                        rt.referent = ad.registerReferent(rt.referent)
                        if (rt.begin_token.previous is not None and rt.begin_token.previous.isValue("ПЕРИОД", None)): 
                            rt.begin_token = rt.begin_token.previous
                        kit.embedToken(rt)
                        t = (rt)
                        break
                    dt = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if (dt.higher is not None): 
                        dt.higher = Utils.asObjectOrNull(ad.registerReferent(dt.higher), DateReferent)
                    rt.referent = ad.registerReferent(dt)
                    hi = (Utils.asObjectOrNull(rt.referent, DateReferent))
                    if ((i < (len(rts) - 1)) and rt.tag is None): 
                        rt.referent.addOccurence(TextAnnotation._new727(kit.sofa, rt.begin_char, rt.end_char, rt.referent))
                    else: 
                        dat = (Utils.asObjectOrNull(rt.referent, DateReferent))
                        kit.embedToken(rt)
                        t = (rt)
                        j = i + 1
                        while j < len(rts): 
                            if (rts[j].begin_char == t.begin_char): 
                                rts[j].begin_token = t
                            if (rts[j].end_char == t.end_char): 
                                rts[j].end_token = t
                            j += 1
                    i += 1
                if ((dat is not None and t.previous is not None and t.previous.is_hiphen) and t.previous.previous is not None and (isinstance(t.previous.previous.getReferent(), DateReferent))): 
                    dat0 = Utils.asObjectOrNull(t.previous.previous.getReferent(), DateReferent)
                    dr = Utils.asObjectOrNull(ad.registerReferent(DateRangeReferent._new728(dat0, dat)), DateRangeReferent)
                    diap = ReferentToken(dr, t.previous.previous, t)
                    kit.embedToken(diap)
                    t = (diap)
                    continue
                if ((dat is not None and t.previous is not None and ((t.previous.is_hiphen or t.previous.isValue("ПО", None) or t.previous.isValue("И", None)))) and (isinstance(t.previous.previous, NumberToken))): 
                    t0 = t.previous.previous
                    dat0 = None
                    num = (t0).value
                    if (dat.day > 0 and (num < dat.day) and num > 0): 
                        if (dat.higher is not None): 
                            dat0 = DateReferent._new729(dat.higher, num)
                        elif (dat.month > 0): 
                            dat0 = DateReferent._new730(dat.month, num)
                    elif (dat.year > 0 and (num < dat.year) and num > 1000): 
                        dat0 = DateReferent._new731(num)
                    if (dat0 is not None): 
                        rt0 = ReferentToken(ad.registerReferent(dat0), t0, t0)
                        kit.embedToken(rt0)
                        if (not t.previous.is_hiphen): 
                            continue
                        dat0 = (Utils.asObjectOrNull(rt0.referent, DateReferent))
                        dr = Utils.asObjectOrNull(ad.registerReferent(DateRangeReferent._new728(dat0, dat)), DateRangeReferent)
                        diap = ReferentToken(dr, rt0, t)
                        if (diap.begin_token.previous is not None and diap.begin_token.previous.isValue("С", None)): 
                            diap.begin_token = diap.begin_token.previous
                        kit.embedToken(diap)
                        t = (diap)
                        continue
                continue
            t = pli[len(pli) - 1].end_token
        self.__applyDateRange0(kit, ad)
    
    def _processReferent(self, begin : 'Token', end : 'Token') -> 'ReferentToken':
        if (begin is None): 
            return None
        if (begin.isValue("ДО", None) and (isinstance(begin.next0_, ReferentToken)) and (isinstance(begin.next0_.getReferent(), DateReferent))): 
            drr = DateRangeReferent._new733(Utils.asObjectOrNull(begin.next0_.getReferent(), DateReferent))
            res1 = ReferentToken(drr, begin, begin.next0_)
            res1.data = (Utils.asObjectOrNull(begin.kit.getAnalyzerData(self), DateAnalyzer.DateAnalizerData))
            return res1
        pli = DateItemToken.tryAttachList(begin, 20)
        if (end is not None and pli is not None): 
            i = 0
            while i < len(pli): 
                if (pli[i].begin_char > end.end_char): 
                    del pli[i:i+len(pli) - i]
                    break
                i += 1
        if (pli is None or len(pli) == 0): 
            return None
        rts = self.__tryAttach(pli, True)
        if (rts is None or len(rts) == 0): 
            return None
        ad = Utils.asObjectOrNull(begin.kit.getAnalyzerData(self), DateAnalyzer.DateAnalizerData)
        res = rts[len(rts) - 1]
        i = 0
        while i < (len(rts) - 1): 
            if ((isinstance(res.referent, DateReferent)) and (isinstance(rts[i].referent, DateReferent))): 
                res.referent.mergeSlots(rts[i].referent, True)
            else: 
                rts[i].data = (ad)
            i += 1
        res.referent.addSlot(DateReferent.ATTR_HIGHER, None, True, 0)
        res.data = (ad)
        return res
    
    def __tryAttach(self, dts : typing.List['DateItemToken'], high : bool) -> typing.List['ReferentToken']:
        if (dts is None or len(dts) == 0): 
            return None
        if ((dts[0].can_be_hour and len(dts) > 2 and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[2].int_value >= 0 and (dts[2].int_value < 60)): 
            if (dts[0].typ == DateItemToken.DateItemType.HOUR or ((dts[0].typ == DateItemToken.DateItemType.NUMBER and ((dts[2].typ == DateItemToken.DateItemType.HOUR or dts[2].typ == DateItemToken.DateItemType.NUMBER))))): 
                if (len(dts) > 3 and dts[3].typ == DateItemToken.DateItemType.DELIM and dts[3].string_value == dts[1].string_value): 
                    pass
                else: 
                    dts1 = list(dts)
                    del dts1[0:0+3]
                    res1 = self.__tryAttach(dts1, False)
                    if (res1 is not None and (isinstance(res1[len(res1) - 1].referent, DateReferent)) and (res1[len(res1) - 1].referent).day > 0): 
                        time = DateReferent._new734(dts[0].int_value, dts[2].int_value)
                        time.higher = Utils.asObjectOrNull(res1[len(res1) - 1].referent, DateReferent)
                        res1.append(ReferentToken(time, dts[0].begin_token, res1[len(res1) - 1].end_token))
                        return res1
        cent = None
        point = None
        year_is_dif = False
        b = False
        wrapyear779 = RefOutArgWrapper(None)
        wrapmon780 = RefOutArgWrapper(None)
        wrapday781 = RefOutArgWrapper(None)
        b = self.__applyRuleFormal(dts, high, wrapyear779, wrapmon780, wrapday781)
        year = wrapyear779.value
        mon = wrapmon780.value
        day = wrapday781.value
        if (b): 
            tt = dts[0].begin_token.previous
            if (tt is not None): 
                if (tt.isValue("№", None) or tt.isValue("N", None)): 
                    b = False
        if (dts[0].typ == DateItemToken.DateItemType.CENTURY): 
            cent = dts[0]
            b = True
        if (len(dts) == 1 and dts[0].typ == DateItemToken.DateItemType.POINTER and dts[0].string_value == "сегодня"): 
            res0 = list()
            res0.append(ReferentToken(DateReferent._new735(DatePointerType.TODAY), dts[0].begin_token, dts[0].end_token))
            return res0
        if (len(dts) == 1 and dts[0].typ == DateItemToken.DateItemType.YEAR and dts[0].year <= 0): 
            res0 = list()
            res0.append(ReferentToken(DateReferent._new735(DatePointerType.UNDEFINED), dts[0].begin_token, dts[0].end_token))
            return res0
        if (not b and dts[0].typ == DateItemToken.DateItemType.POINTER and len(dts) > 1): 
            if (dts[1].typ == DateItemToken.DateItemType.YEAR): 
                year = dts[1]
                point = dts[0]
                b = True
            elif (dts[1].typ == DateItemToken.DateItemType.CENTURY): 
                cent = dts[1]
                point = dts[0]
                b = True
            elif (dts[1].typ == DateItemToken.DateItemType.MONTH): 
                mon = dts[1]
                point = dts[0]
                if (len(dts) > 2 and ((dts[2].typ == DateItemToken.DateItemType.YEAR or dts[2].can_be_year))): 
                    year = dts[2]
                b = True
        if (not b): 
            wrapyear737 = RefOutArgWrapper(None)
            wrapmon738 = RefOutArgWrapper(None)
            wrapday739 = RefOutArgWrapper(None)
            wrapyear_is_dif740 = RefOutArgWrapper(False)
            b = self.__applyRuleWithMonth(dts, high, wrapyear737, wrapmon738, wrapday739, wrapyear_is_dif740)
            year = wrapyear737.value
            mon = wrapmon738.value
            day = wrapday739.value
            year_is_dif = wrapyear_is_dif740.value
        if (not b): 
            wrapyear741 = RefOutArgWrapper(None)
            wrapmon742 = RefOutArgWrapper(None)
            wrapday743 = RefOutArgWrapper(None)
            b = self.__applyRuleYearOnly(dts, wrapyear741, wrapmon742, wrapday743)
            year = wrapyear741.value
            mon = wrapmon742.value
            day = wrapday743.value
        if (not b): 
            if (len(dts) == 2 and dts[0].typ == DateItemToken.DateItemType.HOUR and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
                t00 = dts[0].begin_token.previous
                if (t00 is not None and (((t00.isValue("ТЕЧЕНИЕ", None) or t00.isValue("ПРОТЯГОМ", None) or t00.isValue("ЧЕРЕЗ", None)) or t00.isValue("ТЕЧІЮ", None)))): 
                    pass
                else: 
                    res0 = list()
                    time = DateReferent._new734(dts[0].int_value, dts[1].int_value)
                    res0.append(ReferentToken(time, dts[0].begin_token, dts[1].end_token))
                    cou = 0
                    tt = dts[0].begin_token.previous
                    while tt is not None and (cou < 1000): 
                        if (isinstance(tt.getReferent(), DateReferent)): 
                            dr = Utils.asObjectOrNull(tt.getReferent(), DateReferent)
                            if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                                dr = dr.higher
                            if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is not None): 
                                time.higher = dr
                                break
                        tt = tt.previous; cou += 1
                    return res0
            if ((len(dts) == 4 and dts[0].typ == DateItemToken.DateItemType.MONTH and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[2].typ == DateItemToken.DateItemType.MONTH and dts[3].typ == DateItemToken.DateItemType.YEAR): 
                res0 = list()
                yea = DateReferent._new731(dts[3].int_value)
                res0.append(ReferentToken._new746(yea, dts[3].begin_token, dts[3].end_token, dts[3].morph))
                mon1 = DateReferent._new747(dts[0].int_value, yea)
                res0.append(ReferentToken._new748(mon1, dts[0].begin_token, dts[0].end_token, mon1))
                mon2 = DateReferent._new747(dts[2].int_value, yea)
                res0.append(ReferentToken(mon2, dts[2].begin_token, dts[3].end_token))
                return res0
            if (((len(dts) >= 4 and dts[0].typ == DateItemToken.DateItemType.NUMBER and dts[0].can_be_day) and dts[1].typ == DateItemToken.DateItemType.DELIM and dts[2].typ == DateItemToken.DateItemType.NUMBER) and dts[2].can_be_day and dts[3].typ == DateItemToken.DateItemType.MONTH): 
                if (len(dts) == 4 or ((len(dts) == 5 and dts[4].can_be_year))): 
                    res0 = list()
                    yea = None
                    if (len(dts) == 5): 
                        yea = DateReferent._new731(dts[4].year)
                        res0.append(ReferentToken(yea, dts[4].begin_token, dts[4].end_token))
                    mo = DateReferent._new747(dts[3].int_value, yea)
                    res0.append(ReferentToken(mo, dts[3].begin_token, dts[len(dts) - 1].end_token))
                    da1 = DateReferent._new752(dts[0].int_value, mo)
                    res0.append(ReferentToken(da1, dts[0].begin_token, dts[0].end_token))
                    da2 = DateReferent._new752(dts[2].int_value, mo)
                    res0.append(ReferentToken(da2, dts[2].begin_token, dts[len(dts) - 1].end_token))
                    dr = DateRangeReferent()
                    dr.date_from = da1
                    dr.date_to = da2
                    res0.append(ReferentToken(dr, dts[0].begin_token, dts[len(dts) - 1].end_token))
                    return res0
            if ((dts[0].typ == DateItemToken.DateItemType.MONTH and len(dts) == 1 and dts[0].end_token.next0_ is not None) and ((dts[0].end_token.next0_.is_hiphen or dts[0].end_token.next0_.isValue("ПО", None) or dts[0].end_token.next0_.isValue("НА", None)))): 
                rt = dts[0].kit.processReferent(DateAnalyzer.ANALYZER_NAME, dts[0].end_token.next0_.next0_)
                if (rt is not None): 
                    dr0 = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if ((dr0 is not None and dr0.year > 0 and dr0.month > 0) and dr0.day == 0 and dr0.month > dts[0].int_value): 
                        dr_year0 = DateReferent._new731(dr0.year)
                        res0 = list()
                        res0.append(ReferentToken(dr_year0, dts[0].end_token, dts[0].end_token))
                        dr_mon0 = DateReferent._new747(dts[0].int_value, dr_year0)
                        res0.append(ReferentToken(dr_mon0, dts[0].begin_token, dts[0].end_token))
                        return res0
            if (((len(dts) == 3 and dts[1].typ == DateItemToken.DateItemType.DELIM and dts[1].begin_token.is_hiphen) and dts[0].can_be_year and dts[2].can_be_year) and (dts[0].int_value < dts[2].int_value)): 
                ok = False
                if (dts[2].typ == DateItemToken.DateItemType.YEAR): 
                    ok = True
                elif (dts[0].length_char == 4 and dts[2].length_char == 4 and dts[0].begin_token.previous is not None): 
                    tt0 = dts[0].begin_token.previous
                    if (tt0.isChar('(') and dts[2].end_token.next0_ is not None and dts[2].end_token.next0_.isChar(')')): 
                        ok = True
                    elif (tt0.isValue("IN", None) or tt0.isValue("SINCE", None) or tt0.isValue("В", "У")): 
                        ok = True
                if (ok): 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new731(dts[0].year), dts[0].begin_token, dts[0].end_token))
                    res0.append(ReferentToken(DateReferent._new731(dts[2].year), dts[2].begin_token, dts[2].end_token))
                    return res0
            if (len(dts) > 1 and dts[0].typ == DateItemToken.DateItemType.YEAR): 
                res0 = list()
                res0.append(ReferentToken(DateReferent._new731(dts[0].year), dts[0].begin_token, dts[0].end_token))
                return res0
            if (high): 
                if (len(dts) == 1 and dts[0].can_be_year and dts[0].typ == DateItemToken.DateItemType.NUMBER): 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new731(dts[0].year), dts[0].begin_token, dts[0].end_token))
                    return res0
                if ((((len(dts) == 3 and dts[0].can_be_year and dts[0].typ == DateItemToken.DateItemType.NUMBER) and dts[2].can_be_year and dts[2].typ == DateItemToken.DateItemType.NUMBER) and (dts[0].year < dts[2].year) and dts[1].typ == DateItemToken.DateItemType.DELIM) and dts[1].begin_token.is_hiphen): 
                    res0 = list()
                    y1 = DateReferent._new731(dts[0].year)
                    res0.append(ReferentToken(y1, dts[0].begin_token, dts[0].end_token))
                    y2 = DateReferent._new731(dts[2].year)
                    res0.append(ReferentToken(y1, dts[2].begin_token, dts[2].end_token))
                    ra = DateRangeReferent._new728(y1, y2)
                    res0.append(ReferentToken(ra, dts[0].begin_token, dts[2].end_token))
                    return res0
            if (dts[0].typ == DateItemToken.DateItemType.QUARTAL or dts[0].typ == DateItemToken.DateItemType.HALFYEAR): 
                if (len(dts) == 1 or dts[1].typ == DateItemToken.DateItemType.YEAR): 
                    res0 = list()
                    ii = 0
                    yea = None
                    if (len(dts) > 1): 
                        ii = 1
                        yea = DateReferent._new731(dts[1].int_value)
                        res0.append(ReferentToken._new746(yea, dts[1].begin_token, dts[1].end_token, dts[1].morph))
                    else: 
                        cou = 0
                        tt = dts[0].begin_token
                        while tt is not None: 
                            cou += 1
                            if ((cou) > 200): 
                                break
                            if (isinstance(tt, ReferentToken)): 
                                yea = DateAnalyzer.__findYear_(tt.getReferent())
                                if ((yea) is not None): 
                                    break
                            if (tt.is_newline_before): 
                                break
                            tt = tt.previous
                    if (yea is None): 
                        return None
                    m1 = 0
                    m2 = 0
                    if (dts[0].typ == DateItemToken.DateItemType.HALFYEAR): 
                        if (dts[0].int_value == 1): 
                            m1 = 1
                            m2 = 6
                        elif (dts[0].int_value == 2): 
                            m1 = 7
                            m2 = 12
                        else: 
                            return None
                    elif (dts[0].typ == DateItemToken.DateItemType.QUARTAL): 
                        if (dts[0].int_value == 1): 
                            m1 = 1
                            m2 = 3
                        elif (dts[0].int_value == 2): 
                            m1 = 4
                            m2 = 6
                        elif (dts[0].int_value == 3): 
                            m1 = 7
                            m2 = 9
                        elif (dts[0].int_value == 4): 
                            m1 = 10
                            m2 = 12
                        else: 
                            return None
                    else: 
                        return None
                    mon1 = DateReferent._new747(m1, yea)
                    res0.append(ReferentToken(mon1, dts[0].begin_token, dts[0].begin_token))
                    mon2 = DateReferent._new747(m2, yea)
                    res0.append(ReferentToken(mon2, dts[0].end_token, dts[0].end_token))
                    dr = DateRangeReferent()
                    dr.date_from = mon1
                    dr.date_to = mon2
                    res0.append(ReferentToken(dr, dts[0].begin_token, dts[ii].end_token))
                    return res0
            if ((len(dts) == 3 and dts[1].typ == DateItemToken.DateItemType.DELIM and ((dts[1].string_value == "." or dts[1].string_value == ":"))) and dts[0].can_be_hour and dts[2].can_be_minute): 
                ok = False
                if (dts[0].begin_token.previous is not None and dts[0].begin_token.previous.isValue("В", None)): 
                    ok = True
                if (ok): 
                    time = DateReferent._new734(dts[0].int_value, dts[2].int_value)
                    cou = 0
                    tt = dts[0].begin_token.previous
                    while tt is not None and (cou < 1000): 
                        if (isinstance(tt.getReferent(), DateReferent)): 
                            dr = Utils.asObjectOrNull(tt.getReferent(), DateReferent)
                            if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                                dr = dr.higher
                            if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is not None): 
                                time.higher = dr
                                break
                        tt = tt.previous; cou += 1
                    tt1 = dts[2].end_token
                    if (tt1.next0_ is not None and tt1.next0_.isValue("ЧАС", None)): 
                        tt1 = tt1.next0_
                        dtsli = DateItemToken.tryAttachList(tt1.next0_, 20)
                        if (dtsli is not None): 
                            res1 = self.__tryAttach(dtsli, True)
                            if (res1 is not None and (res1[len(res1) - 1].referent).day > 0): 
                                time.higher = Utils.asObjectOrNull(res1[len(res1) - 1].referent, DateReferent)
                                res1.append(ReferentToken(time, dts[0].begin_token, tt1))
                                return res1
                    res0 = list()
                    res0.append(ReferentToken(time, dts[0].begin_token, tt1))
                    return res0
            if ((len(dts) == 1 and dts[0].typ == DateItemToken.DateItemType.MONTH and dts[0].begin_token.previous is not None) and dts[0].begin_token.previous.morph.class0_.is_preposition): 
                if (dts[0].chars.is_latin_letter and dts[0].chars.is_all_lower): 
                    pass
                else: 
                    res0 = list()
                    res0.append(ReferentToken(DateReferent._new768(dts[0].int_value), dts[0].begin_token, dts[0].end_token))
                    return res0
            return None
        res = list()
        dr_year = None
        dr_mon = None
        dr_day = None
        t0 = None
        t1 = None
        if (cent is not None): 
            ce = DateReferent._new769((- cent.int_value if cent.new_age < 0 else cent.int_value))
            t1 = cent.end_token
            rt = ReferentToken(ce, cent.begin_token, t1)
            res.append(rt)
        if (year is not None and year.year > 0): 
            dr_year = DateReferent._new731((- year.year if year.new_age < 0 else year.year))
            if (not year_is_dif): 
                t1 = year.end_token
                if (t1.next0_ is not None and t1.next0_.isValue("ГОРОД", None)): 
                    tt2 = t1.next0_.next0_
                    if (tt2 is None): 
                        t1 = t1.next0_
                        year.end_token = t1
                    elif ((tt2.whitespaces_before_count < 3) and ((tt2.morph.class0_.is_preposition or tt2.chars.is_all_lower))): 
                        t1 = t1.next0_
                        year.end_token = t1
            t0 = year.begin_token
            res.append(ReferentToken._new746(dr_year, t0, year.end_token, year.morph))
        if (mon is not None): 
            dr_mon = DateReferent._new768(mon.int_value)
            if (dr_year is not None): 
                dr_mon.higher = dr_year
            if (t0 is None or (mon.begin_char < t0.begin_char)): 
                t0 = mon.begin_token
            if (t1 is None or mon.end_char > t1.end_char): 
                t1 = mon.end_token
            if (dr_year is None and t1.next0_ is not None and ((t1.next0_.isValue("ПО", None) or t1.next0_.isValue("НА", None)))): 
                rt = t1.kit.processReferent(DateAnalyzer.ANALYZER_NAME, t1.next0_.next0_)
                if (rt is not None): 
                    dr0 = Utils.asObjectOrNull(rt.referent, DateReferent)
                    if (dr0 is not None and dr0.year > 0 and dr0.month > 0): 
                        dr_year = DateReferent._new731(dr0.year)
                        t0 = t1
                        res.append(ReferentToken(dr_year, t0, t1))
                        dr_mon.higher = dr_year
            res.append(ReferentToken._new746(dr_mon, t0, t1, mon.morph))
            if (day is not None): 
                dr_day = DateReferent._new775(day.int_value)
                dr_day.higher = dr_mon
                if (day.begin_char < t0.begin_char): 
                    t0 = day.begin_token
                if (day.end_char > t1.end_char): 
                    t1 = day.end_token
                tt = t0.previous
                while tt is not None: 
                    if (not tt.isCharOf(",.")): 
                        break
                    tt = tt.previous
                dow = DateItemToken.DAYS_OF_WEEK.tryParse(tt, TerminParseAttr.NO)
                if (dow is not None): 
                    t0 = tt
                    dr_day.day_of_week = dow.termin.tag
                res.append(ReferentToken._new746(dr_day, t0, t1, day.morph))
                if (dts[0].typ == DateItemToken.DateItemType.HOUR and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
                    hou = DateReferent._new777(dr_day)
                    hou.hour = dts[0].int_value
                    hou.minute = dts[1].int_value
                    if (dts[2].typ == DateItemToken.DateItemType.SECOND): 
                        hou.second = dts[2].int_value
                    res.append(ReferentToken(hou, dts[0].begin_token, t1))
                    return res
        if (point is not None and len(res) > 0): 
            poi = DateReferent()
            if (point.string_value == "начало"): 
                poi.pointer = DatePointerType.BEGIN
            elif (point.string_value == "середина"): 
                poi.pointer = DatePointerType.CENTER
            elif (point.string_value == "конец"): 
                poi.pointer = DatePointerType.END
            elif (point.int_value != 0): 
                poi.pointer = Utils.valToEnum(point.int_value, DatePointerType)
            poi.higher = Utils.asObjectOrNull(res[len(res) - 1].referent, DateReferent)
            res.append(ReferentToken(poi, point.begin_token, t1))
            return res
        if (dr_day is not None and not year_is_dif): 
            rt = self.__tryAttachTime(t1.next0_, True)
            if (rt is not None): 
                (rt.referent).higher = dr_day
                rt.begin_token = t0
                res.append(rt)
            else: 
                i = 1
                while i < len(dts): 
                    if (t0.begin_char == dts[i].begin_char): 
                        if (i > 2): 
                            del dts[i:i+len(dts) - i]
                            rt = self.__tryAttachTimeLi(dts, True)
                            if (rt is not None): 
                                (rt.referent).higher = dr_day
                                rt.end_token = t1
                                res.append(rt)
                            break
                    i += 1
        if (len(res) == 1): 
            dt0 = Utils.asObjectOrNull(res[0].referent, DateReferent)
            if (dt0.month == 0): 
                tt = res[0].begin_token.previous
                if (tt is not None and tt.isChar('_') and not tt.is_newline_after): 
                    while tt is not None: 
                        if (not tt.isChar('_')): 
                            break
                        else: 
                            res[0].begin_token = tt
                        tt = tt.previous
                    if (BracketHelper.canBeEndOfSequence(tt, True, None, False)): 
                        tt = tt.previous
                        while tt is not None: 
                            if (tt.is_newline_after): 
                                break
                            elif (tt.isChar('_')): 
                                pass
                            else: 
                                if (BracketHelper.canBeStartOfSequence(tt, True, False)): 
                                    res[0].begin_token = tt
                                break
                            tt = tt.previous
                tt = res[0].end_token.next0_
                if (tt is not None and tt.isCharOf("(,")): 
                    dit = DateItemToken.tryAttach(tt.next0_, None)
                    if (dit is not None and dit.typ == DateItemToken.DateItemType.MONTH): 
                        dr_mon = DateReferent._new778(dt0, dit.int_value)
                        pr_mon = ReferentToken(dr_mon, res[0].begin_token, dit.end_token)
                        if (tt.isChar('(') and pr_mon.end_token.next0_ is not None and pr_mon.end_token.next0_.isChar(')')): 
                            pr_mon.end_token = pr_mon.end_token.next0_
                        res.append(pr_mon)
        if (len(res) > 0 and dr_day is not None): 
            la = res[len(res) - 1]
            tt = la.end_token.next0_
            if (tt is not None and tt.isChar(',')): 
                tt = tt.next0_
            tok = DateItemToken.DAYS_OF_WEEK.tryParse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                la.end_token = tok.end_token
                dr_day.day_of_week = tok.termin.tag
        return res
    
    @staticmethod
    def __findYear_(r : 'Referent') -> 'DateReferent':
        dr = Utils.asObjectOrNull(r, DateReferent)
        if (dr is not None): 
            while dr is not None: 
                if (dr.higher is None and dr.year > 0): 
                    return dr
                dr = dr.higher
            return None
        drr = Utils.asObjectOrNull(r, DateRangeReferent)
        if (drr is not None): 
            dr = DateAnalyzer.__findYear_(drr.date_from)
            if ((dr) is not None): 
                return dr
            dr = DateAnalyzer.__findYear_(drr.date_to)
            if ((dr) is not None): 
                return dr
        return None
    
    def __tryAttachTime(self, t : 'Token', after_date : bool) -> 'ReferentToken':
        if (t is None): 
            return None
        if (t.isValue("ГОРОД", None) and t.next0_ is not None): 
            t = t.next0_
        while t is not None and ((t.morph.class0_.is_preposition or t.morph.class0_.is_adverb or t.is_comma)):
            if (t.morph.language.is_ru): 
                if (not t.isValue("ПО", None) and not t.isValue("НА", None)): 
                    t = t.next0_
                else: 
                    break
            else: 
                t = t.next0_
        if (t is None): 
            return None
        dts = DateItemToken.tryAttachList(t, 10)
        return self.__tryAttachTimeLi(dts, after_date)
    
    def __corrTime(self, t0 : 'Token', time : 'DateReferent') -> 'Token':
        t1 = None
        t = t0
        first_pass2833 = True
        while True:
            if first_pass2833: first_pass2833 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not ((isinstance(t, TextToken)))): 
                break
            term = (t).term
            if (term == "МСК"): 
                t1 = t
                continue
            if ((t.isCharOf("(") and t.next0_ is not None and t.next0_.isValue("МСК", None)) and t.next0_.next0_ is not None and t.next0_.next0_.isChar(')')): 
                t = t.next0_.next0_
                t1 = t
                continue
            if ((term == "PM" or term == "РМ" or t.isValue("ВЕЧЕР", "ВЕЧІР")) or t.isValue("ДЕНЬ", None)): 
                if (time.hour < 12): 
                    time.hour = time.hour + 12
                t1 = t
                continue
            if ((term == "AM" or term == "АМ" or term == "Ч") or t.isValue("ЧАС", None)): 
                t1 = t
                continue
            if (t.isChar('+')): 
                ddd = DateItemToken.tryAttachList(t.next0_, 20)
                if ((ddd is not None and len(ddd) == 3 and ddd[0].typ == DateItemToken.DateItemType.NUMBER) and ddd[1].typ == DateItemToken.DateItemType.DELIM and ddd[2].typ == DateItemToken.DateItemType.NUMBER): 
                    t1 = ddd[2].end_token
                    continue
            if (t.isCharOf(",.")): 
                continue
            break
        return t1
    
    def __tryAttachTimeLi(self, dts : typing.List['DateItemToken'], after_date : bool) -> 'ReferentToken':
        if (dts is None or (len(dts) < 1)): 
            return None
        t0 = dts[0].begin_token
        t1 = None
        time = None
        if (len(dts) == 1): 
            if (dts[0].typ == DateItemToken.DateItemType.HOUR and after_date): 
                time = DateReferent._new734(dts[0].int_value, 0)
                t1 = dts[0].end_token
            else: 
                return None
        elif (dts[0].typ == DateItemToken.DateItemType.HOUR and dts[1].typ == DateItemToken.DateItemType.MINUTE): 
            time = DateReferent._new734(dts[0].int_value, dts[1].int_value)
            t1 = dts[1].end_token
            if (len(dts) > 2 and dts[2].typ == DateItemToken.DateItemType.SECOND): 
                t1 = dts[2].end_token
                time.second = dts[2].int_value
        elif ((((len(dts) > 2 and dts[0].typ == DateItemToken.DateItemType.NUMBER and dts[1].typ == DateItemToken.DateItemType.DELIM) and ((dts[1].string_value == ":" or dts[1].string_value == "." or dts[1].string_value == "-")) and dts[2].typ == DateItemToken.DateItemType.NUMBER) and (dts[0].int_value < 24) and (dts[2].int_value < 60)) and dts[2].length_char == 2 and after_date): 
            time = DateReferent._new734(dts[0].int_value, dts[2].int_value)
            t1 = dts[2].end_token
            if ((len(dts) > 4 and dts[3].string_value == dts[1].string_value and dts[4].typ == DateItemToken.DateItemType.NUMBER) and (dts[4].int_value < 60)): 
                time.second = dts[4].int_value
                t1 = dts[4].end_token
        if (time is None): 
            return None
        tt = self.__corrTime(t1.next0_, time)
        if (tt is not None): 
            t1 = tt
        cou = 0
        tt = t0.previous
        while tt is not None and (cou < 1000): 
            if (isinstance(tt.getReferent(), DateReferent)): 
                dr = Utils.asObjectOrNull(tt.getReferent(), DateReferent)
                if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is None and dr.higher is not None): 
                    dr = dr.higher
                if (dr.findSlot(DateReferent.ATTR_DAY, None, True) is not None): 
                    time.higher = dr
                    break
            tt = tt.previous; cou += 1
        if (t1.next0_ is not None): 
            if (t1.next0_.isValue("ЧАС", None)): 
                t1 = t1.next0_
        return ReferentToken(time, t0, t1)
    
    def __applyRuleFormal(self, its : typing.List['DateItemToken'], high : bool, year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken') -> bool:
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        i = 0
        first_pass2834 = True
        while True:
            if first_pass2834: first_pass2834 = False
            else: i += 1
            if (not (i < (len(its) - 4))): break
            if (its[i].begin_token.previous is not None and its[i].begin_token.previous.isChar(')') and (its[i].whitespaces_before_count < 2)): 
                return False
            if (not its[i].can_be_day and not its[i].can_be_year and not its[i].can_by_month): 
                continue
            if (not its[i].is_whitespace_before): 
                if (its[i].begin_token.previous is not None and ((its[i].begin_token.previous.isCharOf("(;,") or its[i].begin_token.previous.morph.class0_.is_preposition or its[i].begin_token.previous.is_table_control_char))): 
                    pass
                else: 
                    continue
            j = i
            first_pass2835 = True
            while True:
                if first_pass2835: first_pass2835 = False
                else: j += 1
                if (not (j < (i + 4))): break
                if (its[j].is_whitespace_after): 
                    if (high and not its[j].is_newline_after): 
                        continue
                    if (i == 0 and len(its) == 5 and ((j == 1 or j == 3))): 
                        if (its[j].whitespaces_after_count < 2): 
                            continue
                    break
            if (j < (i + 4)): 
                continue
            if (its[i + 1].typ != DateItemToken.DateItemType.DELIM or its[i + 3].typ != DateItemToken.DateItemType.DELIM or its[i + 1].string_value != its[i + 3].string_value): 
                continue
            j = (i + 5)
            if ((j < len(its)) and not its[j].is_whitespace_before): 
                if (its[j].typ == DateItemToken.DateItemType.DELIM and its[j].is_whitespace_after): 
                    pass
                else: 
                    continue
            mon.value = (its[i + 2] if its[i + 2].can_by_month else None)
            if (not its[i].can_be_day): 
                if (not its[i].can_be_year): 
                    continue
                year.value = its[i]
                if (mon.value is not None and its[i + 4].can_be_day): 
                    day.value = its[i + 4]
                elif (its[i + 2].can_be_day and its[i + 4].can_by_month): 
                    day.value = its[i + 2]
                    mon.value = its[i + 4]
                else: 
                    continue
            elif (not its[i].can_be_year): 
                if (not its[i + 4].can_be_year): 
                    if (not high): 
                        continue
                year.value = its[i + 4]
                if (mon.value is not None and its[i].can_be_day): 
                    day.value = its[i]
                elif (its[i].can_by_month and its[i + 2].can_be_day): 
                    mon.value = its[i]
                    day.value = its[i + 2]
                else: 
                    continue
            else: 
                continue
            if ((mon.value.int_value < 10) and not mon.value.is_zero_headed): 
                if (year.value.int_value < 1980): 
                    continue
            delim = its[i + 1].string_value[0]
            if ((delim != '/' and delim != '\\' and delim != '.') and delim != '-'): 
                continue
            if (delim == '.' or delim == '-'): 
                if (year.value == its[i] and (year.value.int_value < 1900)): 
                    continue
            if ((i + 5) < len(its)): 
                del its[i + 5:i + 5+len(its) - i - 5]
            if (i > 0): 
                del its[0:0+i]
            return True
        if (len(its) >= 5 and its[0].is_whitespace_before and its[4].is_whitespace_after): 
            if (its[1].typ == DateItemToken.DateItemType.DELIM and its[2].typ == DateItemToken.DateItemType.DELIM): 
                if (its[0].length_char == 2 and its[2].length_char == 2 and ((its[4].length_char == 2 or its[4].length_char == 4))): 
                    if (its[0].can_be_day and its[2].can_by_month and its[4].typ == DateItemToken.DateItemType.NUMBER): 
                        if ((not its[0].is_whitespace_after and not its[1].is_whitespace_after and not its[2].is_whitespace_after) and not its[3].is_whitespace_after): 
                            iyear = 0
                            y = its[4].int_value
                            if (y > 80 and (y < 100)): 
                                iyear = (1900 + y)
                            elif (y <= (Utils.getDate(datetime.datetime.today()).year - 2000)): 
                                iyear = (y + 2000)
                            else: 
                                return False
                            its[4].year = iyear
                            year.value = its[4]
                            mon.value = its[2]
                            day.value = its[0]
                            return True
        if (high and its[0].can_be_year and len(its) == 1): 
            year.value = its[0]
            return True
        if (its[0].begin_token.previous is not None and its[0].begin_token.previous.isValue("ОТ", None) and len(its) == 4): 
            if (its[0].can_be_day and its[3].can_be_year): 
                if (its[1].typ == DateItemToken.DateItemType.DELIM and its[2].can_by_month): 
                    year.value = its[3]
                    mon.value = its[2]
                    day.value = its[0]
                    return True
                if (its[2].typ == DateItemToken.DateItemType.DELIM and its[1].can_by_month): 
                    year.value = its[3]
                    mon.value = its[1]
                    day.value = its[0]
                    return True
        if ((len(its) == 3 and its[0].typ == DateItemToken.DateItemType.NUMBER and its[0].can_be_day) and its[2].typ == DateItemToken.DateItemType.YEAR and its[1].can_by_month): 
            if (BracketHelper.isBracket(its[0].begin_token, False) and BracketHelper.isBracket(its[0].end_token, False)): 
                year.value = its[2]
                mon.value = its[1]
                day.value = its[0]
                return True
        return False
    
    def __applyRuleWithMonth(self, its : typing.List['DateItemToken'], high : bool, year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken', year_is_diff : bool) -> bool:
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        year_is_diff.value = False
        if (len(its) == 2): 
            if (its[0].typ == DateItemToken.DateItemType.MONTH and its[1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[1]
                mon.value = its[0]
                return True
            if (its[0].can_be_day and its[1].typ == DateItemToken.DateItemType.MONTH): 
                mon.value = its[1]
                day.value = its[0]
                return True
        i = 0
        while i < len(its): 
            if (its[i].typ == DateItemToken.DateItemType.MONTH): 
                break
            i += 1
        if (i >= len(its)): 
            return False
        lang = its[i].lang
        year.value = (None)
        day.value = (None)
        mon.value = its[i]
        i0 = i
        i1 = i
        year_val = 0
        if ((((lang) & ((((MorphLang.RU) | MorphLang.IT | MorphLang.BY) | MorphLang.UA)))) != MorphLang.UNKNOWN): 
            if (((i + 1) < len(its)) and its[i + 1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[i + 1]
                i1 = (i + 1)
                if (i > 0 and its[i - 1].can_be_day): 
                    day.value = its[i - 1]
                    i0 = (i - 1)
            elif (i > 0 and its[i - 1].typ == DateItemToken.DateItemType.YEAR): 
                year.value = its[i - 1]
                i0 = (i - 1)
                if (((i + 1) < len(its)) and its[i + 1].can_be_day): 
                    day.value = its[i + 1]
                    i1 = (i + 1)
            elif (((i + 1) < len(its)) and its[i + 1].can_be_year): 
                year.value = its[i + 1]
                i1 = (i + 1)
                if (i > 0 and its[i - 1].can_be_day): 
                    day.value = its[i - 1]
                    i0 = (i - 1)
            elif ((i == 0 and its[0].typ == DateItemToken.DateItemType.MONTH and len(its) == 3) and its[i + 1].typ == DateItemToken.DateItemType.DELIM and its[i + 2].can_be_year): 
                year.value = its[i + 2]
                i1 = (i + 2)
            elif (i > 1 and its[i - 2].can_be_year and its[i - 1].can_be_day): 
                year.value = its[i - 2]
                day.value = its[i - 1]
                i0 = (i - 2)
            elif (i > 0 and its[i - 1].can_be_year): 
                year.value = its[i - 1]
                i0 = (i - 1)
                if (((i + 1) < len(its)) and its[i + 1].can_be_day): 
                    day.value = its[i + 1]
                    i1 = (i + 1)
            if (year.value is None and i == 1 and its[i - 1].can_be_day): 
                j = i + 1
                while j < len(its): 
                    if (its[j].typ == DateItemToken.DateItemType.DELIM): 
                        j += 1
                        if ((j) >= len(its)): 
                            break
                    if (its[j].typ == DateItemToken.DateItemType.YEAR): 
                        year.value = its[j]
                        day.value = its[i - 1]
                        i0 = (i - 1)
                        i1 = i
                        year_is_diff.value = True
                        break
                    if (not its[j].can_be_day): 
                        break
                    j += 1
                    if ((j) >= len(its)): 
                        break
                    if (its[j].typ != DateItemToken.DateItemType.MONTH): 
                        break
                    j += 1
        elif (lang == MorphLang.EN): 
            if (i == 1 and its[0].can_be_day): 
                i1 = 2
                day.value = its[0]
                i0 = 0
                if ((i1 < len(its)) and its[i1].typ == DateItemToken.DateItemType.DELIM): 
                    i1 += 1
                if ((i1 < len(its)) and its[i1].can_be_year): 
                    year.value = its[i1]
                if (year.value is None): 
                    i1 = 1
                    year_val = self.__findYear(its[0].begin_token)
            elif (i == 0): 
                if (len(its) > 1 and its[1].can_be_year and not its[1].can_be_day): 
                    i1 = 2
                    year.value = its[1]
                elif (len(its) > 1 and its[1].can_be_day): 
                    day.value = its[1]
                    i1 = 2
                    if ((i1 < len(its)) and its[i1].typ == DateItemToken.DateItemType.DELIM): 
                        i1 += 1
                    if ((i1 < len(its)) and its[i1].can_be_year): 
                        year.value = its[i1]
                    if (year.value is None): 
                        i1 = 1
                        year_val = self.__findYear(its[0].begin_token)
        if (year.value is None and year_val == 0 and len(its) == 3): 
            if (its[0].typ == DateItemToken.DateItemType.YEAR and its[1].can_be_day and its[2].typ == DateItemToken.DateItemType.MONTH): 
                i1 = 2
                year.value = its[0]
                day.value = its[1]
        if (year.value is not None or year_val > 0): 
            return True
        if (day.value is not None and len(its) == 2): 
            return True
        return False
    
    def __findYear(self, t : 'Token') -> int:
        year = 0
        prevdist = 0
        tt = t
        while tt is not None: 
            if (tt.is_newline_before): 
                prevdist += 10
            prevdist += 1
            if (isinstance(tt, ReferentToken)): 
                if (isinstance((tt).referent, DateReferent)): 
                    year = ((tt).referent).year
                    break
            tt = tt.previous
        dist = 0
        tt = t
        while tt is not None: 
            if (tt.is_newline_after): 
                dist += 10
            dist += 1
            if (isinstance(tt, ReferentToken)): 
                if (isinstance((tt).referent, DateReferent)): 
                    if (year > 0 and (prevdist < dist)): 
                        return year
                    else: 
                        return ((tt).referent).year
            tt = tt.next0_
        return year
    
    def __applyRuleYearOnly(self, its : typing.List['DateItemToken'], year : 'DateItemToken', mon : 'DateItemToken', day : 'DateItemToken') -> bool:
        year.value = (None)
        mon.value = (None)
        day.value = (None)
        doubt = False
        i = 0
        while i < len(its): 
            if (its[i].typ == DateItemToken.DateItemType.YEAR): 
                break
            elif (its[i].typ == DateItemToken.DateItemType.NUMBER): 
                doubt = True
            elif (its[i].typ != DateItemToken.DateItemType.DELIM): 
                return False
            i += 1
        if (i >= len(its)): 
            if (((len(its) == 1 and its[0].can_be_year and its[0].int_value > 1900) and its[0].can_be_year and (its[0].int_value < 2100)) and its[0].begin_token.previous is not None): 
                if (((its[0].begin_token.previous.isValue("В", None) or its[0].begin_token.previous.isValue("У", None) or its[0].begin_token.previous.isValue("З", None)) or its[0].begin_token.previous.isValue("IN", None) or its[0].begin_token.previous.isValue("SINCE", None))): 
                    if (its[0].length_char == 4 or its[0].begin_token.morph.class0_.is_adjective): 
                        year.value = its[0]
                        return True
            return False
        if ((i + 1) == len(its)): 
            if (its[i].int_value > 1900 or its[i].new_age != 0): 
                year.value = its[i]
                return True
            if (doubt): 
                return False
            if (its[i].int_value > 10 and (its[i].int_value < 100)): 
                if (its[i].begin_token.previous is not None): 
                    if (its[i].begin_token.previous.isValue("В", None) or its[i].begin_token.previous.isValue("IN", None) or its[i].begin_token.previous.isValue("У", None)): 
                        year.value = its[i]
                        return True
                if (its[i].begin_token.isValue("В", None) or its[i].begin_token.isValue("У", None) or its[i].begin_token.isValue("IN", None)): 
                    year.value = its[i]
                    return True
            if (its[i].int_value >= 100): 
                year.value = its[i]
                return True
            return False
        if (len(its) == 1 and its[0].typ == DateItemToken.DateItemType.YEAR and its[0].year <= 0): 
            year.value = its[0]
            return True
        if (((len(its) > 2 and its[0].can_be_year and its[1].typ == DateItemToken.DateItemType.DELIM) and its[1].begin_token.is_hiphen and its[2].typ == DateItemToken.DateItemType.YEAR) and (its[0].year0 < its[2].year0)): 
            year.value = its[0]
            return True
        if (its[0].typ == DateItemToken.DateItemType.YEAR): 
            if ((its[0].begin_token.previous is not None and its[0].begin_token.previous.is_hiphen and (isinstance(its[0].begin_token.previous.previous, ReferentToken))) and (isinstance(its[0].begin_token.previous.previous.getReferent(), DateReferent))): 
                year.value = its[0]
                return True
        return False
    
    def __applyDateRange(self, ad : 'AnalyzerData', its : typing.List['DateItemToken'], lang : 'MorphLang') -> 'DateRangeReferent':
        lang.value = MorphLang()
        if (its is None or (len(its) < 3)): 
            return None
        if ((its[0].can_be_year and its[1].string_value == "-" and its[2].typ == DateItemToken.DateItemType.YEAR) and (its[0].year < its[2].year)): 
            res = DateRangeReferent()
            res.date_from = Utils.asObjectOrNull(ad.registerReferent(DateReferent._new731(its[0].year)), DateReferent)
            rt1 = ReferentToken(res.date_from, its[0].begin_token, its[0].end_token)
            res.date_to = Utils.asObjectOrNull(ad.registerReferent(DateReferent._new731(its[2].year)), DateReferent)
            rt2 = ReferentToken(res.date_to, its[2].begin_token, its[2].end_token)
            lang.value = its[2].lang
            return res
        return None
    
    def __applyDateRange0(self, kit : 'AnalysisKit', ad : 'AnalyzerData') -> None:
        t = kit.first_token
        first_pass2836 = True
        while True:
            if first_pass2836: first_pass2836 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (not ((isinstance(t, TextToken)))): 
                continue
            year_val1 = 0
            year_val2 = 0
            date1 = None
            date2 = None
            lang = MorphLang()
            t0 = t.next0_
            str0_ = (t).term
            if (str0_ == "ON" and (isinstance(t0, TextToken))): 
                tok = DateItemToken.DAYS_OF_WEEK.tryParse(t0, TerminParseAttr.NO)
                if (tok is not None): 
                    dow = DateReferent._new787(tok.termin.tag)
                    rtd = ReferentToken(ad.registerReferent(dow), t, tok.end_token)
                    kit.embedToken(rtd)
                    t = (rtd)
                    continue
            if (str0_ == "С" or str0_ == "C"): 
                lang = MorphLang.RU
            elif (str0_ == "З"): 
                lang = MorphLang.UA
            elif (str0_ == "BETWEEN"): 
                lang = MorphLang.EN
            elif (str0_ == "IN"): 
                lang = MorphLang.EN
                if ((t0 is not None and t0.isValue("THE", None) and t0.next0_ is not None) and t0.next0_.isValue("PERIOD", None)): 
                    t0 = t0.next0_.next0_
            elif (str0_ == "ПО" or str0_ == "ДО"): 
                if ((isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.getReferent(), DateReferent))): 
                    dr = DateRangeReferent._new733(Utils.asObjectOrNull(t.next0_.getReferent(), DateReferent))
                    rt0 = ReferentToken(ad.registerReferent(dr), t, t.next0_)
                    kit.embedToken(rt0)
                    t = (rt0)
                    continue
            else: 
                continue
            if (t0 is None): 
                continue
            if (isinstance(t0, ReferentToken)): 
                date1 = (Utils.asObjectOrNull((t0).referent, DateReferent))
            if (date1 is None): 
                if (isinstance(t0, NumberToken)): 
                    v = (t0).value
                    if ((v < 1000) or v >= 2100): 
                        continue
                    year_val1 = v
                else: 
                    continue
            else: 
                year_val1 = date1.year
            t1 = t0.next0_
            if (t1 is None): 
                continue
            if (t1.isValue("ПО", "ДО") or t1.isValue("ДО", None)): 
                lang = t1.morph.language
            elif (t1.isValue("AND", None)): 
                lang = MorphLang.EN
            elif (t1.is_hiphen and lang == MorphLang.EN): 
                pass
            elif (lang.is_ua and t1.isValue("І", None)): 
                pass
            else: 
                continue
            t1 = t1.next0_
            if (t1 is None): 
                continue
            if (isinstance(t1, ReferentToken)): 
                date2 = (Utils.asObjectOrNull((t1).referent, DateReferent))
            if (date2 is None): 
                if (isinstance(t1, NumberToken)): 
                    nt1 = NumberExToken.tryParseNumberWithPostfix(t1)
                    if (nt1 is not None): 
                        continue
                    v = (t1).value
                    if (v > 0 and (v < year_val1)): 
                        yy = year_val1 % 100
                        if (yy < v): 
                            v += (((math.floor(year_val1 / 100))) * 100)
                    if ((v < 1000) or v >= 2100): 
                        continue
                    year_val2 = v
                else: 
                    continue
            else: 
                year_val2 = date2.year
            if (year_val1 > year_val2 and year_val2 > 0): 
                continue
            if (year_val1 == year_val2): 
                if (date1 is None or date2 is None): 
                    continue
                if (DateReferent.compare(date1, date2) >= 0): 
                    continue
            if (date1 is None): 
                date1 = (Utils.asObjectOrNull(ad.registerReferent(DateReferent._new731(year_val1)), DateReferent))
                rt0 = ReferentToken(date1, t0, t0)
                kit.embedToken(rt0)
                if (t0 == t): 
                    t = (rt0)
            if (date2 is None): 
                date2 = (Utils.asObjectOrNull(ad.registerReferent(DateReferent._new731(year_val2)), DateReferent))
                rt1 = ReferentToken(date2, t1, t1)
                kit.embedToken(rt1)
                t1 = (rt1)
            t = (ReferentToken(ad.registerReferent(DateRangeReferent._new728(date1, date2)), t, t1))
            kit.embedToken(Utils.asObjectOrNull(t, ReferentToken))
    
    M_INITED = None
    
    @staticmethod
    def initialize() -> None:
        if (DateAnalyzer.M_INITED): 
            return
        DateAnalyzer.M_INITED = True
        MetaDate.initialize()
        MetaDateRange.initialize()
        try: 
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
            DateItemToken.initialize()
            Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
        except Exception as ex: 
            raise Utils.newException(ex.__str__(), ex)
        ProcessorService.registerAnalyzer(DateAnalyzer())