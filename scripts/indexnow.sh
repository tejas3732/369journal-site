#!/bin/bash
# Tell IndexNow (Bing, Yandex, Seznam, Naver and others) that the site's pages changed.
# Reads every URL from sitemap.xml. Usage: bash scripts/indexnow.sh
set -euo pipefail
cd "$(dirname "$0")/.."

HOST="369journal.app"
KEY="741881a2eb57ba5edc40033ef15e3c23"

URLS=$(grep -o '<loc>[^<]*</loc>' sitemap.xml | sed -e 's#<loc>##' -e 's#</loc>##' | awk '{printf "%s\"%s\"", (NR>1?",":""), $0}')
BODY="{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"https://$HOST/$KEY.txt\",\"urlList\":[$URLS]}"

STATUS=$(curl -s -o /dev/null -w '%{http_code}' -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" --data "$BODY")
echo "IndexNow responded HTTP $STATUS for $(echo "$URLS" | tr ',' '\n' | wc -l | tr -d ' ') URLs"
# 200 = accepted, 202 = accepted (key check pending). Anything else is a problem.
[ "$STATUS" = "200" ] || [ "$STATUS" = "202" ]
