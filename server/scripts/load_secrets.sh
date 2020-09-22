#!/bin/bash

gcp_secret_prefix="secret:google_secret_manager:"

# load secrets from Google Secret Manager if configured
for i in $(printenv | grep ${gcp_secret_prefix})
do
  env_var_name=$(echo ${i} | cut -d "=" -f 1)
  env_var_value=$(echo ${i} | cut -d "=" -f 2)
  if [[ ${env_var_value} == ${gcp_secret_prefix}* ]]
  then
    # remove prefix
    secret_identifier=$(echo ${env_var_value} | sed -e "s/${gcp_secret_prefix}//g")

    # secret identifiers should look like: "project_id/secret_name"
    project_id=$(echo ${secret_identifier} | cut -d "/" -f 1)
    secret_name=$(echo ${secret_identifier} | cut -d "/" -f 2)

    secret_value="$(gcloud secrets versions access --secret=${secret_name} latest --project=${project_id})"

    export $env_var_name="$secret_value"
  fi
done
