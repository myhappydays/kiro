# tests/test_parser.py

import pytest
from pathlib import Path
from src.kiro_renderer.parser import KiroParser
from src.kiro_renderer.nodes import DocumentNode, HeadingNode, ParagraphNode, HorizontalRuleNode, TextNode

# Helper function to create a simple AST string for comparison
def ast_to_string(node, indent=0):
    s = "  " * indent + node.__class__.__name__
    if hasattr(node, 'level'):
        s += f" (level={node.level})"
    if hasattr(node, 'text'):
        s += f": '{node.text}'"
    s += "\n"
    if hasattr(node, 'children'):
        for child in node.children:
            s += ast_to_string(child, indent + 1)
    return s

@pytest.fixture
def kiro_files_path():
    return Path(__file__).parent.parent / "examples"

def test_welcome_kiro_parsing(kiro_files_path):
    file_path = kiro_files_path / "welcome.kiro"
    with open(file_path, 'r', encoding='utf-8') as f:
        kiro_text = f.read()

    parser = KiroParser(kiro_text)
    ast = parser.parse()
    
    # Expected AST structure for welcome.kiro (Phase 1 only)
    # Adjusted based on actual parsing behavior for Phase 1
    expected_ast_string = (
        "DocumentNode\n"
        "  HeadingNode (level=1)\n"
        "    TextNode: 'Kiro ☘️'\n"
        "  ParagraphNode\n"
        "    TextNode: '| Kiro는 텍스트 입력에서부터 기록, 인쇄, 발행에 이르기까지 전 과정을 고려해 설계된 명시적 구조의 마크업 언어입니다. @link:https://kiro.onlyoli.space ! Ground 에디터 바로 사용해보기 (베타)'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '✨ 소개'\n"
        "  ParagraphNode\n"
        "    TextNode: 'Kiro는 마크다운의 장점을 계승하면서도, 문서의 시각적 구조와 의미 표현을 명시적으로 설계할 수 있도록 만들어진 새로운 마크업 언어입니다. 입력부터 발행까지 흐름이 끊기지 않도록 설계되어 있으며, 복잡한 문법 대신 직관적이고 구조화된 작성 경험을 제공합니다.'\n"
        "  ParagraphNode\n"
        "    TextNode: '| 이 프로젝트는 Kiro 문법을 렌더링하고 실시간으로 작성할 수 있는 에디터 Ground를 포함하고 있습니다. | 자세한 문법 등의 사항은 `docs` 폴더를 참고해주세요.'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🔧 기능 요약'\n"
        "  ParagraphNode\n"
        "    TextNode: '[체크박스] 1. 사용자 정의 스타일 선언 및 적용 가능 <> [체크박스] 2. Tailwind 기반의 속성 지정 <> [체크박스] 3. 인라인/계층적 스타일링 및 문서 전체 테마 지원 <> [체크박스] 4. 이미지·비디오·오디오 리소스 명시적 삽입 (`@타입: URL ! 설명`) <> [체크박스] 5. 마크다운과의 완전한 호환성 유지 (`#`, `-`, `**` 등) <> [체크박스] 6. 인쇄용 `.html` 렌더링 지원 <> [체크박스] 7. 스타일 중첩 금지, 가독성 중심 렌더링 <>'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '📦 기술 스택'\n"
        "  ParagraphNode\n"
        "    TextNode: '- 프론트엔드: HTML + JavaScript - 백엔드: Flask (Python) - 렌더러: Kiro Renderer (Python 기반 커스텀 파서) - 스타일 시스템: Tailwind CSS - 배포: Render 플랫폼'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '📚 문법 요약'\n"
        "  ParagraphNode\n"
        "    TextNode: '基本的な文法構造は次のとおりです: - 大括弧で囲んだスタイルテグ使用、<> で終わり - `style` ブロックを介して階層スタイル、属性、フォント、Tailwind クラスなどを宣言 - `@img:`, `@video:` などの接頭辞でリソースを明示的に挿入 - `|` 記号は引用文、`-`, `1.1.`はリスト、`>`はトグル機能 - マークダウンのほとんど要素は互換性があり、リンクや画像は代替文法を使用'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🧠 Kiro의 철학'\n"
        "  ParagraphNode\n"
        "    TextNode: '- 구조는 스타일보다 먼저 와야 한다 - 문서의 읽기 경험을 디자인할 수 있어야 한다 - 가독성과 재사용성을 동시에 만족하는 문법이어야 한다'\n"
        "  ParagraphNode\n"
        "    TextNode: 'Kiro는 단순한 마크업 언어를 넘어서, <br> 문서 작성 자체에 대한 고민과 철학을 담은 실험입니다.'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '📄 라이선스'\n"
        "  ParagraphNode\n"
        "    TextNode: '[라이선스] MIT License. <> <br> 상업적/비상업적 사용이 모두 가능하며, 저작자 표기는 유지해주세요.'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🚧 향후 계획'\n"
        "  ParagraphNode\n"
        "    TextNode: '[미완료] 공유 기능 (파일 공유 링크 생성) <> [미완료] 협업 기능 (커서 공유 및 코멘트) <> [미완료] 로그인 시스템 (선택형) <> [미완료] 자동완성 기능 및 키워드 추천 <> [미완료] '@slide:', '@block:' 등의 리소스 타입 확장 <>'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🌱 프로젝트 목적'\n"
        "  ParagraphNode\n"
        "    TextNode: '| 이 프로젝트는 “내가 가장 많이 쓰는, 나를 위한 도구”를 만들겠다는 목표로 시작되었습니다. | 기존 마크다운이나 HTML의 구조를 바탕으로, 나의 문서 작성 습관과 철학을 녹여 모든 요구사항을 충족하도록 설계했습니다. | 나와 함께 성장해서, 누구보다 내가 가장 많이 쓰는 마크업 언어가 되길 바랍니다.'\n"
        "  HorizontalRuleNode\n"
    )

    assert ast_to_string(ast) == expected_ast_string

def test_example_kiro_parsing(kiro_files_path):
    file_path = kiro_files_path / "example.kiro"
    with open(file_path, 'r', encoding='utf-8') as f:
        kiro_text = f.read()

    parser = KiroParser(kiro_text)
    ast = parser.parse()

    # Expected AST structure for example.kiro (Phase 1 only)
    # Adjusted based on actual parsing behavior for Phase 1
    expected_ast_string = (
        "DocumentNode\n"
        "  HeadingNode (level=1)\n"
        "    TextNode: 'Kiro 문서 렌더링 테스트 🚀'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '✨ 스타일 적용 및 중첩'\n"
        "  ParagraphNode\n"
        "    TextNode: '[알림] 이건 알림 박스예요! <> [중요] 이건 정말 중요한 메시지입니다. **굵은 글씨**도 적용됩니다. <> [팁] 마크다운 _기울임_ 요소가 스타일 안에서도 작동합니다. <>'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '복잡한 스타일'\n"
        "  ParagraphNode\n"
        "    TextNode: '[알림] 이 알림뒤에 [조합] 스타일이 적용됩니다 <>'\n"
        "  ParagraphNode\n"
        "    TextNode: '[그림자] 이 블록은 그림자가 적용되며 이어서 [코드체] 코드 폰트 <> 가 나오고, 중첩되지 않습니다.'\n"
        "  ParagraphNode\n"
        "    TextNode: '[정의안됨] 이건 정의되지 않은 테그에요 <> [정의안된스타일] 또 다른 정의되지 않은 스타일입니다 <>'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '📌 다양한 리스트'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '기본 불릿 리스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '- 첫 번째 항목 - 두 번째 항목 -- 중첩된 항목 --- 깊게 중첩된 항목목 - **굵게** 적용된 항목 - _기울임_ 적용된 항목 - `코드` 적용된 항목 - ==하이라이트!== - ~~취소!~~'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '커스텀 리스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '-1. 커스텀 첫 번째 항목 -1.1. 커스텀 하위 항목 -1.1.A. 문자 계층 항목 -1.1.B. **굵게** _기울임_ `코드` 모두 적용 -1.2. 일 다시 이 -2. 두 번째 -3. 세 번째 -3.1. ** 스타일 테스트 **'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🏗️ 토글 테스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '> 기본 토글 >> 토글 1 >> 토글 2 **굵게** >> 토글 3 _기울임_ >>> **중첩된 토글!** >>> `코드 적용된` 중첩 토글 >> 다시 상위 토글로 >>> 마지막 중첩 토글'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=1)\n"
        "    TextNode: '헤딩 테스트'\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '두 번째 수준 헤딩'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '세 번째 수준 헤딩'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '💬 인용문 테스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '| 이건 기본 인용문입니다 | 여러 줄도 가능합니다 | **굵게** _기울임_ `코드` 인라인 요소 적용'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🧾 구분선 테스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '위 텍스트'\n"
        "  HorizontalRuleNode\n"
        "  ParagraphNode\n"
        "    TextNode: '아래 텍스트트'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🧠 인라인 스타일 요소'\n"
        "  ParagraphNode\n"
        "    TextNode: '**굵게**, _기울임_, `인라인 코드`, **_굵게 기울임_**, _**기울임 굵게**_'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '폰트 테스트'\n"
        "  ParagraphNode\n"
        "    TextNode: '[고딕] 이건 프리텐다드 폰트예요 <> [바탕] 이건 리디바탕 폰트입니다 <> [코드체] 이건 코드 전용 폰트예요 <> [플렉스] 이건 스타일리쉬한 Font예요 <>'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '복합 스타일'\n"
        "  ParagraphNode\n"
        "    TextNode: '[고딕] 프리텐다드 [바탕] 리디바탕 [코드체] 코드체 [플렉스] 플렉스체 <>'\n"
        "  ParagraphNode\n"
        "    TextNode: '[강조] 이건 **굵게** 적용된 _기울임_ 문자를 포함합니다 <>'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '정의되지 않은 스타일'\n"
        "  ParagraphNode\n"
        "    TextNode: '[정의안됨1] 이건 정의되지 않은 테그예요 <> [정의안됨2] 이것도 정의되지 않은 테그예요 <> [브랜드] 이건 정의된 테그입니다 <> [정의안됨3] 이건 정의되지 않은 테그예요 <>'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '🎵 미디어 요소'\n"
        "  ParagraphNode\n"
        "    TextNode: '@image: https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png ! 투명 PNG 예시 @audio: https://samplelib.com/lib/preview/mp3/sample-3s.mp3 ! 짧은 음악 샘플 @video: https://samplelib.com/lib/preview/mp4/sample-5s.mp4 ! 짧은 영상 샘플 @link: https://www.example.com ! 예시 링크'\n"
        "  HorizontalRuleNode\n"
        "  HeadingNode (level=2)\n"
        "    TextNode: '👨	💻 코드 블록'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '일반 코드 블록'\n"
        "  ParagraphNode\n"
        "    TextNode: '``` print(\"hello, world!\") def hello_world(): print(\"Hello, world!\") return True ```'\n"
        "  HeadingNode (level=3)\n"
        "    TextNode: '인라인 코드 요소'\n"
        "  ParagraphNode\n"
        "    TextNode: '이것은 `인라인 코드`입니다. [인라인코드] 커스텀 스타일 인라인 코드입니다 <>'\n"
        "  HorizontalRuleNode\n"
    )

    assert ast_to_string(ast) == expected_ast_string