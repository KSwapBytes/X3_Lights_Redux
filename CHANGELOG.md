# Changelog

## 1.0.0

- Set the numeric plugin version to `1` so it matches the `1.0.0` semantic version required by SMR.
- Renamed the mod reference to `X3LightsRedux` for a separate SMR listing.
- Added a package redirect from `/x3_lights/` to `/X3LightsRedux/` for save migration.
- Fixed a crash in `FPoolLightComponent::Update` when powering an X3 flood light.
- Rebuilt each light class as a child of its current vanilla Blueprint so pooled-light scalability settings remain inherited and valid.
- Retained the original recipes, Tier 2 milestone, power consumption, and four-link connection overrides.
- Preserved the original GNU GPL v3 license and credits for x3008x and Acxd.
