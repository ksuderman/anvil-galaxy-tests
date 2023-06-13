#!/usr/bin/env bash
set -u

if [[ $# != 2 ]] ; then
  echo "USAGE: $0 /path/to/output/directory"
  exit 1
fi

HISTORY=$1
OUTDIR=$2
CHUNK_FILE=$OUTDIR/chunk.txt
TIMESTAMP=$(date "+%F-%H-%M")

#history="anvil-test-$TIMESTAMP"
#echo "History is $history"
cat << EOF > $OUTDIR/results.json
{
  "tests": []
}
EOF

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
