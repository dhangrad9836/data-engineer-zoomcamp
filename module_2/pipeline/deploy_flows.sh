#!/bin/bash
KESTRA_URL="http://localhost:8080"
KESTRA_USER="admin@kestra.io"
KESTRA_PASS="Admin1234!"
FLOWS_DIR="flows"

echo "Importing all flows into Kestra..."
echo ""

for flow in $FLOWS_DIR/*.yaml; do
  echo "Importing $flow..."
  curl -s -X POST \
    -u "$KESTRA_USER:$KESTRA_PASS" \
    "$KESTRA_URL/api/v1/flows/import" \
    -F "fileUpload=@$flow"
  echo ""
done

echo "All flows imported!"
