execute pathogen#infect()

filetype plugin indent on
syntax on

" Vertical line in insert mode
let &t_ti.="\e[1 q"
let &t_SI.="\e[5 q"
let &t_EI.="\e[1 q"
let &t_te.="\e[0 q"

" Back-space
set backspace=indent,eol,start

" Dracula colorscheme
let g:dracula_italic = 0
colorscheme dracula

set cursorline

" Wildmenu settings
set wildmenu
set wildmode=longest:full,full

" <Nop> arrow keys
cnoremap <Up> <C-W><C-K>
cnoremap <Down> <C-W><C-J>
cnoremap <Left> <C-W><C-H>
cnoremap <Right> <C-W><C-L>

inoremap <Up> <C-W><C-K>
inoremap <Down> <C-W><C-J>
inoremap <Left> <C-W><C-H>
inoremap <Right> <C-W><C-L>

nnoremap <Up> <C-W><C-K>
nnoremap <Down> <C-W><C-J>
nnoremap <Left> <C-W><C-H>
nnoremap <Right> <C-W><C-L>

vnoremap <Up> <C-W><C-K>
vnoremap <Down> <C-W><C-J>
vnoremap <Left> <C-W><C-H>
vnoremap <Right> <C-W><C-L>

" Enable line numbers
set nu

" Use 2 spaces for indentation
set expandtab
set tabstop=2
set softtabstop=2
set shiftwidth=2

" Very high scroll-offset to vertically align
set so=999

" Know when Gutentags is generating tags
set statusline+=%{gutentags#statusline()}

" Hide tag files
let g:gutentags_cache_dir = expand('~/.tags')

" Only index, C, C++, Python files
let g:gutentags_file_list_command = 'find -regex ".*/.*\.\(c\|cpp\|cc\|hpp\|h\)$"'

" Prevent YCM from asking if its safe to load .ycm_extra_conf.py file
let g:ycm_confirm_extra_conf = 0

" Prevent YCM from showing preview window
set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0

" Always show left sidebar
set signcolumn=yes

" Natural splitting
set splitbelow
set splitright

set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-ats6-src-tags
set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-ats-core-src-tags
set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-li-atscppapi_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-controls_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-libs_trunk-tags
set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-yaml-cpp_trunk-tags

