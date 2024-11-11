
@ECHO OFF

set filepath = 'C:\Users\ditin\Desktop\SmartToolbox_Facial\SmartToolbox'

:BEGINPROGRAM

cmd /c "cd %filepath% && .\venv\Scripts\activate && python run.py && ECHO Ok: application ended"

:ENDPROGRAM
@pause