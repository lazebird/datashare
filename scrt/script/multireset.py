tab1 = crt.Session.ConnectInTab("/S 192.168.1.233-10002")
tab2 = crt.Session.ConnectInTab("/S 192.168.1.233-10003")

# stop peer tab when bug occurred
if (crt.GetActiveTab().Index != 3):
  # peertab = crt.Session.ConnectInTab("/S 192.168.1.233-10003")
  # peertab.Activate()
  crt.GetTab(3).Screen.Send("#failed")
