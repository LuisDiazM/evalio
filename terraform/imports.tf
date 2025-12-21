# import {
#   to = module.cloud_run.google_service_account.manager_cr_sa
#   id = "projects/${var.project_id}/serviceAccounts/manager-cr-sa@${var.project_id}.iam.gserviceaccount.com"
# }

# import {
#   to = module.cloud_run.google_project_iam_member.manager_storage_access
#   id = "${var.project_id} roles/storage.objectAdmin serviceAccount:manager-cr-sa@${var.project_id}.iam.gserviceaccount.com"
# }

# import {
#   to = module.cloud_run.google_project_iam_member.manager_artifact_registry_reader
#   id = "${var.project_id} roles/artifactregistry.reader serviceAccount:manager-cr-sa@${var.project_id}.iam.gserviceaccount.com"
# }

# import {
#   to = module.cloud_run.google_project_iam_member.manager_token_creator
#   id = "${var.project_id} roles/iam.serviceAccountTokenCreator serviceAccount:manager-cr-sa@${var.project_id}.iam.gserviceaccount.com"
# }
