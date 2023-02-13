# GCP Storage Bucket Downloader

## Pre-requisites

1. Python 3.6+
2. Google Cloud CLI utility installed and configured


First, to prepare a total list of files to process in the format needed by the script, running the following command from
the same directory as the script:

```bash
gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
```

# Running the script

Open the script and take a look at lines 8-11, these are called "global variables" and are used to configure the script.
Simply replace these values with your desired values and call the script like so.

```bash
python3 ./main.py
```