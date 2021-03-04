# Deployment of MHS Adaptor on Microsoft Azure

## Terraform

This directory contains the [Terraform](https://www.terraform.io/) and [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) configurations used to deploy instances of the MHS
application to **Azure**. For AWS see [mhs-environment/README](../mhs-environment/README.md).

This configuration will create a full test environment running an MHS application.

## Known Limitations

* There may be problems with running terraform apply and kubectl  when the AKS cluster is set as private. In this case the configuration can only be applied from an instance within the same network as the cluster. Yamls and kubectl binary can be copied and apply correctly. Applying terraform the same way require some additional work like allowing more hostnames in firewall, and allowing access to Azure Storage Account from the instance

* The adaptors deployed using these scripts do not read secrets directly from the Azure Key Vault. Secrets are read from a tfvars and written to the key vault. They are also written into the Terraform state output. The output is then used to create secrets in AKS. 

## Terraform structure and details

### 1. [state](state) component - bucket for terraform remote state

The state component should be created first. It contains a Storage Account and Storage Container for Terraform state files. By default Terraform state is kept locally in directory from where the apply was done. Having the state in central location, like on Storage Container / Bucket enables sharing information between components - one Terraform apply can use information from other Terraform apply.

### 2. [base](base) component - jumpbox

The base component is a place for reources common for all other, eventually we may move the database and service bus here. Right now jumpbox VM is created here, which can be used to general purpose testing, or as the name says as jump-box to a second VM within the cluster subnet which we will create as part of mhs component

### 3. [base-secrets](base-secrets) component - Key Vault for secrets

This component creates the Azure Key Vault for storing secrets used by MHS, you can setup the secrets directly via Terraform or later via Azure Console (for that you will have to modify the access policy to add your Console users ClientID and TenantID ot to the Key Vault, by default only the TF Client and Tenant IDs are added). You can check the [variables.tf](base-secrets/variables.tf) file for the names of variables and set them as environment variables with `TF_VAR_` prefix. This is preferred as opposed to loading them from file as you will not upload it by mistake to repo, and tfvars files do not like multiline strings like PEM certificates.

### 4. [mhs](mhs) component - AKS cluster and other things required by MHS adaptor

This compomenet creates the Vnet, ASK Cluster, Service Bus, Cosmos DB, and a jumpbox that can be used to directly acccess the cluster or test its connectivity. The output from this component will contain login information for the created cluster, you will need to export it as env variable to use kubectl in step 6. Step 5 will take these values automatically from remote state. If you plan to connect you cluster to NHS network in this component you will find the VNet info that you may need to provide to NHS, also you may need to change the `N3_` prefixed variables, as well as `mhs_vnet_cidr` to the CIDR you were provided. The subnets for aks, firewall, jumpbox and redis also need to be in this CIDR.

### 5. [mhs-kube-tf](mhs-kube-tf) - Terraform part of defintions for MHS AKS deployment

This compoment creates a kubernetes secrets resources based on values set in step 3. It uses kubernetes provider for terraform.

### 6. [mhs-kube-yaml](mhs-kube-yaml) - Yaml part of definitions for MHS AKS deployment

This component creates the rest of kubernetes resources - services, pods, and dns config. It is supposed to be applied via `kubectl`

## Deploying MHS Manually

To manually deploy the MHS you must ensure that Terraform can authenticate to Azure. See the 
[authentication section of the Terraform Azure documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#authenticating-to-azure)
for details. If running this on your local machine, the simplest option is the "Service Principal with Client Secret" method using environment variables. You must define these variables on your local machine using values from your Azure subscription. 

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

The seeting for image source is in [mhs-kube-yaml](mhs-kube-yaml) [service]-deployment.yaml files, you can change it to point at different image if needed.

The home directory for all commands below is the location of this readme file.

Once you have configured Azure authentication, you can run the following commands to deploy the MHS.

* The state bucket:
  * Change the directory to state component: `cd state`
  * Run terraform init, this will download all required terraform modules and providers for this compoment: `terraform init`
  * Run terraform plan, to see if the syntax does not have errors, and all variables are set correctly: `terraform plan -var-file=../etc/global.tfvars`
  * Run terraform apply: `terraform apply -auto-approve --var_file=../etc/globals.tf`
  * The output from this component will contain a key to Storage Account which will be needed for Terraform applies. The key will be written under `tf_state_account_key` copy it and add to your script that exports the credentials for Azure under `ARM_ACCESS_KEY`:

  ```bash
  export ARM_ACCESS_KEY=TheKeyGoesHere==
  ```

  * Go back to top directory `cd ..`
  * load the values from credentials script again: `. ./export_azure_credentials.sh`

* The base component:
  * As part of this component you will create a jumpbox instance, create a SSH key and put the public part in `files/admin_ssh_key.pub` and the private part in `~/.ssh/admin_ssh_key` This is required to perform the initial configuration of the jumpbox.
  * Change the directory to base component: `cd base`
  * Run terraform init: `terraform init`
  * Run terraform plan: `terraform plan --var-file=../etc/global.tfvars --var-file=../etc/secrets.tfvars`
  * Run terraform apply: `terraform apply -auto-approve --var_file=../etc/global.tfvars --var_file=../etc/secrets.tfvars`
  * The output from this component will have public IP address of jumpbox instance within Azure, which you could later use for testing purposes.
  * Go back to to top directory: `cd ..`

* The base-secrets component:
  * Change the directory to base-secrets: `cd base-secrets`
  * Run terraform init: `terraform init`
  * In this component you set secret values that will be used by Cluster Pods, some multiline values like certificates could not be provided by files so it is advised to set them as environment variables beforehead. The way to do that is to add `TF_VAR_` prefix to exported variable: `export TF_VAR_secret_mhs_ca_chain="----BEGIN CERTIFICATE..."` will set the value for `secret_mhs_ca_chain` variable.
  * Run terraform plan: `terraform plan --var_file=../etc/globals.tfvars --var_file=../etc/secrets.tfvars`
  * Run terraform apply:  `terraform apply -auto-approve --var_file=../etc/globals.tfvars --var_file=../etc/secrets.tfvars`
  * Go back to to top directory: `cd ..`

* The mhs component:
  * Change the directory to mhs: `cd mhs`
  * Run terraform init: `terraform init`
  * Run terraform plan: `terraform plan --var_file=../etc/globals.tfvars`
  * Run terraform apply `terraform apply -auto-approve --var_file=../etc/globals.tfvars`
  * The output of this component will have information of the AKS Cluster, Cosmos DB - Mongo, Redis Cache, Service Bus and also a second jumpbox instance located inside the same Vnet as AKS Cluster.
  * After applying this component you can set your credentials for AKS Cluster, run `terraform output kube_config > [chosen location for the config]/aksconfig
  * Then export the path so `kubectl` will know where to look for it: `export KUBECONFIG=[chosen location for the config]/aksconfig`
  * Go back to top directory: `cd ..`

* The mhs-kube-tf component:
  * Change the directory to mhs-kube-tf: `cd mhs-kube-tf`
  * Run terraform init: `terraform init`
  * Run terraform plan: `terraform plan --var_file=../etc/globals.tfvars`
  * Run terraform apply: `terraform apply -auto-approve --var_file=../etc/globals.tfvars`
  * This will create Kubernetes Secrets resources based on secrets we set in base-secrets component.
  * You can verify if the secrets were created by running: `kubectl get secrets`
  * Go back to top directory: `cd ..`

* The mhs-kube-yaml:
  * Change the directory to mhs-kube-yaml: `cd mhs-kube-yaml`
  * Run `kubectl apply -f .`
  * The above will create all services and pods that run the MHS application.
  * The DNS settings after applying require the restart of CoreDNS pods, do it by running: `kubectl -n kube-system rollout restart deployment coredns`
  * You can check the services: `kubectl get services` and pods: `kubectl get pods`. If some pod requires investigation you can check its logs by running: `kubectl logs [name of the pod, ex: inbound-76f586f7b5-cdgnc]`
  * On the services listing you will see the IP that the loadbalancer for each services use. You can also check the IPs of particular pods by running `kubectl get pods -o wide`

## Your HSCN VNet Config

The connection to HSCN may be different for each use case. The process for us was as follows:

* Request the connection
* State clearly that you need a two-way routable connection. NATed connection will work only for synchronous workflow MHS requests. Any Async type requests will not work fully with NATed connection, as SPINE will not have a way to initiate connection to mhs-inbound.
* Setup the mhs component with correct CIDR for VNet, Next-hop for routing. There are variables for each setting.
* Create the VNet and subnets, provide the VNet ID to NHS.
* NHS has created a peering conection to our VNet. This may also be a VPN-like connection like ExpressRoute which may require some configuration on the MHS side. In our case the peering was ready to use.
* Configure the DNS and check the IP Prefixes of hosts you wish to connect to over HSCN connection. The routing has to be in place for both the HSCN services and Azure services to work at the same time. Add these prefixes to `N3_prefixes` variable.
* Apart from IP routing the DNS requests also have to be routed, Azure provided DNS will not resolve HSCN hosts, and HCSN DNS will not resolve Azure hosts. The [dns.yaml](mhs-kube-yaml/dns.yaml) does the routing - it forwards any `*.nhs.uk` DNS request to HSCN DNS servers, leaving other requsts to be resolved by Azure DNS.
* Set the IP of MHS Inbound loadbabalancer to registered IP you've received from NHS. This is done in `mhs-kube-yaml/inboud-service.yaml`
