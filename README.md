Navigate to [https://uwa-channels.github.io](https://uwa-channels.github.io) for the documentation. The library is described in [arXiv:2609.03207](https://arxiv.org/abs/2609.03207); please cite it if you use the channels, the noise models, or the code.

## Previewing the site locally

The site is built with [Hugo](https://gohugo.io/) and the [Docsy](https://www.docsy.dev/) theme.  Docsy needs the **extended** Hugo build, Node.js 24 or later, and the Dart Sass compiler.  This site vendors Docsy as a git submodule rather than as a Hugo Module.  The commands below mirror what `.github/workflows/` does on every push.

### One-time setup

```bash
# Hugo extended, matching HUGO_VERSION in the deploy workflow
curl -sL "https://github.com/gohugoio/hugo/releases/download/v0.168.0/hugo_extended_0.168.0_linux-amd64.tar.gz" | tar -xz hugo
sudo mv hugo /usr/local/bin/hugo

# the Docsy theme itself
git submodule update --init --recursive

# Docsy's theme dependencies (Bootstrap, Font Awesome)
(cd themes/docsy && npm run install:theme-deps)

# Dart Sass, which Hugo looks up as `sass` on PATH.
# Keep this version in sync with sass-embedded in themes/docsy/package.json.
npm install --no-save --no-package-lock sass-embedded@1.105.0
export PATH="$PWD/node_modules/.bin:$PATH"
```

Re-run the last two commands after the Docsy submodule is bumped.

### Preview

```bash
hugo server
```

Then open <http://localhost:1313>.  Edits to `content/` reload in the browser automatically.  Add `--disableFastRender` if a change does not show up.

### Check what will be deployed

```bash
hugo --minify --baseURL "https://uwa-channels.github.io"
```

This is the exact command the deploy workflow runs, and it writes the finished site to `public/`.  Treat new `WARN` lines as failures: Hugo does not exit non-zero for a malformed shortcode, it warns and renders something subtly wrong.  A clean build prints no `WARN` lines at all.
