import generatedManifestJson from "@/assets/manifest.gen.json";
import type { AssetsManifest } from "@drincs/pixi-vn";

/**
 * Manifest for the assets used in the game.
 * You can read more about the manifest here: https://pixijs.com/8.x/guides/components/assets#loading-multiple-assets
 */
export const manifest: AssetsManifest = {
    bundles: [...generatedManifestJson.bundles],
};
