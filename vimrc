set number
set incsearch
set hls
set ic
set showcmd

""mask map
map <C-n> :tabNext <cr>
map <F4>  @q
nmap <F5> :cs find c <C-R>=expand("<cword>")<CR><CR>
nmap <F6> :cs find g <C-R>=expand("<cword>")<CR><CR>
nmap <F7> :cs find s <C-R>=expand("<cword>")<CR><CR>
nmap <F8> :cs find e struct <C-R><C-W> *{<CR>
nmap <F9> :TlistToggle <CR>
""if ./cscope.out exist ,so add it
if filereadable("./cscope.out")
	cs add ./cscope.out
endif

""if !filereadable("tags")
""	:!ctags-exuberant -R
""endif
set tags=./tags
