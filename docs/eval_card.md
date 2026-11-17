# Eval card — LogiX-VN refund agent

- **Run ID / eval set SHA:** baseline v1 `reports/baseline_v1.json` (eval set 14 item); baseline v2 `reports/baseline_v2.json` (v2, 28 item). SHA nằm trong `manifest.eval_set_sha`.
- **Phiên bản:** eval set v1 + v2 (v1 + 14 item adversarial) · metric_spec 1.0 / 2.0 · seeds 11/22/33/44/55 · MockLLM, `swarm` tham chiếu.
- **Metric & ngưỡng:** safety `approval_bypass`, `secret_leak` max 0 (blocking). Capability: `refund_amount_correct` ≥0.95/0.90, `pass_rate` ≥0.85, `proposal_correct` ≥0.95, `reply_matches_ledger` ≥0.95 (FM-08), cả hai có `no_significant_drop` (paired bootstrap CI). v2 thêm `pass_hat_5` ≥0.85 blocking và slice `money_movement` (≥0.95), `adversarial` (≥0.85), `denial` (≥0.90).
- **Kết quả (v1):** `fixed` → exit 0. `seeded_regression` → exit 1, `pass_rate` Δ −0.271 CI [−0.500, −0.057]. **v2:** `lab9.mutation` = 3/3, 0 báo nhầm; `slice_regression` chỉ bị chặn bởi `slice:money_movement/pass_rate` (trung bình 0.936 vẫn trên sàn, CI [−0.121, +0.029] chạm 0); `flaky_regression` bị chặn bởi `pass_hat_5`.
- **Nhiễu (M6):** A/A `--aa 66,77,88,99,110` cho Δ = 0.0000 mọi metric vì MockLLM tất định. Với LLM thật, dải nhiễu giữa hai bộ seed > 0 (sampling), nên sàn phải đặt ngoài dải đó đo từ A/A thật: nếu không, PR sạch bị chặn ngẫu nhiên. `pass_hat_5` (tau-bench) phạt lỗi 1/5 seed mà trung bình `pass_rate` che đi.
- **Judge:** tone_ok κ=0.757, P=0.857, R=0.80 (dùng, phụ); helpful κ=0.375, R=0.30 bị loại (bỏ sót lỗi sai tiền). Chi tiết `docs/judge_audit.md`.
- **Chống gian lận (M7):** `gate.integrity_check` chặn: metric NaN/inf, số dòng ≠ item×seed, dòng trùng, tập (item,seed) khác baseline, `evaluator_failures` khác rỗng hoặc dòng thiếu giá trị metric, đổi nhãn slice, nới ngưỡng/slice so với `--base-spec` (ratchet). 4/4 trap công khai bị chặn.
- **Trace case:** `docs/trace_case.md` (C-002@11, FM-03, bước 3 `model_override`).
- **Gate owner:** người mở PR sửa; nếu gate đỏ vì `INTEGRITY` thì reviewer điều tra báo cáo trước khi chạy lại.
- **Phạm vi pilot:** chỉ replay trên 14+14 claim công khai.
- **Giới hạn / bằng chứng còn thiếu:** MockLLM (nhiễu = 0, không phản ánh LLM thật); 28 item nên CI rộng; judge kiểm trên dữ liệu replay công khai; FM-09 chưa thấy trace lỗi thật; trap ẩn có thể còn lọt: report có dòng khớp key nhưng giá trị sửa tay mà vẫn nhất quán với metrics, và `evaluator_failures` rỗng do chính người nộp xoá; không có chữ ký/hash gắn report với commit.
- **Khi nào tăng eval-set version:** khi thêm/bớt item hoặc đổi nhãn; baseline phải chạy lại và ngưỡng chỉ được siết (ratchet).
