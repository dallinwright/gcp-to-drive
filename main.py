import os.path

import google
from google.cloud import storage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# Run beforehand this command
# gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
BUCKET = "test-bucket-99099099"
BUCKET_FOLDER = "/"
LOCAL_DESTINATION_FOLDER = "./files/"
INPUT_FILE = "files.txt"


# Configure auth inside the script
credentials, project = google.auth.default()


# Code snipper from GCP
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


def upload_basic(filename: str):
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    mp4_mime_type = "video/mp4"
    avi_mime_type = "video/x-msvideo"
    webm_mime_type = "video/webm"

    selected_mime_type = ""

    if filename.endswith(".mp4"):
        selected_mime_type = mp4_mime_type
    elif filename.endswith(".avi"):
        selected_mime_type = avi_mime_type
    elif filename.endswith(".webm"):
        selected_mime_type = webm_mime_type

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {'name': filename}
        media = MediaFileUpload(filename,
                                mimetype=selected_mime_type)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


def main():
    lines = []

    if not os.path.exists(LOCAL_DESTINATION_FOLDER):
        os.mkdir(LOCAL_DESTINATION_FOLDER)

    # Read in the file, each individual line is an element in the list called "lines"
    with open(INPUT_FILE) as file:
        lines = [line.rstrip() for line in file]

    # Index stores where we are in the list as we loop, think of it as a counter, as we process one line we
    # say ok we are done, and move to the next line.
    index = 0
    initial_length = len(lines)

    # While there are still lines left to process, continue the program
    while len(lines) > 0:
        # Grab the first line in the list to process
        line = lines[0]
        print(f"Processing line: {index} of {initial_length} ({round((index / initial_length) * 100, 2)}%)")

        # Remove the bucket name from the line, so we can just use the filename
        line = line.replace(f"gs://{BUCKET}/", "")

        try:
            # Download the file
            filename = line.split("/")[-1]

            # using partition()
            # String till Substring
            file_path = f"{line.partition(filename)[0]}"

            if not os.path.exists(file_path):
                os.mkdir(file_path)

            download_blob(BUCKET, line, line)
        except Exception as e:
            print(f"Error downloading file: {line}")
            print(e)
        # upload to google drive

        # Keeps track and removes lines as they are processed. If the program dies, it can start from where it left off.
        lines.pop(0)
        with open('processed.txt', 'w') as f:
            f.writelines(line + '\n' for line in lines)

        index += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
