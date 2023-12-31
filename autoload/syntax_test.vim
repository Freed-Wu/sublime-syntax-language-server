""
" @section Introduction, intro
" @library
" NOTE: Don't edit this file directly!
" <doc/@plugin(name).txt> is generated by <https://github.com/google/vimdoc>.
" See <README.md> for more information about installation and screenshots.
"
" Note: if you use |indentLine|, remember: >
"     let g:indentLine_fileTypeExclude = ['syntax_test']
" <

""
" Set b:current_syntax and b:syntax_test_comment,
"
" If filetype detect fails,
" (e.g., |rainbow_csv| uses |autocmd| |Syntax| to change filetype)
" you can assign it manually. >
"     call syntax_test#init('csv')
" <
"
" Use |b:current_syntax|'s language server.
" Source |b:current_syntax|'s syntax, then source syntax_test's syntax.
function! syntax_test#init(...) abort
  " https://github.com/google/vimdoc/issues/122
  ""
  " Use the first word of the first line to be default comment symbol.
  " If the first line is blank, use 'commentstring'.
  "
  " http://www.sublimetext.com/docs/syntax.html#testing
  call g:sublime_syntax#utils#plugin.Flag('b:syntax_test_comment',
        \ get(split(getline(1)), 0, '')
        \ )
  if empty(b:syntax_test_comment)
    let b:syntax_test_comment = get(split(&commentstring, '\s*%s'), 0, '#')
  endif

  if a:0 == 1
    let b:current_syntax = a:1
  else
    filetype detect
    " 'syntax' may be incorrect "ON" when modeline change filetype.
    " So we use 'filetype'.
    if ! exists('b:current_syntax')
      let b:current_syntax = empty(&filetype) ? expand('%:e') : &filetype
    endif
  endif
  execute 'set filetype=' . b:current_syntax . '.syntax_test'
endfunction
