Public lastrange As Range
Function get_title(r As Range) As Range
    Dim titleaddr As String
    titleaddr = Left(r.Address, InStrRev(r.Address, "$")) & "1"
    ' MsgBox "select： " & r.Address & Chr(13) & " titleaddr=" & titleaddr & Chr(13) & " title=" & get_title.Value
    Set get_title = ActiveSheet.Range(titleaddr)
End Function

Sub on_select(r As Range)
    If Not r.Count = 1 Or r.row = 1 Then
        Exit Sub
    End If
    Dim title As Range
    Set title = get_title(r)
    If title.Value = "日期" Or title.Value = "下一个账期" Then Call Calendar.SelectedDate2(r)
    If title.Value = "实收款" Or title.Value = "实付款/项目成本" Then Call project_completion(r)
    If Not lastrange Is Nothing Then Call order_completion(lastrange)
    Set lastrange = r
End Sub

Sub order_completion(r As Range)
    Dim title As Range
    Set title = get_title(r)
    If Not title.Value = "关联项目" Then Exit Sub
    If IsEmpty(r.Value) Then Exit Sub
    Dim cel As Range
    For Each cel In Worksheets("项目信息").Range("B2:B2000")
        If cel.Value = r.Value Then Exit For
    Next
    If cel Is Nothing Then Exit Sub
    ActiveSheet.Range("F" & r.row) = Worksheets("项目信息").Range("C" & cel.row)
    ActiveSheet.Range("G" & r.row) = Worksheets("项目信息").Range("I" & cel.row).Value
End Sub

Sub project_completion(r As Range)
    Dim prjname As String
    prjname = ActiveSheet.Range("B" & r.row).Value
    If IsEmpty(prjname) Or prjname = "" Then Exit Sub
    Dim cel As Range
    Dim total_in As Long
    Dim total_out As Long
    Dim cval As Long
    Dim pval As Long
    For Each cel In Worksheets("资金流水").Range("E2:E2000")
        If cel.Value = prjname Then
            ' MsgBox "row: " & cel.row & " value: " & Worksheets("资金流水").Range("H" & cel.row).Value
            cval = CLng(Worksheets("资金流水").Range("H" & cel.row).Value)
            pval = CLng(Worksheets("资金流水").Range("I" & cel.row).Value)
            If cval > 0 Then
                total_in = total_in + cval
            Else
                total_out = total_out + cval
            End If
            If pval > 0 Then
                total_in = total_in + pval
            Else
                total_out = total_out + pval
            End If
        End If
    Next
    ActiveSheet.Range("G" & r.row) = total_in
    ActiveSheet.Range("H" & r.row) = total_out
End Sub

Private Sub Worksheet_SelectionChange(ByVal r As Range) ' should put into sheet's code
    on_select r
End Sub
