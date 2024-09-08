import sys
import os

# 프로젝트 경로 설정
sys.path.insert(0, os.path.abspath('../'))  # 프로젝트의 상위 디렉토리로 변경
# kakao_chatbot 모듈이 포함된 디렉토리 추가
sys.path.insert(0, os.path.abspath('../kakao_chatbot'))
# kakao_chatbot.response 모듈이 포함된 디렉토리 추가
sys.path.insert(0, os.path.abspath('../kakao_chatbot/response'))


# 프로젝트 정보
project = 'kakao-chatbot'
copyright = "Copyright (c) 2024 Han Lee (이한결)\nCopyright (c) 2024 Seoyoung Hong (홍석영)"
author = "Han Lee <hanlee@indiemaker.kr>, Seokyoung Hong <seokyoung@sio2.kr>"
release = '0.1.2'

# 확장 모듈 설정
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
]

# 템플릿 경로 설정
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# 언어 설정
language = 'ko'

# 소스 파일 형식 추가
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# HTML 테마 설정
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = ['custom.css']

# MyST-Parser 설정 (옵션)
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "substitution",
    "tasklist",
]

# 자동 문서화 설정
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
