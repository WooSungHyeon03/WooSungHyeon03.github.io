---
title: "[Paper Review] Mip-Splatting: Alias-free 3D Gaussian Splatting"
date: "2026-01-18 18:00:00 +0900"
categories: [Paper Review]
tags: [Paper Review, 3D Vision]
math: true
---

Author: [Zehao Yu](https://arxiv.org/search/cs?searchtype=author&query=Yu,+Z), [Anpei Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+A), [Binbin Huang](https://arxiv.org/search/cs?searchtype=author&query=Huang,+B), [Torsten Sattler](https://arxiv.org/search/cs?searchtype=author&query=Sattler,+T), [Andreas Geiger](https://arxiv.org/search/cs?searchtype=author&query=Geiger,+A)

[[github]](https://github.com/autonomousvision/mip-splatting) [[page]](https://niujinshuchong.github.io/mip-splatting/) [[paper]](https://arxiv.org/abs/2311.16493) [[Online Viewer]](https://niujinshuchong.github.io/mip-splatting-demo/)



### 1. Introduction

---

![Figure 1](/assets/img/Paper-Review/Mip-Splatting/Figure1.webp)

3DGS는 최적화 이후 low-pass filtering을 위해 2D dilation operation을 수행하게 됩니다. 하지만 이 과정 때문에 훈련 뷰보다 확대하거나 축소 했을 때 artifact가 생기게 됩니다. 축소 시 screen에 투영된 2D Gaussian의 크기가 줄어들게 되며 이때 동일한 dilation을 적용하면 dilation artifact가 발생합니다. 반대로 확대 시 2D Gaussian의 크기가 커짐에도 동일한 dilation이 적용되어 erosion이 발생하여 Gaussian 사이에 잘못된 간격이 생기는 erosion artifact가 발생합니다.

Mip-Splatting은 고주파가 입력 이미지의 sampling rate에 의해 본질적으로 제한된다는 통찰을 바탕으로 Nyquist-Shannon Sampling Theorem에 따라 훈련 뷰를 기반으로 Gaussian 프리머티브의 다중 뷰 주파수 경계를 도출합니다. 최적화동안 3D Gaussian 프리머티브에 low-pass filter를 적용함으로써 3D representation의 최대주파수가 Nyquist limit을 충족하도록 제한합니다. 

훈련 후 filter는 장면 표현의 고유한 부분이 되어 시점 변화에 관계없이 일정하게 유지됩니다. 하지만 그럼에도 축소 시 aliasing이 발생합니다. 이를 해결하기 위해 2D Mip filter를 도입합니다. 2D Mip filter는 2D box filter를 모방하여 이를 2D Gaussian low pass filter로 근사합니다.

### 3.Preliminaries

---

#### 3.1. Sampling Theorem

Nyquist-Shannon Sampling Theorem은 정보의 손실 없이 이산적인 샘플로부터 정확하게 재구성할 수 있는 조건을 설명하며 다음과 같은 조건이 충족되어야합니다.

- 최대 주파수 $$ν$$를 넘는 주파수가 있어서는 안 된다
- Sampling rate $$\overset{\wedge}{v}$$은 최대 주파수 $$ν$$의 2배여야 한다.

실제로 이산 샘플로부터 신호를 재구성할 때 샘플링 전에 신호에 low-pass 또는 anti-aliasing filter를 적용합니다. 이 filter는  $$\frac{\overset{\wedge}{\nu}}{2}$$이상의 주파수 성분을 제거하고 aliasing을 유발하는 고주파를 감쇄시킵니다.

3DGS는 픽셀보다 작은 2D Gaussian이 퇴화된 경우를 방지하기 위해 다음과 같이 dilation을 적용합니다.

$$
G^{2D}_k(x)
= \exp\left(
-\frac{1}{2}\,(x - p_k)^{T}\,(\Sigma^{2D}_k + sI)^{-1}\,(x - p_k)
\right)
$$

여기서 $$I$$는 2D 단위 행렬이며 $$s$$는 dilation hyperparameter 입니다. 이것은 2D Gaussian의 최댓값은 유지하면서 scale을 조정합니다.

### 4. Sensitivity to Sampling Rate

---

기존 3DGS의 최적화가 Fig 1과 같이 ambiguities로 인해 어려움을 겪습니다. Fig 1의 (a)에서 Gaussian kernel(size ≈ 1 pixel) dilation 적용으로 인해 (b)에서 Dirac $$δ$$로 표현되는 degenerate 3D Gaussian은 유사한 이미지를 생성합니다. Gaussian이 작을수록 더 높은 주파수를 표현하기 때문에 이 dilation은 결과적으로 스케일의 과소평가를 초래합니다.

카메라를 확대하거나 더 가까이 이동하면 erosion이 발생합니다. 이는 dilation이 적용된 2D Gaussian이 스크린 상에서 상대적으로 더 작게 작용하기 때문입니다. 이 경우 렌더링된 이미지는 고주파 artifact를 나타내며 (d)와 같이 객체 구조를 더 가늘게 렌더링합니다. 반대로 축소하면 dilation은 radiance를 픽셀 전체에 퍼뜨립니다. (c)에서 3D 객체의 투영이 차지하는 면적이 1픽셀보다 작지만 팽창된 Gaussian은 감쇠되지 않아서 물리적으로 픽셀에 도달하는 빛보다 더 많은 빛을 축적하게 됩니다. 이는 수백만 개의 Gaussian을 포함하는 scene에서 특히 문제가 됩니다.

하지만 dilation이 없다면 복잡한 장면에서 최적화가 어려우며 densification으로 인해 수많은 작은 Gaussian이 생성되며 aliasing 효과가 발생합니다.

### 5.Mip Gaussian Splatting

---

Mip Splatting은 다음과 같은 2가지 방법을 제안합니다

- 훈련이미지에 의해 결정된 최대 sampling rate의 절반 이하로 제한하는 3D smoothing filter를 도입하여 확대 시 발생하는 고주파 artifact를 제거합니다.
- 2D screen space dilation을 물리적 이미지 프로세스에 내재된 box filter를 근사하는 2D Mip filter로 교체함으로써 aliasing과 dilation문제를 완화합니다.

#### 5.1. 3D Smoothing Filter

최대 주파수는 학습 뷰에 의해 정의된 sampling rate에 의해 제한됩니다.  Nyquist theorem에 따라 3D 표현의 최대 주파수를 제한하는 것을 목표로 합니다.

**Multiview Frequency Bounds:** sampling rate은 image resolution, camera focal length, 물체까지의 카메라 거리에 관련이 있습니다. focal length $$f$$를 가진 이미지의 경우, 스크린 공간에서의 sampling 간격은 1입니다. 이 sampling 간격이 3D World space로 역투영되면 주어진 깊이 $$d$$에서 World Space 간격 $$\overset{\wedge}{T}$$가 발생하며 그 역수인 sampling 주파수$$\overset{\wedge}{\nu}$$는 다음과 같습니다.

$$
\hat{T} = \frac{1}{\hat{\nu}} = \frac{d}{f}
$$

주파수$$\overset{\wedge}{v}$$로 추출된 샘플들이 주어지면  $$\frac{\overset{\wedge}{v}}{2}$$ 또는  $$\frac{f}{2d}$$의 주파수를 가진 신호 성분들로 재구성할 수 있습니다. 결과적으로 $$2\overset{\wedge}{T}$$보다 작은 primitive는 그 크기가 샘플링 간격의 2배 미만으로 splatting 과정 중에 aliasing artifact를 유발합니다.

단순화를 위해 depth $$d$$는 프리머티브의 중심 $$p_k$$로 근사하며 샘플링 간격 추정시 occlusion은 무시합니다. 프리머티브의 sampling rate은 깊이에 의존하며 카메라마다 다르기 때문에, 프리머티브$$k$$에 대한 최대 sampling rate은 다음과 같이 정의합니다. 

$$
\hat{\nu}_k=\max\left(\left\{\mathbb{1}_n(p_k)\cdot \frac{f_n}{d_n}\right\}_{n=1}^{N}\right)
$$

$$N$$은 전체 이미지 수이며 $$\mathbb{1}_n(p_k)$$는 프리미티브의 가시성을 평가하는 indicator 함수입니다. Gaussian의 중심 $$p_k$$가 $$n$$번째 camera의 view frustum에 위치할 경우 1이 됩니다. 직관적으로 해당 프리머티브를 재구성할 수 있는 카메라가 적어도 하나 존재하도록 sampling rate을 선택합니다. 이 과정은 매 $$m$$ =100 iter마다 프리머티브의 최대 sampling rate을 다시 계산합니다. 아래 그림은 N=5일때 예시입니다.

![Figure 3](/assets/img/Paper-Review/Mip-Splatting/Figure3.webp)

**3D Smoothing:** 최대 sampling rate  $$\hat{\nu}_k$$가 주어지면 최대 주파수를 제한합니다. 이는 스크린 공간에 투영하기 전에 각 프리머티브에 Gaussian low-pass filter $$\mathcal{G}_{\text{low}}$$를 적용함으로써 달성할 수 있습니다.

$$
\mathcal{G}_k(\mathbf{x})_{\text{reg}} = (\mathcal{G}_k \otimes \mathcal{G}_{\text{low}})(\mathbf{x})
$$

이 연산은 공분산 행렬 $$Σ_1$$과$$Σ_2$$를 가진 두 Guassian을 컨볼루션하면 분산이 $$Σ_1+Σ_2$$인 또 다른 Guassian이 생성되므로 효율적입니다.

$$
\mathcal{G}_k(\mathbf{x})_{\text{reg}} = \sqrt{\frac{|\Sigma_k|}{\left|\Sigma_k + \frac{s}{\hat{\nu}_k} \cdot \mathbf{I}\right|}} e^{-\frac{1}{2}(\mathbf{x}-\mathbf{p}_k)^T \left(\Sigma_k + \frac{s}{\hat{\nu}_k} \cdot \mathbf{I}\right)^{-1} (\mathbf{x}-\mathbf{p}_k)} \tag{9}
$$

$$s$$는 filter의 사이즈를 조절하는 하이퍼파라미터입니다. 3D filter 사이즈 $$\frac{s}{\hat{\nu}_k}$$는 training view에 따라 달라집니다. 3D Gaussian smoothing을 적용함으로써 어떤 Gaussian의 최대 주파수 성분도 최대 sampling rate의 절반을 초과하지 않도록 보장합니다. 또한 $$\mathcal{G}_{\text{low}}$$는 3D representation의 고유한 부분이 되어 학습 후에도 일정하게 유지됩니다.

#### 5.2. 2D Mip Filter

3D smoothing이 효과적으로 고주파 artifact를 완화하지만 여전히 더 낮은 sampling rate에서 렌더링(축소하거나 카메라를 멀리 이동)할때 aliasing이 발생할 수 있습니다. 이를 극복하기 위해 기존 dilation 대신에 2D Mip filter를 적용합니다. Mip-Splatting은 카메라 센서의 픽셀에 도달하는 광자들이 픽셀 영역에 걸쳐 통합되는 물리적 이미지 프로세스를 복제합니다. 이상적인 모델은 이미지 공간에서 2D box filter를 사용하겠지만, 효율성을 위해 이를 2D Gaussian filter로 근사합니다.

$$
G_k^{2D}(\mathbf{x})_{\text{mip}} = \sqrt{\frac{\left|\Sigma_k^{2D}\right|}{\left|\Sigma_k^{2D} + s\mathbf{I}\right|}} e^{- \frac{1}{2} (\mathbf{x} - \mathbf{p}_k)^T \left(\Sigma_k^{2D} + s\mathbf{I}\right)^{-1} (\mathbf{x} - \mathbf{p}_k)}
$$

$$s$$는 스크린공간에서 단일 픽셀을 덮도록 선택됩니다. Mip filter가 EWA filter와 유사하지만 기저 원리는 다릅니다. Mip filter는 이미지 프로세스의 box filter를 복제하도록 설계되어 단일 픽셀의 정확한 근사를 목표로 합니다. 반면 EWA 필터의 역할은 주파수 신호의 대역폭을 제한하는 것이며, 필터의 크기는 경험적으로 선택됩니다. EWA논문은 단위 공분산 행렬을 권장하여 스크린에서 3x3pixel 영역을 차지하게 합니다. 하지만 이러한 접근 방식은 아래 실험 결과에서 보여주듯이 축소할 때 지나치게 smoothing 됩니다.

![Figure 2](/assets/img/Paper-Review/Mip-Splatting/Figure2.webp)

### 6. Experiments

---

#### 6.1 Implementation

2D Mip filter의 분산을 단일 픽셀에 근사하도록 0.1로 선택하고, 3D smoothing filter의 분산을 0.2로 선택하여, 3DGS의 확장을 EWA filter로 대체한 3DGS+EWA 및 3DGS와의 공정한 비교를 위해 총합을 0.3으로 설정했습니다.

![Table 1](/assets/img/Paper-Review/Mip-Splatting/Table1.webp)

![Figure 4](/assets/img/Paper-Review/Mip-Splatting/Figure4.webp)

![Table 2](/assets/img/Paper-Review/Mip-Splatting/Table2.webp)

![Figure 5](/assets/img/Paper-Review/Mip-Splatting/Figure5.webp)

![Table 3](/assets/img/Paper-Review/Mip-Splatting/Table3.webp)

![Table 4](/assets/img/Paper-Review/Mip-Splatting/Table4.webp)

#### 6.4. Limitations

1. 효율성을 위해 box filter를 근사치로 Gaussian filter를 사용하지만 이 근사는 스크린 공간에서 Gaussian이 작을 때 오차를 유발합니다.
2. $$m=100$$ iter 마다 sampling rate을 계산해야하므로 training overhead가 소폭 증가합니다.

