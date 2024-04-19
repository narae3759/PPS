<div style="background-color: #FEF7DE; padding: 1rem 1rem 0.3rem; margin: 1rem">
<b>🎯 목표</b>

<li>Langchain 이해 및 활용</li>
<li>업무에 필요한 보고서 생성 기능 만들기</li>
<li>정해진 문서 기반의 챗봇 만들기</li>
<li>웹 크롤링을 통한 검색 기능 만들기</li>

</div>

---

<div>
    <img src="https://github.com/narae3759/PPS/assets/93372888/a94cd16f-c0ff-433c-b9be-e299a2ecf473" width=100%/>
</div>

## 1. LLM(Large Language Model)

* LLM이란 트랜스포머 기반 모델로, 우리가 텍스트를 입력하면 그에 맞는 대답을 하는 생성AI 분야이다. 
* 생성 AI는 다양하게 활용할 수 있고 직관적으로 편리함을 느낄 수 있다는 장점이 있다.
* 하지만 많게는 조 단위의 데이터를 학습하기 때문에 모델의 크기가 매우 커 많은 자원과 시간이 필요한 분야이다.

---

## 2. LLM의 활용

LLM은 크게 3가지 방법으로 개발하게 되는데 

보통 1, 2번을 프롬프트 엔지니어링(Prompt Engineering)이라고 한다.

<div style="background-color: #D9F0FF; padding: 1rem 1rem 0.3rem; margin: 1rem">
<b>🚨 프롬프트 엔지니어링(Prompt Engineering)</b>

LLM에 입력하는 텍스트를 프롬프트(Prompt)라고 하는데, 원하는 방향으로 출력을 유도하고 제한하기 위한 기술을 말한다.
</div>


### 1️⃣ In-Context Learning 

문서 생성을 예시로 들어보자. 

나는 냉장고에 있는 재료를 입력하면 그 재료로 만들 수 있는 다이어트 레시피를 추천해주는 서비스를 만들고 싶은데, 미리 정해진 FORMAT에 맞춰 출력되었으면 좋겠다.

<div style="background-color: #D9D9D9; padding: 1rem 1rem; margin: 1rem">
INGREDIENTS: {ingredients}<br>
<br>
FORMAT:<br>
요리명:<br>
준비물: <br>
칼로리:<br>
방법:<br>
1. <br>
2. <br>
...
</div>

이처럼 텍스트를 입력할 때 출력하고 싶은 FORMAT을 미리 작성해서 원하는 답을 유도하는 것을 In-Context Learning이라고 한다. 

### 2️⃣ N-Shot Learning

N-Shot은 원하는 답을 얻기 위해 LLM에게 제공하는 예(example)의 수를 말한다. 

예를 들어 영화 리뷰의 긍/부정을 분류하고 싶다.

만약 예시 없이 LLM에 영화 리뷰를 입력하게 되면 "이 문장은 긍정입니다", "긍정", "긍정입니다" 등 다양한 답변을 얻게 된다. 이를 방지하기 위해 예시를 여러 개 제시하여 일관성을 갖도록 할 수 있다. 

<div style="background-color: #D9D9D9; padding: 1rem 1rem; margin: 1rem">
예시)<br>
영화 진짜 감동적이다 // 긍정<br>
중간에 너무 뜬금없더라 // 부정<br>
웃겨서 배터지는 줄 알았어 // 긍정<br>
</div>


### 3️⃣ Fine Tuning

새로운 데이터를 통해 LLM을 재학습하는 것을 말한다. 

모델이 매우 크기 때문에 많은 GPU가 필요하며, 이는 큰 비용을 초래한다.

---
