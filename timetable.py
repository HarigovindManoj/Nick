from datetime import datetime
from engine.command import speak

FiveTo6 = '''

In this time you have to
Pray and after that 
do Meditation and also drink
cofee

'''

SixTo9 = '''

Breakfast
Study

'''

NineTo12 = '''

Study
Rest
Lunch

'''

TwelveTo15 = '''

In this time you have to 
Study and after 5 minutes you need to take some
Rest and have your
Lunch

'''

FifteenTo21 = '''

Study
Rest
Lunch

'''

TwentyOneTo22 = '''

Study
Rest
Lunch

'''

def Time():

    hour  = int(datetime.now().strftime("%H"))

    if hour>=5 and hour<6:
        speak(FiveTo6)
        return FiveTo6
    elif hour>=6 and hour<9:
        speak(SixTo9)
        return SixTo9
    elif hour>=9 and hour<12:
        speak(NineTo12)
        return NineTo12
    elif hour>=12 and hour<15:
        speak(TwelveTo15)
        return TwelveTo15
    elif hour>=15 and hour<21:
        speak(FifteenTo21)
        return FifteenTo21
    elif hour>=21 and hour<22:
        speak(TwentyOneTo22)
        return TwentyOneTo22
    else:
        return '''In This Time,You have to sleep'''