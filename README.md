# gcp-to-drive

Bash Equivalent:
```bash
gcloud storage ls -r gs://test-bucket-99099099/ | grep -i "mp3" > files.txt

for line in $(cat files.txt); do
    echo $line
    gcloud storage cp gs://test-bucket-99099099/$line ./files/
done
```
