execute pathogen#infect()

" ---- GENERAL VIM SETTINGS ----

" Enable plugin indent
filetype plugin indent on

" Setup autoread
set autoread

" Syntax highlighting
syntax on

" Display a vertical line in insert mode
let &t_ti.="\e[1 q"
let &t_SI.="\e[5 q"
let &t_EI.="\e[1 q"
let &t_te.="\e[0 q"

" Disable 1s display when switching from insert to normal mode
if ! has('gui_running')
  set ttimeoutlen=10
  augroup FastEscape
    autocmd!
    au InsertEnter * set timeoutlen=0
    au InsertLeave * set timeoutlen=1000
  augroup END
endif

" Prevent vim from auto commenting
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Enable back-space
set backspace=indent,eol,start

" Enable highlighting current line
set cursorline

" Map arrow-keys to move around splits
cnoremap <C-k> <C-W><C-K>
cnoremap <C-j> <C-W><C-J>
cnoremap <C-h> <C-W><C-H>
cnoremap <C-l> <C-W><C-L>

inoremap <C-k> <C-W><C-K>
inoremap <C-j> <C-W><C-J>
inoremap <C-h> <C-W><C-H>
inoremap <C-l> <C-W><C-L>

nnoremap <C-k> <C-W><C-K>
nnoremap <C-j> <C-W><C-J>
nnoremap <C-h> <C-W><C-H>
nnoremap <C-l> <C-W><C-L>

vnoremap <C-k> <C-W><C-K>
vnoremap <C-j> <C-W><C-J>
vnoremap <C-h> <C-W><C-H>
vnoremap <C-l> <C-W><C-L>

" Enable line numbers
set nu

" Very high scroll-offset to vertically align
set so=999

" Always show left sidebar
set signcolumn=yes

" Natural splitting
set splitbelow
set splitright

" Indentation for different file types 
autocmd Filetype c,cpp set cindent 
autocmd Filetype c,cpp set expandtab tabstop=2 softtabstop=2 shiftwidth=2 cinoptions=g+1,h1,(0,w1,N-s
autocmd Filetype python set expandtab tabstop=8 softtabstop=4 shiftwidth=4

" Wildmenu to full
set wildmenu
set wildmode=longest:full,full

" ---- AIRLINE PLUGIN ----

" Airline cache enable
let g:airline_highlighting_cache = 1

" ---- DRACULA PLUGIN ----

" Dracula colorscheme
" Disable blue-box in dracula
let g:dracula_italic = 0
colorscheme dracula
highlight Normal ctermbg=None

" ---- CTAGS SETTINGS ----

" Load in tags for C/C++ files
let cur_dir = expand('%:p')
:while cur_dir != '/'
:	for tag_file in split(globpath(cur_dir, 'tags-*'), '\n')
:		let resolved_tag_file = resolve(tag_file)
:		exec 'set tags+='.resolved_tag_file
:	endfor
:	let cur_dir = fnamemodify(cur_dir, ':h')
:endwhile

" Ctag shortcut for opening vertical split
nnoremap <C-w><C-[> :vert winc ]<CR>

" ---- YOU COMPLETE ME PLUGIN ----

" Disable signature help
let g:ycm_disable_signature_help = 1

" Allow YCM to look at tag files
let g:ycm_collect_identifiers_from_tags_files = 1

" Prevent YCM from asking if its safe to load .ycm_extra_conf.py file
let g:ycm_confirm_extra_conf = 0

" Prevent YCM from showing preview window
set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0

" Global YCM configuration file
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'
