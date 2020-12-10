# Deployment of MHS Adaptor on Microsoft Azure

## Terraform

This directory contains the [Terraform](https://www.terraform.io/) configurations used to deploy instances of the MHS
application to **Azure**. For AWS see [mhs-environment/README](../mhs-environment/README.md).

This configuration will create a full test environment running an MHS application.

## Known Issues

None

## Deploying MHS Manually

To manually deploy the MHS you must ensure that Terraform can authenticate to Azure. See the 
[authentication section of the Terraform Azure documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure)
for details. If running this on your local machine, the simplest option is the "Service Principal with Client Secret" 
method using environment variables. You must define these variables on your local machine using values from your
Azure subscription. 

For example, you might use a Bash script to define the environment variables as follows:

```bash
export ARM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export ARM_TENANT_ID="00000000-0000-0000-0000-000000000000"
export ARM_CLIENT_ID="00000000-0000-0000-0000-000000000000"
export ARM_CLIENT_SECRET="00000000-0000-0000-0000-000000000000"
export TF_VAR_client_id=${ARM_CLIENT_ID}
export TF_VAR_client_secret=${ARM_CLIENT_SECRET}
```

Our scripts deploy container images from [Docker Hub](https://hub.docker.com/u/nhsdev):
* nhsdev / nia-mhs-route
* nhsdev / nia-mhs-outbound
* nhsdev / nia-mhs-inbound

Once you have configured Azure authentication, you can run the following commands to deploy the MHS:

```
TODO: COMMANDS HERE
```

## Your HSCN VNet Config

TODO

## Terraform structure and details

## 0. General setup, [files](files), [etc](etc)

First the directiores, the `files` one is for storing the files that terraform uses, currently it consists of a SSH Public key which will be copied over to instances to allow SSH connections. The `etc` directory contains tfvars files with values for terraform variables. In order to use them run `terraform (plan | apply) --var-file ../etc/globals.tfvars --var-file ../etc/secrets.tfvars` in any of the terraform based components described below.

The values prefixed with `TF_VAR` are indicating variables for terraform. This script will later be extended with key for Terraform State Bucket.

In order to run the application as we did, deploy the following components in stated order:

## 1. [state](state) component - bucket for terraform remote state

The state component should be created first. It contains a Storage Account and Storage Container for Terraform state files. By default Terraform state is kept locally in directory from where the apply was done. Having the state in central location, like on Storage Container / Bucket enables sharing information between components - one Terraform apply can use information from other Terraform apply. To apply the state component, enter the directory and run `terraform init && terraform apply -auto-approve --var-file ../etc/globals.tfvars` In the list of outputs you will find a key to the Storage Account, copy it and add to the script with env vars from step 0, in a way shown below:

```bash
export ARM_ACCESS_KEY=TheKeyGoesHere==
```

## 2. [base](base) component - jumpbox

The base component is a place for reources common for all other, eventually we may move the database and service bus here. Right now jumpbox VM is created here, which can be used to general purpose testing, or as the name says as jump-box to a second VM within the cluster subnet which we will create in step 4. The way of applying is the same as for state, enter the directory and run `terraform init && terraform apply -auto-approve --var-file ../etc/globals.tfvars --var-file ../etc/secrets.tfvars` In the secrets.tfvars you can specify CIDRs that will allowed to connect to the new jumpbpox.

## 3. [base-secrets](base-secrets) component - Key Vault for secrets

This component creates the Azure Key Vault for storing secrets used by MHS, you can setup the secrets directly via Terraform or later via Azure Console (for that you will have to modify the access policy to add your Console users ClientID and TenantID ot to the Key Vault, by default only the TF Client and Tenant IDs are added). You can check the [variables.tf](base-secrets/variables.tf) file for the names of variables and set them as environment variables with `TF_VAR_` prefix. This is preferred as opposed to loading them from file as you will not upload it by mistake to repo, and tfvars files do not like multiline strings like PEM certificates.

## 4. [mhs](mhs) component - AKS cluster and other things required by MHS adaptor

This compomenet creates the Vnet, ASK Cluster, Service Bus, Cosmos DB, and a jumpbox that can be used to directly acccess the cluster or test its connectivity. The output from this component will contain login information for the created cluster, you will need to export it as env variable to use kubectl in step 6. Step 5 will take these values automatically from remote state. Once the terraform has applied, run `terraform output kube_config > ~/.kube/aksconfg` and then `export KUBECONFIG=~/.kube/aksconfg`. If you plan to connect you cluster to NHS network in this component you will find the VNet info that you may need to provide to NHS, also you may need to change the `N3_` prefixed variables, as well as `mhs_vnet_cidr` to the CIDR you were provided. The subnets for aks, firewall, jumpbox and redis also need to be in this CIDR.

## 5. [mhs-kube-tf](mhs-kube-tf) - Terraform part of defintions for MHS AKS deployment

This compoment creates a kubernetes secrets resources based on values set in step 3. It uses kubernetes provider for terraform. If the Cluster is publicly accessible apply will look the same as for other components: `terraform init && terraform apply -auto-approve`. If the cluster is private the apply will have to be done from an instance with access to Cluster and Storage Account created in step 1.

## 6. [mhs-kube-yaml](mhs-kube-yaml) - Yaml part of definitions for MHS AKS deployment

This component creates the rest of kubernetes resources - services, pods, and dns config. The cluster is by default accessible from the internet so you'll be able to run `kubectl apply -f mhs-kube-yaml/` from your machine. If you've set your cluster to be private you will need to run this and previos step 5, from a jumpbox within the same network as cluster. Terraform outputs for `base` and `mhs` components will give you IPs of the needed jumpboxes, to connect run `ssh -i .ssh/[jumpbpx_ssh_private_key] -W [mhs_jumpbox] [base_jumpbox]` copy the code and kubectl binary and configure from there.
The DNS routing configured in [dns.yaml](mhs-kube-yaml/dns.yaml) requires the DNS pods to be restarted after the configuration is applied, to do that run: `kubectl -n kube-system rollout restart deployment coredns`
