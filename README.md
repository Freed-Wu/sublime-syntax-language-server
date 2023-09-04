# sublime-syntax-language-server

[![readthedocs](https://shields.io/readthedocs/sublime-syntax-language-server)](https://sublime-syntax-language-server.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/sublime-syntax-language-server/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/sublime-syntax-language-server/main)
[![github/workflow](https://github.com/Freed-Wu/sublime-syntax-language-server/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/sublime-syntax-language-server/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/sublime-syntax-language-server/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/sublime-syntax-language-server)
[![DeepSource](https://deepsource.io/gh/Freed-Wu/sublime-syntax-language-server.svg/?show_trend=true)](https://deepsource.io/gh/Freed-Wu/sublime-syntax-language-server)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/sublime-syntax-language-server/total)](https://github.com/Freed-Wu/sublime-syntax-language-server/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/sublime-syntax-language-server/latest/total)](https://github.com/Freed-Wu/sublime-syntax-language-server/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)
[![github/v](https://shields.io/github/v/release/Freed-Wu/sublime-syntax-language-server)](https://github.com/Freed-Wu/sublime-syntax-language-server)

[![pypi/status](https://shields.io/pypi/status/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#description)
[![pypi/v](https://shields.io/pypi/v/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#history)
[![pypi/downloads](https://shields.io/pypi/dd/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#files)
[![pypi/format](https://shields.io/pypi/format/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/sublime-syntax-language-server)](https://pypi.org/project/sublime-syntax-language-server/#files)

Language server and vim plugin for
[sublime-syntax](https://www.sublimetext.com/docs/syntax.html)
and
[syntax-test](https://www.sublimetext.com/docs/syntax.html#testing)'s
[scope names](https://www.sublimetext.com/docs/scope_naming.html).

sublime-syntax is a subtype of yaml. See
[json schema](https://www.schemastore.org/json)
to get support of yaml language server.

- [x] document hover
- [x] completion
- [x] diagnostic: requires [syntest](https://github.com/trishume/syntect)

For vim plugin:

- [x] ftplugin: commentstring, etc
- [x] compilers: bat, syntest
- [x] syntax highlight, include incorrect header

## Document Hover

![Document Hover](https://user-images.githubusercontent.com/32936898/246753924-17f4063c-3f2c-4956-b60a-996d351ccb79.jpg)

## Completion

![Completion](https://user-images.githubusercontent.com/32936898/246778261-76ca6d66-0e1d-4184-a7d7-2660ba79008c.jpg)

## Diagnostic

![Diagnostic](https://user-images.githubusercontent.com/32936898/194603713-1dbc6a4c-cd9a-4894-8cd0-bae0563fa176.png)

## Compilers

Install

- [syntest](https://github.com/trishume/syntect) for `syntax_test_*`
- [bat](https://github.com/sharkdp/bat) for `*.sublime-syntax`

### syntest

#### Build From Source

```sh
git clone --depth=1 https://github.com/trishume/syntect
cd syntect
cargo build --release --example syntest
sudo install -D target/release/examples/syntest -t /usr/local/bin
```

#### For Archlinux

```sh
yay -S syntest
```

## Syntax Highlight

Every syntax test file should have a correct header. If you input a typo, syntax
highlight will tell you:

![Correct](https://user-images.githubusercontent.com/32936898/194894921-0f9167a8-a297-4719-986f-93298111963a.png)

![Incorrect](https://user-images.githubusercontent.com/32936898/194894923-9b82fd5f-2f13-4651-abe5-1a645e737671.png)

If you input correct keyword of sublime syntax file, it will be highlighted as `Keyword`.
Note `watch` should be `match` and `strings` should be `string`:

![Keyword](https://user-images.githubusercontent.com/32936898/195125476-59f056e1-7001-4aa9-b2ba-62a8fd0e0d2e.png)

## More usages

[`:help sublime-syntax`](doc/sublime-syntax.txt)

## Vim Plugin

You can use
[branch release](https://github.com/Freed-Wu/sublime-syntax-language-server/tree/release)
to avoid downloading unnecessary files for vim plugin. Such as for
[dein.vim](https://github.com/Shougo/dein.vim):

```vim
call dein#add('Freed-Wu/sublime-syntax-language-server', {
      \ 'rev': 'release',
      \ })
```
