# ================
# Simple code snippet to get started with Control-M Workbench
# and Control-M Python Client
# This code requires the python client library installed
# Check it on https://controlm.github.io/ctm-python-client/tutorials.html
# ================

from ctm_python_client.core.workflow import *
from ctm_python_client.core.comm import Environment
from ctm_python_client.core.monitoring import *
# from ctm_python_client.ext.viz import get_graph
from aapi import *
import json

ctmhost = "a90473c38638242c1b5a4c9d4e7b3015-537144556.us-west-2.elb.amazonaws.com"
ctmport = "8443"
ctmuser= "workbench"
ctmpswd = "workbench"
agenthost = "workbench"
ctmfolder = "pmp-python-mc-pipeline"

ctm_workflow = Workflow(
    Environment.create_onprem(ctmhost, ctmport, ctmuser, ctmpswd),
    WorkflowDefaults(
        controlm_server="workbench",
        application="pmp",
        sub_application="MultiCloud Pipelines",
        host="workbench",
        run_as=ctmuser
    )
)

jobDataBrew1 = JobAwsGlueDataBrew("pmp-databrew-clean-telematics-data", 
        connection_profile          = "ADB-BENCH",
        job_name                    = "clean-telematics-data",
        output_job_logs             = "unchecked",
        output                      = { }
    )


jobGlue1 = JobAwsGlue("jog-Glue-S3-to-Redshift", 
        connection_profile          = "AWS-GLUE-BENCH",
        glue_job_name               = "GlueS3toRedshift",
        status_polling_frequency    = "10"
    )

jobADF1 = JobAzureDataFactory("pmp-mc-smb-ADF_SparkPipeline",
        connection_profile          = "ADF-BENCH",
        resource_group_name         = "jgSBDemo_v52",
        data_factory_name           = "FY21DemoADF-wgkt6m72loema",
        pipeline_name               = "SimplePipeline",
        parameters                  = "{}"
    )

jobDataFlow1 = JobGCPDataFlow("pmp-dflow-gcs-to-bq-personal",
        connection_profile          = "DFLOW-BENCH",
        project_id                  = "sso-gcp-dba-ctm4-pub-cc10274",
        region                      = "us-central1",
        log_level                   = "INFO",
        parameters__json_format     = "{\"jobName\": \"pmp-dflow-gcs-to-bq-personal\",    \"environment\": {        \"bypassTempDirValidation\": false,        \"tempLocation\": \"gs://prj1968-bmc-data-platform-foundation/bmc_personal_details/temp\",        \"ipConfiguration\": \"WORKER_IP_UNSPECIFIED\",        \"additionalExperiments\": []    },    \"parameters\": {        \"javascriptTextTransformGcsPath\": \"gs://prj1968-bmc-data-platform-foundation/bmc_personal_details/bmc_personal_details_transform.js\",        \"JSONPath\": \"gs://prj1968-bmc-data-platform-foundation/bmc_personal_details/bmc_personal_details.json\",        \"javascriptTextTransformFunctionName\": \"transform\",        \"outputTable\": \"sso-gcp-dba-ctm4-pub-cc10274:bmc_dataplatform_foundation.bmc_personal_details_V2\",        \"inputFilePattern\": \"gs://prj1968-bmc-data-platform-foundation/bmc_personal_details/bmc_personal_details.csv\",        \"bigQueryLoadingTemporaryDirectory\": \"gs://prj1968-bmc-data-platform-foundation/bmc_personal_details/tmpbq\"    }}", 
        template_location_gs_       = "gs://dataflow-templates-us-central1/latest/GCS_Text_to_BigQuery",
        template_type               = "Classic Template"
    )

jobpmpSLA = JobSLAManagement("pmp-mc-pipeline-service",
        service_name='Predictive Maintenance Telematics Analytics pipeline',
        service_priority='1',
        complete_in=JobSLAManagement.CompleteIn(time='00:05')
    )

ctm_workflow.chain([jobGlue1, jobDataBrew1, jobpmpSLA], inpath=ctmfolder)
ctm_workflow.chain([jobGlue1, jobADF1, jobDataFlow1, jobpmpSLA], inpath=ctmfolder)
build_results = ctm_workflow.build()

#print("Workflow JSON:")
#print(ctm_workflow.dumps_json(indent=2))

if build_results.is_ok():
    print("Build was successful")
    run = ctm_workflow.run(open_in_browser=True)
#    run = ctm_workflow.run()
    run.print_statuses()
else:
    print("Error building job flow")
    print(ctm_workflow.dumps_json(indent=2))
    exit()

# attr = dir(run)
# print(attr)

import time
time.sleep(10)
print("Monitoring")
print(run.get_statuses())