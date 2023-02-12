# gcp-to-drive

Bash Equivalent:

```bash
gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
```

gcloud iam service-accounts create gcs-drive-function-sa

gcloud projects add-iam-policy-binding <PROJECT_ID> --member=serviceAccount:gcs-drive-function-sa@<PROJECT_ID>.iam.gserviceaccount.com --role=roles/storage.objectViewer

gcloud projects add-iam-policy-binding anthid-development --member=serviceAccount:gcs-drive-function-sa@anthid-development.iam.gserviceaccount.com --role=roles/storage.objectViewer