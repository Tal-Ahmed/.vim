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

" Airline cache enable
let g:airline_highlighting_cache = 1

" Airline settings
if ! has('gui_running')
  set ttimeoutlen=10
  augroup FastEscape
    autocmd!
    au InsertEnter * set timeoutlen=0
    au InsertLeave * set timeoutlen=1000
  augroup END
endif

" Dracula colorscheme
let g:dracula_italic = 0
colorscheme dracula
highlight Normal ctermbg=None

set cursorline

" Wildmenu settings
set wildmenu
set wildmode=longest:full,full

" <Nop> arrow keys
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

" Only index, C, C++ files
let g:gutentags_file_list_command = 'find -regex ".*/.*\.\(c\|cpp\|cc\|hpp\|h\)$"'

let g:gutentags_ctags_extra_args = ['--extra=+f']

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

autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-ats6-src-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-ats-core-src-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-core-ats-core_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-li-atscppapi_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-lixclient_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-controls_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-plugin-libs_trunk-tags
autocmd Filetype c,cpp set tags+=~/.tags/home-mtalha-dev-ats-libs-ats-lib-yaml-cpp_trunk-tags

" Global YCM configuration file
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'

" YCM custom IDE-like mappings
nnoremap rr :YcmCompleter RefactorRename 
nnoremap gd :YcmCompleter GoToDefinition<CR>
nnoremap gD <C-]><CR>
nnoremap gt :YcmCompleter GetType<CR>
