#!/bin/bash
set -xe

echo $1
cat $1
DURATION=$(cat $1 | grep "real" | grep -o "[0-9][a-z0-9\.]\+")
STATUS=$(cat $1 | grep "STATUS:" | grep -oP '(?<=STATUS\: )\w+')
DATE=$(cat $1 | grep "LAST DEPLOYED:" | grep -oP '(?<=LAST DEPLOYED\: )[^\n]+')
REPORT_DIR=$2
GIT_TOKEN=$3
GIT_BRANCH=main
REMOTE="https://$GITHUB_ACTOR:$GIT_TOKEN@github.com/$GITHUB_REPOSITORY.git"

setup_git() {
  # initializes git info
  git config --local user.email "action@github.com"
  git config --local user.name "GitHub Action"
  git pull
}

push_report() {
  git stash
  git pull origin $GIT_BRANCH
  git stash pop | true
  git add reports/$REPORT_DIR
  git commit -m "Submitting $REPORT_DIR report for deployment from $DATE"
  git push "$REMOTE" "HEAD:$GIT_BRANCH" -v -v
#  git push origin $GIT_BRANCH
}

setup_git
mkdir -p "reports/$REPORT_DIR"
if [ ! -f "reports/$REPORT_DIR/deployments.json" ]; then
    echo '{"results": {"deployments": []}}' > "reports/$REPORT_DIR/deployments.json"
fi
touch "reports/$REPORT_DIR/deployments.html"
python .github/scripts/report_deployment.py $REPORT_DIR "{\"status\": \"$STATUS\", \"time\": \"$DURATION\", \"date\": \"$DATE\"}"
push_report
