---
title: "Äá» Xuáº¥t Dá»± Ãn"
date: 2026-04-27
weight: 2
pre : " <b> 2. </b> "
---

# Äá»€ XUáº¤T Dá»° ÃN: Há»‡ thá»‘ng Parking IoT thÃ´ng minh

**Giáº£i phÃ¡p AWS Serverless cho giÃ¡m sÃ¡t bÃ£i Ä‘á»— xe, nháº­n diá»‡n biá»ƒn sá»‘ vÃ  há»— trá»£ AI**

## 1. TÃ³m táº¯t Ä‘iá»u hÃ nh

Dá»± Ã¡n nháº±m xÃ¢y dá»±ng há»‡ thá»‘ng **Parking IoT thÃ´ng minh** giÃºp tá»± Ä‘á»™ng hÃ³a quÃ¡ trÃ¬nh giÃ¡m sÃ¡t bÃ£i Ä‘á»— xe, nháº­n diá»‡n phÆ°Æ¡ng tiá»‡n vÃ  quáº£n lÃ½ dá»¯ liá»‡u theo thá»i gian thá»±c. Há»‡ thá»‘ng sá»­ dá»¥ng cÃ¡c thiáº¿t bá»‹ IoT nhÆ° **ESP32 Camera** vÃ  **ESP32 cáº£m biáº¿n** Ä‘á»ƒ thu tháº­p hÃ¬nh áº£nh xe ra/vÃ o, tráº¡ng thÃ¡i vá»‹ trÃ­ Ä‘á»— vÃ  dá»¯ liá»‡u tá»« bÃ£i xe.

Dá»¯ liá»‡u tá»« thiáº¿t bá»‹ Ä‘Æ°á»£c gá»­i lÃªn AWS thÃ´ng qua cÃ¡c dá»‹ch vá»¥ nhÆ° **AWS IoT Core**, **Amazon S3**, **Amazon API Gateway** vÃ  Ä‘Æ°á»£c xá»­ lÃ½ báº±ng **AWS Lambda**. HÃ¬nh áº£nh phÆ°Æ¡ng tiá»‡n Ä‘Æ°á»£c lÆ°u trá»¯ trong Amazon S3, sau Ä‘Ã³ kÃ­ch hoáº¡t Lambda Ä‘á»ƒ xá»­ lÃ½ áº£nh vÃ  gá»i **Amazon Rekognition** nháº±m nháº­n diá»‡n biá»ƒn sá»‘ xe. Káº¿t quáº£ nháº­n diá»‡n vÃ  dá»¯ liá»‡u cáº£m biáº¿n Ä‘Æ°á»£c lÆ°u vÃ o **Amazon DynamoDB** Ä‘á»ƒ phá»¥c vá»¥ viá»‡c tra cá»©u, quáº£n lÃ½ vÃ  hiá»ƒn thá»‹ trÃªn Web/App.

NgoÃ i ra, há»‡ thá»‘ng cÃ²n tÃ­ch há»£p **Amazon Bedrock** thÃ´ng qua lá»›p **Lambda AI Service** Ä‘á»ƒ há»— trá»£ phÃ¢n tÃ­ch dá»¯ liá»‡u, tráº£ lá»i cÃ¡c truy váº¥n thÃ´ng minh vÃ  cung cáº¥p tráº£i nghiá»‡m quáº£n lÃ½ bÃ£i Ä‘á»— xe hiá»‡n Ä‘áº¡i hÆ¡n. Vá»›i kiáº¿n trÃºc AWS Serverless, há»‡ thá»‘ng cÃ³ kháº£ nÄƒng má»Ÿ rá»™ng linh hoáº¡t, giáº£m chi phÃ­ váº­n hÃ nh vÃ  khÃ´ng cáº§n quáº£n lÃ½ mÃ¡y chá»§ truyá»n thá»‘ng.

---

## 2. TuyÃªn bá»‘ váº¥n Ä‘á»

### 2.1. ThÃ¡ch thá»©c hiá»‡n táº¡i

CÃ¡c bÃ£i Ä‘á»— xe truyá»n thá»‘ng thÆ°á»ng gáº·p nhiá»u háº¡n cháº¿ trong quÃ¡ trÃ¬nh váº­n hÃ nh vÃ  quáº£n lÃ½. Viá»‡c kiá»ƒm soÃ¡t xe ra/vÃ o cÃ²n phá»¥ thuá»™c nhiá»u vÃ o con ngÆ°á»i, dá»… xáº£y ra sai sÃ³t khi ghi nháº­n biá»ƒn sá»‘, thá»i gian vÃ o bÃ£i hoáº·c tráº¡ng thÃ¡i chá»— Ä‘á»—. Khi sá»‘ lÆ°á»£ng phÆ°Æ¡ng tiá»‡n tÄƒng lÃªn, viá»‡c quáº£n lÃ½ thá»§ cÃ´ng sáº½ trá»Ÿ nÃªn khÃ³ khÄƒn, thiáº¿u tÃ­nh chÃ­nh xÃ¡c vÃ  máº¥t nhiá»u thá»i gian.

Má»™t sá»‘ váº¥n Ä‘á» chÃ­nh cÃ³ thá»ƒ ká»ƒ Ä‘áº¿n nhÆ°:

* KhÃ³ kiá»ƒm tra nhanh tÃ¬nh tráº¡ng cÃ²n trá»‘ng hoáº·c Ä‘Ã£ Ä‘áº§y cá»§a tá»«ng vá»‹ trÃ­ Ä‘á»— xe.
* Viá»‡c ghi nháº­n xe ra/vÃ o cÃ²n thá»§ cÃ´ng, dá»… nháº§m láº«n biá»ƒn sá»‘ hoáº·c thá»i gian.
* Dá»¯ liá»‡u hÃ¬nh áº£nh, biá»ƒn sá»‘ vÃ  tráº¡ng thÃ¡i bÃ£i xe chÆ°a Ä‘Æ°á»£c quáº£n lÃ½ táº­p trung.
* NgÆ°á»i quáº£n lÃ½ khÃ³ theo dÃµi lá»‹ch sá»­ hoáº¡t Ä‘á»™ng cá»§a phÆ°Æ¡ng tiá»‡n.
* KhÃ³ má»Ÿ rá»™ng há»‡ thá»‘ng khi sá»‘ lÆ°á»£ng camera, cáº£m biáº¿n hoáº·c vá»‹ trÃ­ Ä‘á»— tÄƒng lÃªn.
* Viá»‡c xÃ¢y dá»±ng há»‡ thá»‘ng riÃªng cÃ³ thá»ƒ tá»‘n chi phÃ­ náº¿u pháº£i Ä‘áº§u tÆ° mÃ¡y chá»§ váº­t lÃ½.

### 2.2. Giáº£i phÃ¡p Ä‘á» xuáº¥t

Dá»± Ã¡n Ä‘á» xuáº¥t xÃ¢y dá»±ng há»‡ thá»‘ng **Parking IoT thÃ´ng minh trÃªn ná»n táº£ng AWS Serverless**. Há»‡ thá»‘ng sá»­ dá»¥ng ESP32 Camera Ä‘á»ƒ chá»¥p áº£nh xe ra/vÃ o, ESP32 cáº£m biáº¿n Ä‘á»ƒ ghi nháº­n tráº¡ng thÃ¡i chá»— Ä‘á»—, sau Ä‘Ã³ gá»­i dá»¯ liá»‡u lÃªn AWS Ä‘á»ƒ xá»­ lÃ½ vÃ  lÆ°u trá»¯ táº­p trung.

Giáº£i phÃ¡p bao gá»“m cÃ¡c chá»©c nÄƒng chÃ­nh:

* ESP32 Camera chá»¥p áº£nh phÆ°Æ¡ng tiá»‡n khi xe ra hoáº·c vÃ o bÃ£i.
* ESP32 cáº£m biáº¿n phÃ¡t hiá»‡n tráº¡ng thÃ¡i tá»«ng vá»‹ trÃ­ Ä‘á»— xe.
* áº¢nh xe Ä‘Æ°á»£c táº£i lÃªn Amazon S3 thÃ´ng qua Presigned URL.
* AWS Lambda xá»­ lÃ½ sá»± kiá»‡n khi cÃ³ áº£nh má»›i Ä‘Æ°á»£c upload lÃªn S3.
* Amazon Rekognition phÃ¢n tÃ­ch hÃ¬nh áº£nh vÃ  há»— trá»£ nháº­n diá»‡n biá»ƒn sá»‘ xe.
* DynamoDB lÆ°u thÃ´ng tin xe, biá»ƒn sá»‘, thá»i gian, tráº¡ng thÃ¡i vÃ  dá»¯ liá»‡u cáº£m biáº¿n.
* Web/App cho ngÆ°á»i dÃ¹ng truy cáº­p, Ä‘Äƒng nháº­p, xem tráº¡ng thÃ¡i bÃ£i xe vÃ  lá»‹ch sá»­ xe ra/vÃ o.
* Amazon Cognito há»— trá»£ xÃ¡c thá»±c vÃ  phÃ¢n quyá»n ngÆ°á»i dÃ¹ng.
* Amazon Bedrock há»— trá»£ lá»›p AI Ä‘á»ƒ phÃ¢n tÃ­ch dá»¯ liá»‡u vÃ  tráº£ lá»i cÃ¢u há»i thÃ´ng minh.
* Amazon CloudWatch giÃ¡m sÃ¡t log, lá»—i vÃ  tráº¡ng thÃ¡i hoáº¡t Ä‘á»™ng cá»§a há»‡ thá»‘ng.

### 2.3. Hiá»‡u quáº£ ká»³ vá»ng

Há»‡ thá»‘ng giÃºp giáº£m thao tÃ¡c thá»§ cÃ´ng, tÄƒng Ä‘á»™ chÃ­nh xÃ¡c trong quáº£n lÃ½ bÃ£i xe, há»— trá»£ giÃ¡m sÃ¡t theo thá»i gian thá»±c vÃ  táº¡o ná»n táº£ng dá»¯ liá»‡u phá»¥c vá»¥ phÃ¢n tÃ­ch AI trong tÆ°Æ¡ng lai. Nhá» sá»­ dá»¥ng kiáº¿n trÃºc Serverless, há»‡ thá»‘ng cÃ³ thá»ƒ má»Ÿ rá»™ng linh hoáº¡t theo sá»‘ lÆ°á»£ng thiáº¿t bá»‹, sá»‘ lÆ°á»£ng xe vÃ  nhu cáº§u sá»­ dá»¥ng thá»±c táº¿.

---

## 3. Kiáº¿n trÃºc giáº£i phÃ¡p

Há»‡ thá»‘ng Ã¡p dá»¥ng kiáº¿n trÃºc **AWS Serverless** nháº±m giáº£m chi phÃ­ quáº£n lÃ½ háº¡ táº§ng, tÄƒng kháº£ nÄƒng má»Ÿ rá»™ng vÃ  dá»… dÃ ng tÃ­ch há»£p vá»›i cÃ¡c dá»‹ch vá»¥ AI, IoT vÃ  cÆ¡ sá»Ÿ dá»¯ liá»‡u trÃªn AWS.

![SÆ¡ Ä‘á»“ kiáº¿n trÃºc Parking IoT](/images/2-proposal-architecture.png)

### 3.1. CÃ¡c dá»‹ch vá»¥ AWS chá»§ chá»‘t

#### Giao diá»‡n ngÆ°á»i dÃ¹ng

* **Amazon Route 53:** Quáº£n lÃ½ tÃªn miá»n cho há»‡ thá»‘ng.
* **Amazon CloudFront:** PhÃ¢n phá»‘i ná»™i dung website vá»›i tá»‘c Ä‘á»™ cao.
* **AWS WAF:** Báº£o vá»‡ website khá»i cÃ¡c truy cáº­p Ä‘á»™c háº¡i.
* **Amazon S3 Static Website:** LÆ°u trá»¯ giao diá»‡n Web/App tÄ©nh.

#### XÃ¡c thá»±c vÃ  phÃ¢n quyá»n

* **Amazon Cognito:** Quáº£n lÃ½ Ä‘Äƒng nháº­p, xÃ¡c thá»±c ngÆ°á»i dÃ¹ng vÃ  phÃ¢n quyá»n truy cáº­p.
* **IAM:** Quáº£n lÃ½ quyá»n truy cáº­p giá»¯a cÃ¡c dá»‹ch vá»¥ AWS.

#### API vÃ  xá»­ lÃ½ backend

* **Amazon API Gateway:** Nháº­n request tá»« Web/App hoáº·c thiáº¿t bá»‹.
* **AWS Lambda API Backend:** Xá»­ lÃ½ nghiá»‡p vá»¥ chÃ­nh cá»§a há»‡ thá»‘ng.
* **AWS Lambda xá»­ lÃ½ áº£nh:** Xá»­ lÃ½ áº£nh sau khi Ä‘Æ°á»£c táº£i lÃªn S3.
* **AWS Lambda xá»­ lÃ½ dá»¯ liá»‡u cáº£m biáº¿n:** Xá»­ lÃ½ dá»¯ liá»‡u gá»­i tá»« ESP32 cáº£m biáº¿n.
* **AWS Lambda AI Service:** Káº¿t ná»‘i vá»›i Amazon Bedrock Ä‘á»ƒ xá»­ lÃ½ cÃ¡c chá»©c nÄƒng AI.

#### IoT vÃ  thiáº¿t bá»‹ biÃªn

* **ESP32 Camera:** Chá»¥p áº£nh xe ra/vÃ o.
* **ESP32 cáº£m biáº¿n:** Gá»­i tráº¡ng thÃ¡i chá»— Ä‘á»— xe.
* **AWS IoT Core:** Nháº­n dá»¯ liá»‡u tá»« thiáº¿t bá»‹ IoT thÃ´ng qua giao thá»©c MQTT.

#### LÆ°u trá»¯ vÃ  cÆ¡ sá»Ÿ dá»¯ liá»‡u

* **Amazon S3:** LÆ°u trá»¯ hÃ¬nh áº£nh xe.
* **Amazon DynamoDB:** LÆ°u dá»¯ liá»‡u biá»ƒn sá»‘, lá»‹ch sá»­ xe ra/vÃ o, tráº¡ng thÃ¡i chá»— Ä‘á»— vÃ  thÃ´ng tin ngÆ°á»i dÃ¹ng.

#### Xá»­ lÃ½ áº£nh vÃ  AI

* **Amazon Rekognition:** PhÃ¢n tÃ­ch hÃ¬nh áº£nh, há»— trá»£ nháº­n diá»‡n biá»ƒn sá»‘ xe.
* **Amazon Bedrock:** Há»— trá»£ phÃ¢n tÃ­ch dá»¯ liá»‡u vÃ  tráº£ lá»i truy váº¥n thÃ´ng minh báº±ng AI.

#### GiÃ¡m sÃ¡t há»‡ thá»‘ng

* **Amazon CloudWatch:** Ghi log, theo dÃµi lá»—i, giÃ¡m sÃ¡t Lambda, API Gateway, IoT Core vÃ  cÃ¡c thÃ nh pháº§n liÃªn quan.

---

## 4. Luá»“ng hoáº¡t Ä‘á»™ng cá»§a há»‡ thá»‘ng

### 4.1. Luá»“ng ngÆ°á»i dÃ¹ng truy cáº­p Web/App

NgÆ°á»i dÃ¹ng truy cáº­p há»‡ thá»‘ng thÃ´ng qua trÃ¬nh duyá»‡t web hoáº·c thiáº¿t bá»‹ di Ä‘á»™ng. Website Ä‘Æ°á»£c lÆ°u trá»¯ trÃªn Amazon S3 Static Website vÃ  phÃ¢n phá»‘i thÃ´ng qua Amazon CloudFront. Route 53 Ä‘áº£m nhiá»‡m vai trÃ² quáº£n lÃ½ tÃªn miá»n, cÃ²n AWS WAF giÃºp báº£o vá»‡ há»‡ thá»‘ng khá»i cÃ¡c truy cáº­p khÃ´ng há»£p lá»‡.

**Luá»“ng xá»­ lÃ½:**

NgÆ°á»i dÃ¹ng â†’ Route 53 â†’ CloudFront â†’ AWS WAF â†’ Amazon S3 Static Website â†’ API Gateway â†’ Lambda Backend â†’ DynamoDB

Trong Ä‘Ã³:

* NgÆ°á»i dÃ¹ng truy cáº­p vÃ o tÃªn miá»n cá»§a há»‡ thá»‘ng.
* Route 53 Ä‘iá»u hÆ°á»›ng request Ä‘áº¿n CloudFront.
* CloudFront phÃ¢n phá»‘i giao diá»‡n website tá»« Amazon S3.
* AWS WAF kiá»ƒm tra vÃ  cháº·n cÃ¡c request Ä‘á»™c háº¡i.
* Web/App gá»i API Gateway Ä‘á»ƒ láº¥y dá»¯ liá»‡u.
* Lambda Backend xá»­ lÃ½ request vÃ  truy váº¥n DynamoDB.
* DynamoDB tráº£ dá»¯ liá»‡u vá» cho Web/App Ä‘á»ƒ hiá»ƒn thá»‹.

---

### 4.2. Luá»“ng xÃ¡c thá»±c ngÆ°á»i dÃ¹ng

Há»‡ thá»‘ng sá»­ dá»¥ng Amazon Cognito Ä‘á»ƒ xÃ¡c thá»±c ngÆ°á»i dÃ¹ng trÆ°á»›c khi cho phÃ©p truy cáº­p vÃ o cÃ¡c chá»©c nÄƒng quáº£n lÃ½. NgÆ°á»i dÃ¹ng cÃ³ thá»ƒ Ä‘Äƒng nháº­p báº±ng tÃ i khoáº£n Ä‘Ã£ Ä‘Æ°á»£c cáº¥p. Sau khi Ä‘Äƒng nháº­p thÃ nh cÃ´ng, Cognito cáº¥p token Ä‘á»ƒ Web/App gá»­i kÃ¨m trong cÃ¡c request Ä‘áº¿n API Gateway.

**Luá»“ng xá»­ lÃ½:**

NgÆ°á»i dÃ¹ng â†’ Amazon Cognito â†’ API Gateway â†’ Lambda Backend â†’ DynamoDB

Trong Ä‘Ã³:

* NgÆ°á»i dÃ¹ng nháº­p tÃ i khoáº£n vÃ  máº­t kháº©u trÃªn Web/App.
* Amazon Cognito xÃ¡c thá»±c thÃ´ng tin Ä‘Äƒng nháº­p.
* Náº¿u Ä‘Äƒng nháº­p thÃ nh cÃ´ng, Cognito tráº£ vá» token.
* Web/App gá»­i token trong request Ä‘áº¿n API Gateway.
* API Gateway sá»­ dá»¥ng Cognito Authorizer Ä‘á»ƒ kiá»ƒm tra quyá»n truy cáº­p.
* Lambda Backend xá»­ lÃ½ chá»©c nÄƒng tÆ°Æ¡ng á»©ng náº¿u ngÆ°á»i dÃ¹ng há»£p lá»‡.

---

### 4.3. Luá»“ng ESP32 Camera gá»­i áº£nh xe

Khi cÃ³ xe Ä‘i vÃ o hoáº·c Ä‘i ra bÃ£i Ä‘á»—, ESP32 Camera sáº½ chá»¥p áº£nh phÆ°Æ¡ng tiá»‡n. Thay vÃ¬ upload áº£nh trá»±c tiáº¿p qua Lambda, thiáº¿t bá»‹ sáº½ xin **Presigned URL** tá»« API Gateway. Sau Ä‘Ã³ ESP32 Camera dÃ¹ng URL nÃ y Ä‘á»ƒ upload áº£nh JPEG trá»±c tiáº¿p lÃªn Amazon S3.

CÃ¡ch lÃ m nÃ y giÃºp giáº£m táº£i cho Lambda, tÄƒng hiá»‡u quáº£ upload áº£nh vÃ  phÃ¹ há»£p vá»›i kiáº¿n trÃºc AWS.

**Luá»“ng xá»­ lÃ½:**

ESP32 Camera â†’ API Gateway â†’ Lambda Backend â†’ Presigned URL â†’ ESP32 Camera upload áº£nh lÃªn S3 â†’ S3 Trigger Lambda â†’ Amazon Rekognition â†’ DynamoDB

CÃ¡c bÆ°á»›c chi tiáº¿t:

1. ESP32 Camera phÃ¡t hiá»‡n xe hoáº·c Ä‘Æ°á»£c kÃ­ch hoáº¡t Ä‘á»ƒ chá»¥p áº£nh.
2. ESP32 Camera gá»­i request Ä‘áº¿n API Gateway Ä‘á»ƒ xin Presigned URL.
3. API Gateway chuyá»ƒn request Ä‘áº¿n Lambda Backend.
4. Lambda Backend táº¡o Presigned URL cho phÃ©p upload áº£nh lÃªn Amazon S3.
5. ESP32 Camera nháº­n Presigned URL.
6. ESP32 Camera upload áº£nh JPEG trá»±c tiáº¿p lÃªn Amazon S3.
7. Khi áº£nh má»›i Ä‘Æ°á»£c upload, S3 phÃ¡t sinh sá»± kiá»‡n ObjectCreated.
8. S3 Trigger kÃ­ch hoáº¡t Lambda xá»­ lÃ½ áº£nh.
9. Lambda gá»i Amazon Rekognition Ä‘á»ƒ phÃ¢n tÃ­ch hÃ¬nh áº£nh.
10. Káº¿t quáº£ nháº­n diá»‡n biá»ƒn sá»‘ Ä‘Æ°á»£c lÆ°u vÃ o DynamoDB.

VÃ­ dá»¥ dá»¯ liá»‡u áº£nh Ä‘Æ°á»£c lÆ°u:

```json
{
  "image_id": "car_001.jpg",
  "plate_number": "51A-12345",
  "direction": "in",
  "timestamp": "2026-04-27T10:30:00",
  "s3_url": "s3://parking-image-bucket/car_001.jpg"
}
```

---

### 4.4. Luá»“ng ESP32 cáº£m biáº¿n gá»­i dá»¯ liá»‡u vá»‹ trÃ­ Ä‘á»—

ESP32 cáº£m biáº¿n Ä‘Æ°á»£c dÃ¹ng Ä‘á»ƒ phÃ¡t hiá»‡n tráº¡ng thÃ¡i cá»§a tá»«ng vá»‹ trÃ­ Ä‘á»— xe. Cáº£m biáº¿n cÃ³ thá»ƒ lÃ  cáº£m biáº¿n siÃªu Ã¢m, há»“ng ngoáº¡i hoáº·c cáº£m biáº¿n tá»«, tÃ¹y theo thiáº¿t káº¿ thá»±c táº¿. Dá»¯ liá»‡u cáº£m biáº¿n Ä‘Æ°á»£c gá»­i lÃªn AWS IoT Core báº±ng giao thá»©c MQTT.

**Luá»“ng xá»­ lÃ½:**

ESP32 cáº£m biáº¿n â†’ AWS IoT Core â†’ Lambda xá»­ lÃ½ dá»¯ liá»‡u cáº£m biáº¿n â†’ DynamoDB

CÃ¡c bÆ°á»›c chi tiáº¿t:

1. ESP32 cáº£m biáº¿n Ä‘á»c tráº¡ng thÃ¡i vá»‹ trÃ­ Ä‘á»—.
2. Thiáº¿t bá»‹ gá»­i dá»¯ liá»‡u lÃªn AWS IoT Core báº±ng MQTT.
3. AWS IoT Core nháº­n dá»¯ liá»‡u tá»« thiáº¿t bá»‹.
4. IoT Rule chuyá»ƒn dá»¯ liá»‡u Ä‘áº¿n Lambda xá»­ lÃ½ dá»¯ liá»‡u cáº£m biáº¿n.
5. Lambda kiá»ƒm tra, chuáº©n hÃ³a vÃ  lÆ°u dá»¯ liá»‡u vÃ o DynamoDB.
6. Web/App truy váº¥n DynamoDB Ä‘á»ƒ hiá»ƒn thá»‹ tráº¡ng thÃ¡i bÃ£i xe theo thá»i gian thá»±c.

VÃ­ dá»¥ dá»¯ liá»‡u cáº£m biáº¿n:

```json
{
  "slot_id": "A01",
  "status": "occupied",
  "timestamp": "2026-04-27T10:30:00"
}
```

Trong Ä‘Ã³:

* `slot_id`: MÃ£ vá»‹ trÃ­ Ä‘á»— xe.
* `status`: Tráº¡ng thÃ¡i vá»‹ trÃ­ Ä‘á»—, vÃ­ dá»¥ `available` hoáº·c `occupied`.
* `timestamp`: Thá»i gian ghi nháº­n dá»¯ liá»‡u.

---

### 4.5. Luá»“ng xá»­ lÃ½ AI Service

Há»‡ thá»‘ng tÃ­ch há»£p lá»›p AI Ä‘á»ƒ há»— trá»£ ngÆ°á»i dÃ¹ng vÃ  quáº£n trá»‹ viÃªn truy váº¥n dá»¯ liá»‡u bÃ£i Ä‘á»— xe báº±ng ngÃ´n ngá»¯ tá»± nhiÃªn. Web/App gá»­i cÃ¢u há»i Ä‘áº¿n API Gateway, sau Ä‘Ã³ Lambda AI Service xá»­ lÃ½ yÃªu cáº§u, láº¥y dá»¯ liá»‡u tá»« DynamoDB náº¿u cáº§n vÃ  gá»i Amazon Bedrock Ä‘á»ƒ táº¡o pháº£n há»“i.

**Luá»“ng xá»­ lÃ½:**

Web/App â†’ API Gateway â†’ Lambda AI Service â†’ Amazon Bedrock â†’ DynamoDB â†’ Web/App

CÃ¡c chá»©c nÄƒng AI cÃ³ thá»ƒ há»— trá»£:

* Há»i sá»‘ lÆ°á»£ng chá»— trá»‘ng hiá»‡n táº¡i.
* TÃ³m táº¯t sá»‘ lÆ°á»£ng xe Ä‘ang cÃ³ trong bÃ£i.
* PhÃ¢n tÃ­ch khung giá» bÃ£i xe Ä‘Ã´ng nháº¥t.
* Gá»£i Ã½ khu vá»±c cÃ²n chá»— trá»‘ng.
* Há»— trá»£ quáº£n trá»‹ viÃªn tra cá»©u lá»‹ch sá»­ xe ra/vÃ o.
* TÃ³m táº¯t tÃ¬nh tráº¡ng hoáº¡t Ä‘á»™ng cá»§a bÃ£i xe trong ngÃ y.

VÃ­ dá»¥ cÃ¢u há»i:

> Hiá»‡n táº¡i cÃ²n bao nhiÃªu chá»— trá»‘ng trong bÃ£i xe?

VÃ­ dá»¥ pháº£n há»“i:

> Hiá»‡n táº¡i bÃ£i xe cÃ²n 12 chá»— trá»‘ng, trong Ä‘Ã³ khu A cÃ²n 5 chá»— vÃ  khu B cÃ²n 7 chá»—.

---

### 4.6. Luá»“ng giÃ¡m sÃ¡t há»‡ thá»‘ng

Amazon CloudWatch Ä‘Æ°á»£c sá»­ dá»¥ng Ä‘á»ƒ ghi log vÃ  giÃ¡m sÃ¡t hoáº¡t Ä‘á»™ng cá»§a cÃ¡c dá»‹ch vá»¥ trong há»‡ thá»‘ng. CloudWatch cÃ³ thá»ƒ nháº­n log tá»« Lambda, API Gateway, IoT Core vÃ  cÃ¡c thÃ nh pháº§n xá»­ lÃ½ dá»¯ liá»‡u.

**Luá»“ng giÃ¡m sÃ¡t:**

API Gateway / Lambda / IoT Core / Rekognition / DynamoDB â†’ CloudWatch

CloudWatch giÃºp:

* Theo dÃµi lá»—i khi Lambda xá»­ lÃ½ tháº¥t báº¡i.
* Kiá»ƒm tra request Ä‘áº¿n API Gateway.
* Theo dÃµi dá»¯ liá»‡u tá»« thiáº¿t bá»‹ IoT.
* Ghi nháº­n log xá»­ lÃ½ áº£nh vÃ  dá»¯ liá»‡u cáº£m biáº¿n.
* Há»— trá»£ phÃ¡t hiá»‡n sá»± cá»‘ trong quÃ¡ trÃ¬nh váº­n hÃ nh.

---

## 5. Triá»ƒn khai ká»¹ thuáº­t

### 5.1. Giai Ä‘oáº¡n 1: PhÃ¢n tÃ­ch vÃ  thiáº¿t káº¿ há»‡ thá»‘ng

Trong giai Ä‘oáº¡n Ä‘áº§u, nhÃ³m thá»±c hiá»‡n kháº£o sÃ¡t yÃªu cáº§u há»‡ thá»‘ng vÃ  xÃ¡c Ä‘á»‹nh pháº¡m vi triá»ƒn khai. CÃ¡c cÃ´ng viá»‡c chÃ­nh bao gá»“m:

* XÃ¡c Ä‘á»‹nh sá»‘ lÆ°á»£ng cá»•ng ra/vÃ o cáº§n láº¯p ESP32 Camera.
* XÃ¡c Ä‘á»‹nh sá»‘ lÆ°á»£ng vá»‹ trÃ­ Ä‘á»— cáº§n theo dÃµi báº±ng cáº£m biáº¿n.
* Thiáº¿t káº¿ sÆ¡ Ä‘á»“ kiáº¿n trÃºc há»‡ thá»‘ng.
* Thiáº¿t káº¿ luá»“ng dá»¯ liá»‡u giá»¯a thiáº¿t bá»‹ IoT vÃ  AWS.
* Thiáº¿t káº¿ cáº¥u trÃºc báº£ng DynamoDB.
* XÃ¡c Ä‘á»‹nh quyá»n truy cáº­p cho ngÆ°á»i dÃ¹ng, quáº£n lÃ½ vÃ  quáº£n trá»‹ viÃªn.

### 5.2. Giai Ä‘oáº¡n 2: Triá»ƒn khai thiáº¿t bá»‹ IoT

Giai Ä‘oáº¡n nÃ y táº­p trung vÃ o viá»‡c cáº¥u hÃ¬nh vÃ  kiá»ƒm thá»­ thiáº¿t bá»‹ ESP32.

CÃ¡c cÃ´ng viá»‡c chÃ­nh:

* Cáº¥u hÃ¬nh ESP32 Camera Ä‘á»ƒ chá»¥p áº£nh phÆ°Æ¡ng tiá»‡n.
* Cáº¥u hÃ¬nh ESP32 cáº£m biáº¿n Ä‘á»ƒ Ä‘á»c tráº¡ng thÃ¡i vá»‹ trÃ­ Ä‘á»—.
* Káº¿t ná»‘i ESP32 cáº£m biáº¿n vá»›i AWS IoT Core báº±ng MQTT.
* Kiá»ƒm thá»­ gá»­i dá»¯ liá»‡u cáº£m biáº¿n lÃªn AWS IoT Core.
* Kiá»ƒm thá»­ ESP32 Camera xin Presigned URL vÃ  upload áº£nh lÃªn Amazon S3.
* Kiá»ƒm tra cháº¥t lÆ°á»£ng hÃ¬nh áº£nh biá»ƒn sá»‘ trong cÃ¡c Ä‘iá»u kiá»‡n Ã¡nh sÃ¡ng khÃ¡c nhau.

### 5.3. Giai Ä‘oáº¡n 3: XÃ¢y dá»±ng backend trÃªn AWS

Backend cá»§a há»‡ thá»‘ng Ä‘Æ°á»£c xÃ¢y dá»±ng báº±ng cÃ¡c dá»‹ch vá»¥ serverless cá»§a AWS.

CÃ¡c cÃ´ng viá»‡c chÃ­nh:

* Táº¡o Amazon API Gateway Ä‘á»ƒ nháº­n request tá»« Web/App vÃ  thiáº¿t bá»‹.
* Táº¡o Lambda Backend xá»­ lÃ½ nghiá»‡p vá»¥.
* Táº¡o chá»©c nÄƒng cáº¥p Presigned URL cho ESP32 Camera.
* Táº¡o Amazon S3 Bucket Ä‘á»ƒ lÆ°u áº£nh xe.
* Cáº¥u hÃ¬nh S3 Event ObjectCreated Ä‘á»ƒ trigger Lambda xá»­ lÃ½ áº£nh.
* TÃ­ch há»£p Amazon Rekognition Ä‘á»ƒ phÃ¢n tÃ­ch hÃ¬nh áº£nh.
* Táº¡o báº£ng DynamoDB Ä‘á»ƒ lÆ°u dá»¯ liá»‡u bÃ£i xe.
* Táº¡o Lambda xá»­ lÃ½ dá»¯ liá»‡u cáº£m biáº¿n tá»« AWS IoT Core.
* Cáº¥u hÃ¬nh IAM Role cho cÃ¡c dá»‹ch vá»¥ cÃ³ quyá»n truy cáº­p phÃ¹ há»£p.

### 5.4. Giai Ä‘oáº¡n 4: XÃ¢y dá»±ng giao diá»‡n Web/App

Giao diá»‡n Web/App giÃºp ngÆ°á»i dÃ¹ng vÃ  quáº£n trá»‹ viÃªn theo dÃµi tráº¡ng thÃ¡i bÃ£i Ä‘á»— xe.

CÃ¡c chá»©c nÄƒng chÃ­nh:

* ÄÄƒng nháº­p vÃ  xÃ¡c thá»±c ngÆ°á»i dÃ¹ng.
* Hiá»ƒn thá»‹ sÆ¡ Ä‘á»“ bÃ£i Ä‘á»— xe.
* Hiá»ƒn thá»‹ tráº¡ng thÃ¡i tá»«ng vá»‹ trÃ­ Ä‘á»—.
* Hiá»ƒn thá»‹ danh sÃ¡ch xe ra/vÃ o.
* Hiá»ƒn thá»‹ biá»ƒn sá»‘ xe, hÃ¬nh áº£nh vÃ  thá»i gian ghi nháº­n.
* TÃ¬m kiáº¿m lá»‹ch sá»­ xe theo biá»ƒn sá»‘.
* Xem thá»‘ng kÃª sá»‘ lÆ°á»£ng xe trong bÃ£i.
* Quáº£n lÃ½ ngÆ°á»i dÃ¹ng theo vai trÃ².

### 5.5. Giai Ä‘oáº¡n 5: TÃ­ch há»£p AI vÃ  giÃ¡m sÃ¡t

Giai Ä‘oáº¡n cuá»‘i táº­p trung vÃ o viá»‡c tÃ­ch há»£p AI vÃ  hoÃ n thiá»‡n há»‡ thá»‘ng giÃ¡m sÃ¡t.

CÃ¡c cÃ´ng viá»‡c chÃ­nh:

* XÃ¢y dá»±ng Lambda AI Service.
* TÃ­ch há»£p Amazon Bedrock Ä‘á»ƒ há»— trá»£ truy váº¥n thÃ´ng minh.
* Káº¿t ná»‘i AI Service vá»›i DynamoDB.
* Táº¡o dashboard hoáº·c chá»©c nÄƒng thá»‘ng kÃª dá»¯ liá»‡u bÃ£i xe.
* Cáº¥u hÃ¬nh CloudWatch Ä‘á»ƒ theo dÃµi log.
* Thiáº¿t láº­p cáº£nh bÃ¡o lá»—i há»‡ thá»‘ng.
* Thiáº¿t láº­p cáº£nh bÃ¡o chi phÃ­ báº±ng AWS Budgets.
* Kiá»ƒm thá»­ toÃ n bá»™ há»‡ thá»‘ng trÆ°á»›c khi váº­n hÃ nh.

---

## 6. Æ¯á»›c tÃ­nh ngÃ¢n sÃ¡ch

Chi phÃ­ triá»ƒn khai há»‡ thá»‘ng Parking IoT phá»¥ thuá»™c vÃ o sá»‘ lÆ°á»£ng thiáº¿t bá»‹, sá»‘ lÆ°á»£ng áº£nh xá»­ lÃ½, sá»‘ request API, dung lÆ°á»£ng lÆ°u trá»¯ áº£nh vÃ  má»©c Ä‘á»™ sá»­ dá»¥ng AI.

### 6.1. Chi phÃ­ pháº§n cá»©ng

| Háº¡ng má»¥c | Sá»‘ lÆ°á»£ng | Má»¥c Ä‘Ã­ch sá»­ dá»¥ng |
| :--- | :---: | :--- |
| ESP32 Camera | Theo sá»‘ cá»•ng ra/vÃ o | Chá»¥p áº£nh xe vÃ  biá»ƒn sá»‘ |
| ESP32 cáº£m biáº¿n | Theo sá»‘ vá»‹ trÃ­ Ä‘á»— | Gá»­i tráº¡ng thÃ¡i chá»— Ä‘á»— |
| Cáº£m biáº¿n siÃªu Ã¢m / há»“ng ngoáº¡i | Theo sá»‘ vá»‹ trÃ­ Ä‘á»— | PhÃ¡t hiá»‡n xe táº¡i vá»‹ trÃ­ Ä‘á»— |
| Nguá»“n Ä‘iá»‡n | Theo thiáº¿t bá»‹ | Cáº¥p nguá»“n cho ESP32 |
| DÃ¢y ná»‘i, há»™p báº£o vá»‡ | Theo nhu cáº§u | Báº£o vá»‡ thiáº¿t bá»‹ khi láº¯p Ä‘áº·t |
| Router / WiFi | 1 hoáº·c nhiá»u | Káº¿t ná»‘i thiáº¿t bá»‹ vá»›i Internet |

### 6.2. Chi phÃ­ dá»‹ch vá»¥ AWS

CÃ¡c dá»‹ch vá»¥ AWS cÃ³ thá»ƒ phÃ¡t sinh chi phÃ­ bao gá»“m:

| Dá»‹ch vá»¥ AWS | Má»¥c Ä‘Ã­ch sá»­ dá»¥ng |
| :--- | :--- |
| AWS IoT Core | Nháº­n dá»¯ liá»‡u MQTT tá»« ESP32 cáº£m biáº¿n |
| Amazon S3 | LÆ°u trá»¯ áº£nh xe |
| AWS Lambda | Xá»­ lÃ½ backend, xá»­ lÃ½ áº£nh vÃ  dá»¯ liá»‡u cáº£m biáº¿n |
| Amazon API Gateway | Nháº­n request tá»« Web/App vÃ  thiáº¿t bá»‹ |
| Amazon Rekognition | PhÃ¢n tÃ­ch hÃ¬nh áº£nh, há»— trá»£ nháº­n diá»‡n biá»ƒn sá»‘ |
| Amazon DynamoDB | LÆ°u dá»¯ liá»‡u xe, biá»ƒn sá»‘, tráº¡ng thÃ¡i chá»— Ä‘á»— |
| Amazon CloudFront | PhÃ¢n phá»‘i giao diá»‡n website |
| Amazon Cognito | XÃ¡c thá»±c vÃ  quáº£n lÃ½ ngÆ°á»i dÃ¹ng |
| Amazon CloudWatch | Ghi log vÃ  giÃ¡m sÃ¡t há»‡ thá»‘ng |
| Amazon Bedrock | Há»— trá»£ chá»©c nÄƒng AI nÃ¢ng cao |
| AWS Budgets | Theo dÃµi vÃ  cáº£nh bÃ¡o chi phÃ­ |

Äá»‘i vá»›i mÃ´ hÃ¬nh demo hoáº·c triá»ƒn khai quy mÃ´ nhá», chi phÃ­ cÃ³ thá»ƒ Ä‘Æ°á»£c kiá»ƒm soÃ¡t báº±ng cÃ¡ch giá»›i háº¡n sá»‘ lÆ°á»£ng áº£nh xá»­ lÃ½, giáº£m thá»i gian lÆ°u áº£nh trÃªn S3, tá»‘i Æ°u sá»‘ láº§n gá»i API Gateway vÃ  chá»‰ sá»­ dá»¥ng Amazon Bedrock khi cáº§n thiáº¿t.

---

## 7. ÄÃ¡nh giÃ¡ rá»§i ro vÃ  chiáº¿n lÆ°á»£c giáº£m thiá»ƒu

| Rá»§i ro | Má»©c Ä‘á»™ | Chiáº¿n lÆ°á»£c giáº£m thiá»ƒu |
| :--- | :---: | :--- |
| ESP32 máº¥t káº¿t ná»‘i máº¡ng | Trung bÃ¬nh | LÆ°u táº¡m dá»¯ liá»‡u cá»¥c bá»™ vÃ  gá»­i láº¡i khi cÃ³ máº¡ng |
| áº¢nh biá»ƒn sá»‘ bá»‹ má» | Cao | Äiá»u chá»‰nh gÃ³c camera, Ã¡nh sÃ¡ng vÃ  khoáº£ng cÃ¡ch chá»¥p |
| Nháº­n diá»‡n biá»ƒn sá»‘ sai | Trung bÃ¬nh | Káº¿t há»£p kiá»ƒm tra thá»§ cÃ´ng vÃ  cáº£i thiá»‡n cháº¥t lÆ°á»£ng áº£nh |
| Thiáº¿t bá»‹ bá»‹ há»ng do mÃ´i trÆ°á»ng | Trung bÃ¬nh | DÃ¹ng há»™p báº£o vá»‡, kiá»ƒm tra Ä‘á»‹nh ká»³ thiáº¿t bá»‹ |
| API Gateway hoáº·c Lambda bá»‹ lá»—i | Trung bÃ¬nh | Theo dÃµi log báº±ng CloudWatch vÃ  xá»­ lÃ½ lá»—i |
| VÆ°á»£t chi phÃ­ AWS | Trung bÃ¬nh | Thiáº¿t láº­p AWS Budgets vÃ  cáº£nh bÃ¡o chi phÃ­ |
| Dá»¯ liá»‡u bá»‹ truy cáº­p trÃ¡i phÃ©p | Cao | DÃ¹ng Cognito, IAM, WAF vÃ  phÃ¢n quyá»n cháº·t cháº½ |
| Há»‡ thá»‘ng khÃ³ má»Ÿ rá»™ng | Tháº¥p | Thiáº¿t káº¿ serverless, dá»… thÃªm thiáº¿t bá»‹ vÃ  dá»‹ch vá»¥ |

---

## 8. Káº¿t quáº£ ká»³ vá»ng

### 8.1. Vá» ká»¹ thuáº­t

Sau khi hoÃ n thÃ nh, há»‡ thá»‘ng dá»± kiáº¿n Ä‘áº¡t Ä‘Æ°á»£c cÃ¡c káº¿t quáº£ sau:

* XÃ¢y dá»±ng Ä‘Æ°á»£c há»‡ thá»‘ng Parking IoT hoáº¡t Ä‘á»™ng theo thá»i gian thá»±c.
* ESP32 Camera cÃ³ thá»ƒ chá»¥p áº£nh xe ra/vÃ o vÃ  upload áº£nh lÃªn Amazon S3.
* ESP32 cáº£m biáº¿n cÃ³ thá»ƒ gá»­i tráº¡ng thÃ¡i vá»‹ trÃ­ Ä‘á»— xe lÃªn AWS IoT Core.
* AWS Lambda xá»­ lÃ½ dá»¯ liá»‡u tá»± Ä‘á»™ng, khÃ´ng cáº§n mÃ¡y chá»§ riÃªng.
* Amazon Rekognition há»— trá»£ phÃ¢n tÃ­ch áº£nh vÃ  nháº­n diá»‡n biá»ƒn sá»‘.
* DynamoDB lÆ°u trá»¯ dá»¯ liá»‡u táº­p trung, há»— trá»£ truy váº¥n nhanh.
* Web/App hiá»ƒn thá»‹ tráº¡ng thÃ¡i bÃ£i xe, lá»‹ch sá»­ xe ra/vÃ o vÃ  thÃ´ng tin biá»ƒn sá»‘.
* Amazon Bedrock há»— trá»£ chá»©c nÄƒng AI, giÃºp ngÆ°á»i dÃ¹ng truy váº¥n dá»¯ liá»‡u thÃ´ng minh.
* CloudWatch há»— trá»£ giÃ¡m sÃ¡t lá»—i vÃ  theo dÃµi hoáº¡t Ä‘á»™ng há»‡ thá»‘ng.

### 8.2. Vá» váº­n hÃ nh

Há»‡ thá»‘ng giÃºp quÃ¡ trÃ¬nh quáº£n lÃ½ bÃ£i Ä‘á»— xe trá»Ÿ nÃªn tá»± Ä‘á»™ng vÃ  hiá»‡u quáº£ hÆ¡n. NgÆ°á»i quáº£n lÃ½ cÃ³ thá»ƒ theo dÃµi tráº¡ng thÃ¡i bÃ£i xe tá»« xa, kiá»ƒm tra lá»‹ch sá»­ xe ra/vÃ o vÃ  giáº£m phá»¥ thuá»™c vÃ o thao tÃ¡c thá»§ cÃ´ng.

CÃ¡c lá»£i Ã­ch váº­n hÃ nh gá»“m:

* Giáº£m thá»i gian kiá»ƒm tra xe ra/vÃ o.
* TÄƒng Ä‘á»™ chÃ­nh xÃ¡c khi quáº£n lÃ½ biá»ƒn sá»‘ vÃ  tráº¡ng thÃ¡i chá»— Ä‘á»—.
* Há»— trá»£ giÃ¡m sÃ¡t bÃ£i xe theo thá»i gian thá»±c.
* Dá»… dÃ ng má»Ÿ rá»™ng thÃªm camera hoáº·c cáº£m biáº¿n.
* Giáº£m nhu cáº§u váº­n hÃ nh mÃ¡y chá»§ truyá»n thá»‘ng.
* TÄƒng tÃ­nh báº£o máº­t thÃ´ng qua xÃ¡c thá»±c vÃ  phÃ¢n quyá»n ngÆ°á»i dÃ¹ng.

---

## 9. Káº¿t luáº­n

Dá»± Ã¡n **Parking IoT thÃ´ng minh sá»­ dá»¥ng AWS Serverless** lÃ  giáº£i phÃ¡p phÃ¹ há»£p Ä‘á»ƒ hiá»‡n Ä‘áº¡i hÃ³a viá»‡c quáº£n lÃ½ bÃ£i Ä‘á»— xe. Há»‡ thá»‘ng káº¿t há»£p cÃ¡c cÃ´ng nghá»‡ IoT, xá»­ lÃ½ áº£nh, lÆ°u trá»¯ dá»¯ liá»‡u, xÃ¡c thá»±c ngÆ°á»i dÃ¹ng vÃ  trÃ­ tuá»‡ nhÃ¢n táº¡o nháº±m táº¡o ra má»™t ná»n táº£ng quáº£n lÃ½ bÃ£i xe tá»± Ä‘á»™ng, linh hoáº¡t vÃ  cÃ³ kháº£ nÄƒng má»Ÿ rá»™ng.

Vá»›i cÃ¡c dá»‹ch vá»¥ nhÆ° **AWS IoT Core**, **Amazon S3**, **AWS Lambda**, **Amazon API Gateway**, **Amazon Rekognition**, **Amazon DynamoDB**, **Amazon Cognito**, **Amazon CloudFront**, **AWS WAF**, **Amazon CloudWatch** vÃ  **Amazon Bedrock**, há»‡ thá»‘ng cÃ³ thá»ƒ Ä‘Ã¡p á»©ng tá»‘t cÃ¡c yÃªu cáº§u vá» giÃ¡m sÃ¡t thá»i gian thá»±c, nháº­n diá»‡n biá»ƒn sá»‘, quáº£n lÃ½ ngÆ°á»i dÃ¹ng vÃ  phÃ¢n tÃ­ch dá»¯ liá»‡u thÃ´ng minh.

Dá»± Ã¡n khÃ´ng chá»‰ giÃºp giáº£i quyáº¿t cÃ¡c háº¡n cháº¿ cá»§a mÃ´ hÃ¬nh quáº£n lÃ½ bÃ£i xe thá»§ cÃ´ng mÃ  cÃ²n táº¡o ná»n táº£ng Ä‘á»ƒ phÃ¡t triá»ƒn cÃ¡c chá»©c nÄƒng nÃ¢ng cao trong tÆ°Æ¡ng lai nhÆ° dá»± bÃ¡o máº­t Ä‘á»™ xe, tá»‘i Æ°u vá»‹ trÃ­ Ä‘á»—, cáº£nh bÃ¡o báº¥t thÆ°á»ng vÃ  há»— trá»£ quáº£n lÃ½ báº±ng AI.
