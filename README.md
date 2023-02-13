# GCP Storage Bucket Downloader

## Prerequisites

1. Python 3.6+
2. Google Cloud CLI utility installed and configured

### Install the python dependencies

Open a terminal and change directory to the root of this project. Then run the following command:

`pip install -r requirements.txt`

First, to prepare a total list of files to process in the format needed by the script, running the following command from
the same directory as the script:

```bash
gcloud storage ls -r gs://test-bucket-99099099/ > files.txt
```

## Running the script

Open the script and take a look at lines 8-11, these are called "global variables" and are used to configure the script.
Simply replace these values with your desired values and call the script like so.

```bash
python3 ./main.py
```

## Troubleshooting

If any errors are occurred, see the logs in the terminal for the root cause.

The script itself keeps a "files to be processed" log in the files.txt and updates it in on the fly after files have been
downloaded. If there is a problem, the script will stop and you can resume the download by running the script again.

One thing to check if the download dies, is the size of the file. Perhaps the time taken is much larger then waited for,
or the file is corrupted. In that case, delete the local copy and rerun the script.

If the rerun of the script fails again, feel free to download the singular file from the UI, remove the line from the files.txt
and resume the script.

If for any reason something unforseen happens, you can always delete the files.txt and start over. You can also
feel free to edit the script if you feel up for it.
