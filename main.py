import os.path

import google.auth
from google.cloud import storage

# Run beforehand this command
# gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt
BUCKET = "test-bucket-99099099"
BUCKET_FOLDER = "/"
LOCAL_DESTINATION_FOLDER = "./files"
INPUT_FILE = "files.txt"

# Configure auth inside the script, this will use the local user's credentials
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


def main():
    # Needed for a code health standpoint, as we are assiging the lines to
    # process below. This is just a placeholder.
    lines = []

    # Make sure the output path exists, if not create it
    if not os.path.exists(LOCAL_DESTINATION_FOLDER):
        os.mkdir(LOCAL_DESTINATION_FOLDER)

    # Read in the file, each individual line is an element in the list called
    # "lines"
    with open(INPUT_FILE) as file:
        lines = [line.rstrip() for line in file]

    # Index stores where we are in the list as we loop, think of it as a counter, as we process one line we
    # say ok we are done, and move to the next line.
    index = 0
    initial_length = len(lines)

    print(f"Total lines to process: {initial_length}")

    # While there are still lines left to process, continue the program
    while len(lines) > 0:
        # Grab the first line in the list to process
        file_to_download = lines[0]
        print(
            f"Processing line: {index} of {initial_length} ({round((index / initial_length) * 100, 2)}%)")

        # Remove the bucket name from the line, so we can just use the filename
        file_to_download = file_to_download.replace(f"gs://{BUCKET}/", "")

        try:
            # Get just the filename
            filename = file_to_download.split("/")[-1]

            # using partition()
            # String till Substring, this allows us to conserve the path
            file_path = f"{LOCAL_DESTINATION_FOLDER}/{file_to_download.partition(filename)[0]}"

            if not os.path.exists(file_path):
                os.mkdir(file_path)

            destination_file_name = f"{LOCAL_DESTINATION_FOLDER}/{file_to_download}"

            print(
                f"Downloading file: {file_to_download} to {destination_file_name}...")

            download_blob(BUCKET, file_to_download, destination_file_name)

            print(
                f"Downloaded file: {file_to_download} to {destination_file_name}")
        except Exception as e:
            print(f"Error downloading file: {file_to_download}")
            print(e)
            continue

        # Keeps track and removes lines as they are processed. If the program
        # dies, it can start from where it left off.
        try:
            lines.pop(0)
            with open('files.txt', 'w') as f:
                f.writelines(line + '\n' for line in lines)

            print(f"Removed line: {file_to_download}")
        except Exception as e:
            print(f"Error removing line: {file_to_download}")
            print(e)

        index += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
