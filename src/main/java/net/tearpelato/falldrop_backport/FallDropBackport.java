package net.tearpelato.falldrop_backport;

import net.fabricmc.api.ModInitializer;
import net.tearpelato.falldrop_backport.init.*;

public class FallDropBackport implements ModInitializer {
    @Override
    public void onInitialize() {
        ModCreativeTabs.registerCreativeModeTabs();

        ModItems.registerModItems();
        ModBlocks.registerModBlocks();

        ModParticleTypes.registerParticles();
        ModTrunkPlacerTypes.registerTrunkPlacer();
        ModFoliagePlacerTypes.registerFoliagePlacer();
        ModEntities.registerModEntities();
        ModBlockEntities.registerBlockEntities();
        ModStats.registerStats();
        ModSounds.registerSounds();
        ModMapDecorationTypes.registerMapDecorationTypes();

        ModFlammableBlocks.registerFlammableBlocks();
        ModStrippableBlocks.registerStrippableBlocks();
        ModTreeDecoratorType.registerTreeDecorators();
        ModFuels.registerModFuels();


    }
}
