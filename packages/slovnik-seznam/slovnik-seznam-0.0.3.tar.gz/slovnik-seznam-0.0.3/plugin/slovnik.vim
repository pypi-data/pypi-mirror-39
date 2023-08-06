" ============================================================================
" File:         slovnik.vim
" Description:  Provide slovnik.seznam.cz translation
" Maintainer:   Matěj Cepl <mcepl -at- cepl dot eu>
" Version:      0.1
" Last Change:  11 Aug, 2014
" License:      This program is free software. It comes without any warranty,
"               to the extent permitted by applicable law. You can redistribute
"               it and/or modify it under the terms of the Do What The Fuck You
"               Want To Public License, Version 2, as published by Sam Hocevar.
"               See http://sam.zoy.org/wtfpl/COPYING for more details.
"
" Bugs:         Send bugreports/patches directly to me via mail

" Only do this when not done yet for this buffer
" Usually, not needed, just for the keeping normal API
if exists("b:did_ftplugin")
    finish
endif
let b:did_ftplugin = 1

" Load this plugin only once
if exists("g:slovnik_seznam_loaded")
    finish
endif
let g:slovnik_seznam_loaded = 1

function s:checkSlovnikSeznam()
    if !executable('slovnik')
        echohl WarningMsg
        echo "You need to install slovnik first from PyPI."
        echohl None
        return 0
    endif
    return 1
endfunction

function s:Translate()
    let inslovo = inputdialog('Enter the word to translate: ', "", "")
    if inslovo != ""
        let result = system("slovnik " . inslovo)
        unsilent echo result
    endif
endfunction

" Define new commands
command! Translate   silent call s:Translate()

nnoremap <silent> <script> <leader>p :call <SID>Translate()<CR>
