# 🌐 Smart Korean Food Menu Analyzer for Foreigners

## 소개

Smart Korean Food Menu Analyzer는 외국인 유학생과 관광객이 한국 음식점 메뉴를 보다 쉽게 이해할 수 있도록 개발된 클라우드 기반 OCR 애플리케이션입니다.

사용자는 한국어 메뉴판 사진을 업로드할 수 있으며, 시스템은 OCR 기술을 사용하여 메뉴 텍스트를 추출한 후 자체 구축한 한국 음식 데이터베이스와 매칭합니다. 이후 영어 번역, 음식 설명, 매운맛 단계, 돼지고기 포함 여부, 알레르기 유발 성분 등의 정보를 제공합니다.

### Live Demo

[Streamlit Cloud 링크](https://smart-korean-food-menu-analyzer-for-foreigners.streamlit.app/)

### GitHub Repository

[GitHub 레포지토리 링크](https://github.com/atieh98/Smart-Korean-Food-menu-analyzer-For-Foreigners)

---

## 주요 기능

### 🍽 한국어 메뉴 OCR 인식

한국어 언어팩이 적용된 Tesseract OCR을 사용하여 업로드된 메뉴 이미지에서 음식명을 추출합니다.

### 🌶 음식 안전 및 식단 정보 제공

인식된 각 메뉴에 대해 다음 정보를 제공합니다.

* 영어 번역
* 음식 설명
* 매운맛 단계
* 돼지고기 포함 여부
* 알레르기 정보

### 🧑‍💻 개발자 모드

이미지 처리 파이프라인을 확인할 수 있는 진단용 모드를 제공합니다.

포함 기능:

* 스택된 메뉴 이미지 출력
* 이진화(Binary Thresholding) 결과 확인
* OCR 처리 과정 점검

### ☁️ 클라우드 배포

애플리케이션은 Streamlit Cloud에 배포되어 있으며 웹 브라우저를 통해 바로 사용할 수 있습니다.

---

## 기술 스택

* Python 3
* Streamlit
* OpenCV
* NumPy
* PyTesseract
* Tesseract OCR

---

## 핵심 구현 내용

### 1. 다중 열 메뉴 처리

많은 한국 음식점 메뉴판은 여러 개의 열(Column)로 구성되어 있습니다.

OCR 성능 향상을 위해 이미지를 3개의 영역으로 분할한 후 하나의 이미지로 수직 결합하여 OCR을 수행합니다.

```python
uniform_width = w_slice + (2 * padding)

col1 = image[0:h, 0:uniform_width]
col2 = image[0:h, w_slice - padding : w_slice * 2 + padding]
col3 = image[0:h, w - uniform_width : w]

stacked_image = np.vstack((col1, col2, col3))
```

이 방식은 모든 이미지 조각의 너비를 동일하게 유지하여 NumPy 스택 오류를 방지하고, 열 경계에 위치한 텍스트도 안정적으로 보존합니다.

---

### 2. 이미지 전처리 파이프라인

OCR 추출 전에 업로드된 이미지에 여러 단계의 전처리를 수행합니다.

#### Step 1: 그레이스케일 변환

이미지를 흑백 형태로 변환합니다.

#### Step 2: Bilateral Filtering

텍스트 경계는 유지하면서 노이즈를 제거합니다.

```python
denoised = cv2.bilateralFilter(gray, 11, 85, 85)
```

#### Step 3: Adaptive Gaussian Thresholding

OCR에 적합한 고대비 이진 이미지를 생성합니다.

```python
binary = cv2.adaptiveThreshold(
    denoised,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    15,
    7
)
```

#### Step 4: Morphological Closing

문자 사이의 작은 공백을 줄이고 연결성을 향상시킵니다.

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
cleaned_binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

---

### 3. 3단계 음식명 매칭 전략

OCR 결과에는 공백 오류, 특수문자 노이즈 또는 부분적인 문자 인식 오류가 포함될 수 있습니다.

신뢰도를 높이기 위해 3단계 매칭 전략을 적용했습니다.

#### Level A: 직접 매칭

OCR 결과 내부에서 음식명을 완전히 일치하는 방식으로 검색합니다.

#### Level B: 정규식 간격 허용 매칭

문자 사이에 OCR 노이즈가 포함되어도 매칭이 가능하도록 처리합니다.

예시:

```text
김.밥 → 김밥
```

구현 방식:

```python
pattern = ".*".join(list(food_name))

if re.search(pattern, cleaned_text_block):
    matched_items.append(...)
```

#### Level C: 문자 밀도 기반 매칭

인식된 한 줄 안에 목표 음식명의 문자가 얼마나 포함되어 있는지 계산하여 보조 매칭을 수행합니다.

이를 통해 OCR 결과가 일부 손상된 경우에도 음식명을 복구할 수 있습니다.

---

## 프로젝트 구조

```text
Smart-Korean-Food-menu-analyzer-For-Foreigners/

├── app.py
├── image_processing.py
├── menu_analyzer.py
├── requirements.txt
├── packages.txt
└── images/
```

---

## 설치 방법

### 저장소 복제

```bash
git clone https://github.com/atieh98/Smart-Korean-Food-menu-analyzer-For-Foreigners.git

cd Smart-Korean-Food-menu-analyzer-For-Foreigners
```

### Python 의존성 설치

```bash
pip install -r requirements.txt
```

### Linux 필수 패키지

Streamlit Cloud와 같은 Linux 환경에 배포할 경우 다음 패키지가 필요합니다.

```text
tesseract-ocr
tesseract-ocr-kor
```

---

## 실행 방법

```bash
streamlit run app.py
```

---

# 시스템 동작 과정

## Step 1 — 메뉴 이미지 업로드

사용자는 Streamlit 인터페이스를 통해 한국 음식점 메뉴 이미지를 업로드합니다.

![Step 1 - Upload](./images/step1_upload.png)

업로드된 이미지는 노이즈 제거 및 OCR 준비를 위해 OpenCV 전처리 파이프라인으로 전달됩니다.

---

## Step 2 — OpenCV 전처리

이미지는 다음과 같은 컴퓨터 비전 기법을 통해 처리됩니다.

* Bilateral Filtering
* Adaptive Gaussian Thresholding
* Morphological Closing
* Uniform Column Segmentation

![Step 2 - Preprocessing](./images/step2_preprocessing.png)

이 전처리 단계는 텍스트 가독성과 OCR 정확도를 향상시키며, 특히 다중 열 메뉴판에서 효과적으로 동작합니다.

---

## Step 3 — OCR 텍스트 추출

전처리된 이미지는 한국어 언어팩이 적용된 Tesseract OCR을 사용하여 분석됩니다.

인식된 텍스트는 내부 음식 데이터베이스와 비교하기 위해 사용자 정의 매칭 엔진으로 전달됩니다.

![Step 3 - OCR Logs](./images/step3_logs.png)

매칭 엔진은 OCR 인식 오류를 줄이기 위해 여러 단계의 매칭 전략을 적용합니다.

---

## Step 4 — 메뉴 분석 결과 출력

성공적으로 인식된 음식들은 정보 카드 형태로 출력됩니다.

각 카드에는 다음 정보가 포함됩니다.

* 한국어 음식명
* 영어 번역
* 음식 설명
* 매운맛 단계
* 돼지고기 포함 여부
* 알레르기 경고

![Step 4 - Output Result](./images/step4_result.png)

이를 통해 외국인 유학생과 관광객은 한국 음식 메뉴를 보다 쉽게 이해하고 음식 선택에 참고할 수 있습니다.

---

## 향후 개선 방향

향후 다음과 같은 기능을 추가할 수 있습니다.

* 한국 음식 데이터베이스 확장
* 추가 언어 지원
* 메뉴 카테고리 자동 분류
* OCR 보정 알고리즘 개선
* 음식점별 메뉴 학습 기능

---

## 참고 자료

* OpenCV Documentation — https://opencv.org/
* Streamlit Documentation — https://streamlit.io/
* Tesseract OCR — https://github.com/tesseract-ocr/tesseract
* Python Documentation — https://docs.python.org/3/
* NumPy Documentation — https://numpy.org/
