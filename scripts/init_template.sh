#!/usr/bin/env bash
# Post-fork initializer: rename the placeholder package and neutral values
# to your project's identity. Run once, from the repository root, right after
# cloning/forking this template.
#
# Usage: ./scripts/init_template.sh <project-name> <package-name> <email>
# Example:
#   ./scripts/init_template.sh my-dbx-project my_dbx_package me@example.com

set -euo pipefail

PROJECT_NAME="${1:?Usage: init_template.sh <project-name> <package-name> <email>}"
PACKAGE_NAME="${2:?Usage: init_template.sh <project-name> <package-name> <email>}"
EMAIL="${3:?Usage: init_template.sh <project-name> <package-name> <email>}"

echo "Initializing template:"
echo "  project name : $PROJECT_NAME"
echo "  package name : $PACKAGE_NAME"
echo "  email        : $EMAIL"

# 1. Rename the package directory.
if [ -d "src/package_name" ]; then
  mv src/package_name "src/$PACKAGE_NAME"
else
  echo "src/package_name already renamed; skipping directory rename."
fi

# 2. Global textual replace across code, tests, docs and configs.
FILES=$(grep -rl "package_name\|dbxprojectstemplate\|YOUR-EMAIL" \
  --include="*.py" --include="*.yml" --include="*.yaml" --include="*.toml" \
  --include="*.md" --include="*.sh" \
  src tests docs resources tasks .github AGENTS.md Taskfile.yml databricks.yml 2>/dev/null || true)

for f in $FILES; do
  sed -i.bak \
    -e "s/dbxprojectstemplate/$PROJECT_NAME/g" \
    -e "s/package_name/$PACKAGE_NAME/g" \
    -e "s/YOUR-EMAIL/$EMAIL/g" \
    "$f"
  rm -f "$f.bak"
done

# 3. Remind about the remaining manual TODOs.
echo
echo "Done. Manual steps left (search for TODO(post-fork)):"
echo "  - databricks.yml: workspace host(s), prod root_path, permissions"
echo "  - pyproject.toml: authors, dependencies"
echo "  - src/$PACKAGE_NAME/sample_data.py: replace the sample table with your domain"
grep -rn "TODO(post-fork)" . --include="*.yml" --include="*.toml" || true
echo "Then commit the rename: git add -A && git commit -m 'chore: initialize project from template'"
