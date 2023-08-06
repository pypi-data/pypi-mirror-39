#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import textract
text = textract.process("resume/เรซูเม่ส้มโอ _ ไทย.pdf", extension="pdf")
#print text
import tnthai.segment as tn



#text = text.decode('utf-8')
thai_unicode_char = 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะ ัาำ ิ ี ึ ื ุ ู ฺ ฿เแโใไๅๆ ็ ่ ้ ๊ ๋ ์ ํ ๐๑๒๓๔๕๖๗๘๙' + u"\u0e4e\u0e4f\u0e5a\u0e5b".encode('utf-8')

import string


f = open("rawpdftext", "w")
f.write(text)
f.close()

tmpans = ""

for ele in text:
    if ele in thai_unicode_char:
        tmpans += ele
    elif 'A' < ele and ele < 'Z':
        tmpans += ele
    elif 'a' < ele and ele < 'z':
        tmpans += ele
    elif ele in string.printable:
        tmpans += ele

f = open("filteredtext", "w")
f.write(tmpans)
f.close()

tmpans = tmpans.replace("\x80", "")
tmpans = tmpans.decode('utf-8', errors='ignore').encode('utf-8')

f = open("decodeignore", "w")
f.write(tmpans)
f.close()
