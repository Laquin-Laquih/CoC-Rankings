def is_arabic(ch):
	if('\u0600' <= ch <= '\u06FF' or
		'\u0750' <= ch <= '\u077F' or
		'\u08A0' <= ch <= '\u08FF' or
		'\uFB50' <= ch <= '\uFDFF' or
		'\uFE70' <= ch <= '\uFEFF' or
		'\U00010E60' <= ch <= '\U00010E7F' or
		'\U0001EE00' <= ch <= '\U0001EEFF'):
		return True
	else:
		return False

def fullwidth(num):
	if(num == 1):
		return '\uFF11'
	if(num == 2):
		return '\uFF12'
	if(num == 3):
		return '\uFF13'
	if(num == 4):
		return '\uFF14'
	if(num == 5):
		return '\uFF15'