-- NeoPlay catalog — publish GCompris tiếng Việt
-- =============================================================================
-- Run against the NeoPlay Supabase project with an ADMIN connection (SQL editor,
-- or psql/API with the sb_secret_… key). The publishable key has no write
-- access. Apply neo-play/supabase/schema.sql first if this is a fresh project.
--
-- Idempotent: every statement upserts, so re-running is safe.
-- catalog_meta.revision bumps automatically via the schema triggers — never
-- touch it by hand.
--
-- Publish target is app_RELEASES. `app_versions` is a read-only compatibility
-- view over it; writing to the view is not supported.
--
-- sha256 below was taken from the PUBLISHED release asset (downloaded from
-- GitHub), not from a local build. Assets are immutable per
-- github-release-convention.md — a new version gets a new row, existing rows
-- are never re-pointed.
--
--   $ curl -fsSL -o gcompris-vi_0.2.0_all.deb \
--       https://github.com/ThingEdu/gcompris-vi/releases/download/v0.2.0/gcompris-vi_0.2.0_all.deb
--   $ sha256sum gcompris-vi_0.2.0_all.deb
--   451ab9b37acab3e6d3b968ef76455f883e218865276b35c44469ce117636b91a
-- =============================================================================

-- -----------------------------------------------------------------------------
-- NOTE ON THE EXISTING 'gcompris' ENTRY
-- -----------------------------------------------------------------------------
-- seed.sql already carries an app id 'gcompris' with an 'apt_repo' release
-- (pkg_id gcompris-qt). That row is invisible to every shipped client, because
-- the app_versions view filters source_type to ('deb','flathub') — so GCompris
-- does not currently appear in the store at all.
--
-- This script publishes a SEPARATE app id, 'gcompris-vi', as a 'deb' release.
-- It is visible immediately, and it leaves the existing 'gcompris' row alone.
--
-- Once clients understand 'apt_repo', both entries become visible and you will
-- want to reconcile them — either drop the plain 'gcompris' entry, or keep it
-- as the non-localised option. That is a product decision, deliberately not
-- made here.

-- -----------------------------------------------------------------------------
-- Category (already present in seed.sql; harmless to assert)
-- -----------------------------------------------------------------------------

insert into categories (id) values ('learn')
on conflict (id) do nothing;

-- -----------------------------------------------------------------------------
-- App — display metadata
-- -----------------------------------------------------------------------------

insert into apps (id, name, summary, description, author, icon) values
    (
        'gcompris-vi',
        'GCompris tiếng Việt',
        'Bộ hoạt động giáo dục cho trẻ 2-10 tuổi, bản tiếng Việt',
        'Hơn 200 hoạt động về đọc, toán, khoa học, địa lý và tin học căn bản, đã dịch đầy đủ sang tiếng Việt. Kèm bản đồ Việt Nam có quần đảo Hoàng Sa và Trường Sa, bản đồ hành chính 34 tỉnh thành, và hai trò chơi riêng của Làng Maker.',
        'ThingEdu',
        'mdi.school'
    )
on conflict (id) do update set
    name        = excluded.name,
    summary     = excluded.summary,
    description = excluded.description,
    author      = excluded.author,
    icon        = excluded.icon;

insert into app_categories (app_id, category_id) values
    ('gcompris-vi', 'learn')
on conflict (app_id, category_id) do nothing;

-- -----------------------------------------------------------------------------
-- Release — one immutable release per row
-- -----------------------------------------------------------------------------
-- launch_exec is gcompris-qt: this package is a localisation layer and ships no
-- binary of its own. The command comes from the gcompris-qt package that the
-- .deb depends on, and apt pulls it in during install.
--
-- size is the ARTIFACT size (536 KB → 1 MB ceiling), per app-entry-convention.
-- On a device that does NOT already have GCompris, apt additionally pulls
-- gcompris-qt-data (~100 MB) as a dependency, which this figure does not cover.
-- NEO images ship GCompris, so the common case is accurate.

insert into app_releases
    (app_id, version, source_type, url, sha256, pkg_id, launch_exec, size)
values
    (
        'gcompris-vi',
        '0.2.0',
        'deb',
        'https://github.com/ThingEdu/gcompris-vi/releases/download/v0.2.0/gcompris-vi_0.2.0_all.deb',
        '451ab9b37acab3e6d3b968ef76455f883e218865276b35c44469ce117636b91a',
        'gcompris-vi',
        array['gcompris-qt'],
        1
    )
on conflict (app_id, version) do update set
    source_type = excluded.source_type,
    url         = excluded.url,
    sha256      = excluded.sha256,
    pkg_id      = excluded.pkg_id,
    launch_exec = excluded.launch_exec,
    size        = excluded.size;

-- -----------------------------------------------------------------------------
-- Verify
-- -----------------------------------------------------------------------------

select a.id, a.name, r.version, r.source_type, r.size, r.launch_exec
from apps a join app_releases r on r.app_id = a.id
where a.id = 'gcompris-vi';

select revision from catalog_meta;
