#!/usr/bin/env bash
# ==============================================================================
# install_on_neo.sh — GCompris tiếng Việt (NEO Installation Script Convention v2)
#
# Human-friendly installer: installs GCompris tiếng Việt's .deb package from GitHub
# Releases. The NEOPlay store does NOT run this script — it installs the same
# .deb directly. This is for developers and manual setups:
#
#   Latest:   curl -fsSL https://raw.githubusercontent.com/<org>/<repo>/main/scripts/install_on_neo.sh | bash
#   Pinned:   bash install_on_neo.sh --version=X.Y.Z
#   Remove:   bash install_on_neo.sh --uninstall
#
# Unmodified standard template apart from the Configuration block and the
# legacy-cleanup step in --uninstall. Spec: neo-play-hub
# docs/conventions/installation-script-convention.md.
#
# COMMAND is gcompris-qt, which ships in the gcompris-qt package this .deb
# depends on — gcompris-vi is a localisation layer and installs no binary of
# its own. Note /usr/games is on a normal user's PATH but not root's
# (/etc/login.defs ENV_PATH vs ENV_SUPATH), so run this as yourself, not as
# root; the script only uses sudo for apt.
# ==============================================================================
set -euo pipefail

# -- Configuration (the only section an app dev edits) -------------------------
REPO="ThingEdu/gcompris-vi"   # GitHub repo that publishes the releases
PKG="gcompris-vi"             # Debian package name (the .deb `Package:` field)
COMMAND="gcompris-qt"         # command on PATH after install (from gcompris-qt)
DEB_ARCH="all"                # .deb architecture suffix: "all" or "arm64"/...

RAW_INSTALL_URL="https://raw.githubusercontent.com/${REPO}/main/scripts/install_on_neo.sh"

# -- Output helpers -------------------------------------------------------------
info()  { echo -e "\033[1;32m[INFO]\033[0m  $*"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m  $*"; }
error() { echo -e "\033[1;31m[ERROR]\033[0m $*" >&2; }

# -- Parse arguments ------------------------------------------------------------
UNINSTALL=false
INSTALL_VERSION=""

for arg in "$@"; do
    case "$arg" in
        --uninstall)  UNINSTALL=true ;;
        --version=*)  INSTALL_VERSION="${arg#*=}"; INSTALL_VERSION="${INSTALL_VERSION#v}" ;;
        # Warn-and-ignore keeps old scripts working when new flags appear.
        *)            warn "Ignoring unknown option: $arg" ;;
    esac
done

SUDO="sudo"
if [ "$(id -u)" -eq 0 ]; then
    SUDO=""
fi

# -- Uninstall -------------------------------------------------------------------
if [ "$UNINSTALL" = true ]; then
    info "Uninstalling $PKG..."
    if command -v apt-get &>/dev/null && dpkg -s "$PKG" &>/dev/null; then
        $SUDO apt-get remove -y "$PKG"
    fi
    # Legacy cleanup: deploy/install_vi.sh was the pre-.deb install path. It
    # patched core.rcc in place (keeping core.rcc.orig), dropped a .qm into the
    # translations directory and copied the voice packs into three locations.
    # None of that is known to dpkg, so apt-get remove leaves it behind.
    R=/usr/share/gcompris-qt/rcc
    if [ -f "$R/core.rcc.orig" ] && [ -z "$(dpkg-divert --listpackage "$R/core.rcc" 2>/dev/null)" ]; then
        info "Restoring core.rcc patched by the old install_vi.sh"
        $SUDO mv -f "$R/core.rcc.orig" "$R/core.rcc"
    fi
    for f in /usr/share/gcompris-qt/translations/gcompris_vi.qm \
             /usr/share/gcompris-qt/translations/gcompris_qt_vi.qm \
             /usr/share/locale/vi/LC_MESSAGES/gcompris_qt.qm; do
        # dpkg -S finds an owner for files the package installed; only sweep
        # the leftovers nothing owns.
        if [ -f "$f" ] && ! dpkg -S "$f" >/dev/null 2>&1; then
            info "Removing leftover $f"
            $SUDO rm -f "$f"
        fi
    done
    for d in "$R"/data2/voices-* "$R"/data3/voices-* \
             "$HOME"/.cache/gcompris-qt/data3/voices-* \
             "$HOME"/.cache/KDE/gcompris-qt/data2/voices-*; do
        [ -d "$d" ] || continue
        for v in "$d"/voices-vi*.rcc; do
            [ -e "$v" ] || continue
            info "Removing leftover $v"
            $SUDO rm -f "$v"
        done
    done

    info "$PKG has been uninstalled."
    exit 0
fi

# -- Pre-flight checks -----------------------------------------------------------
info "Detected architecture: $(uname -m)"

if ! command -v apt-get &>/dev/null; then
    error "This installer requires an apt-based system (Armbian/Debian/Ubuntu)."
    exit 1
fi
if ! command -v curl &>/dev/null; then
    error "curl is required. Install it with: sudo apt-get install curl"
    exit 1
fi

# -- Step 1: Resolve version ------------------------------------------------------
if [ -z "$INSTALL_VERSION" ]; then
    info "Resolving latest release..."
    INSTALL_VERSION="$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
        | sed -nE 's/.*"tag_name": *"v?([^"]+)".*/\1/p' | head -n1)"
    if [ -z "$INSTALL_VERSION" ]; then
        error "Could not resolve the latest release. Check your network,"
        error "or pin a version: bash install_on_neo.sh --version=X.Y.Z"
        exit 1
    fi
fi
info "Installing $PKG $INSTALL_VERSION"

DEB_NAME="${PKG}_${INSTALL_VERSION}_${DEB_ARCH}.deb"
DEB_URL="https://github.com/${REPO}/releases/download/v${INSTALL_VERSION}/${DEB_NAME}"

# -- Step 2: Download --------------------------------------------------------------
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

info "Downloading $DEB_URL"
if ! curl -fSL --progress-bar -o "$TMP_DIR/$DEB_NAME" "$DEB_URL"; then
    error "Download failed. Does release v${INSTALL_VERSION} include ${DEB_NAME}?"
    error "See: https://github.com/${REPO}/releases"
    exit 1
fi

# -- Step 3: Install ----------------------------------------------------------------
# --allow-downgrades keeps the script idempotent when pinning an older version.
info "Installing via apt (dependencies come from the .deb's Depends field)..."
$SUDO apt-get update -qq || true
$SUDO apt-get install -y --allow-downgrades "$TMP_DIR/$DEB_NAME"

# -- Step 4: Verify ------------------------------------------------------------------
if ! command -v "$COMMAND" &>/dev/null; then
    error "Installation failed: '$COMMAND' is not available on PATH."
    exit 1
fi
info "Verified: $(command -v "$COMMAND")"

# -- Done -----------------------------------------------------------------------------
echo ""
info "$PKG $INSTALL_VERSION installed successfully."
echo ""
echo "  Run:        $COMMAND"
echo "  Vietnamese: set LANG=vi_VN.UTF-8 in /etc/default/locale"
echo "  Uninstall:  curl -fsSL $RAW_INSTALL_URL | bash -s -- --uninstall"
echo ""
