;Dim $account = $CmdLine[1]
;Dim $password = $CmdLine[2]
;�ر�firefox������֤���ڣ�һֱ���ž��С�
while True
	Dim $dialogTitle = "��Ҫ��֤"
	WinActivate($dialogTitle)
	WinWaitActive($dialogTitle)
	Sleep(1*1000)
	WinClose($dialogTitle)
WEnd

;IE����֤�����ܹ���ȡ����ȷ����������£�
;Dim $account = $CmdLine[1]
;Dim $password = $CmdLine[2]
;Dim $dialogTitle = "Windows ��֤"
;WinActivate($dialogTitle)
;WinWaitActive($dialogTitle)
;Sleep(1*1000)
;ControlSetText($dialogTitle,"","Edit1",$account)
;Sleep(1*1000)
;ControlSetText($dialogTitle,"","Edit2",$password)
;ControlClick($dialogTitle,"","Button2")
;Sleep(1*1000) """

