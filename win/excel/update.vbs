Sub on_select(r As Range)
    If Not r.Count = 1 Then
        Exit Sub
    End If
    Dim titleaddr As String
    titleaddr = Left(r.Address, 2) & "$1"
    Dim title As Range
    Set title = ActiveSheet.Range(titleaddr)
    ' MsgBox "select： " & r.Address & " title=" & title.Value
    If title.Value = "日期" Or title.Value = "下一个账期" Then
        Call Calendar.SelectedDate2(r)
    End If
End Sub

Private Sub Worksheet_SelectionChange(ByVal r As Range) ' should put into sheet's code
    on_select r
End Sub


