# For tests, run emulator in memory-only mode so that it doesn't overwrite local
# development data and so the /reset endpoint works.
gcloud beta emulators datastore start \
  --host-port="localhost:8082" \
  --consistency=1.0 \
  --no-store-on-disk
