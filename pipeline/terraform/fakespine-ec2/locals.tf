locals {
  mhs_inbound_url = length(var.inbound_server_base_url) == 0 ? data.terraform_remote_state.mhs.outputs.inbound_lb_domain_name : var.inbound_server_base_url

    fake_spine_base_environment_variables = [
    {
      name = "INBOUND_SERVER_BASE_URL",
      value = var.inbound_server_base_url
    },
    {
      name = "FAKE_SPINE_OUTBOUND_DELAY_MS",
      value = var.outbound_delay_ms
    },
    {
      name = "FAKE_SPINE_INBOUND_DELAY_MS",
      value = var.inbound_delay_ms
    }
  ]

  fake_spine_secret_environment_variables = [
    {
      name = "FAKE_SPINE_PRIVATE_KEY",
      value = var.fake_spine_private_key
    },
    {
      name = "FAKE_SPINE_CERTIFICATE",
      value = var.fake_spine_certificate
    },
    {
      name = "FAKE_SPINE_CA_STORE",
      value = var.fake_spine_ca_store
    },
    {
      name = "MHS_SECRET_PARTY_KEY",
      value = var.party_key_arn
    }
  ]
}
