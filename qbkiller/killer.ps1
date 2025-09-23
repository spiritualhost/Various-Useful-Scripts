# Stop the QBCFMonitorService (Network Connection Monitor)
taskkill /im QBCFMonitorService.exe /f

#Stop the webconnecter (tray + app)
taskkill /im Intuit.QBDT.Webconnector.QBWCMonitor.exe /f
taskkill /im Intuit.QBDFT.Webconnector.Application.exe /f

#Stop the data protect service
taskkill /im QBIDPService.exe /f

#Stop the patch nagger
taskkill /im QBUpdateMonitorService.exe /f