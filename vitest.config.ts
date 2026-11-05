import { defineConfig } from "vitest/config";

// vite.config.ts の plugin 群（assetpack・PWA・pixi-vn の生成）を test に持ち込まないための別の設定。
export default defineConfig({
    test: {
        include: ["tests/**/*.test.ts"],
        environment: "node",
    },
});
