---
title: "[Study] pinhole camera model"
date: 2026-01-10 18:00:00 +0900
categories: [Study]
tags: [Study,3D Vision]
---

 ![Figure 1](/assets/img/Study/pinhole-camera-model/Figure1.webp)

컴퓨터 비전에서는 보통 오른손 좌표계를 사용하며 이미지 좌표계에서는 왼쪽 아래를 (0,0)으로 설정합니다

![Figure 2](/assets/img/Study/pinhole-camera-model/Figure2.webp)

카메라로 사진을 찍으면 렌즈를 통해 객체의 빛이 통과하여 image plane에 객체가 반대로 상이 맺히게 됩니다.

![Figure 6](/assets/img/Study/pinhole-camera-model/Figure6.webp)

컴퓨터 비전에서는 계산의 편의성을 위하여 image plane을 카메라 앞에 두게 됩니다.
camera center와 image plane 사이의 거리를 focal length(f)라 칭합니다. 
![Figure 3](/assets/img/Study/pinhole-camera-model/Figure3.webp)

그림과 같이 현실 세계의 X = (X, Y, Z) 점이 image plane 상에 어느 좌표에 맺히는지는 삼각형의 닮음을 이용하여 계산합니다.


![Figure 4](/assets/img/Study/pinhole-camera-model/Figure4.webp)
(X,Y,Z)와 각 좌표를 N배 한 (NX,NY,NZ)는 image plane상에 같은 좌표에 맺히게 됩니다.

![Figure 5](/assets/img/Study/pinhole-camera-model/Figure5.webp)

카메라 1대로는 depth ambiguity로 인하여 X의 정확한 3차원 좌표를 알 수 없습니다.



 ![Figure 7](/assets/img/Study/pinhole-camera-model/Figure7.webp)

카메라 왜곡은 2가지 종류가 있습니다.

1. 렌즈 왜곡(Lens distortion): 카메라가 어떤 렌즈를 사용하느냐에 따라서 가장자리가 실제 모습을 담지 못하고 휘게 됩니다.
2. 접선 왜곡(Tangential distortion): 렌즈 중심,센서 중심,광축이 일직선이 되어야 하지만 삐뚤어져서 생기는 문제입니다. 하지만 보통 컴퓨터 비전에서는 접선 왜곡을 무시합니다.

 ![Figure 8](/assets/img/Study/pinhole-camera-model/Figure8.webp)

해당 수식은 Radial distortion을 모델링한 식입니다. k는 얼마나 왜곡되었는지 정하는 계수이며 r은 중심으로 부터의 거리입니다.

 ![Figure 9](/assets/img/Study/pinhole-camera-model/Figure9.webp)

 ![Figure 10](/assets/img/Study/pinhole-camera-model/Figure10.webp)

여기서 f_x와 f_y는 똑같은 값으로 하는 경우가 많기 때문에 굳이 표시를 하지 않는 경우가 많습니다.

s가 skew라고 하며 x축과 y축이 정확히 수직이 아닐 경우를 조정하는 값이지만 대부분은 0으로 둡니다.

 ![Figure 11](/assets/img/Study/pinhole-camera-model/Figure11.webp)

카메라의 외부 파라미터를 기반으로 카메라를 회전(R)하고 이동(t)할 수 있습니다

 ![Figure 12](/assets/img/Study/pinhole-camera-model/Figure12.webp)

만약 월드 좌표계상에서 점X를 카메라 좌표계로 변환하고 싶다면 C를 월드 좌표계상의 카메라 좌표라 한다면 R(X-C)+t를 통해 구할 수 있습니다

 ![Figure 13](/assets/img/Study/pinhole-camera-model/Figure13.webp)

카메라 캘리브레이션이란 여러 개의 실제 이미지를 바탕으로 내/외부 파라미터를 추정하는 작업입니다.

 ![Figure 14](/assets/img/Study/pinhole-camera-model/Figure14.webp)

이미 내부파라미터는 알고있기 때문에 R,t,렌즈 왜곡을 구하는 작업입니다.

---

> 해당 내용은 동아대학교 임한신 교수님의 수업 자료를 바탕으로 첨부하였습니다.

---

