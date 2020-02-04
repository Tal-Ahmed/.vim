execute pathogen#infect()

" ---- GENERAL VIM SETTINGS ----

" Enable plugin indent
filetype plugin indent on

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
autocmd Filetype c,cpp set expandtab tabstop=2 shiftwidth=2
autocmd Filetype python set expandtab tabstop=8 softtabstop=4 shiftwidth=4

" Wildmenu to full
set wildmenu
set wildmode=longest:full,full

" ---- NERD COMMENT PLUGIN ----

" Nerd comment shortcuts for C, C++, Python
autocmd Filetype c,cpp vnoremap gc :norm 0i<C-r>='//'<CR><CR>
autocmd Filetype c,cpp vnoremap gu :norm ^<C-r>=len('//')<CR>x<CR>
autocmd Filetype python vnoremap gc :norm 0i<C-r>='#'<CR><CR>
autocmd Filetype python vnoremap gu :norm ^<C-r>=len('#')<CR>x<CR>

" ---- AIRLINE PLUGIN ----

" Airline cache enable
let g:airline_highlighting_cache = 1

" ---- DRACULA PLUGIN ----

" Dracula colorscheme
" Disable blue-box in dracula
let g:dracula_italic = 0
colorscheme dracula
highlight Normal ctermbg=None

" ---- GUTENTAGS PLUGIN ----

" Load in tags for C/C++ files
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-ats6-src-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-li-atscppapi_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-controls_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-libs_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-yaml-cpp_trunk-tags

" Know when Gutentags is generating tags
set statusline+=%{gutentags#statusline()}

" Ctag shortcuts
nnoremap <C-w><C-[> :vert winc ]<CR>

" Hide tag files
let g:gutentags_cache_dir = expand('~/.tags')

" Only index, C, C++ files
let g:gutentags_file_list_command = 'find -regex ".*/.*\.\(c\|cpp\|cc\|hpp\|h\)$"'

" Tag file names as well
let g:gutentags_ctags_extra_args = ['--extra=+f']

" ---- YOU COMPLETE ME PLUGIN ----

" Prevent YCM from asking if its safe to load .ycm_extra_conf.py file
let g:ycm_confirm_extra_conf = 0

" Prevent YCM from showing preview window
set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0

" Global YCM configuration file
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'

" YCM custom IDE-like mappings
nnoremap rr :YcmCompleter RefactorRename 
nnoremap gD :YcmCompleter GoToDefinition<CR>
noremap gt :YcmCompleter GetType<CR>
