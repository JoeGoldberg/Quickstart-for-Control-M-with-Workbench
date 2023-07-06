@echo off

rem ------------------------------------------------------------------+
rem Deploy an updated job type                                        |
rem ------------------------------------------------------------------+
ctm deploy jobtype "C:\Users\JOGOLDBE\OneDrive - BMC Software, Inc\BMC_Stuff\Install Material\CTM\Integrations\GDF032022-jg.ctmai" workbench workbench -e eksbench

rem ------------------------------------------------------------------+
rem Windows batch file that reads data from the file specified        |
rem as the second parameter and stores it in a secret with a name     |
rem specified in the first parameter                                  |
rem ------------------------------------------------------------------+
ctmsecret.bat aws-secret-key "C:\Users\JOGOLDBE\git\Quickstart-for-Control-M-with-Workbench-Local\ctmsecrets\aws-secret-key.dat"
rem
rem -------------------------------------------------------------------------------------------------------------------------------------------------
rem Google Service Account works via "-p" but not via this batch file; issue to be investigated
ctmsecret.bat gcp-service-account "C:\Users\JOGOLDBE\git\Quickstart-for-Control-M-with-Workbench-Local\ctmsecrets\gcp-service-account-key-value.dat"
rem -------------------------------------------------------------------------------------------------------------------------------------------------

ctmsecret azure-736885f534e94d86a5c991b812193116-secret "C:\Users\JOGOLDBE\git\Quickstart-for-Control-M-with-Workbench-Local\ctmsecrets\azure-736885f534e94d86a5c991b812193116-secret.dat"

rem ------------------------------------------------------------------+
rem Deploy Connection Profiles and Folders                            |
rem ------------------------------------------------------------------+
ctm deploy cp-Glue-Databrew-ADF-DFLOW.json -e eksbench
ctm deploy fldr-pmp-mc-pipeline.json
