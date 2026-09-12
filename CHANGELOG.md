# Changelog

Follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
[Semantic Versioning](https://semver.org/).

## [0.2.0] — 2026-09-12

First `.deb` package. v0.1.0 shipped the translation and voices as loose files;
from this release it installs through `apt` and depends on `gcompris-qt-data`.

### Added

- **Debian package `gcompris-vi`** (`Architecture: all`) — builds anywhere,
  installs on NEO One (ARM64). Contains no compiled code.
- **Vietnam map with the Hoàng Sa and Trường Sa archipelagos**, patched into the
  *Find the country on the map* activity (Decree 18/2020/NĐ-CP, Article 11(2)).
- **34-province administrative map** for *Find the region on the map* — GCompris
  upstream has none.
- **Two Làng Maker mini apps**: *Làng Maker* (`lang_maker`) and *Đối Đôi Làng*
  (`lang_doidoi`, a 57-image Dobble-style deck with three game modes).
- **`scripts/install_on_neo.sh`** — one-line install per NEO Installation Script
  Convention v2, including cleanup of the older `deploy/install_vi.sh` layout.
- **`tools/them_tieng_viet.py`** — the `LanguageList.qml` patch split out into
  its own tool, shared by `install_vi.sh` and the package's postinst.

### Changed

- **`tools/rcc_repack.py` writes the `.rcc` format in pure Python**, no longer
  shelling out to Qt's `rcc`. This is what lets postinst patch `.rcc` files on
  the NEO One itself with nothing but `python3`.
- **Upgrading GCompris no longer drops the Vietnamese localisation.** The five
  `.rcc` files owned by `gcompris-qt-data` are patched through `dpkg-divert`,
  and a dpkg trigger re-applies the patch whenever the upstream package is
  upgraded. Removing the package restores everything to stock.

### Testing

- 148 tests run during the package build; `lintian` reports nothing.
- Verified against real `gcompris-qt-data 3.1-2`: install, five diversions,
  correct patched content in all five `.rcc` files, re-patch after an upstream
  upgrade, and removal restoring `core.rcc` to its original md5.
- Tested on real NEO One hardware.

### Not included yet

- **Voice pack** — 202/888 files done, not in the package. Use
  `deploy/install_vi.sh` meanwhile.
- **Family kinship terms** are still not classroom-ready — see
  [docs/NOI_DUNG_CAN_THIET_KE_LAI.md](docs/NOI_DUNG_CAN_THIET_KE_LAI.md).

## [0.1.0] — 2026-09-01

### Added

- Translation of 4,277/4,277 strings — 3,662 translated, 615 deliberately left
  in English. Verified on real GCompris: 382/382 activities display Vietnamese.
- Voice pack of 202 files (8.2 minutes) generated with VieNeu-TTS, voice Bình
  (northern male).
- `deploy/install_vi.sh` — manual install of the translation, `core.rcc` patch
  and voice pack.

[0.2.0]: https://github.com/ThingEdu/gcompris-vi/releases/tag/v0.2.0
[0.1.0]: https://github.com/ThingEdu/gcompris-vi/releases/tag/v0.1.0
