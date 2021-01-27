Function findsheet(name As String) As Worksheet
    Dim sh          As Worksheet
    For Each sh In Worksheets
        If sh.name = name Then
            Set findsheet = sh
            Exit Function
        End If
    Next
    Set findsheet = Nothing
End Function
Function getsheet(name As String, clear_flag As Boolean) As Worksheet
    Dim sh          As Worksheet
    Set sh = findsheet(name)
    If Not sh Is Nothing Then
        If clear_flag Then
            sh.Cells.Clear
        End If
        Set getsheet = sh
        Exit Function
    End If
    Set sh = Worksheets.Add(after:=Worksheets(Worksheets.Count)) ' add to end
    sh.name = name
    Set getsheet = sh
End Function

Sub init_db()
    Dim sh          As Worksheet
    Set sh = getsheet("初始数据", True)
    'sh.Range("A1:A3").Interior.Color = RGB(0, 255, 0)
    sh.Range("A1:A3").Interior.ColorIndex = 10
    sh.Range("A1:A3").Font.Bold = True
    sh.Range("A1:A3").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:A3").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:I1") = Array("项目类别", "管理型", "傻瓜机", "纯软件", "纯硬件", "软硬件", "仅开发费", "仅抽成", "开发费+抽成")
    sh.Range("A2:M2") = Array("账单类别", "开发费", "layout费", "license费", "工资", "奖金", "房租", "水电", "聚餐", "食品", "办公", "饮料", "其他")
    sh.Range("A3:E3") = Array("客户名称", "S", "B", "Y", "O")
End Sub

Sub init_projects()
    Dim sh          As Worksheet
    Set sh = getsheet("项目信息", True)
    sh.Range("A1:K1").Interior.ColorIndex = 10
    sh.Range("A1:K1").Font.Bold = True
    sh.Range("A1:K1").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:K1").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:K1") = Array("时间", "项目名称", "客户名称", "项目类别", "项目描述", "应收款", "实收款", "实付款/项目成本", "下一个账期", "项目状态", "备注")
End Sub

Sub init_orders()
    Dim sh          As Worksheet
    Set sh = getsheet("资金流水", True)
    sh.Range("A1:K2").Interior.ColorIndex = 10
    sh.Range("A1:K2").Font.Bold = True
    sh.Range("A1:K2").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:K2").HorizontalAlignment = Excel.xlCenter
    sh.Range("I1:K1").Merge
    sh.Range("I1:K1") = "产品账户"
    sh.Range("A2:K2") = Array("时间", "描述", "类别", "预计金额", "实际金额", "客户名称", "关联项目", "下一个账期", "8+4", "xxx", "xxx")
End Sub

Sub init_reimbursement()
    Dim sh          As Worksheet
    Set sh = getsheet("报销单", True)
    sh.Range("A1:E1").Interior.ColorIndex = 10
    sh.Range("A1:E1").Font.Bold = True
    sh.Range("A1:E1").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:E1").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:E1") = Array("日期", "描述", "费用", "人员", "备注")
End Sub

Sub init()
    init_db
    init_projects
    init_orders
    init_reimbursement
End Sub

Sub destroy()
    Dim sh          As Worksheet
    Set sh = getsheet("reserve", True)
    For Each sh In Worksheets
        If Not sh.name = "reserve" Then
            sh.Delete
        End If
    Next
End Sub

