import {
  to = module.cloud_run.google_service_account.manager_cr_sa
  id = "projects/evalio-462923/serviceAccounts/manager-cr-sa@evalio-462923.iam.gserviceaccount.com"
}

import {
  to = module.cloud_run.google_project_iam_member.manager_storage_access
  id = "evalio-462923 roles/storage.objectAdmin serviceAccount:manager-cr-sa@evalio-462923.iam.gserviceaccount.com"
}

import {
  to = module.cloud_run.google_project_iam_member.manager_artifact_registry_reader
  id = "evalio-462923 roles/artifactregistry.reader serviceAccount:manager-cr-sa@evalio-462923.iam.gserviceaccount.com"
}

import {
  to = module.cloud_run.google_project_iam_member.manager_token_creator
  id = "evalio-462923 roles/iam.serviceAccountTokenCreator serviceAccount:manager-cr-sa@evalio-462923.iam.gserviceaccount.com"
}
