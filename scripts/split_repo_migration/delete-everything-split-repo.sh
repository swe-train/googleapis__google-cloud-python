#!/bin/bash
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script was written as part of a project to migrate
# split repositories to a mono repository google-cloud-python.
# This script will delete all files in a split repository and
# update the README to indicate that the repository is archived.

# sourced vs execution detection obtained from https://stackoverflow.com/a/28776166
SOURCED=0
if [ -n "$ZSH_VERSION" ]; then
  case $ZSH_EVAL_CONTEXT in *:file) SOURCED=1;; esac
elif [ -n "$KSH_VERSION" ]; then
  [ "$(cd -- "$(dirname -- "$0")" && pwd -P)/$(basename -- "$0")" != "$(cd -- "$(dirname -- "${.sh.file}")" && pwd -P)/$(basename -- "${.sh.file}")" ] && SOURCED=1
elif [ -n "$BASH_VERSION" ]; then
  (return 0 2>/dev/null) && SOURCED=1
else # All other shells: examine $0 for known shell binary filenames.
     # Detects `sh` and `dash`; add additional shell filenames as needed.
  case ${0##*/} in sh|-sh|dash|-dash) SOURCED=1;; esac
fi

(( SOURCED -ne 1 )) || { \
  echo "Please do not source this script, but execute it directly."
  return -10
}

# We require executing the script so that an early exit (explicitly or via -e)
# does not kill the user's shell.

# `-e` enables the script to automatically fail when a command fails
set -e

# Ensure that both arguments are provided
if [ $# -lt 2 ]
then
  echo "Usage: $0 <split-repo-name> <target-path>

Args:
   split-repo-name: The name of the split repository. For example, \`python-access-approval\`.
   artifact-name: The name of the artifact on PyPI. For example, \`google-cloud-access-approval\`.
"
  exit 1
fi

# The name of the split repository. (e.g. python-access-approval)
SPLIT_REPO=$1
# The name of the artifact on PyPI. (e.g. google-cloud-access-approval)
ARTIFACT_NAME=$2

SPLIT_REPO_DIR="/tmp/delete-library.${SPLIT_REPO}.$(date +"%Y-%m-%d.%H:%M:%S")"

git clone "git@github.com:googleapis/${SPLIT_REPO}.git" $SPLIT_REPO_DIR

cd $SPLIT_REPO_DIR

# Create a git branch
git checkout -b 'migrate-library'

# Quick check to make sure there are no handwritten samples. 
# Handwritten samples should be migrated to python-docs-samples before repository code is deleted.
# Exclude the samples/generated_samples/* directory which contains autogenerated samples.
NUM_PY_SAMPLES_FILES=$(find samples -type f -name "*.py" ! -path "samples/generated_samples/*" | grep -v "nox.*\.py" | grep -v "__init__\.py" | wc -l)

# Fail if there are handwritten samples.
if [[ $NUM_PY_SAMPLES_FILES -ne "0" ]]; then
  echo "Please migrate handwritten samples to python-docs-samples before deleting the source."
  exit 1
fi

# Fail if this repository has a customized version of the autogenerated code.
# This specific check is to ensure that autogenerated files are not excluded.
STANDARD_EXCLUDES=$(grep owlbot.py -e 'excludes=\["\*\*/gapic_version.py"]' | wc -l)

if [[ $STANDARD_EXCLUDES -ne "1" ]]; then
  echo "A non-standard value for \`excludes\` is not supported in the repository"
  exit 1
fi

# Fail if this repository has a customized version of the autogenerated code.
# This specific check is to make sure that the owlbot.py file does not contain `s.replace` or `sed`
# which has historically been used to modify the generated code.
NUM_STRING_REPLACEMENTS=$(grep owlbot.py -e 's.replace' | wc -l)
if [[ $NUM_STRING_REPLACEMENTS -ne "0" ]]; then
  echo "s.replace() is not supported in the python mono repository"
  exit 1
fi

NUM_STRING_REPLACEMENTS=$(grep owlbot.py -we 'sed' | wc -l)
if [[ $NUM_STRING_REPLACEMENTS -ne "0" ]]; then
  echo "s.replace() is not supported in the python mono repository"
  exit 1
fi

# Delete everything except LICENSE, SECURITY.md, README.rst, .git and .repo-metadata.json
ls -A | grep -v 'LICENSE\|SECURITY.md\|README.rst\|.git\|.repo-metadata.json' | xargs rm -rf

# Additional cleanup for files/folders with .git prefix
rm -rf .github
rm -rf .gitignore

# Append a prefix to the README to state that this repository has been archived and the source has moved.
README_RST="${SPLIT_REPO_DIR}/README.rst"

if [[ ! -f $README_RST ]]; then
  echo "README.rst file not found"
  exit 1
fi

{ cat - $README_RST | sponge $README_RST ; } << EOF
:**NOTE**: **This github repository is archived. The repository contents and history have moved to** \`google-cloud-python\`_.

.. _google-cloud-python: https://github.com/googleapis/google-cloud-python/tree/main/packages/${ARTIFACT_NAME}


EOF

# Stage all files
git add .

# Commit all files
git commit -m 'build: update README to indicate that source has moved and delete all files'

# Push the branch. Note force push option is used to allow this script to be called multiple times.
git push origin -f migrate-library
