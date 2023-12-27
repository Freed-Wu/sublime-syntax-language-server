# Configure

## (Neo)[Vim](https://www.vim.org)

### [coc.nvim](https://github.com/neoclide/coc.nvim)

```json
{
  "languageserver": {
    "sublime-syntax": {
      "command": "sublime-syntax-language-server",
      "filetypes": ["syntax_test", "yaml"]
    },
  }
}
```

### [vim-lsp](https://github.com/prabirshrestha/vim-lsp)

```vim
if executable('sublime-syntax-language-server')
  augroup lsp
    autocmd!
    autocmd User lsp_setup call lsp#register_server({
          \ 'name': 'sublime-syntax',
          \ 'cmd': {server_info->['sublime-syntax-language-server']},
          \ 'whitelist': ['syntax_test', 'yaml'],
          \ })
  augroup END
endif
```

## [Neovim](https://neovim.io)

```lua
vim.api.nvim_create_autocmd({ "BufEnter" }, {
  pattern = { "syntax_test_*", "*.sublime-syntax" },
  callback = function()
    vim.lsp.start({
      name = "sublime-syntax",
      cmd = { "sublime-syntax-language-server" }
    })
  end,
})
```

## [Emacs](https://www.gnu.org/software/emacs)

```elisp
(make-lsp-client :new-connection
(lsp-stdio-connection
  `(,(executable-find "sublime-syntax-language-server")))
  :activation-fn (lsp-activate-on "syntax_test_*" "*.sublime-syntax")
  :server-id "sublime-syntax")))
```

## [Sublime](https://www.sublimetext.com)

```json
{
  "clients": {
    "sublime-syntax": {
      "command": [
        "sublime-syntax-language-server"
      ],
      "enabled": true,
      "selector": "source.sublime-syntax"
    }
  }
}
```

## [Visual Studio Code](https://code.visualstudio.com/)

[An official support of generic LSP client is pending](https://github.com/microsoft/vscode/issues/137885).

### [vscode-glspc](https://gitlab.com/ruilvo/vscode-glspc)

`~/.config/Code/User/settings.json`:

```json
{
  "glspc.serverPath": "sublime-syntax-language-server",
  "glspc.languageId": "syntax_test"
}
```
