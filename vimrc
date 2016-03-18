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
""if ./cscope.out exist ,so add it
if filereadable("./cscope.out")
	cs add ./cscope.out
endif

""if !filereadable("tags")
""	:!ctags-exuberant -R
""endif
set tags=./tags

""YouCompleteMe
"let g:ycm_warning_symbol = '**'
"let g:ycm_error_symbol = '>>'
"let g:syntastic_ignore_files=[".*\.c$"]
let g:ycm_global_ycm_extra_conf='~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm/.ycm_extra_conf.py'

""turns off Syntastic
let g:ycm_show_diagnostics_ui = 0
let g:ycm_seed_identifiers_with_syntax=1

""filetype on
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm '\"")|else|exe "norm $"|endif|endif
"""YCM""
set nocompatible              " be iMproved, required
filetype off                  " required
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'L9'
Plugin 'git://git.wincent.com/command-t.git'
Plugin 'file:///home/gmarik/path/to/plugin'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'user/L9', {'name': 'newL9'}
Plugin 'Valloric/YouCompleteMe'
call vundle#end()            " required
filetype plugin indent on    " required

