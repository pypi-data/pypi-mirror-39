# -*- coding: utf-8 -*-

import copy

def replaceDayOfWeek(srcIncludingHangul, srcNation='ko'):
    convertedStr = copy.copy(srcIncludingHangul)

    convertedStr = convertedStr.replace( '월', 'Monday')
    convertedStr = convertedStr.replace( '화', 'Tuesday')
    convertedStr = convertedStr.replace( '수', 'Wednesday')
    convertedStr = convertedStr.replace( '목', 'Thursday')
    convertedStr = convertedStr.replace( '금', 'Friday')
    convertedStr = convertedStr.replace( '토', 'Saturday')
    convertedStr = convertedStr.replace( '일', 'Sunday')
    return convertedStr
