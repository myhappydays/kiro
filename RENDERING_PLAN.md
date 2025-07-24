# Kiro v2.0 렌더링 계획

이 문서는 Kiro의 각 요소를 어떤 HTML 구조로 변환할지에 대한 최종 목표를 정의합니다.

## 1. 기본 원칙

- **시맨틱 HTML**: 모든 요소는 의미에 가장 적합한 HTML 태그로 변환하여 웹 접근성과 표준을 준수한다.
- **CSS 클래스 기반 스타일링**: 인라인 `style` 속성 사용을 지양하고, `kiro-[요소명]` 형태의 CSS 클래스를 부여하여 디자인 커스터마이징을 용이하게 한다.
- **파서와 렌더러의 분리**: 파서는 AST(추상 구문 트리)를 생성하는 데 집중하고, 렌더러는 이 AST를 받아 HTML로 변환하는 역할만 담당한다.

---

## 2. 요소별 렌더링 목표

### 🔹 마크다운 호환 요소

| Kiro 문법 | HTML 결과물 | 비고 |
| :--- | :--- | :--- |
| `# 제목` | `<h1>제목</h1>` | `#` 개수에 따라 `<h1>` ~ `<h6>`로 변환 |
| `---` | `<hr>` | |
| `**굵게**` | `<strong>굵게</strong>` | |
| `*기울임*` | `<em>기울임</em>` | |
| `~~취소선~~` | `<s>취소선</s>` | |
| `인라인 코드` | `<code>인라인 코드</code>` | |
| ```python ...` | `<pre><code class="language-python">...</code></pre>` | Pygments 라이브러리가 생성한 HTML을 그대로 사용 |

### 🔹 리스트 시스템

1.  **표준 리스트 (`-`, `*`, `+`)**
    -   **Kiro**: `- 항목 1
  - 항목 1-1`
    -   **HTML**: `<ul><li>항목 1<ul><li>항목 1-1</li></ul></li></ul>`
    -   들여쓰기 레벨에 따라 `<ul>`를 중첩하여 계층을 표현한다.

2.  **보고서형 리스트 (`-1.A.`)**
    -   **Kiro**: `-1. 첫째
-1.A. 첫째의 첫째`
    -   **HTML (권장)**:
        ```html
        <ol class="kiro-report-list">
            <li class="level-1">1. 첫째</li>
            <li class="level-2">1.A. 첫째의 첫째</li>
        </ol>
        ```
    -   **설명**: 전체를 하나의 `<ol>`로 묶어 리스트임을 명시한다. 각 항목은 `<li>`로 처리하되, 계층 정보를 `level-n` 클래스로 부여하여 CSS로 정교한 들여쓰기 제어가 가능하게 한다. 사용자가 입력한 `1.A.` 키는 `<li>` 태그 안에 텍스트로 그대로 유지한다.

### 🔹 Kiro 전용 구문

1.  **스타일 시스템 (`<style>`, `[name]<>`)**
    -   **`<style>` 블록**: HTML로 렌더링되지 않는다. 파서는 이 블록의 내용을 내부 CSS 규칙 사전으로 저장한다.
    -   **`[tip]내용<>`**: `<span class="kiro-tip">내용</span>` 으로 변환된다.
    -   **최종 결과물**: 파서가 수집한 CSS 규칙 사전의 내용은 최종 HTML 문서의 `<head>` 안에 `<style>` 태그로 삽입되거나, 별도의 CSS 파일로 생성된다.

2.  **외부 리소스 (`@type: ...`)**
    -   `@img: path/to/image.png (설명)` -> `<figure><img src="path/to/image.png" alt="설명"><figcaption>설명</figcaption></figure>`
    -   `@link: https://... (설명)` -> `<a href="https://..." class="kiro-link">설명</a>`

3.  **인용 (`|`)**
    -   `| 인용문` -> `<blockquote><p>인용문</p></blockquote>`

4.  **각주 (`[^id]`, `[^id]: ...`)**
    -   **참조 `[^1]`**: `<sup><a href="#fn-1" id="fnref-1" class="kiro-footnote-ref">1</a></sup>`
    -   **내용 `[^1]: 내용`**: 문서 마지막에 생성될 각주 목록 영역에 `<li id="fn-1">내용 <a href="#fnref-1" class="kiro-footnote-backref">↩</a></li>` 형태로 추가된다. 전체 각주 목록은 `<ol class="kiro-footnotes">`로 감싸진다.

5.  **토글 (`>`)**
    -   `> 제목` -> `<details><summary>제목</summary></details>`
    -   `> 제목
>> 내용` -> `<details><summary>제목</summary><div><p>내용</p></div></details>`
    -   중첩된 토글은 중첩된 `<details>` 태그로 표현한다.

6.  **이스케이프 (`\`)**
    -   파서가 처리하며, 렌더러는 일반 텍스트로 받는다. 예를 들어 `\*`는 파서에서 `*`로 변환되어 렌더러에 전달된다.
