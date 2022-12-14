Sub sample_prjs()
    Dim sh          As Worksheet
    Set sh = getsheet("项目信息", False)
    sh.Range("A2:K2") = Array("1/11/2021", "XXX项目", "L", "软硬件", "产品开发", "100000", "", "", "1/14/2021", "进行", "")
    sh.Range("A3:K3") = Array("1/13/2021", "1月Z客户license", "Z", "license", "8+4和16+4", "50000", "", "", "1/22/2021", "进行", "")
End Sub

Sub sample_orders()
    Dim sh          As Worksheet
    Set sh = getsheet("资金流水", False)
    sh.Range("A2:L2") = Array("1/12/2021", "项目启动预付款", "开发费", "50000", "XXX项目", "L", "50000", "", "", "", "", "")
    sh.Range("A3:L3") = Array("1/18/2021", "芯片出货", "license费", "20000", "", "S", "20000", "", "10000", "", "10000", "")
    sh.Range("A4:L4") = Array("1/20/2021", "发工资", "工资", "10000", "", "", "-10000", "", "", "", "", "")
    sh.Range("A5:L5") = Array("1/21/2021", "补贴", "其他", "5000", "", "", "", "-5000", "", "", "", "")
End Sub

Sub sample_reimbursements()
    Dim sh          As Worksheet
    Set sh = getsheet("报销单", False)
    sh.Range("A2:E2") = Array("1/12/2021", "聚餐", "聚餐", "300", "lqy", "")
    sh.Range("A3:E3") = Array("1/14/2021", "购物", "食品", "100", "lss", "")
End Sub

Sub sample_all()
    sample_prjs
    sample_orders
    sample_reimbursements
End Sub
