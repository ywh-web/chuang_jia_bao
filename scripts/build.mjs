import { cpSync, existsSync, rmSync } from 'node:fs'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const root = resolve(fileURLToPath(new URL('.', import.meta.url)), '..')
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
const frontendModules = resolve(root, 'frontend', 'node_modules')

if (!existsSync(frontendModules)) {
  const install = spawnSync(npm, ['--prefix', 'frontend', 'ci'], {
    cwd: root,
    stdio: 'inherit',
  })

  if (install.status !== 0) {
    process.exit(install.status ?? 1)
  }
}

const build = spawnSync(npm, ['--prefix', 'frontend', 'run', 'build'], {
  cwd: root,
  stdio: 'inherit',
})

if (build.status !== 0) {
  process.exit(build.status ?? 1)
}

rmSync(resolve(root, 'dist'), { recursive: true, force: true })
cpSync(resolve(root, 'frontend', 'dist'), resolve(root, 'dist'), {
  recursive: true,
})

console.log('Cloudflare Pages output copied to ./dist')
