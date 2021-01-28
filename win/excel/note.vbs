Sub init_notes()
    Dim sh          As Worksheet
    Set sh = getsheet("说明", True)
    With sh.Range("A1:C1")
        .Interior.ColorIndex = 10
        .Font.Bold = True
        .Font.Color = RGB(255, 255, 255)
        .HorizontalAlignment = Excel.xlCenter
        .AutoFilter
    End With
    sh.Range("A1:C1") = Array("标签名称", "使用说明", "备注")
    sh.Range("A2:C2") = Array("初始数据", "用于添加基础数据选项", "")
    sh.Range("A3:C3") = Array("项目信息", "用于添加项目信息", "只有项目存在账单跟踪能力")
    sh.Range("A4:C4") = Array("资金流水", "用于记录公司账户金额变化", "")
    sh.Range("A5:C5") = Array("报销单", "用于记录员工代付和报销项", "")
End Sub
