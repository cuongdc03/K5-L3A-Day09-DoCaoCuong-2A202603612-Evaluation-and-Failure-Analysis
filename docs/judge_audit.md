# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5` (n=100 mỗi file, FAIL là lớp dương).

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Đạt (confusion tp24 fp4 fn6 tn66) | **dùng** (làm tín hiệu phụ, không làm gate tiền) |
| helpful | 100 | 0.375 | 1.000 | 0.300 | **Không đạt** κ và recall (tp9 fp0 fn21 tn70) | **loại** |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú / sửa rubric |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." | PASS | FAIL | Người | Xưng "em"/"nha" quá suồng sã. Rubric: thêm "xưng hô chuẩn Dạ/anh-chị; cấm 'nha', 'em'" |
| 2 | H-017 "Dạ, bạn ơi ... rồi nha." | PASS | FAIL | Người | Gọi khách là "bạn". Rubric: cấm "bạn" với khách; judge nhầm vì có "Dạ" |
| 3 | H-029 "Dạ, vui lòng chờ... không cần nhắn thêm." | PASS | FAIL | Người | Giọng ra lệnh. Rubric: câu cấm khách liên hệ lại = FAIL dù mở đầu lịch sự |
| 4 | H-042 "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." | FAIL | PASS | Người | Ngắn nhưng đủ ý; judge phạt vì thiếu xin lỗi. Rubric: xin lỗi chỉ bắt buộc khi lỗi do LogiX |
| 5 | H-051 "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." | FAIL | PASS | Người | "refund" được CS LogiX cho phép. Rubric: whitelist thuật ngữ tiếng Anh `refund` |
| 6 | HL-015 "...đã hoàn 55.000đ cho đơn O-112" (ledger 40.000đ) | PASS | FAIL | Người | Judge không thấy ledger nên không biết sai tiền |
| 7 | HL-016 (xin lỗi dài, hoàn 55.000đ; ledger 35.000đ) | PASS | FAIL | Người | Lịch sự che mất số sai; judge chấm văn phong |

## Kết luận
- **Loại `judge_helpful` khỏi gate.** κ=0.375 (<0.6) và recall=0.30 (<0.7): bỏ sót 21/30 reply hỏng. Precision 1.0 chỉ vì nó hiếm khi kêu FAIL, nên "không báo nhầm" không có nghĩa là bắt được lỗi. Các FN điển hình (HL-015/016/020) là **sai số tiền** — judge không được xem ledger, và lỗi này đã có grader code (`RefundAmountCorrect`, `ReplyMatchesLedger`). Tiền và approval không bao giờ giao cho judge.
- Judge helpful dùng làm gate sẽ báo xanh trên agent sai tiền ⇒ nguy hiểm hơn không có judge. Tỉ lệ lỗi quan sát 0.09, hiệu chỉnh Rogan-Gladen ≈ 0.30: thấp hơn thực tế 3 lần.
- `judge_tone` qua floors nhưng 6 FN (suồng sã/ra lệnh) cho thấy chỉ là tín hiệu phụ; tỉ lệ lỗi quan sát 0.28 → hiệu chỉnh 0.30.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật. Mẫu 100 dòng ⇒ κ có khoảng tin cậy rộng.
