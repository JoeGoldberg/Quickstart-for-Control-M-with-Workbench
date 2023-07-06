# Quickstart-for-Control-M-with-Workbench
Deploy a basic Control-M environment for dev/test using the Control-M Workbench appliance on an AWS EKS cluster
## Introduction
This repo contains artifacts to implement one approach to getting strated with Control-M for engineers and anyone wishing to start exploiting the production-grade capabilities Control-M provides without the associated commitment and effort of installing and configuring a complete Control-M stack.

Control-M Workbench is a pre-built, ready-to-run appliance that enables you to get started with Control-M very quickly without 
having to install or configure a sophisticated environment. This approach helps you to learn or experiment with Control-M and to unit-test workflows before pushing them down the deployment pipeline.

## Approach
Workbench is an image that resides on Docker Hub (see [Control-M Workbench](https://hub.docker.com/r/controlm/workbench)). You can use any container runtime that supports Docker containers. If you have a run-time on your desktop, you can have your own, personal copy with as little as one simple "docker run" command. 

This topic describes how to operate Control-M Workbench as a Kubernetes Service on AWS EKS. Many variations to this configuraiton are possible. This description is intended to provide one approach and to help you implement this setup quickly so that you can proceed to the real task you are probably wishing to achieve; orchestrate you application and data pipelines.

# Choose Instance Type with at least 16GB RAM to accomodate Workbench container
eksctl create cluster --name jogoldbe-eks-for-workbench --region us-west-2 --version 1.25 --vpc-public-subnets subnet-08cf82d2426c0fb65,subnet-03eebd7641a76e0c6 --instance-types=m5.xlarge --nodes=1
If you don't have an EKS cluster, see this tutorial for [**creating a cluster using the eksctl tool**](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)

You can find the latest Control-M Automation API documentation, including a programming guide, on the [**project web page**](https://docs.bmc.com/docs/display/public/workloadautomation/Control-M+Automation+API+-+Getting+Started+Guide).
