#!/usr/bin/env bash
set -u

HISTORY=$1
OUTDIR=$2
CHUNK_FILE=$OUTDIR/chunk.txt
TIMESTAMP=$(date "+%F-%H-%M")


# This is needed until https://github.com/galaxyproject/galaxy/pull/16233
# makes it into production
cat << EOF > $OUTDIR/results.json
{
  "tests": []
}
EOF

GALAXY_URL=$(abm config show galaxy | jq -r .url)
GALAXY_KEY=$(abm config show galaxy | jq -r .key)

export DEFAULT_TOOL_TEST_WAIT=600

while read tool_args ; do
  galaxy-tool-test \
    -u $GALAXY_URL \
    -k $GALAXY_KEY \
    -a $GALAXY_KEY \
    -j $OUTDIR/results.json \
    --history-name $HISTORY \
    --no-history-cleanup \
    --verbose \
    --append \
    $tool_args
done < $CHUNK_FILE
echo "history=$HISTORY"
