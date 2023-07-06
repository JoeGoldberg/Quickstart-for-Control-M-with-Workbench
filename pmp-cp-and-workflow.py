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

ctmhost = "--redacted--.us-west-2.elb.amazonaws.com"
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

cpGlue = ConnectionProfileAwsGlue("AWS-GLUE-BENCH",
        centralized         = True,
        aws_region          = "us-west-2",
        authentication      = "SECRET",
        aws_access_key_id   = "--redacted--",
        aws_secret          = {"Secret": "aws-secret-key"},
        glue_url            = "glue.us-west-2.amazonaws.com",
        connection_timeout  = "40"
        )
ctm_workflow.add(cpGlue)

cpDataBrew = ConnectionProfileAwsGlueDataBrew("ADB-BENCH",
        centralized         = True,
        authentication      = "SECRET",
        aws_access_key      = "--redacted--",
        aws_secret          = {"Secret": "aws-secret-key"},
        aws_api_base_url    = "https://databrew.{{AWSRegion}}.amazonaws.com",
        aws_logs_url        = "https://logs.{{AWSRegion}}.amazonaws.com",
        aws_region          = "us-west-2",
        connection_timeout  = "40"
        )
ctm_workflow.add(cpDataBrew)

cpADF = ConnectionProfileAzureDataFactory("ADF-BENCH",
        tenant_id           = "--redacted--",
        identity_type       = "PRINCIPAL",
        client_secret       = {"Secret": "azure-736885f534e94d86a5c991b812193116-secret"},
        subscription_id     = "--redacted--",
        application_id      = "--redacted--",
        management_url      = "management.azure.com",
        rest_login_url      = "login.microsoftonline.com",
        connection_timeout  = "75",
        centralized         = True
        )
ctm_workflow.add(cpADF)

cpDataFlow = ConnectionProfileGCPDataFlow("DFLOW-BENCH",
        centralized         = True,
        data_flow_url       = "https://dataflow.googleapis.com",
        identity_type       = "service_account",
        service_account_key  = {"Secret": "gcp-service-account"}
        )
ctm_workflow.add(cpDataFlow)
#with open("debug_cp.json", "w") as write_file:
#    json.dump(ctm_workflow.dumps_json(indent=0), write_file, indent=4, sort_keys=True)

cpdeploy_results = ctm_workflow.deploy()

if cpdeploy_results.is_ok():
    print("Connection Profile deploy was successful")
    ctm_workflow.clear_all()
else:
    print("Error deploying Connection Profile")
    print(ctm_workflow.dumps_json(indent=2))
    exit()

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