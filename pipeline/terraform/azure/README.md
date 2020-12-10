# Deployment of MHS Adaptor on Microsoft Azure

## 0. General setup, ./files, ./etc

First the directiores, the `files` one is for storing the files that terraform uses, currently it consists of a SSH Public key which will be copied over to instances to allow SSH connections. The `etc` directory contains tfvars files with values for terraform variables. In order to use them run `terraform (plan | apply) --var-file ../etc/globals.tfvars --var-file ../etc/secrets.tfvars` in any of the terraform based components described below.

In order to run terraform for Azure Resource Manager, you need a set of credentials, ways to get them are described [here](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure) We have used a scrpit that exported the required environment variables, using the Service Principal with Client Secret method, this script is not part of this code as it contains values specific to each Azure Account / Subscription ./ User. The values required are:

```bash
export ARM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export ARM_TENANT_ID="00000000-0000-0000-0000-000000000000"
export ARM_CLIENT_ID="00000000-0000-0000-0000-000000000000"
export ARM_CLIENT_SECRET="00000000-0000-0000-0000-000000000000"
export TF_VAR_client_id=${ARM_CLIENT_ID}
export TF_VAR_client_secret=${ARM_CLIENT_SECRET}
```

The values prefixed with `TF_VAR` are indicating variables for terraform. This script will later be extended with key for Terraform State Bucket.

## 1. State component - bucket for terraform remote state

The state component should be created first. It contains a Storage Account and Storage Container for Terraform state files. By default Terraform state is kept locally in directory from where the apply was done. Having the state in central location, like on Storage Container / Bucket enables sharing information between components - one Terraform apply can use information from other Terraform apply. To apply the state component, enter the directory and run `terraform apply -auto-approve --var-file ../etc/globals.tfvars` In the list of outputs you will find a key to the Storage Account, copy it and add to the script with env vars from step 0, in a way shown below:

```bash
export ARM_ACCESS_KEY=TheKeyGoesHere==
```

## 2. Base component - jumpbox

The base component is a place for reources common for all other, eventually we may move the database and service bus here. Right now jumpbox VM is created here, which can be used to general purpose testing, or as the name says as jump-box to a second VM within the cluster subnet which we will create in step 4. The way of applying is the same as for state, enter the directory and run `terraform apply -auto-approve --var-file ../etc/globals.tfvars --var-file ../etc/secrets.tfvars` In the secrets.tfvars you can specify CIDRs that will allowed to connect to the new jumpbpox.

## 3. Base-secrets component - Key Vault for secrets

This component creates the Azure Key Vault for storing secrets used by MHS, you can setup the secrets directly via Terraform or later via Azure Console (for that you will have to modify the access policy to add your Console users ClientID and TenantID ot to the Key Vault, by default only the TF Client and Tenant IDs are added). You can check the [variables.tf](base-secrets/variables.tf) file for the names of variables and set them as environment variables with `TF_VAR_` prefix. This is preferred as opposed to loading them from file as you will not upload it by mistake to repo, and tfvars files do not like multiline strings like PEM certificates.

## 4. MHS component - AKS cluster and other things required by MHS adaptor

## 5. MHS-kube-tf - Terraform part of defintions for MHS AKS deployment

## 6. MHS-kube-yaml - Yaml part of definitions for MHS AKS deployment
