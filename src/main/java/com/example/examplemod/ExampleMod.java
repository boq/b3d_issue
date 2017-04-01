package com.example.examplemod;

import net.minecraft.block.Block;
import net.minecraft.client.renderer.block.model.ModelResourceLocation;
import net.minecraft.creativetab.CreativeTabs;
import net.minecraft.item.ItemBlock;
import net.minecraftforge.client.model.ModelLoader;
import net.minecraftforge.client.model.b3d.B3DLoader;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventHandler;
import net.minecraftforge.fml.common.event.FMLPreInitializationEvent;
import net.minecraftforge.fml.common.registry.GameRegistry;

@Mod(modid = ExampleMod.MODID, version = ExampleMod.VERSION)
public class ExampleMod {
	private static final String BLOCK_ID = "arrow";
	public static final String MODID = "model_test";
	public static final String VERSION = "1.0";

	@EventHandler
	public void preLoad(FMLPreInitializationEvent event) {
		B3DLoader.INSTANCE.addDomain(MODID);

		final Block block = new BlockArrow();
		block.setCreativeTab(CreativeTabs.MISC);
		GameRegistry.register(block.setRegistryName(BLOCK_ID));

		final ItemBlock item = new ItemBlock(block);
		GameRegistry.register(item.setRegistryName(BLOCK_ID));

		ModelLoader.setCustomModelResourceLocation(item, 0, new ModelResourceLocation(block.getRegistryName(), "inventory"));
	}
}
