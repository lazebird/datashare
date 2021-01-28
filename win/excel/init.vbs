Public dbtitles As Variant
Public prjtypes As Variant
Public ordertypes As Variant
Public customers As Variant
Public debittypes As Variant
Public employees As Variant

Function findsheet(name As String) As Worksheet
    Set findsheet = Worksheets(name)
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
    Set sh = Worksheets.Add(after:=Worksheets(Worksheets.Count))        ' add to end
    sh.name = name
    Set getsheet = sh
End Function
Function get_validatelist(name As String, addr As String) As String
    If Worksheets(name) Is Nothing Then Exit Function
    get_validatelist = "='" & name & "'!" & Worksheets(name).Range(addr).Address
    Exit Function
    ' string will expire when new project added, may be use xlValidateCust?
    Dim cel As Range
    Dim str As String
    For Each cel In Worksheets(name).Range(addr)
        If Not IsEmpty(cel.Value) Then str = str & cel.Value
    Next
    If IsEmpty(str) Then str = ""
    get_validatelist = str
End Function

Sub init_datas()
    dbtitles = Array("项目类别", "订单类别", "客户名称", "账户类型", "员工")
    prjtypes = Array("管理型", "傻瓜机", "纯软件", "纯硬件", "软硬件", "仅开发费", "仅抽成", "开发费+抽成")
    ordertypes = Array("开发费", "layout费", "license费", "工资", "奖金", "房租", "水电", "聚餐", "食品", "办公", "饮料", "其他")
    customers = Array("S", "L", "Y", "O")
    debittypes = Array("公账", "私账", "lic50", "lic100", "lic200", "lic250")
    employees = Array("csg", "lss", "lqy", "zxf")
End Sub
Sub init_db()
    init_datas
    Dim sh          As Worksheet
    Set sh = getsheet("初始数据", True)
    'sh.Range("A1:A4").Interior.Color = RGB(0, 255, 0)
    With sh.Range("A1:A5")
        .Interior.ColorIndex = 10
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .HorizontalAlignment = Excel.xlCenter
    End With
    Dim i As Integer
    Dim r As Range
    Set r = sh.Range("A1:A5")
    For i = LBound(dbtitles) To UBound(dbtitles)
        r(i + 1) = dbtitles(i)
    Next i
    
    Set r = sh.Range("B1:Z1")
    ' MsgBox "address " & r.Address & Chr(13) & "r(0) address " & r(0).Address & Chr(13) & "r(1) address " & r(1).Address
    For i = LBound(prjtypes) To UBound(prjtypes)
        r(i + 1) = prjtypes(i)
    Next i
    
    Set r = sh.Range("B2:Z2")
    For i = LBound(ordertypes) To UBound(ordertypes)
        r(i + 1) = ordertypes(i)
    Next i
    
    Set r = sh.Range("B3:Z3")
    For i = LBound(customers) To UBound(customers)
        r(i + 1) = customers(i)
    Next i
    
    Set r = sh.Range("B4:Z4")
    For i = LBound(debittypes) To UBound(debittypes)
        r(i + 1) = debittypes(i)
    Next i

    Set r = sh.Range("B5:Z5")
    For i = LBound(employees) To UBound(employees)
        r(i + 1) = employees(i)
    Next i
End Sub

Sub init_projects()
    Dim sh          As Worksheet
    Set sh = getsheet("项目信息", True)
    sh.Range("A1:K1").Interior.ColorIndex = 10
    sh.Range("A1:K1").Font.Bold = True
    sh.Range("A1:K1").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:K1").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:K1") = Array("日期", "项目名称", "客户名称", "项目类别", "项目描述", "应收款", "实收款", "实付款/项目成本", "下一个账期", "项目状态", "备注")
    
    sh.Range("C2:C1000").Validation.Add xlValidateList, Formula1:=get_validatelist("初始数据", "B3:Z3")
    sh.Range("D2:D1000").Validation.Add xlValidateList, Formula1:=get_validatelist("初始数据", "B1:Z1")
    sh.Range("J2:J1000").Validation.Add xlValidateList, Formula1:="等待,进行,结束"
End Sub

Sub init_orders()
    Dim sh          As Worksheet
    Set sh = getsheet("资金流水", True)
    sh.Range("A1:Z1").Interior.ColorIndex = 10
    sh.Range("A1:Z1").Font.Bold = True
    sh.Range("A1:Z1").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:Z1").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:H1") = Array("日期", "描述", "类别", "预计金额", "实际金额", "关联项目", "客户名称", "下一个账期")
    'sh.Range("I1:Z1").Merge
    'sh.Range("I1:Z1") = "资金账户"
    Dim i As Integer
    Dim r As Range
    Set r = sh.Range("I1:Z1")
    For i = LBound(debittypes) To UBound(debittypes)
        r(i + 1) = debittypes(i)
    Next i
    
    sh.Range("C2:C1000").Validation.Add xlValidateList, Formula1:=get_validatelist("初始数据", "B2:Z2")
    sh.Range("F2:F1000").Validation.Add xlValidateList, Formula1:=get_validatelist("项目信息", "B2:B2000")
    sh.Range("G2:G1000").Validation.Add xlValidateList, Formula1:=get_validatelist("初始数据", "B3:Z3")
End Sub

Sub init_reimbursement()
    Dim sh          As Worksheet
    Set sh = getsheet("报销单", True)
    sh.Range("A1:E1").Interior.ColorIndex = 10
    sh.Range("A1:E1").Font.Bold = True
    sh.Range("A1:E1").Font.Color = RGB(255, 255, 255)
    sh.Range("A1:E1").HorizontalAlignment = Excel.xlCenter
    sh.Range("A1:E1") = Array("日期", "描述", "费用", "人员", "备注")
    
    sh.Range("D2:D1000").Validation.Add xlValidateList, Formula1:=get_validatelist("初始数据", "B5:Z5")
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
