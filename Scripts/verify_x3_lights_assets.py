import unreal


MOD_ROOT = "/x3_lights"

EXPECTED = [
    ("StreetLight", "BP_X3Lights_StreetLight", "Desc_X3Lights_StreetLight", "Recipe_X3Lights_StreetLight", 0.2, False, [("Desc_IronPlate_C", 2), ("Desc_IronRod_C", 12), ("Desc_Wire_C", 2), ("Desc_Cable_C", 2)]),
    ("CeilingLight", "BP_X3Lights_Ceiling", "Desc_X3Lights_Ceiling", "Recipe_X3Lights_Ceiling", 0.5, False, [("Desc_IronPlate_C", 6), ("Desc_IronRod_C", 8), ("Desc_Wire_C", 8), ("Desc_Cable_C", 2)]),
    ("FloodLightPole", "BP_X3Lights_FloodPole", "Desc_X3Lights_FloodPole", "Recipe_X3Lights_FloodPole", 1.8, False, [("Desc_Cement_C", 6), ("Desc_IronPlate_C", 12), ("Desc_IronRod_C", 24), ("Desc_Wire_C", 20), ("Desc_Cable_C", 4)]),
    ("FloodLightWall", "BP_X3Lights_FloodWall", "Desc_X3Lights_FloodWall", "Recipe_X3Lights_FloodWall", 0.9, False, [("Desc_IronPlate_C", 6), ("Desc_IronRod_C", 6), ("Desc_Wire_C", 12), ("Desc_Cable_C", 2)]),
    ("LightsControlPanel", "BP_X3Lights_ControlPanel", "Desc_X3Lights_ControlPanel", "Recipe_X3Lights_ControlPanel", None, True, [("Desc_IronPlate_C", 8), ("Desc_IronRod_C", 4), ("Desc_Wire_C", 10), ("Desc_Cable_C", 6)]),
]

VANILLA_PARENTS = {
    "BP_X3Lights_StreetLight": "/Game/FactoryGame/Buildable/Factory/StreetLight/Build_StreetLight",
    "BP_X3Lights_Ceiling": "/Game/FactoryGame/Buildable/Factory/CeilingLight/Build_CeilingLight",
    "BP_X3Lights_FloodPole": "/Game/FactoryGame/Buildable/Factory/Floodlight/Build_FloodlightPole",
    "BP_X3Lights_FloodWall": "/Game/FactoryGame/Buildable/Factory/Floodlight/Build_FloodlightWall",
    "BP_X3Lights_ControlPanel": "/Game/FactoryGame/Buildable/Factory/LightsControlPanel/Build_LightsControlPanel",
}


editor = unreal.EditorAssetLibrary


def bp_class(path):
    cls = editor.load_blueprint_class(path)
    if not cls:
        name = path.rsplit("/", 1)[-1]
        cls = unreal.load_class(None, path + "." + name + "_C")
    if not cls:
        raise RuntimeError("Missing blueprint class " + path)
    return cls


def amount_pairs(values):
    return [(value.get_editor_property("ItemClass").get_name(), value.get_editor_property("Amount")) for value in values]


def component_templates(blueprint):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    result = []
    for handle in subsystem.k2_gather_subobject_data_for_blueprint(blueprint):
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object_for_blueprint(data, blueprint)
        if isinstance(obj, unreal.FGCircuitConnectionComponent):
            result.append(obj)
    return result


def main():
    unreal.AssetRegistryHelpers.get_asset_registry().scan_paths_synchronous([MOD_ROOT], force_rescan=True)
    subcategory_cls = bp_class(MOD_ROOT + "/SC_X3Lights")
    expected_recipe_paths = []

    for directory, build_name, desc_name, recipe_name, power, downstream_only, ingredients in EXPECTED:
        root = MOD_ROOT + "/" + directory
        build_path = root + "/" + build_name
        desc_path = root + "/" + desc_name
        recipe_path = root + "/" + recipe_name
        build_cls = bp_class(build_path)
        desc_cls = bp_class(desc_path)
        recipe_cls = bp_class(recipe_path)
        build = unreal.get_default_object(build_cls)
        desc = unreal.get_default_object(desc_cls)
        recipe = unreal.get_default_object(recipe_cls)

        asset_data = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_package_name(build_path)
        assert len(asset_data) == 1, build_path
        parent_tag = str(asset_data[0].get_tag_value("ParentClass"))
        vanilla_parent = VANILLA_PARENTS[build_name]
        assert vanilla_parent + "." + vanilla_parent.rsplit("/", 1)[-1] + "_C" in parent_tag, (build_name, parent_tag)

        if power is not None:
            actual_power = build.get_editor_property("mPowerConsumption")
            assert abs(actual_power - power) < 0.0001, (build_name, actual_power, power)
        assert desc.get_editor_property("mBuildableClass") == build_cls
        assert desc.get_editor_property("mSubCategories") == [subcategory_cls]
        assert amount_pairs(recipe.get_editor_property("mIngredients")) == ingredients
        assert amount_pairs(recipe.get_editor_property("mProduct")) == [(desc_cls.get_name(), 1)]

        components = component_templates(editor.load_asset(build_path))
        matched = 0
        for component in components:
            name = component.get_name()
            if downstream_only and not name.startswith("DownstreamConnection"):
                continue
            assert component.get_editor_property("mMaxNumConnectionLinks") == 4, (build_name, name)
            matched += 1
        assert matched > 0, build_name
        expected_recipe_paths.append(recipe_cls.get_path_name())
        print("[X3Verify] {} power={} links={} ingredients={}".format(build_name, power, matched, ingredients))

    schematic_cls = bp_class(MOD_ROOT + "/Unlock_X3Lights_Mk1Schematic")
    schematic = unreal.get_default_object(schematic_cls)
    assert schematic.get_editor_property("mTechTier") == 2
    assert abs(schematic.get_editor_property("mTimeToComplete") - 120.0) < 0.0001
    assert amount_pairs(schematic.get_editor_property("mCost")) == [
        ("Desc_IronPlate_C", 50),
        ("Desc_IronRod_C", 100),
        ("Desc_Wire_C", 100),
        ("Desc_Cable_C", 150),
    ]
    unlocks = schematic.get_editor_property("mUnlocks")
    assert len(unlocks) == 1
    actual_recipe_paths = [value.get_path_name() for value in unlocks[0].get_editor_property("mRecipes")]
    assert actual_recipe_paths == expected_recipe_paths, actual_recipe_paths

    root_cls = bp_class(MOD_ROOT + "/RootGameWorld_x3_lights")
    root = unreal.get_default_object(root_cls)
    assert root.get_editor_property("bRootModule")
    assert [value.get_path_name() for value in root.get_editor_property("mSchematics")] == [schematic_cls.get_path_name()]
    assert editor.does_asset_exist(MOD_ROOT + "/x3_lights")
    assert editor.does_asset_exist(MOD_ROOT + "/X3Lights_Icon")
    print("[X3Verify] schematic and root registration verified")


main()
