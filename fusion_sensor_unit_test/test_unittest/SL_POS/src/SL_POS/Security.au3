;Dim $account = $CmdLine[1]
;Dim $password = $CmdLine[2]
;关闭firefox代理验证窗口，一直开着就行。
while True
	Dim $dialogTitle = "需要验证"
	WinActivate($dialogTitle)
	WinWaitActive($dialogTitle)
	Sleep(1*1000)
	WinClose($dialogTitle)
WEnd

;IE的验证窗口能够获取，正确处理程序如下：
;Dim $account = $CmdLine[1]
;Dim $password = $CmdLine[2]
;Dim $dialogTitle = "Windows 验证"
;WinActivate($dialogTitle)
;WinWaitActive($dialogTitle)
;Sleep(1*1000)
;ControlSetText($dialogTitle,"","Edit1",$account)
;Sleep(1*1000)
;ControlSetText($dialogTitle,"","Edit2",$password)
;ControlClick($dialogTitle,"","Button2")
;Sleep(1*1000) """

