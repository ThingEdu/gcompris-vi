# Releasing

Adapted from `docs/template/RELEASING.md.template`. Two extra rules apply here
because gcompris-vi is distributed as a NEO app:

- **Tags and release assets are immutable.** Never move a tag or re-upload an
  asset — the NeoPlay store pins each release's sha256, so a swapped artifact
  fails to install on every device. A fix gets a new patch version.
  (neo-play-hub `docs/conventions/github-release-convention.md`)
- **The version appears identically** in `debian/changelog`, the tag `vX.Y.Z`,
  and the asset name `gcompris-vi_X.Y.Z_all.deb`.

## 1. Update the version

There is no separate version file: **`debian/changelog` is the source of
truth**, and `dpkg-buildpackage` takes the package version from its top entry.
Add a new entry with `dch -i`, or edit it by hand:

```
gcompris-vi (X.Y.Z) unstable; urgency=medium
  * ...
 -- ThingEdu <tuan@rogo.com.vn>  <date -R output>
```

The package is `3.0 (native)`, so the version carries no `-1` Debian revision.
Include an RC suffix if appropriate (`0.3.0~rc1` — a tilde sorts *before* the
release in dpkg, unlike Ruby's `.rc`).

## 2. Update `CHANGELOG.md`

Describe what changed for teachers and students, not raw commit titles. This
text becomes the GitHub release notes in step 7.

## 3. Commit

No code changes, so CI does not need to run — add `[ci skip]`:

```bash
git commit -m "Release X.Y.Z [ci skip]"
```

## 4. Tag the release

```bash
git tag -s vX.Y.Z -m "gcompris-vi X.Y.Z"
```

**Signing is not set up yet** — there is no GPG key on the release machine, so
`-s` fails today. Either create a key
([quick guide](https://gitready.com/advanced/2014/11/02/gpg-sign-releases.html))
and set `git config user.signingkey`, or fall back to an annotated tag `-a`
until then. v0.2.0 was tagged unannotated and cannot be re-signed: the tag is
immutable.

## 5. Push

```bash
git push --follow-tags
```

## 6. Build and publish

Replaces the template's `gem build` / `gem push`. The package is
`Architecture: all`, so it builds on any machine and installs on ARM64 NEO
devices. Build in a clean bookworm container so the result does not depend on
the host:

```bash
mkdir -p dist && rm -f dist/*
podman run --rm -v "$PWD":/src:ro,z -v "$PWD/dist":/out:z debian:bookworm bash -c '
  set -e
  apt-get update -qq
  apt-get install -y -qq --no-install-recommends build-essential debhelper \
      devscripts gettext qttools5-dev-tools nodejs python3 python3-pytest lintian
  cp -a /src /build && cd /build
  dpkg-buildpackage -us -uc -b
  cp ../*.deb ../*.changes /out/
  lintian /out/*.deb
'
```

`build-essential` is required even though nothing compiles —
`dpkg-checkbuilddeps` demands it implicitly. `nodejs` matters: without it the
three tests that execute `lang_doidoi.js` are silently skipped, and those are
the only guard on the dealing invariant. A correct build reports **148 passed**.

## 7. Add a GitHub release

```bash
gh release create vX.Y.Z dist/gcompris-vi_X.Y.Z_all.deb \
  --target main --title "gcompris-vi X.Y.Z" --notes-file <(...)  # CHANGELOG section
```

Asset name must be exactly `gcompris-vi_X.Y.Z_all.deb` — NeoPlay builds the
download URL from that pattern. Mark work-in-progress builds as
`--prerelease`; only full releases can go in the store.

## 8. Publish to NeoPlay, then announce

Record the release's sha256 in the store row and hand it to ThingEdu:

```bash
sha256sum dist/gcompris-vi_X.Y.Z_all.deb
```

Update `docs/neo-play/publish-gcompris-vi.sql` with the new version, URL and
sha256, and run it against the NeoPlay Supabase project with the **secret**
key. Never add a row for an artifact you have not hashed from the published
release — hash the downloaded asset, not the local build.

Then announce, and thank the people who shaped this version.
