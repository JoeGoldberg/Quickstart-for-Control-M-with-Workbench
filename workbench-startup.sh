#!/bin/bash

# Deploy an updated job type
ctm deploy jobtype "C:\Users\JOGOLDBE\OneDrive - BMC Software, Inc\BMC_Stuff\Install Material\CTM\Integrations\GDF032022-jg.ctmai" workbench workbench -e eksbench

# Windows batch file that reads data from the file specified
# as the second parameter and stores it in a secret with a name
# specified in the first parameter
ctmsecret.bat gcp-service-account gcp-service-account-key-value.dat

# Deploy Connection Profiles and Folders
ctm deploy cp-Glue-Databrew-ADF-DFLOW.json -e eksbench
ctm deploy fldr-pmp-mc-pipeline.json