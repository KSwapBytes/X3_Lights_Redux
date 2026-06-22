import unreal


MOD_ROOT = "/x3_lights"
ICON_SOURCE = r"C:\SatisfactoryModding\Repositories\x3_lights\Resources\Icon128.png"

IRON_PLATE = "/Game/FactoryGame/Resource/Parts/IronPlate/Desc_IronPlate"
IRON_ROD = "/Game/FactoryGame/Resource/Parts/IronRod/Desc_IronRod"
WIRE = "/Game/FactoryGame/Resource/Parts/Wire/Desc_Wire"
CABLE = "/Game/FactoryGame/Resource/Parts/Cable/Desc_Cable"
CONCRETE = "/Game/FactoryGame/Resource/Parts/Cement/Desc_Cement"

BUILD_GUN = "/Game/FactoryGame/Equipment/BuildGun/BP_BuildGun"
ORGANISATION_CATEGORY = "/Game/FactoryGame/Schematics/SchematicCategories/SC_Organisation"
UNLOCK_RECIPE = "/Game/FactoryGame/Unlocks/BP_UnlockRecipe"

BUILDINGS = [
    {
        "id": "StreetLight",
        "build_name": "BP_X3Lights_StreetLight",
        "desc_name": "Desc_X3Lights_StreetLight",
        "recipe_name": "Recipe_X3Lights_StreetLight",
        "source_build": "/Game/FactoryGame/Buildable/Factory/StreetLight/Build_StreetLight",
        "source_desc": "/Game/FactoryGame/Buildable/Factory/StreetLight/Desc_StreetLight",
        "source_recipe": "/Game/FactoryGame/Recipes/Buildings/Recipe_StreetLight",
        "display_name": "Cheap: Street Light",
        "power": 0.2,
        "ingredients": [(IRON_PLATE, 2), (IRON_ROD, 12), (WIRE, 2), (CABLE, 2)],
        "menu_priority": 1.1,
    },
    {
        "id": "CeilingLight",
        "build_name": "BP_X3Lights_Ceiling",
        "desc_name": "Desc_X3Lights_Ceiling",
        "recipe_name": "Recipe_X3Lights_Ceiling",
        "source_build": "/Game/FactoryGame/Buildable/Factory/CeilingLight/Build_CeilingLight",
        "source_desc": "/Game/FactoryGame/Buildable/Factory/CeilingLight/Desc_CeilingLight",
        "source_recipe": "/Game/FactoryGame/Recipes/Buildings/Recipe_CeilingLight",
        "display_name": "Cheap: Ceiling Light",
        "power": 0.5,
        "ingredients": [(IRON_PLATE, 6), (IRON_ROD, 8), (WIRE, 8), (CABLE, 2)],
        "menu_priority": 2.1,
    },
    {
        "id": "FloodLightPole",
        "build_name": "BP_X3Lights_FloodPole",
        "desc_name": "Desc_X3Lights_FloodPole",
        "recipe_name": "Recipe_X3Lights_FloodPole",
        "source_build": "/Game/FactoryGame/Buildable/Factory/Floodlight/Build_FloodlightPole",
        "source_desc": "/Game/FactoryGame/Buildable/Factory/Floodlight/Desc_FloodlightPole",
        "source_recipe": "/Game/FactoryGame/Recipes/Buildings/Recipe_FloodlightPole",
        "display_name": "Cheap: Flood Light Tower",
        "power": 1.8,
        "ingredients": [(CONCRETE, 6), (IRON_PLATE, 12), (IRON_ROD, 24), (WIRE, 20), (CABLE, 4)],
        "menu_priority": 3.1,
    },
    {
        "id": "FloodLightWall",
        "build_name": "BP_X3Lights_FloodWall",
        "desc_name": "Desc_X3Lights_FloodWall",
        "recipe_name": "Recipe_X3Lights_FloodWall",
        "source_build": "/Game/FactoryGame/Buildable/Factory/Floodlight/Build_FloodlightWall",
        "source_desc": "/Game/FactoryGame/Buildable/Factory/Floodlight/Desc_FloodlightWall",
        "source_recipe": "/Game/FactoryGame/Recipes/Buildings/Recipe_FloodlightWall",
        "display_name": "Cheap: Wall Mounted Flood Light",
        "power": 0.9,
        "ingredients": [(IRON_PLATE, 6), (IRON_ROD, 6), (WIRE, 12), (CABLE, 2)],
        "menu_priority": 4.1,
    },
    {
        "id": "LightsControlPanel",
        "build_name": "BP_X3Lights_ControlPanel",
        "desc_name": "Desc_X3Lights_ControlPanel",
        "recipe_name": "Recipe_X3Lights_ControlPanel",
        "source_build": "/Game/FactoryGame/Buildable/Factory/LightsControlPanel/Build_LightsControlPanel",
        "source_desc": "/Game/FactoryGame/Buildable/Factory/LightsControlPanel/Desc_LightsControlPanel",
        "source_recipe": "/Game/FactoryGame/Recipes/Buildings/Recipe_LightsControlPanel",
        "display_name": "Cheap: Lights Control Panel",
        "power": None,
        "ingredients": [(IRON_PLATE, 8), (IRON_ROD, 4), (WIRE, 10), (CABLE, 6)],
        "menu_priority": 10.1,
        "downstream_only": True,
    },
]


asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
editor = unreal.EditorAssetLibrary
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()


def log(message):
    print("[X3Lights] " + str(message))


def ensure_dir(path):
    if not editor.does_directory_exist(path):
        if not editor.make_directory(path):
            raise RuntimeError("Could not create directory " + path)


def load_asset(path):
    asset = editor.load_asset(path) or unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Could not load asset " + path)
    return asset


def bp_class(path):
    cls = None
    try:
        cls = editor.load_blueprint_class(path)
    except Exception:
        cls = None
    if cls:
        return cls
    name = path.rsplit("/", 1)[-1]
    cls = unreal.load_class(None, path + "." + name + "_C")
    if not cls:
        raise RuntimeError("Could not load blueprint class " + path)
    return cls


def duplicate_or_load(source, destination):
    if editor.does_asset_exist(destination):
        return load_asset(destination)
    asset = editor.duplicate_asset(source, destination)
    if not asset:
        raise RuntimeError("Could not duplicate {} to {}".format(source, destination))
    log("duplicated {} -> {}".format(source, destination))
    return asset


def create_blueprint_or_load(name, package_path, parent_class):
    destination = package_path + "/" + name
    if editor.does_asset_exist(destination):
        return load_asset(destination)
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    asset = asset_tools.create_asset(name, package_path, None, factory)
    if not asset:
        raise RuntimeError("Could not create blueprint " + destination)
    return asset


def create_child_blueprint_or_load(source_path, destination):
    if editor.does_asset_exist(destination):
        return load_asset(destination)
    package_path, name = destination.rsplit("/", 1)
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", bp_class(source_path))
    asset = asset_tools.create_asset(name, package_path, None, factory)
    if not asset:
        raise RuntimeError("Could not create child blueprint " + destination)
    log("created safe vanilla child {} -> {}".format(source_path, destination))
    return asset


def create_data_asset_or_load(name, package_path, data_class):
    destination = package_path + "/" + name
    if editor.does_asset_exist(destination):
        return load_asset(destination)
    factory = unreal.DataAssetFactory()
    factory.set_editor_property("data_asset_class", data_class)
    asset = asset_tools.create_asset(name, package_path, data_class, factory)
    if not asset:
        raise RuntimeError("Could not create data asset " + destination)
    return asset


def compile_save(asset):
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(asset)
    except Exception as exc:
        log("compile warning for {}: {}".format(asset.get_path_name(), exc))
    editor.save_loaded_asset(asset, only_if_is_dirty=False)


def set_text(obj, property_name, value):
    try:
        obj.set_editor_property(property_name, value)
    except Exception:
        obj.set_editor_property(property_name, unreal.Text(value))


def item_amount(class_path, amount):
    value = unreal.ItemAmount()
    value.set_editor_property("ItemClass", bp_class(class_path))
    value.set_editor_property("Amount", amount)
    return value


def import_icon():
    destination = MOD_ROOT + "/X3Lights_Icon"
    if editor.does_asset_exist(destination):
        return load_asset(destination)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", ICON_SOURCE)
    task.set_editor_property("destination_path", MOD_ROOT)
    task.set_editor_property("destination_name", "X3Lights_Icon")
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    asset_tools.import_asset_tasks([task])
    icon = load_asset(destination)
    editor.save_loaded_asset(icon, only_if_is_dirty=False)
    return icon


def component_templates(blueprint):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint)
    result = []
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        obj = unreal.SubobjectDataBlueprintFunctionLibrary.get_object_for_blueprint(data, blueprint)
        if isinstance(obj, unreal.FGCircuitConnectionComponent):
            result.append(obj)
    return result


def configure_connections(blueprint, downstream_only):
    changed = []
    for component in component_templates(blueprint):
        name = component.get_name()
        if downstream_only and not name.startswith("DownstreamConnection"):
            continue
        component.set_editor_property("mMaxNumConnectionLinks", 4)
        changed.append(name)
    if not changed:
        raise RuntimeError("No matching power connection components in " + blueprint.get_path_name())
    log("{} connection templates set to 4: {}".format(blueprint.get_name(), changed))


def directory_path(path):
    value = unreal.DirectoryPath()
    value.set_editor_property("Path", path)
    return value


def primary_asset_rules():
    value = unreal.PrimaryAssetRules()
    value.set_editor_property("Priority", 2)
    value.set_editor_property("ChunkId", 1)
    value.set_editor_property("bApplyRecursively", True)
    return value


def configure_game_feature_data(asset):
    schematic_scan = unreal.PrimaryAssetTypeInfo()
    schematic_scan.set_editor_property("PrimaryAssetType", "FGSchematic")
    schematic_scan.set_editor_property("AssetBaseClass", unreal.FGSchematic)
    schematic_scan.set_editor_property("bHasBlueprintClasses", True)
    schematic_scan.set_editor_property("Directories", [directory_path(MOD_ROOT)])
    schematic_scan.set_editor_property("Rules", primary_asset_rules())
    asset.set_editor_property("PrimaryAssetTypesToScan", [schematic_scan])
    editor.save_loaded_asset(asset, only_if_is_dirty=False)


def main():
    ensure_dir(MOD_ROOT)
    for building in BUILDINGS:
        ensure_dir(MOD_ROOT + "/" + building["id"])
    asset_registry.scan_paths_synchronous([MOD_ROOT], force_rescan=True)

    game_feature_data = create_data_asset_or_load("x3_lights", MOD_ROOT, unreal.FGGameFeatureData)
    configure_game_feature_data(game_feature_data)
    icon = import_icon()

    subcategory_bp = create_blueprint_or_load("SC_X3Lights", MOD_ROOT, unreal.FGBuildSubCategory)
    subcategory_cls = bp_class(MOD_ROOT + "/SC_X3Lights")
    set_text(unreal.get_default_object(subcategory_cls), "mDisplayName", "Cheap Lights")
    compile_save(subcategory_bp)

    recipe_classes = []
    for building in BUILDINGS:
        directory = MOD_ROOT + "/" + building["id"]
        build_path = directory + "/" + building["build_name"]
        desc_path = directory + "/" + building["desc_name"]
        recipe_path = directory + "/" + building["recipe_name"]

        # A child of the current vanilla Blueprint inherits Coffee Stain's pooled-light
        # implementation. Duplicating and recompiling the full Blueprint can serialize
        # empty FPoolBoolScalability arrays and crash when the light is powered.
        build_bp = create_child_blueprint_or_load(building["source_build"], build_path)
        desc_bp = duplicate_or_load(building["source_desc"], desc_path)
        recipe_bp = duplicate_or_load(building["source_recipe"], recipe_path)

        build_cls = bp_class(build_path)
        desc_cls = bp_class(desc_path)
        recipe_cls = bp_class(recipe_path)

        build_cdo = unreal.get_default_object(build_cls)
        set_text(build_cdo, "mDisplayName", building["display_name"])
        if building["power"] is not None:
            build_cdo.set_editor_property("mPowerConsumption", building["power"])
        configure_connections(build_bp, building.get("downstream_only", False))

        desc_cdo = unreal.get_default_object(desc_cls)
        desc_cdo.set_editor_property("mBuildableClass", build_cls)
        desc_cdo.set_editor_property("mSubCategories", [subcategory_cls])
        desc_cdo.set_editor_property("mMenuPriority", building["menu_priority"])

        recipe_cdo = unreal.get_default_object(recipe_cls)
        recipe_cdo.set_editor_property(
            "mIngredients",
            [item_amount(path, amount) for path, amount in building["ingredients"]],
        )
        recipe_cdo.set_editor_property("mProduct", [item_amount(desc_path, 1)])
        recipe_cdo.set_editor_property("mProducedIn", [bp_class(BUILD_GUN)])
        for asset in [build_bp, desc_bp, recipe_bp]:
            compile_save(asset)
        recipe_classes.append(recipe_cls)

    schematic_bp = duplicate_or_load(
        "/Game/FactoryGame/Schematics/Progression/Schematic_2-3",
        MOD_ROOT + "/Unlock_X3Lights_Mk1Schematic",
    )
    schematic_cls = bp_class(MOD_ROOT + "/Unlock_X3Lights_Mk1Schematic")
    schematic_cdo = unreal.get_default_object(schematic_cls)
    set_text(schematic_cdo, "mDisplayName", "X3-Lights")
    set_text(schematic_cdo, "mDescription", "Unlocks cheaper, lower-power versions of the vanilla lights.")
    schematic_cdo.set_editor_property("mType", unreal.SchematicType.EST_MILESTONE)
    schematic_cdo.set_editor_property("mTechTier", 2)
    schematic_cdo.set_editor_property("mTimeToComplete", 120.0)
    schematic_cdo.set_editor_property("mMenuPriority", 99.0)
    schematic_cdo.set_editor_property(
        "mCost",
        [
            item_amount(IRON_PLATE, 50),
            item_amount(IRON_ROD, 100),
            item_amount(WIRE, 100),
            item_amount(CABLE, 150),
        ],
    )
    schematic_cdo.set_editor_property("mSchematicCategory", bp_class(ORGANISATION_CATEGORY))
    schematic_cdo.set_editor_property("mSchematicDependencies", [])
    schematic_cdo.set_editor_property("mDependenciesBlocksSchematicAccess", False)
    schematic_cdo.set_editor_property("mHiddenUntilDependenciesMet", False)
    schematic_cdo.set_editor_property("mRelevantEvents", [])
    brush = schematic_cdo.get_editor_property("mSchematicIcon")
    brush.set_editor_property("resource_object", icon)
    schematic_cdo.set_editor_property("mSchematicIcon", brush)
    try:
        schematic_cdo.set_editor_property("mSmallSchematicIcon", icon)
    except Exception:
        pass
    unlock = unreal.new_object(
        bp_class(UNLOCK_RECIPE),
        outer=schematic_cdo,
        name="Unlock_X3Lights_Recipes",
    )
    unlock.set_editor_property("mRecipes", recipe_classes)
    schematic_cdo.set_editor_property("mUnlocks", [unlock])
    compile_save(schematic_bp)

    root_bp = create_blueprint_or_load("RootGameWorld_x3_lights", MOD_ROOT, unreal.GameWorldModule)
    root_cls = bp_class(MOD_ROOT + "/RootGameWorld_x3_lights")
    root_cdo = unreal.get_default_object(root_cls)
    root_cdo.set_editor_property("bRootModule", True)
    root_cdo.set_editor_property("mSchematics", [schematic_cls])
    compile_save(root_bp)

    editor.save_directory(MOD_ROOT, only_if_is_dirty=False, recursive=True)
    log("created {} legacy-compatible building paths".format(len(BUILDINGS)))
    log("schematic={}".format(schematic_cls.get_path_name()))
    log("root={}".format(root_cls.get_path_name()))


main()
