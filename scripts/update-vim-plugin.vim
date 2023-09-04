#!/usr/bin/env -S nvim --headless -u
" Update syntax/syntax_test.vim
let g:filename = expand('<sfile>:p:h:h')
      \ . '/src/sublime_syntax_language_server/assets/json/sublime-syntax.json'
let g:dict = json_decode(join(readfile(g:filename), ''))
let g:xilinx = join(reverse(sort(keys(g:dict))), '\|')
noswapfile edit syntax/syntax_test.vim
" vint: -ProhibitCommandRelyOnUser -ProhibitCommandWithUnintendedSideEffect
%substitute/syntax match .*Keyword `\\<\\%(\zs.*\ze\\)\\ze\\%(\\\.\\|\\>\\)` contained/\=trim(g:xilinx)/
" vint: +ProhibitCommandRelyOnUser +ProhibitCommandWithUnintendedSideEffect
write
quit
