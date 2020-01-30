" <Nop> arrow keys
cnoremap <Up> <Nop>
cnoremap <Down> <Nop>
cnoremap <Left> <Nop>
cnoremap <Right> <Nop>

inoremap <Up> <Nop>
inoremap <Down> <Nop>
inoremap <Left> <Nop>
inoremap <Right> <Nop>

nnoremap <Up> <Nop>
nnoremap <Down> <Nop>
nnoremap <Left> <Nop>
nnoremap <Right> <Nop>

vnoremap <Up> <Nop>
vnoremap <Down> <Nop>
vnoremap <Left> <Nop>
vnoremap <Right> <Nop>

" Enable line numbers
set nu

" Use 2 spaces for indentation
set expandtab
set tabstop=2
set softtabstop=2
set shiftwidth=2

" Very high scroll-offset to vertically align
set so=999

" Pathogen 
execute pathogen#infect()

" Know when Gutentags is generating tags
set statusline+=%{gutentags#statusline()}

" Hide tag files
let g:gutentags_cache_dir = expand('~/.tags')

" Dracula colorscheme
"colorscheme dracula
