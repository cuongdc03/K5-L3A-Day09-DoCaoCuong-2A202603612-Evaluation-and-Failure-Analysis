# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `<shape> <claim>@<seed>`, run ID trong report |
| Triệu chứng | Grader nào fail; reply nói gì so với ledger ghi gì |
| Bước sai đầu tiên | Số thứ tự event + kind + trích payload (≤1 dòng) |
| Vì sao là bước *đầu tiên* | Các bước trước đó đúng ra sao (dẫn số event) |
| Failure mode | Mã FM-xx trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng claim@seed trên shape `fixed`: bước đó khác thế nào |
| Regression test | Tên test + grader/assert nào bắt được; đã thấy fail trên variant lỗi và pass trên `fixed` chưa |
| Chưa chắc chắn | Điều trace không chứng minh được |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.

---
## Case của nhóm: C-002@11 trên `seeded_regression` (FM-03)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run `E-seeded_regression-…` trong `reports/eval_seeded_regression.json` (item E-002) |
| Triệu chứng | `pass_rate`, `db_fact_kept`, `refund_amount_correct` đều fail. Lab 8: `status resolved != denied`. Ledger refund 20.000đ, count 1; nhãn 0đ, `denied`. Reply: "LogiX đã hoàn 20.000đ cho đơn O-202." |
| Bước sai đầu tiên | Event 3 `model_override {"delay_days": 5}`: agent ghi đè `delay_days` của DB bằng số ngày trong ticket. |
| Vì sao là bước đầu tiên | Event 1 handoff và event 2 `investigator` (lookup_order ok, đơn O-202 `delivered`) đều đúng; từ event 3 trở đi quote (event 4, 20.000đ) và refund chỉ là hệ quả. |
| Failure mode | FM-03 ticket_trust |
| Đối chứng | `fixed` cùng claim@seed: không có event `model_override`, không hoàn tiền, status `denied`. |
| Regression test | `tests/test_lab9_regression.py::test_misreport_caught_only_by_reply_matches_ledger` (FM-08) và `DbFactKept` bắt event `model_override` (đỏ trên `seeded_regression`, xanh trên `fixed`). |
| Chưa chắc chắn | Swarm gốc cũng sai ở C-002@55 (seed % 5 == 0); trace không chứng minh nguyên nhân do ticket hay do rule riêng của seed. Biến thể `quiet_override` không ghi event nên `DbFactKept` bị mù, chỉ `refund_amount_correct` bắt được. |
