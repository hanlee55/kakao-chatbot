import os

# 현재 디렉토리 및 프로젝트 디렉토리 설정
current_dir = os.path.dirname(__file__)
bname = os.path.basename(current_dir)
project_dir = current_dir.replace(f"{bname}", "")
docs_dir = os.path.join(project_dir, 'docs', 'source')
kakao_dir = os.path.join(docs_dir, 'kakao_chatbot')
response_dir = os.path.join(kakao_dir, 'response')
components_dir = os.path.join(response_dir, 'components')

# 필요한 디렉토리 생성
os.makedirs(docs_dir, exist_ok=True)
os.makedirs(kakao_dir, exist_ok=True)
os.makedirs(response_dir, exist_ok=True)
os.makedirs(components_dir, exist_ok=True)

# 모듈 파일 리스트
modules = [
    'kakao_chatbot.event',
    'kakao_chatbot.base',
    'kakao_chatbot.context',
    'kakao_chatbot.customerror',
    'kakao_chatbot.input',
    'kakao_chatbot.utils',
    'kakao_chatbot.validation',
    'kakao_chatbot.response',
    'kakao_chatbot.response.base',
    'kakao_chatbot.response.interaction',
    'kakao_chatbot.response.components.card',
    'kakao_chatbot.response.components.common',
    'kakao_chatbot.response.components.itemcard',
    'kakao_chatbot.response.components.simple',
]

# 각 모듈에 대한 파일 내용 작성


def create_module_content(module_name, module_path):
    return '# ' + module_name + ' 모듈\n\n```{eval-rst}\n.. automodule:: ' + module_path + '\n   :members:\n   :undoc-members:\n   :show-inheritance:\n```\n'


# 파일 생성 및 내용 작성
for module in modules:
    module_name = module.split('.')[-1]
    module_path = module
    file_name = module.replace('.', '/') + '.md'
    file_path = os.path.join(docs_dir, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.exists(file_path):
        print(f"{file_path} 파일이 이미 존재합니다.")
        continue
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(create_module_content(module_name, module_path))

print("필요한 모듈 파일이 생성되었습니다.")
