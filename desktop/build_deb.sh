#!/bin/bash
set -e

# Configuration
VERSION="1.1.0"
APP_NAME="phonedock-desktop"
PKG_NAME="${APP_NAME}_${VERSION}_amd64"
BUILD_DIR="build_deb"
DIST_DIR="dist"

echo "Building PhoneDock v${VERSION}..."

# 1. Clean previous builds
rm -rf "$BUILD_DIR"
rm -rf "$DIST_DIR"
mkdir -p "$BUILD_DIR"

# 2. Run PyInstaller
echo "Running PyInstaller..."
./venv/bin/pyinstaller --noconfirm --onefile --windowed \
    --name "phonedock" \
    --add-data "discovery.py:." \
    --add-data "connection.py:." \
    --add-data "video_view.py:." \
    --add-data "onboarding_view.py:." \
    main.py

# 3. Create Debian structure
echo "Creating Debian package structure..."
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/DEBIAN"

cp "$DIST_DIR/phonedock" "$BUILD_DIR/usr/bin/"
cp "phonedock.desktop" "$BUILD_DIR/usr/share/applications/"

# 4. Create control file
cat > "$BUILD_DIR/DEBIAN/control" <<EOF
Package: phonedock-desktop
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: PhoneDock Dev <dev@phonedock.com>
Description: Turn your Android phone into a native extension of your Windows PC.
 PhoneDock is a local-first Android device bridge that allows you to
 interact with your physical Android phone directly from your desktop.
EOF

# 5. Build .deb
echo "Packaging .deb..."
dpkg-deb --build "$BUILD_DIR" "${DIST_DIR}/${PKG_NAME}.deb"

echo "Build complete: ${DIST_DIR}/${PKG_NAME}.deb"
