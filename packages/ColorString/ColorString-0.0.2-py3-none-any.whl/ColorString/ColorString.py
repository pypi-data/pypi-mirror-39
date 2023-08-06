
FGcols = {	'black'		:	'30',
			'red'		:	'31',
			'green'		:	'32',
			'yellow'	:	'33',
			'blue'		:	'34',
			'magenta'	:	'35',
			'cyan'		:	'36',
			'white'		:	'37',
			'default'	:	'39',
			'bright black'		:	'90',
			'bright red'		:	'91',
			'bright green'		:	'92',
			'bright yellow'		:	'93',
			'bright blue'		:	'94',
			'bright magenta'	:	'95',
			'bright cyan'		:	'96',
			'bright white'		:	'97' }


BGcols = {	'black'		:	'40',
			'red'		:	'41',
			'green'		:	'42',
			'yellow'	:	'43',
			'blue'		:	'44',
			'magenta'	:	'45',
			'cyan'		:	'46',
			'white'		:	'47',
			'default'	:	'49',
			'bright black'		:	'100',
			'bright red'		:	'101',
			'bright green'		:	'102',
			'bright yellow'		:	'103',
			'bright blue'		:	'104',
			'bright magenta'	:	'105',
			'bright cyan'		:	'106',
			'bright white'		:	'107' }

def _StringToFGColor(x):
	global FGcols
	return FGcols[x]+'m'

def _StringToBGColor(x):
	global BGcols
	return BGcols[x]+'m'	
	
def _IntToFGColor(x):
	return '38;5;{:d}m'.format(x)

def _IntToBGColor(x):
	return '48;5;{:d}m'.format(x)
	
def _RGBtoColor(x):
	return 16 + 36*x[0] + 6*x[1] + x[2]


def GetFGCode(x):
	CSI = '\x1b['
	if isinstance(x,str):
		code = CSI + _StringToFGColor(x)
	elif isinstance(x,int):
		code = CSI + _IntToFGColor(x)
	elif isinstance(x,list):
		code = CSI + _IntToFGColor(_RGBtoColor(x))
	else:
		code=''
	return code


def GetBGCode(x):
	CSI = '\x1b['
	if isinstance(x,str):
		code = CSI + _StringToBGColor(x)
	elif isinstance(x,int):
		code = CSI + _IntToBGColor(x)
	elif isinstance(x,list):
		code = CSI + _IntToBGColor(_RGBtoColor(x))
	else:
		code=''
	return code

def GetEndFormat():
	CSI = '\x1b['
	END = CSI+'0m'
	return END

def ColorString(s,fgcolor='default',bgcolor='default'):
	
	CSI = '\x1b['
	END = CSI+'0m'

	FG = GetFGCode(fgcolor)
	BG = GetBGCode(bgcolor)

	return FG+BG+s+END
