Navigate to [https://uwa-channels.github.io](https://uwa-channels.github.io) for the documentation. The library is described in [arXiv:2609.03207](https://arxiv.org/abs/2609.03207); please cite it if you use the channels, the noise models, or the code.

## Previewing the site locally

The site is built with [Hugo](https://gohugo.io/) and the [Docsy](https://www.docsy.dev/) theme.  Docsy needs the **extended** Hugo build, and this site vendors Docsy as a git submodule rather than as a Hugo Module, so Docsy's own dependencies have to be fetched by hand.  The commands below mirror what `.github/workflows/` does on every push.

### One-time setup

```bash
# Hugo extended, matching HUGO_VERSION in the deploy workflow
curl -sL "https://github.com/gohugoio/hugo/releases/download/v0.164.0/hugo_extended_0.164.0_linux-amd64.tar.gz" | tar -xz hugo
sudo mv hugo /usr/local/bin/hugo

# the Docsy theme itself
git submodule update --init --recursive

# Docsy's theme dependencies, which Hugo Modules would otherwise fetch.
# Keep these versions in sync with themes/docsy/go.mod.
git clone --depth 1 --branch 6.7.2 https://github.com/FortAwesome/Font-Awesome.git themes/github.com/FortAwesome/Font-Awesome
git clone --depth 1 --branch v5.3.8 https://github.com/twbs/bootstrap.git themes/github.com/twbs/bootstrap

# PostCSS, used by Docsy to process the stylesheets
npm install postcss postcss-cli autoprefixer
```

### Preview

```bash
hugo server
```

Then open <http://localhost:1313>.  Edits to `content/` reload in the browser automatically.  Add `--disableFastRender` if a change does not show up.

### Check what will be deployed

```bash
hugo --minify --baseURL "https://uwa-channels.github.io"
```

This is the exact command the deploy workflow runs, and it writes the finished site to `public/`.  Treat new `WARN` lines as failures: Hugo does not exit non-zero for a malformed shortcode, it warns and renders something subtly wrong.  Four `WARN deprecated:` lines about `languageName`, `LanguageDirection`, `AllPages`, and `LanguageName` are pre-existing and come from Docsy, not from page content.
