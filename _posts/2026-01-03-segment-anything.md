---
title: "[Paper Review] Segment Anything"
date: 2026-01-03 18:00:00 +0900
categories: [Paper Review]
tags: [Paper Review]
---
Author: [Alexander Kirillov](https://arxiv.org/search/cs?searchtype=author&query=Kirillov,+A), [Eric Mintun](https://arxiv.org/search/cs?searchtype=author&query=Mintun,+E), [Nikhila Ravi](https://arxiv.org/search/cs?searchtype=author&query=Ravi,+N), [Hanzi Mao](https://arxiv.org/search/cs?searchtype=author&query=Mao,+H), [Chloe Rolland](https://arxiv.org/search/cs?searchtype=author&query=Rolland,+C), [Laura Gustafson](https://arxiv.org/search/cs?searchtype=author&query=Gustafson,+L), [Tete Xiao](https://arxiv.org/search/cs?searchtype=author&query=Xiao,+T), [Spencer Whitehead](https://arxiv.org/search/cs?searchtype=author&query=Whitehead,+S), [Alexander C. Berg](https://arxiv.org/search/cs?searchtype=author&query=Berg,+A+C), [Wan-Yen Lo](https://arxiv.org/search/cs?searchtype=author&query=Lo,+W), [Piotr Dollár](https://arxiv.org/search/cs?searchtype=author&query=Doll%C3%A1r,+P), [Ross Girshick](https://arxiv.org/search/cs?searchtype=author&query=Girshick,+R)

[[`Github`](https://github.com/facebookresearch/segment-anything?tab=readme-ov-file/)][[`Paper`](https://ai.facebook.com/research/publications/segment-anything/)] [[`Project`](https://segment-anything.com/)] [[`Demo`](https://segment-anything.com/demo)] [[`Dataset`](https://segment-anything.com/dataset/index.html)] [[`Blog`](https://ai.facebook.com/blog/segment-anything-foundation-model-image-segmentation/)] [[`BibTeX`](https://github.com/facebookresearch/segment-anything?tab=readme-ov-file#citing-segment-anything)]

### Introduction
---
방대한 데이터셋으로 훈련된 LLM, foundation model은 새로운 task가 주어지더라도  정교한 프롬프트 엔지니어링을 통해 zero-shot에서도 범용적인 성능을 내고 있습니다.<br>
그리고 foundation model을 task에 맞게 fine-tuning 했을때 더 좋은 성능을 낼 수 있습니다.<br>
하지만 현재 컴퓨터 비전의 대부분의 문제들중 대다수는 방대한 훈련 데이터셋이 존재하지 않습니다.<br>
그래서 해당 논문은 image segmentation을 위한 foundation model을 구축하는 것을 목표로 합니다.<br>
SAM은 promptable하면서 방대한 데이터셋으로 훈련시켜 generalization한 model을 구축합니다.<br>
해당 모델을 구축하기 위해 세가지를 제시합니다.<br>
1. What **task** will enable zero-shot generalization?
2. What is the corresponding **model** architecture?
3. What **data** can power this task and model?


![Figure 1](/assets/img/Paper-Review/Segment-Anything/Figure1.webp)
<br>


#### task<br>
프롬프트가 모호하여 여러 객체를 지칭할 수 있는 경우에도  출력은 해당 객체 중 적어도 하나에 대한 합리적인 mask여야 함을 의미합니다.<br>
(예를 들어 셔츠 라는 프롬프트를 입력했다면 셔츠 자체를 나타낼 수도 있고 그것을 입고 있는 사람을 나타낼 수도 있음)<br>

![Figure 3](/assets/img/Paper-Review/Segment-Anything/Figure3.webp)
<br>

#### model<br>
모호한 프롬프트에도 유연하게 대처하며 mask를 실시간으로 생성하기 위해서 다음과 같은 구조를 제시합니다.<br>
image encoder가 image embedding을 계산<br>
prompt encoder가 prompt embedding을 계산<br>
이후 두 information sources가 lightweight mask decoder에서 결합하여 segmentation mask를 예측합니다. <br>
SAM은 이렇게 encoder와 decoder를 분리함으로써 동일한 image embedding은 다른 prompts와 함께 재사용되어 비용 부담이 분산됩니다<br>


![Figure 4](/assets/img/Paper-Review/Segment-Anything/Figure4.webp)
<br>


Image encoder에서는 scalability와 pretraining methods를 고려하여 pre-trained ViT인 MAE를 사용합니다.<br>
Image encoder는 프롬프트가 적용되기전에 image 당 한번 사용됩니다.<br>

Prompt encoder는 (point,box,text)와 (mask) 이렇게 두가지 프롬프트를 고려합니다.<br>
point,box는 각 프롬프트 유형에 대한 pretrained embedding으로 합산된 positional encoding으로 표현<br>
text는 CLIP의 off-the-shelf text encoder로 표현<br>
mask는 convolution을 사용하여 embedding되며 image embedding과 요소별로 합산됩니다.<br>

mask decoder는 image embedding과 프롬프트 embedding 및 출력 토큰을 효율적으로 mask에 매핑합니다.<br>
Transformer의 decoder block을 수정하여 뒤에 dynamic mask prediction head로 이어집니다.<br>
decoder block에서 모든 embedding을 업데이트하기 위해 prompt-image 사이로 self-attention과 cross-attention을 사용합니다.<br>
두 개의 block을 실행 후 image embedding을 업샘플링하고 MLP가 출력 토큰을 dynamic linear classifier로 매핑하며, 각 image 위치에서 mask foreground 확률을 계산합니다.<br>
SAM은 focal loss와 dice loss를 선형 조합으로 mask 예측을 지도합니다.<br>
기하학적 프롬프트 혼합을 사용하여 프롬프트 세분화 작업을 학습하며, mask 당 11라운드에서 프롬프트를 무작위로 샘플링합니다.<br>

모호한 프롬프트를 대체하기 위해 단일 프롬프트에 여러 유효한 mask를 출력하도록 하였으며 3개의 mask정도가 일반적인 경우 충분했습니다.<br>
그래서 학습 중 mask에 대한 최소한의 손실만 역전파하도록 하였으며 각 mask의 순위를 매기기 위해 IoU를 통해 신뢰도를 예측합니다.<br>

모델의 효율을 높이기 위해 이미 계산된 image embedding이 주어지면, prompt encoder와 mask decoder는 웹 브라우저에서 CPU를 사용하여 50ms안에 실행됩니다.<br>



#### data<br>
generalization한 model을 구축하기 위한 방대한 데이터셋은 충분하지 않습니다.<br>
데이터를 수집하고 model을 학습시키는 과정을 반복합니다. 그리고 3가지 단계로 이루어진 data engine을 제시합니다.<br>
첫번째 assisted-manual은 SAM이 annotators의 annotating mask를 돕습니다.<br>
annotators는 브라우저에서 클릭기반으로 labeling하며 실시간으로 SAM이 돕게 됩니다. annotators는 mask를 중요도 순서대로 객체에 labeling하도록 요청받았지만 mask 하나를 주석하는 데 30초 이상 걸리면 다음 image 로 진행하도록 권장했습니다.<br>
SAM은 일반적인 공개 segmentation 데이터셋으로 훈련한 다음으로 새로 annotation된 mask만을 사용하여 재훈련합니다.<br>
많은 mask가 수집되어 image encoder는 ViT-B에서 ViT-H로 확장됩니다 총 6번의 모델 재훈련을 수행했습니다.<br>
모델이 개선됨에 따라 mask 당 평균 34초에서 14초로 감소되었으며 평균 mask 수도 20개에서 44개로 증가했습니다.<br>
이 단계에서 120k image 로부터 4.3M의 mask를 수집했습니다.<br>

두번째 semi-automatic은 SAM이 객체에 자동으로 mask를 생성할 수 있으며 annotators가 나머지 객체에 대한 annotating에 집중할 수 있도록 해줍니다. <br>
이 단계에서는 모델의 segmentation 능력 향상을 위해 mask의 다양성을 증가시키는 것을 목표로 합니다.<br>
그래서 annotators가 덜 중요한 객체에 집중하기 위해 먼저 SAM이 자동으로 mask를 생성하고 annotators는 mask가 되지않은 objects에 작업하도록 했습니다.<br>
SAM이 중요한 객체를 인식하기 위해 먼저 일반적인 객체 카테고리를 사용한 mask를 학습합니다. 이 과정에서 우리는 5.9M mask와 180k image 를 얻습니다. 그리고 우리가 모은 새로운 데이터셋으로 다시 5번 훈련 시킵니다.<br>
자동으로 생성된 mask를 제외하고 annotating하는 데 34초 정도 걸렸으며 평균 image  당 mask 수도 44개에서 72개로 증가했습니다.<br>

세번째 fully automatic은 foreground points의 regular grid으로 SAM에게 prompt를 제공하며, SAM은 image  당 평균 100개의 고품질 mask를 생성합니다.<br>
해당 단계에서는 model이 모호한 case에도 유효한 mask를 생성하도록 훈련 시킵니다.<br>
먼저 32x32 regular grid of point로 프롬프트를 제시했으며, 각 점에 대해 유효한 객체에 대한 mask를 예측했습니다.<br>
만약 point가 부분 또는 하위부분에 해당하면 model은 해당 부분과 객체 전체를 반환합니다. 그리고 반환한 mask에 대해 IoU를 사용하여 임계값 이상인 신뢰할 수 있는 mask들을 선택합니다. 마지막으로 신뢰할 수 있는 mask들을 선택한 후, NMS를 적용하여 중복을 필터링 합니다.<br>
추가적으로 SAM은 작은 객체도 잘 분할하기 위해image 를 crop하여 확대하여 추론하였습니다.<br>
이렇게 11M 이상의 image와 1B 이상의 mask인 SA-1B를 구축하였습니다.<br>

![Figure 2](/assets/img/Paper-Review/Segment-Anything/Figure2.webp)
<br>



### 5. Segment Anything Dataset
---
image는 평균 3300x4950사이즈의 고해상도이지만 접근성 및 저장 문제를 야기할 수 있기 때문에 image의 가장 짧은 변을 1500으로 다운샘플링하였습니다. 하지만 대부분의 기존 비전 데이터셋보다 훨씬 높은 고해상도 입니다.<br>
mask 중 99.1%가 자동으로 생성되었습니다. 그래서 mask의 품질이 중요한데 mask의 품질을 측정하기 위해 랜덤으로 500개의 image를 선정하여 annotators에게 annotating mask를 하고 자동으로 생성된 mask와 비교해본 결과 94%의 쌍이 90% 이상의 IoU를 보였습니다.<br>

 다른 데이터셋과 비교했을때 보통 사진사는 객체를 가운데 두고 찍으려는 편향이 있습니다. 하지만 SA-1B는 다른 데이터셋에 비해 사진 전체에 골고루 분포되어 있음을 나타냅니다.<br>
 
![Figure 5](/assets/img/Paper-Review/Segment-Anything/Figure5.webp)
<br>

SA-1B는 다른 데이터셋에 비해 image도 많고 mask도 많음을 그래프로 보여줍니다.<br>
![Figure 6](/assets/img/Paper-Review/Segment-Anything/Figure6.webp)
<br>


### 6. Segment Anything RAI Analysis
---
대부분의 데이터셋은 저소득층 국가로부터의 image 비율이 상당히 낮습니다.<br>
하지만 SA-1B는 일관적으로 많다는 것을 보여주고 있습니다.<br>
![Figure 7](/assets/img/Paper-Review/Segment-Anything/Figure7.webp)
<br>

아래는 다른 데이터셋에 비하여  저소득층 국가의 image가 많다는 것을 보여주는 표 입니다.<br>
![Table 1](/assets/img/Paper-Review/Segment-Anything/Table1.webp)
<br>

아래는 SA-1B가 두 성별과 여러 나이대의 사람들과 여러 인종을 골고루 포함해서 SAM의 성능이 일관됨을 보여줍니다.<br>
![Table 2](/assets/img/Paper-Review/Segment-Anything/Table2.webp)
<br>

### 7. Zero-Shot Transfer Experiments
SAM이 Zero-Shot에서도 좋은 성능을 낼 수 있는지 실험합니다.<br>
SAM이 Zero-Shot image에서는 1. edge를 탐지하고 2. 모든 것을 분할하고 3. 탐지된 객체들을 분할하여 4. 프롬프트로 부터 객체를 분할합니다. <br>
실험은 단일 foreground point로 부터 객체를 segmentation해야하지만 하나의 점은 여러 객체를 참조할 수 있으므로 어려운 문제입니다. <br>
대부분의 데이터셋에서 GT mask는 가능한 모든 mask를 열거하지 않기때문에 다른 데이터셋 GT를 신뢰할 수 없습니다.<br>
따라서 저희는 annotators가 mIoU를 1(무의미)부터 10(픽셀 단위 완벽)까지 평가하는 인간 연구로 보완합니다.<br>

한번도 훈련되지 않은 새로운 image 데이터셋이며 23개의 데이터셋 모음을 사용합니다.<br>
![Figure 8](/assets/img/Paper-Review/Segment-Anything/Figure8.webp)
<br>

인간 실험은 인간이 하기때문에 한계가 있어서 아래 (b)에 명시되어있는 하위 항목만 실험합니다.<br>
![Figure 9](/assets/img/Paper-Review/Segment-Anything/Figure9.webp)
<br>

먼저 23개의 데이터셋에 대한 mIoU를 모두 평가합니다.<br>
그리고 SAM과 RITM모델을 비교하는데 (a)보시면 SAM이 16개의 데이터셋에서 더 좋은 성능을 내는 것을 볼 수 있습니다.<br>
여기서 가장 신뢰도가 높은 mask를 선택하는 대신 SAM의 3개의 mask중 가장  관련성 높은 mask를 선택하는 *oracle* 결과는 모든 데이터셋에서 더 높은 결과를 냈습니다.(c)<br>
인간 연구인 (b)에서도 평균적으로 SAM이 높은 점수를 내어 더 높은 성능을 입증했습니다.<br>

#### 7.2. Zero-Shot Edge Detection
SAM은 BSDS500을 사용하여 엣지 탐지에 대해 평가합니다. SAM은 16x16 regular grid of foreground points로  프롬프트를 제공하여 점당 3개씩 총 768개의 mask를 생성합니다. 중복된 mask는 NMS에 의해 제거되고 임계값 미적용 mask 확률 맵에 대해 Sobel 필터링과 후처리를 사용하여 edge를 계산합니다. SAM은 edge detection을 위해 훈련되지 않았음에도 합리적인 edge를 생성한다는 것을 관찰했습니다. 결과는 아래와 같습니다.<br>
![Figure 10](/assets/img/Paper-Review/Segment-Anything/Figure10.webp)
<br>

SAM은 어떤 edge를 억제해야하는지 학습하는 최첨단 model보다 뒤처집니다. 그에도 불구하고 선구적인 딥러닝 model과 비교했을때 좋은 성능을 보입니다. 결과는 아래와 같습니다.<br>
![Table 3](/assets/img/Paper-Review/Segment-Anything/Table3.webp)
<br>

#### 7.3. Zero-Shot Object Proposals
다음으로 SAM의 객체 제안에 대해 평가합니다.<br>
우리는 객체 생성을 제안시키기 위해 자동 mask 생성 파이프라인을 약간 수정하여 실행하고 mask를 제안으로 출력합니다.<br>
결과는 다른 객체 제안 모델보다 좋은 성능을 냅니다 결과는 아래와 같습니다.<br>
![Table 4](/assets/img/Paper-Review/Segment-Anything/Table4.webp)
<br>

#### 7.4. Zero-Shot Instance Segmentation
우리는 SAM을 instance 분할기의 분할 모듈로 사용합니다. <br>
객체 검출 모델(ViTDet)을 실행하고 해당 출력 상자로 SAM에게 프롬프트를 제공합니다.<br>
SAM이 표에서는 ViTDet보다 뒤쳐지지만 인간 연구에서는 ViTDet을 능가한다는 것을 관찰합니다. 결과는 아래와 같습니다.<br>
![Table 5](/assets/img/Paper-Review/Segment-Anything/Table5.webp)
<br>

#### 7.5. Zero-Shot Text-to-Mask
SAM의 free form text로부터 객체를 segmentation에 대해 평가합니다.<br>
면적이 100²보다 큰 수동으로 수집된 각 mask에 대해 CLIP Image embedding을 추출합니다.<br>
훈련 중에 추출된 CLIP image embedding을 첫번째 프롬프트로 합니다. 여기서 CLIP의 image embedding이 text embedding과 정렬되도록 훈련되었기 때문에, image embedding으로 훈련하고 추론 시에는 text embedding을 사용 할 수 있습니다. 즉, 추론 시에는 text를 CLIP의 text encoder를 통해 실행한 다음 결과 text embedding을 SAM에 프롬프트로 제공합니다.<br>
결과는 아래와 같이 text 프롬프트 만으로 올바른 객체를 선택하지 못할때 추가적인 점이 예측을 수정하는 경우가 많습니다.<br>
![Figure 12](/assets/img/Paper-Review/Segment-Anything/Figure12.webp)
<br>

#### 7.6. Ablations
단일 point 프롬프트를 사용하여 23개의 데이터셋에서 여러 ablations를 수행합니다.<br>
아래는 data engine단계에서 누적 데이터로 훈련된 SAM의 성능을 보여줍니다.<br>

![Figure 13](/assets/img/Paper-Review/Segment-Anything/Figure13.webp)
<br>

 각 단계가 mIoU를 증가시키는 것을 관찰합니다.<br>
 자동 mask는 수동 및 반자동 mask보다 훨씬 많습니다. 이를 해결하기 위해, 자동 및 반자동 mask를 10배 오버샘플링하는 것이 최의 결과를 가져옵니다. 하지만 이 설정은 훈련을 복잡하게 만들기 때문에 우리는 자동으로 생성된 mask만 사용하는 네번째 설정을 테스트 합니다.<br>
SA-1B의 11M개의 image를 ablation하기 위해 1M개와 0.1M개로 균일하게 서브샘플링합니다.<br>
0.1M개의 image에서는 모든 설정에서 mIoU가 크게 감소했으나 1M개의 image에서는 전체 데이터셋과 유사한 결과가 관찰됩니다.<br>
마지막으로, 그림 13(오른쪽)은 ViT-B, ViT-L, ViT-H image encoder를 사용한 결과를 보여줍니다. ViT-H는 ViT-B에 비해 상당한 성능 향상을 보이지만, ViT-L에 비해서는 미미한 성능 향상만을 보입니다. 현재로서는 image encoder 스케일링을 더 진행하는 것이 효과적이지 않은 것으로 보입니다.<br>

### Conclusion
---
Segment Anything 프로젝트는 image segmentation을 foundation model 시대로 끌어올리려는 시도입니다. 저희의 주요 기여는 이러한 도약을 가능하게 하는 새로운 작업(프롬프트 가능한 분할), 모델(SAM), 그리고 데이터셋(SA-1B)입니다. SAM이 파운데이션 모델의 지위를 달성할지는 커뮤니티에서 어떻게 사용되는지에 따라 달라지겠지만, 어쨌든 저희는 이 연구의 관점, 10억 개 이상의 mask 공개, 그리고 저희의 프롬프트 가능한 분할 모델이 앞으로 나아갈 길을 닦는 데 도움이 될 것으로 기대합니다.
