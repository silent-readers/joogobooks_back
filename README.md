# <div align='center' id='top'> :book: Joogobooks </div>

## 개요

- :dizzy: Joongobooks는 중고도서거래를 위한 서비스입니다.
- :technologist: 더이상 읽지 않거나 필요하지 않은 소장 중인 책을 홈페이지에 등록할 수 있고, 사용자들이 필요로 하는 도서를 찾아 확인 후 구매할 수 있습니다.
- :robot: AI chat-bot을 이용해 책을 추천받는 서비스를 이용할 수 있습니다.

## 목차
1. [프로젝트 목표](#goal)
2. [개발 환경 및 배포 URL](#dev)
3. [프로젝트 구조](#tree)
4. [역할 분담](#role)
5. [개발 기간](#task)
6. [UI](#ui)
7. [페이지 기능](#pages)
8. [개발하며 겪은 이슈](#issues)
9. [마무리](#realization)

<hr>

## <span id="goal">1. 프로젝트 목표</span>
- 개인이 쉽게 자신의 소장도서를 판매할 수 있는 플랫폼을 제공합니다.
- 등록된 도서 목록을 누구나 쉽게 확인 가능하도록 하여 잠재적인 고객들이 쉽게 접근 가능할 수 있는 플랫폼을 제공합니다.
- 개인의 소장도서를 상품으로 등록하여 수익 창출이 가능할 수 있게 도와주는 온라인 장터입니다.
- openAI 에서 제공한 API를 활용하여 책을 추천하는 AI chatbot을 구현해 책을 추천받을 수 있는 서비스를 제공합니다.

<p align="right"><a href="#top">(Top)</a></p>
<br>

## <span id="dev">2. 개발환경 및 배포 URL</span>
### 개발환경
- Front : HTML, CSS, Vanilla JS
- Back : Python, Django Rest Framework
- openAI api

### 배포 URL
- URL : 🔗

<p align="right"><a href="#top">(Top)</a></p>
<br>

## <span id="tree">3. 프로젝트 구조</span>
<p align="right"><a href="#top">(Top)</a></p>
<img src="/readme/erd.png">


## <span id="role">4. 역할 분담</span>
<img src="/readme/TeamProject - Joongobooks.png">

### 구현기능
- 🔐<strong>계정</strong>
    - 회원가입
    - 로그인/로그아웃
    - 프로필 생성/수정
- :computer: <strong>중고도서 정보</strong>
    - 중고도서 이미지 파일 업로드, 미리보기
    - 등록 / 수정 / 삭제
    - 중고도서 목록 보기
- :robot: <strong>AI catbot (recommend)</strong>
    - chatbot 질문하기 / 답변받기
    - 하루 2번 사용가능
<p align="right"><a href="#top">(Top)</a></p>


## <span id="task">5. 개발 기간</span>
- 개발기간(23.08.17 ~ 23.09.04)
<img src="/readme/duration.png">

- 🔗<a href="https://www.notion.so/1-ba1d7268559a4fd6aebd2ac6d2e7a9d5?pvs=4"> Notion에서 Issue 관리</a>

- 🔗<a href="https://www.notion.so/7337f3775c0d43e5a75959562622ebbf"> 회의록</a>
<p align="right"><a href="#top">(Top)</a></p>

## <span id="ui">6. UI</span>

<img src="/readme/ui1.png" alt="ui1.png">

<img src="/readme/ui2.png" alt="ui1.png">

<p align="right"><a href="#top">(Top)</a></p>

## <span id="pages">7. 페이지 기능</span>
<p align="right"><a href="#top">(Top)</a></p>

## <span id="issues">8. 개발하며 겪은 이슈</span>
- 슬기님
- 승겸님
- 유림님
    - bookSearchView를 만들면서 카테고리 설정과 키워드 검색을 동시에 적용한 결과를 만들고 싶었는데, Search와 DjangoFilterBackend를 하나의 검색버튼으로 동시에 적용시킬 수 없었습니다. 그리고 검색을 filter를 사용해서 하자니 이름이 일치하는 것들만 결과물로 나와서, BookSearchFilter를 새로 만들어 적용시켰습니다. FilterSet을 상속받되, 책 제목을 검색할 때 키워드를 포함하는 모든 결과물들을 가지고 올 수 있도록 title은 icontains, sale_condition은 exact 필드를 사용하였습니다.
- 병훈님
- 예원님
<p align="right"><a href="#top">(Top)</a></p>

## <span id="realization">9. 마무리</span>
<p align="right"><a href="#top">(Top)</a></p>
- 짧은 기간의 프로젝트에서 기획부터 배포까지 진행하려니 시간이 촉박했지만, 온전히 프로젝트에 집중해서 단기간에 Django 실력을 늘린 것 같아 뿌듯합니다! 이번 프로젝트를 통해 Django도, Github로 협력하는 법도 많이 배워가는 것 같습니다. 처음에 기획했던 기능 구현을 프로젝트 기간 내 다 하지 못한 것은 아쉽지만, 추후에도 기능을 계속 업데이트 해 나가서 보다 완성도있는 프로젝트가 되게 할 예정입니다. 이 프로젝트를 위해 열심히 임해준 팀원들에게 너무 감사합니다!