"""Run: python3 tests/check_content_jar.py build/libs/<mod>.jar"""
import json
from pathlib import Path
import sys
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
package = "net/tearpelato/falldrop_backport/"
with ZipFile(sys.argv[1]) as jar:
    names = set(jar.namelist())
    metadata = json.loads(jar.read("fabric.mod.json"))
    assert metadata["id"] == "falldrop_backport"
    assert metadata["entrypoints"]["main"] == [
        "net.tearpelato.falldrop_backport.FallDropBackport"
    ]
    for name in names:
        assert "terrablender" not in name.lower(), name
        assert "OverworldRegion" not in name, name
        if not name.endswith("/"):
            assert b"terrablender" not in jar.read(name).lower(), name

    # Every retained asset/data file must be packaged byte-for-byte, not just samples.
    resources = 0
    for source_set in ("main", "generated"):
        resource_root = root / "src" / source_set / "resources"
        for directory in ("assets", "data"):
            for source in (resource_root / directory).rglob("*"):
                if source.is_file():
                    name = source.relative_to(resource_root).as_posix()
                    assert jar.read(name) == source.read_bytes(), name
                    resources += 1

    for name in (
        "assets/minecraft/textures/block/poplar_sapling.png",
        "data/minecraft/worldgen/configured_feature/poplar_trees.json",
        "data/minecraft/worldgen/structure_set/abandoned_camp.json",
    ):
        assert name in names, name
    for name in ("ModBlocks", "ModItems", "ModBiomes"):
        assert package + "init/" + name + ".class" in names, name

    initializer = jar.read(package + "FallDropBackport.class")
    for registry, codec in (
        ("ModTrunkPlacerTypes", "PoplarTrunkPlacer"),
        ("ModFoliagePlacerTypes", "PoplarFoliagePlacer"),
        ("ModTreeDecoratorType", "decorator/ShelfMushroomDecorator"),
    ):
        assert registry.encode() in initializer, registry
        registry_bytes = jar.read(package + "init/" + registry + ".class")
        assert codec.encode() in registry_bytes and b"CODEC" in registry_bytes, registry
        assert b"CODEC" in jar.read(package + "worldgen/placer/" + codec + ".class"), codec

    biome = json.loads(jar.read("data/minecraft/worldgen/biome/dappled_forest.json"))
    for feature in ("red_poplar", "orange_poplar", "yellow_poplar",
                    "brow_mushroom_dappled_forest", "red_shrub"):
        assert "minecraft:" + feature in biome["features"][9], feature
        assert "data/minecraft/worldgen/placed_feature/" + feature + ".json" in names, feature

print(f"PASS: {resources} unchanged content resources, biome/features, codec registrations; no TerraBlender")
