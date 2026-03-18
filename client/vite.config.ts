import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import checker from "vite-plugin-checker";

export default defineConfig({
  plugins: [
    react(),
    checker({
      typescript: true,
    }),
  ],
  server: {
    port: 3000,
    open: true,
    proxy: {
      "/api": "http://localhost:80", // TODO
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    emptyOutDir: true,
  },
});
