#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# | Script for generating master documentation ROS2 packages |
# ------------------------------------------------------------

# Usage:
# Place this script into your src\docs folder and run it
# script will go through src and find all the packages, create separate documentations
# and combine it in master project
#
# IMPORTANT!!! 
# BE SURE THAT PACKAGE_NAME AND PROJECT_PACKAGE_NAME AND DIRECTORY OF THE PACKAGE ARE THE SAME 
# 
# created by Artyom Tuzov

# Dir flags
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROS_WS_DIR="$SCRIPT_DIR/.."
BUILD_DIR="$SCRIPT_DIR/build"
MASTER_DIR="$SCRIPT_DIR/master"
MASTER_SRC="$MASTER_DIR/source"
MASTER_BUILD="$MASTER_DIR/build"
PROJECT_NAME="Overlord100"

# Clear previous documentation
echo "==> Cleaning old directories..."
rm -rf "$BUILD_DIR" "$MASTER_DIR"
mkdir -p "$BUILD_DIR" "$MASTER_SRC"

echo "==> Found ROS2 workspace: $ROS_WS_DIR"

# Separate generation for every package
echo "==> Generating rosdoc2 documentation"
PKG_PATHS=( $(find "$ROS_WS_DIR" -name "package.xml" -exec dirname {} \;) )
PKG_NAMES=()
for PKG_PATH in "${PKG_PATHS[@]}"; do
    PKG_NAME=$(basename "$PKG_PATH")
    PKG_NAMES+=("$PKG_NAME")
    echo "- Building docs for package '$PKG_NAME'"
    rosdoc2 build \
        --package-path "$PKG_PATH" \
        --output-directory "$BUILD_DIR/$PKG_NAME"
done

# Initialize Sphinx master project
if [ ! -f "$MASTER_SRC/conf.py" ]; then
    echo "==> Initializing Sphinx project in $MASTER_DIR"
    sphinx-quickstart "$MASTER_DIR" \
        --quiet \
        --project "$PROJECT_NAME Master Docs" \
        --author "$PROJECT_NAME Team" \
        --release "0.1" \
        --language "ru" \
        --makefile \
        --no-batchfile \
        --sep
else
    echo "==> Sphinx project already initialized"
fi

# Copy docs into Sphinx source
echo "==> Copying rosdoc2 outputs into Sphinx source"
for PKG_NAME in "${PKG_NAMES[@]}"; do
    SRC_DIR="$BUILD_DIR/$PKG_NAME"
    DST_DIR="$MASTER_SRC/$PKG_NAME"
    echo "- Copying $SRC_DIR -> $DST_DIR"
    rm -rf "$DST_DIR"
    cp -a "$SRC_DIR" "$DST_DIR"
done

# 5) Генерация master/source/index.rst с raw HTML ссылками
echo "==> Generating master index.rst with external links"
cat > "$MASTER_SRC/index.rst" <<EOF
.. $PROJECT_NAME Master Documentation

Main page of master-documentation
====================================

Each package are shown below:

.. raw:: html

   <ul>
EOF

for PKG_NAME in "${PKG_NAMES[@]}"; do
    echo "   <li><a href=\"$PKG_NAME/$PKG_NAME/index.html\">$PKG_NAME</a></li>" >> "$MASTER_SRC/index.rst"
done

cat >> "$MASTER_SRC/index.rst" <<EOF
   </ul>
EOF

# Theme conf and html adding
CONF="$MASTER_SRC/conf.py"
echo "==> Configuring theme and html_extra_path in conf.py"
cat >> "$CONF" <<EOF

# -----------------------------------------------------------------------------
# Theme and extra paths
# -----------------------------------------------------------------------------
import os

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 1,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
# Use the whole dir as _static source
html_extra_path = ['.']
# -----------------------------------------------------------------------------
EOF

# Building
echo "==> Building master documentation (make html)"
make -C "$MASTER_DIR" html

echo "==> Done! Open '$MASTER_BUILD/index.html' to view the combined docs."
