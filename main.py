import os
import traceback

import google.auth
from google.cloud import storage
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload

# Run beforehand this command
# gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
BUCKET = "test-bucket-99099099"
BUCKET_FOLDER = "/"
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


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


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
    initial_length = len(lines)

    # While there are still lines left to process, continue the program
    while len(lines) > 0:
        line = lines[0]

        # Helpful progress display
        print(f"Processing line: {index} of {initial_length} ({round((index / initial_length) * 100, 2)}%)")

        filename = line.split("/")[-1]
        os.mkdir(f"./files")
        destination = f"./files/{filename}"

        download_blob(BUCKET, line, destination)

        # Keeps track and removes lines as they are processed. If the program dies, it can start from where it left off.
        lines.pop(0)
        with open('processed.txt', 'w') as f:
            f.writelines(line + '\n' for line in lines)

        index += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
