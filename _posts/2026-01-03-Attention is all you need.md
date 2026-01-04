---
title: "[Paper Review] Attention Is All You Need"
date: 2026-01-04 18:00:00 +0900
categories: [Paper Review]
tags: [Paper Review]
math: true 
---

Author: [Ashish Vaswani](https://arxiv.org/search/cs?searchtype=author&query=Vaswani,+A), [Noam Shazeer](https://arxiv.org/search/cs?searchtype=author&query=Shazeer,+N), [Niki Parmar](https://arxiv.org/search/cs?searchtype=author&query=Parmar,+N), [Jakob Uszkoreit](https://arxiv.org/search/cs?searchtype=author&query=Uszkoreit,+J), [Llion Jones](https://arxiv.org/search/cs?searchtype=author&query=Jones,+L), [Aidan N. Gomez](https://arxiv.org/search/cs?searchtype=author&query=Gomez,+A+N), [Lukasz Kaiser](https://arxiv.org/search/cs?searchtype=author&query=Kaiser,+L), [Illia Polosukhin](https://arxiv.org/search/cs?searchtype=author&query=Polosukhin,+I)

[[paper]](https://arxiv.org/abs/1706.03762) [[github]](https://github.com/tensorflow/tensor2tensor)

### 1 Introduction

---

지금까지 언어 모델링 및 기계 번역과 같은 시퀀스 모델링 및 변환 문제에서 순환 신경망은 SOTA 방법론으로 확고히 자리 잡았습니다.

하지만 이러한 순환 신경망은 순차적인 특성이 훈련의 병렬화를 방해하여 메모리 제약이 배치 크기를 제한하기 때문에 더 긴 시퀀스 길이에서 문제가 발생합니다. 시퀀스가 길어질수록 RNN의 고질적인 문제인 초반의 단어에 대해서 vanishing gradient 문제가 발생하며, context vector에 input정보가 다 담겨야해서 bottleneck이 발생합니다.

그래서 해당 논문은 순환을 완전히 배제한 트랜스포머를 제안합니다. 트랜스포머는 병렬화를 가능하게 하여 새로운 SOTA를 달성했습니다.



### 3 Model Architecture

---

![Figure 1](./assets/img/Paper-Review/Attention Is All You Need/Figure1.webp)

위 사진은 트랜스포머의 구조를 나타낸 그림입니다. 그림에서는 encoder와 decoder가 하나씩 되어있지만 실제로는 encoder와 decoder가 N개씩 이루어져있습니다.



#### 3.1 Encoder and Decoder Stacks

해당 논문에서는 encoder의 개수를 N=6 개로 합니다.

encoder는 두 개의 하위 계층으로 나눠집니다. 하나는 Multi-Head Attention이고 두번째는 Feed-Forward 입니다.

트랜스포머는 두 하위 계층에서 ResNet에서 선보인 Residual Connection을 채택함으로써 학습과정에서 잔차만 학습하도록 하여 효율을 높였습니다.

Residual Connection을 용이하게 하기 위해서 하위 계층과 임베딩 계층의 output 차원을 모두 d<sub>model</sub> = 512 로 통일하였습니다.

<br>

decoder의 개수도 N=6 개로 합니다.

decoder에서는 encoder의 두 하위계층에서 출력된 output을 처리하는 세번째 하위 계층인 Multi-Head Attention이 있습니다. 

decoder의 하위 계층도 encoder와 동일하게 residual connection을 도입하고 normalization을 수행하게 됩니다.

decoder의 Self-Attention을 수정하여 앞에 있는 단어가 뒤에 있는 단어를 Attention수행하는 것을 방지합니다.

쉽게 말해서 I love you 를 한글로 번역한다고 할 때, I를 번역할 때 love you라는 단어를 보지 못하도록 masking 처리합니다.

love도 마찬가지로 번역한다고 하면 앞에 있는 I를 참고할 수 있지만 뒤에 you는 보지 못하도록 masking 처리합니다.  

이렇게 하는 이유는 encoder를 지났을 때 결과값이 각각의 단어 I,love,you 모두 서로가 어떻게 번역이 되어야하는지 이미 가지고 있는 상태입니다.

그래서 masking 처리하지 않으면 훈련 시 GT를 주고 GT를 예측하는 것과 같은 개념입니다.



#### 3.2 Attention

Attention은 query와 (key,value)쌍 으로 구분합니다. 여기서 query,key,value는 모두 vector이며 Attention을 계산할 때 query와 (key,value)쌍을 weighted sum을 통해 구하게 됩니다.

 

![Figure 2](./assets/img/Paper-Review/Attention Is All You Need/Figure2.webp)



#### 3.2.1 Scaled Dot-Product Attention

Fig.2의 왼쪽 그림인 Scaled Dot-Product Attention에 대해서 설명하겠습니다.

input은 d<sub>k</sub>차원의 query,key 그리고 d<sub>v</sub>차원의 value로 구성됩니다. query와 key는 차원을 같도록 만들어서 dot product가 가능하게 합니다.

저희는 query를 모든 key들과 dot product수행하며   $\sqrt{d_{k}}$로 나눕니다. 그리고 softmax를 적용하여 values에 대한 가중치를 얻습니다.

그 가중치를 values와 dot product를 수행합니다. 수식은 아래와 같습니다.

$$
\operatorname{Attention}(Q, K, V) = \operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

여기서  굳이  $\sqrt{d_{k}}$를 나누는 이유는 d<sub>k</sub>값이 커지면 $QK^{\top}$가 너무 커지거나 작아져서 softmax의 기울기가 0에 가까운 vanishing gradient 문제가 발생하기 때문에 값을 낮추기 위해서 나눠줍니다. 아래는 softmax 함수입니다.

![softmax](./assets/img/Paper-Review/Attention Is All You Need/softmax.webp)



#### 3.2.2 Multi-Head Attention

d<sub>model</sub>만큼 한번에 연산을 하는 대신에 h로 d<sub>model</sub>를 나눠서 병렬적으로 Scaled Dot-Product를 진행 후 차원이 d<sub>v</sub>인 output들을 얻습니다.

그리고 해당 output들을 concat하는 방식으로 이루어져 있습니다.

$$
\begin{align*}
\operatorname{MultiHead}(Q, K, V) &= \operatorname{Concat}(\text{head}_1, \dots, \text{head}_h) W^O \\
\quad \text{where } \text{head}_i &= \operatorname{Attention}(QW_i^Q, KW_i^K, VW_i^V)
\end{align*}
$$

이렇게 query,key,value를 도출하기 위한 차원도 다음과 같이 맞췄습니다.

$W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$,

$W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k}$,

$W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$,

$W^O \in \mathbb{R}^{h d_v \times d_{\text{model}}}$

해당 논문에서는d<sub>model</sub>=512이며 h=8로 설정하여 d<sub>k</sub>,d<sub>v</sub> = 8로 설정 하였습니다.



#### 3.2.3 Applications of Attention in our Model

이렇게 Multi-Head Attention은 3 하위 계층에서 사용됩니다. 

decoder에서는 encoder-decoder attention을 사용합니다. decoder는 queries는 이전 decoder layer에서 오는 것이며 keys,values는 encoder의 output으로 받게 됩니다. 

encoder는 self-attention을 포함합니다. encoder의 self-attention에서 queries,keys,values는 이전 encoder에서 받아옵니다.

decoder는 처음 embedding에서 self-attention을 수행할 수 있습니다. 해당 layer에서는 masking(-$\infty$)를 해서 앞의 단어만 참고할 수 있도록 설계하였습니다.



#### 3.3 Position-wise Feed-Forward Networks

Attention layer 이후에 fully connected feed-forward network를 통과합니다.

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

구조가 MLP와 동일하며 activation function은 ReLU를 사용하였습니다. input 차원은 d<sub>model</sub>=512이며 중간 차원인 d<sub>ff</sub> = 2048으로 한번 펼쳤다가 다시 output은 d<sub>model</sub>=512으로 출력합니다.

#### 3.4 Embeddings and Softmax

트랜스포머는 input token과 output token 모두 d<sub>model</sub>=512 차원의 벡터로 변화하기 위해 학습된 임베딩을 사용합니다.

decoder의 최종 출력은 선형 변환을 거친 후 softmax를 통하여 input token에 대한 예측 확률이 나오게 됩니다.

트랜스포머는 encoder input embedding layer, decoder input embedding layer,softmax이전에 선형변환에서 동일한 가중치 행렬을 공유합니다. 이러한 가중치 공유는 모델의 파라미터 수를 줄일 수 있습니다

embedding layer에 $\sqrt{d_{model}}dmodel$을 곱해줍니다.



#### 3.5 Positional Encoding

각 token에 관계성과 위치 정보를 삽입하기 위해 임베딩과 동일한 차원인 d<sub>model</sub>=512 Positional Encoding을 더해줍니다.

$$
PE_{(pos, 2i)} = \sin(pos/10000^{2i/d_{\text{model}}})
$$

$$
PE_{(pos, 2i +1)} = \cos(pos/10000^{2i/d_{\text{model}}})
$$

파장은 2π부터 10000 · 2π까지 등비수열을 형성합니다.

이 함수를 채택한 이유는 PE가 고정된 offset에 선형 함수로 표현될 수 있기 때문입니다.

![Positional Encoding](./assets/img/Paper-Review/Attention Is All You Need/positional encoding.webp)

학습가능한 positional embedding으로 대체 할 수 있으며 실험 상 둘다 비슷한 성능을 냈습니다.

### 4 Why Self-Attention

---

Self-Attention을 사용한 이유는 병렬화가 가능하여 computational complexity가 낮으며 long-range dependencies 문제를 해결 할 수 있습니다.

![Table1](./assets/img/Paper-Review/Attention Is All You Need/Table1.webp)

### 5 Training

---



#### 5.1 Training Data and Batching

학습은 450만 개의 문장 쌍으로 구성된 standard WMT 2014 English-German 데이터셋으로 학습했습니다.

영어-프랑스어는 3600만 개의 문장으로 구성된  significantly larger WMT 2014 English-French 데이터셋으로 학습했습니다.

#### 5.2 Hardware and Schedule

총 8개의 NVIDIA P100 GPU로 이루어진 컴퓨터로 학습을 진행하였으며 각 학습 단계는 약 0.4초가 소요 되었습니다.

기본 트랜스포머 모델은 100,000 스탭 또는 12시간 동안 학습했습니다.

빅 트랜스포머 모델은 스텝 시간은 1초였으며 300,000 스탭(3.5일)동안 학습했습니다.

#### 5.3 Optimizer

Adam Optimizer를  $\beta_1 = 0.9,\ \beta_2 = 0.98,\ \epsilon = 10^{-9}$ 로 사용 했으며 학습률은 다음 공식을 사용했습니다.

$$
lrate = d_{\text{model}}^{-0.5} \cdot \min(\text{step\_num}^{-0.5}, \text{step\_num} \cdot \text{warmup\_steps}^{-1.5})
$$

warm up steps 동안 학습률을 선형적으로 증가시키고, 스탭 수의 역제곱근에 비례하여 감소 시켰으며 warm up steps = 4000을 사용했습니다.

#### 5.4 Regularization

학습 중 세 가지 정규화를 사용합니다.

Residual Dropout : 각 서브 layer의 output에 dropout을 적용하며,이는 서브 layer input에 더해지고 정규화되기 전에 수행됩니다. 또한, encoder와 decoder 모두 embedding과 positional encoding의 합에 dropout을 적용 했습니다. P<sub>drop</sub> = 0.1을 사용했습니다.

Label Smoothing: 훈련 중 $\epsilon_{\mathrm{ls}} = 0.1$ 을 사용했습니다. 이는 perplexity를 높이지만 정확도와 BLEU 점수에 기여합니다.

### 6 Results

---

해당 부분은 결과를 나타냅니다.  

![Table2](./assets/img/Paper-Review/Attention Is All You Need/Table2.webp)

![Table3](./assets/img/Paper-Review/Attention Is All You Need/Table3.webp)

Table 1 (A)에서 볼 수 있듯이 Single Head Attention은 성능 하락으로 이어집니다.

Table 3 (B)에서 볼 수 있듯이 d<sub>k</sub>를 줄이는 것은 성능 하락으로 이어집니다.

![Table4](./assets/img/Paper-Review/Attention Is All You Need/Table4.webp)



### 7 Conclusion

---

우리는 Attention 기반 모델의 미래에 대해 기대가 크며 이를 다른 작업에도 적용할 계획입니다. 

우리는 Transformer를 텍스트 외의 입력 및 출력 모달리티를 포함하는 문제로 확장하고, 이미지, 오디오 및 비디오와 같은 대규모 입력 및 출력을 효율적으로 처리하기 위해 지역적이고 제한된 Attention 메커니즘을 조사할 계획입니다. 

생성을 덜 순차적으로 만드는 것은 우리의 또 다른 연구 목표입니다.

---



아래는 Attention을 시각화한 것 입니다. 

![Figure 3](./assets/img/Paper-Review/Attention Is All You Need/Figure3.webp)

![Figure 4](./assets/img/Paper-Review/Attention Is All You Need/Figure4.webp)

![Figure 5](./assets/img/Paper-Review/Attention Is All You Need/Figure5.webp)

