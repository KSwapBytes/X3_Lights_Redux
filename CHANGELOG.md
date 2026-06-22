# Changelog

## 1.2.1

- Fixed a crash in `FPoolLightComponent::Update` when powering an X3 flood light.
- Rebuilt each legacy light class as a child of its current vanilla Blueprint so pooled-light scalability settings remain inherited and valid.
- Retained the four-link connection overrides through safe inherited-component templates.
- Preserved the original GNU GPL v3 license and added prominent credits for x3008x and Acxd.
- Added links to the original project, current source repository, and issue tracker.

## 1.2.0

- Rebuilt all five legacy assets from current Satisfactory 1.2 vanilla classes.
- Updated compatibility to game build 491125 and SML 3.12.
- Preserved the original `/x3_lights` asset paths for existing saves.
- Restored the original costs, power consumption, and connection limits.
