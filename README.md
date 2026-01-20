# 🤖 AI Helpy Chat UI Automation Test Project

## 📌 프로젝트 개요
본 프로젝트는 **AI Helpy Chat** 서비스의 핵심 기능에 대해  
UI 자동화 테스트를 적용하여 **품질 검증의 효율성과 신뢰성**을 높이기 위한 QA 프로젝트입니다.

Selenium 기반 UI 자동화 테스트를 통해  
로그인, 채팅, 검색, 도구 기능 등 주요 사용자 흐름을 검증했으며,  
**Jenkins CI 환경에서 테스트를 자동 실행**하여 코드 변경 시 빠른 피드백이 가능하도록 구성했습니다.

테스트 구조는 **Page Object Model(POM)** 을 적용해  
유지보수성과 재사용성을 고려하여 설계했습니다.

---

## 🗓 프로젝트 기간
- 2025.12.08 ~ 2025.12.24

---

## 🎯 프로젝트 목표
- 반복적인 UI 테스트 자동화를 통한 **테스트 효율성 향상**
- 수동 테스트에서 놓치기 쉬운 **회귀 결함 조기 발견**
- Jenkins CI 연계를 통한 **테스트 자동 실행 환경 구축**
- 테스트 표준화를 통한 **품질 안정성 및 QA 생산성 강화**

---

## 🧪 테스트 범위
- 회원가입 및 로그인 기능
- 채팅 메시지 입력 및 AI 응답 검증
- 채팅 수정 및 추가 동작 확인
- 검색 기능 동작 검증
- 도구 메뉴 클릭 및 기능 생성 확인
- 입력값 유효성 및 UI 상태 변화 검증

---

## 🛠 사용 기술 및 도구

| 구분 | 기술 |
|------|------|
| Language | Python |
| Test Framework | pytest |
| UI Automation | Selenium |
| CI Tool | Jenkins |

---

## 👩‍💻 프로젝트 팀 소개

| 이름 | 역할 |
|------|------|
| 김나라 (팀장) | 채팅 고급 기능, 검색·히스토리·도구 TC 및 고급 기능 자동화 코드 작성 |
| 양정은 (부팀장) | 채팅 기본 기능 TC 작성, 채팅·검색·도구 자동화 코드 작성 |
| 이명주 | 계정/조직 TC 작성 및 자동화 코드 작성 |

---

## 📁 프로젝트 폴더 구조

```text
QA_PROJECT1_TEAM05/
├── pages/                 # Page Object Model (POM)
│   ├── login_page.py
│   ├── chat_page.py
│   ├── search_page.py
│   └── tool_page.py
│
├── tests/                 # 테스트 시나리오
│   ├── test_login.py
│   ├── test_chat_*.py
│   ├── test_search.py
│   └── test_tool_*.py
│
├── utils/                 # 공통 유틸리티
│   ├── driver.py
│   ├── helper.py
│   └── constants.py
│
├── Jenkinsfile            # CI 파이프라인 설정
├── README.md
├── requirements_win.txt
└── requirements_mac.txt
```

---

## 🚀 프로젝트 이후 개인 개선 사항

> 프로젝트 종료 이후, QA 역량 강화를 위해 개인적으로 아래 항목들을 개선 및 보완하고 있습니다.

- **Jenkins 파이프라인을 추가**하여 UI 자동화 테스트의 자동 실행 환경 구성
- **테스트 케이스 구조 리팩토링**을 통한 가독성 및 유지보수성 향상
  - 채팅 고급 기능에 대한 POM 구조화 작업
  - POM 구조 내에서 페이지별 UI 로케이터를 정리·분리
- 테스트 결과 리포트 도입 검토 (예: Allure)

---

