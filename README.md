# vietnamese-pos-tagging

## 1.	Mục tiêu

Xây dựng chương trình (tool) gán nhãn từ loại (POS tagger) cho tiếng Việt.

Kết quả đạt được là chương trình, có 2 chức năng:

-	Đánh giá độ chính xác trên tập Test: tỉ lệ số từ gán nhãn đúng trên tổng số từ

-	Input vào một câu tiếng Việt, cho ra nhãn của từng từ trong câu, ví dụ.


o	Câu input: “Dù khá đắt nhưng tôi vẫn đồng ý.”

o	Kết quả: “Dù/C khá/R đắt/A nhưng/C tôi/P vẫn/R đồng_ý/V ./.”

## 2.	Dữ liệu cho trước
-	File traing: “vi_train.pos”
-	File test: “vi_test.pos”
-	File hướng dân thông tin về nhãn POS: [Thông tin về nhãn POS](https://github.com/nthanhkhang/vietnamese-pos-tagging/blob/main/Thon%20tin%20nhan%20tu%20loai-v2.pdf)
