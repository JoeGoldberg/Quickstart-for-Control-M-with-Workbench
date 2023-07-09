# Quickstart-for-Control-M-with-Workbench
Deploy a basic Control-M environment for dev/test using the Control-M Workbench appliance on an AWS EKS cluster
## Introduction
This repo contains artifacts to implement one approach to getting strated with Control-M for engineers and anyone wishing to start exploiting the production-grade capabilities Control-M provides without the associated commitment and effort of installing and configuring a complete Control-M stack.

Control-M Workbench is a pre-built, ready-to-run appliance that enables you to get started with Control-M very quickly without 
having to install or configure a traditional configuration. This approach helps you to learn or experiment with Control-M and to unit-test workflows before pushing them down the deployment pipeline.

## Approach
Workbench is an image that resides on Docker Hub (see [Control-M Workbench](https://hub.docker.com/r/controlm/workbench)). You can use any container runtime that supports Docker containers. If you have a run-time on your desktop, you can have your own, personal copy with as little as one simple "docker run" command. 

This topic describes how to operate Control-M Workbench as a Kubernetes Service on AWS EKS. Some characteristics of this approach that may be desirable include:
* The Control-M environment can be accessible from other hosts and even to the public
* Resource constraints can be addressed more easily
* It's easier to share among team members or multiple teams
* It's easier to attach additional agents if required

This description is not a recommendation. Many variations are possible and this is just one sample approach to help you get started quickly so that you can proceed to the real task you are probably wishing to achieve; orchestrate you application and data pipelines.

## Choose Instance Type with at least 16GB RAM to accomodate Workbench container
If you choose this path of an AWS EKS cluster, ensure you have at least one node capable of hosting the Workbench whch requires 8-10GB memory. 

If using eksctl to build a cluster, add parameters simlar to this:

```
eksctl create cluster --name jogoldbe-eks-for-workbench --region us-west-2 --version 1.25 --vpc-public-subnets subnet-08cf82d2426c0fb65,subnet-03eebd7641a76e0c6 --instance-types=m5.xlarge --nodes=1
```

If you don't have an EKS cluster, see this tutorial for [**creating a cluster using the eksctl tool**](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html)

You can find the latest Control-M Automation API documentation, including a programming guide, on the [**project web page**](https://docs.bmc.com/docs/display/public/workloadautomation/Control-M+Automation+API+-+Getting+Started+Guide).
