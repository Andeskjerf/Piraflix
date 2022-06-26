import { defineConfig } from "vite";
import { NodeGlobalsPolyfillPlugin } from "@esbuild-plugins/node-globals-polyfill";
import { NodeModulesPolyfillPlugin } from "@esbuild-plugins/node-modules-polyfill";
// import esbuildVue from "esbuild-plugin-vue-next";
import eslintPlugin from "vite-plugin-eslint";
import vue from "@vitejs/plugin-vue";
import path from "path";
import rollupConfig from "./rollup.config";

export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
            @import "@/styles/global";
            @import "@/styles/loader";
          `,
      },
    },
  },
  plugins: [vue(), eslintPlugin()],
  resolve: {
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json"],
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: "esnext",
    polyfillModulePreload: true,
    outDir: "./dist",
    assetsDir: "./assets",
    sourcemap: true,
    bundle: true,
    rollupOptions: rollupConfig,
  },
  optimizeDeps: {
    esbuildOptions: {
      platform: "browser",
      // outdir: "./out",
      bundle: true,
      sourcemap: true,
      minify: true,
      format: "esm",
      // splitting: false,
      target: ["es2020", "esnext"],
      define: { global: "globalThis" },
      plugins: [
        NodeGlobalsPolyfillPlugin({ buffer: true }),
        NodeModulesPolyfillPlugin(),
        // esbuildVue(),
      ],
    },
  },
});
