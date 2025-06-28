import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: './', // 👈 faz os caminhos dos assets serem relativos
  build: {
    outDir: 'dist' // (opcional, já é padrão)
  }
})
