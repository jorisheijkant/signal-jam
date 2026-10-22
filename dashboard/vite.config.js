import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { execSync } from 'child_process'
import { readFileSync } from 'fs'

// Hosts like Vercel clone without tags, so fall back to the package.json version
function getAppVersion() {
  try {
    return execSync('git describe --tags', { stdio: 'pipe' }).toString().trim()
  } catch {
    const { version } = JSON.parse(readFileSync('./package.json', 'utf-8'))
    return `v${version}`
  }
}

const gitVersion = getAppVersion()

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  define: {
    __APP_VERSION__: JSON.stringify(gitVersion)
  }
})
