import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { execSync } from 'child_process'

const gitVersion = execSync('git describe --tags --always').toString().trim()

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  define: {
    __APP_VERSION__: JSON.stringify(gitVersion)
  }
})
