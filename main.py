import os
import traceback

import google.auth
from google.cloud import storage
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload

# Run beforehand this command
# gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
BUCKET = "test-bucket-99099099"
FOLDER = "/"
EXTENSION = ".mp3"
INPUT_FILE = "files.txt"


def upload_to_drive(local_path, remote_path):
    GDRIVE_FOLDER_IDS = str(os.environ["GDRIVE_FOLDER_IDS"]).split(",")
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
    service = discovery.build('drive', 'v3', credentials=credentials)
    media = MediaFileUpload(local_path)
    print("Starting to upload in the drive")
    response = service.files().create(media_body=media,
                                      body={"name": remote_path.split("/")[-1], "parents": GDRIVE_FOLDER_IDS}).execute()
    print(response)


def download_file_from_gcs(bucket, key):
    print("Downloading key: {} from bucket: {}".format(key, bucket))

    client = storage.Client()

    source_bucket = client.bucket(bucket)

    blob_object = source_bucket.blob(key)

    tmpdir = "./files/{}".format(key.split("/")[-1])

    blob_object.download_to_filename(tmpdir)

    return tmpdir


def drive_upload(event, context):
    try:
        if event["name"][-1] == "/":
            print("Folder: {} is created in the bucket: {}".format(
                event["name"],
                event["bucket"]
            ))
            return

        # Downloading file from GCS
        local_path = download_file_from_gcs(event["bucket"], event["name"])

        # Uploading the file to drive
        upload_to_drive(local_path, event["name"])

    except Exception as e:
        print(traceback.format_exc())


def main():
    lines = []

    # Read in the file, each individual line is an element in the list called "lines"
    with open(INPUT_FILE) as file:
        lines = [line.rstrip() for line in file]

    # Index stores where we are in the list as we loop, think of it as a counter, as we process one line we
    # say ok we are done, and move to the next line.
    index = 0

    # While there are still lines left to process, continue the program
    while len(lines) > 0:
        line = lines[0]

        filename = line.split("/")[-1]
        downloaded_filename = download_file_from_gcs(BUCKET, filename)

        print(downloaded_filename)

        # Keeps track and removes lines as they are processed. If the program dies, it can start from where it left off.
        lines.pop(0)
        with open('processed.txt', 'w') as f:
            f.writelines(line + '\n' for line in lines)

        index += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
