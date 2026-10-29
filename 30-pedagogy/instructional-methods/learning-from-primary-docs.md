---
schema_version: "2.0.0"
id: method-learning-from-primary-docs
type: practice
title: "Học kỹ năng kỹ thuật từ tài liệu gốc: bản đồ, truy hồi, soi định nghĩa, ôn giãn cách"
locale: vi
stage: [S3, S4, S5, S6]
axes: [AX-01, AX-03, AX-07]
capabilities: [CAP-02, CAP-03, CAP-04]
context: [technical-skill-learning, self-directed-learning, tutoring]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance:
  kind: authored
  citations:
    - url: https://pubmed.ncbi.nlm.nih.gov/26173288/
      locator: "Dunlosky et al. (2013), PubMed abstract: practice testing and distributed practice high utility; rereading low"
    - url: https://pubmed.ncbi.nlm.nih.gov/21252317/
      locator: "Karpicke & Blunt (2011), PubMed abstract: retrieval practice vs concept mapping"
    - url: https://pubmed.ncbi.nlm.nih.gov/16507066/
      locator: "Roediger & Karpicke (2006), PubMed abstract: testing vs restudying, confidence"
    - url: https://pubmed.ncbi.nlm.nih.gov/16719566/
      locator: "Cepeda et al. (2006), PubMed abstract: spacing and retention interval"
    - url: https://docs.python.org/3/tutorial/controlflow.html#else-clauses-on-loops
      locator: "The Python Tutorial, section 4.5 'else Clauses on Loops' (docs for Python 3.15.2), read 2026-10-29"
    - url: http://www.catb.org/~esr/faqs/smart-questions.html
      locator: "Raymond & Moen, 'How To Ask Questions The Smart Way', section 'Before You Ask', read 2026-10-29"
    - url: https://github.com/xiaolai/the-craft-of-selfteaching
      locator: "Idea lineage only (Tier 4/5, CC BY-NC-ND 3.0): markdown/Part.1.F, Part.1.G, Part.3.G, read 2026-10-29"
prerequisites: [method-forward-reference-management, method-self-regulated-learning]
leads_to: [practice-ai-assistance-ladder, practice-cognitive-offloading-atrophy]
source_ids: [evidence-dunlosky-2013-learning-techniques, evidence-karpicke-2011-retrieval-vs-concept-mapping, evidence-roediger-2006-test-enhanced-learning, evidence-cepeda-2006-distributed-practice]
---

# Học từ tài liệu gốc để không cần tutor nữa

> Protocol do tác giả biên soạn (`evidence_grade: U`). Mục tiêu sư phạm là
> **tốt nghiệp**: người học tự học được một mục tài liệu chưa từng gặp, và mức hỗ
> trợ của tutor giảm dần về AL0.

## 1. Capability Contract

Sau module này, giáo viên hoặc AI tutor có thể:

1. **Dẫn** người học qua bốn lượt đọc tài liệu chính thức (docs, đặc tả, hướng dẫn
   gốc): bản đồ → truy hồi → soi định nghĩa → ôn giãn cách.
2. **Thay** vòng đọc lại bằng kiểm tra đóng tài liệu ở mỗi lượt.
3. **Thiết kế** một câu hỏi soi định nghĩa: thuật ngữ bao gồm gì, loại trừ gì, ở
   trường hợp biên nào.
4. **Dạy** thói quen "tìm trước khi hỏi" và cách đặt một câu hỏi chính xác.
5. **Giảm dần** hỗ trợ theo [AI Assistance Ladder](../edtech-ai/ai-assistance-ladder.md)
   và ghi lại bằng chứng độc lập ở mỗi bậc.

## 2. Instructional Problem Solved

Người học quen học qua bài giảng hoặc bản tóm tắt có sẵn. Khi gặp công cụ mới, họ
hỏi người khác hoặc hỏi AI thay vì mở tài liệu gốc. Tài liệu gốc thường đầy đủ và
chính xác hơn bản tóm tắt, nhưng khó đọc với người mới: nhiều tham chiếu trước,
văn phong ngắn gọn, mỗi chữ trong định nghĩa đều có tác dụng.

Hai thất bại hay gặp:
- **Đọc như đọc truyện:** lướt, thấy quen, nghĩ là đã hiểu. Bỏ sót một chữ quyết
  định trong định nghĩa.
- **Uỷ thác toàn bộ:** nhờ AI tóm tắt docs. Có câu trả lời đúng nhưng người học
  không luyện được việc đọc và truy hồi. Xem
  [cognitive offloading](../edtech-ai/cognitive-offloading-and-atrophy.md).

**Dự đoán trước khi đọc tiếp.** Không chạy code, đoán đoạn sau in gì với ba danh
sách `[1, 3, 5]`, `[1, 4, 5]` và `[]`:

```python
for x in xs:
    if x % 2 == 0:
        print("found even", x)
        break
else:
    print("no even number")
```

Ghi ba dự đoán. Đáp án ở mục 5.

## 3. Preconditions & Contraindications

**Dùng khi:**
- Người học đã có một nền tối thiểu trong lĩnh vực (đọc được ví dụ đơn giản nhất
  của tài liệu). Với Python, ví dụ là chạy được một đoạn code ngắn.
- Có tài liệu chính thức, đúng phiên bản, đủ chất lượng.
- Mục tiêu là năng lực tự học lâu dài, không chỉ hoàn thành một việc gấp.

**Không dùng, hoặc dùng hạn chế, khi:**
- Người học hoàn toàn mới. Tài liệu gốc viết cho người đã biết nghề; với người
  mới, ví dụ mẫu có hướng dẫn cần đi trước (xem
  [Cognitive Load Theory](../../10-foundations/learning-science/cognitive-load-theory.md)).
- Kỹ năng vận động hoặc an toàn cao (bơi, thao tác y khoa, điện). Đọc không thay
  được luyện tập có giám sát và phản hồi.
- Tài liệu lỗi thời hoặc sai phiên bản. Kiểm tra số phiên bản trước lượt 1.
- Có nhu cầu tiếp cận (khó đọc, khiếm thị). Đọc thành tiếng, chuyển văn bản sang
  giọng nói hay phóng to chữ là điều chỉnh tiếp cận, không tính là "hỗ trợ nội
  dung" trên thang AL.

## 4. Method Anatomy & Expert Think-Aloud

### Lượt 0 — Chốt mục tiêu
Một câu: "Sau buổi này tôi dùng được X để làm Y." Ví dụ: "dùng `for…else` để báo
khi không tìm thấy phần tử".

### Lượt 1 — Bản đồ (map pass)
Xem mục lục, glossary, index, trang "what's new", số phiên bản. Đọc lướt mục liên
quan đến hết, chấp nhận chưa hiểu hết. Mọi thuật ngữ chưa biết đưa vào sổ tham
chiếu mở theo [Quản lý tham chiếu trước](forward-reference-management.md). Có
giới hạn thời gian.

> *Think-aloud:* "Mục tiêu lượt này là biết định nghĩa nằm ở đâu, không phải hiểu.
> Tôi ghi 'break' vào sổ vì mục 4.5 dựa vào nó, và nó nằm ngay ở 4.4."

### Lượt 2 — Truy hồi thay đọc lại (retrieval-check pass)
Sau mỗi đoạn: **đóng tài liệu**, viết hoặc nói (a) nó làm gì, (b) một ví dụ tự
nghĩ ra, (c) một dự đoán output. Sau đó mở lại, đối chiếu, đánh dấu chỗ sai.
Không đọc lại đoạn trước khi đã thử nhớ.

> *Think-aloud:* "Nếu tôi chỉ đọc lại, tôi sẽ thấy quen và tự tin. Viết ra từ trí
> nhớ cho tôi thấy ngay chỗ hổng: tôi nhớ 'else chạy khi xong vòng lặp' nhưng
> không chắc khi nào là 'xong'."

### Lượt 3 — Soi định nghĩa từng chữ (definition probe)
Với mỗi thuật ngữ then chốt, lập bảng ba cột:

| Bao gồm | Loại trừ | Trường hợp biên cần thử |
| :--- | :--- | :--- |
| `else` chạy khi vòng `for` kết thúc mà không gặp `break` | Không chạy khi vòng bị dừng bởi `break`; `return` hay ngoại lệ cũng bỏ qua `else` | Danh sách rỗng; `else` thẳng hàng với `for` hay với `if`? |

Mỗi ô trong cột cuối thành một dự đoán, rồi chạy code để kiểm.

> *Think-aloud:* "Mục 4.5 nói `else` chạy sau lần lặp cuối, *tức là* nếu không có
> `break`. Cụm 'lần lặp cuối' gợi ý phải có ít nhất một lần lặp. Cụm sau mới là
> tiêu chí thật. Danh sách rỗng là ca thử đúng chỗ hai cách đọc này khác nhau."

### Lượt 4 — Ôn giãn cách (spaced revisit)
Hẹn ít nhất một lần ôn sau một khoảng thời gian, chọn theo việc người học cần nhớ
bao lâu. Mỗi lần ôn: truy hồi đóng tài liệu → một bài mới (chuyển giao) → mở
tài liệu kiểm tra → cập nhật sổ. Module không đưa lịch tối ưu.

### Tìm trước khi hỏi, và hỏi chính xác
Thứ tự tìm: index và ô tìm kiếm của tài liệu → thông báo lỗi nguyên văn → thử
nghiệm nhỏ → mới hỏi người hoặc AI. Một câu hỏi chính xác có: mục tiêu, đã đọc
mục nào, đã thử gì, ví dụ tối thiểu tái hiện được, kết quả mong đợi và kết quả
thật. Danh sách "Before You Ask" của Raymond & Moen là nguồn tham khảo cho thứ tự
này (một bài luận nghề nghiệp, không phải bằng chứng thực nghiệm).

### I Do → We Do → You Do theo thang hỗ trợ
- **I Do (AL4):** tutor làm mẫu cả bốn lượt trên một mục, nói to quyết định.
- **We Do (AL3 → AL2):** người học làm, tutor đưa khung bảng soi định nghĩa, rồi
  chỉ còn hỏi probe ("ca biên nào bạn chưa thử?").
- **You Do (AL1 → AL0):** tutor chỉ hỏi "bạn sẽ tìm ở mục nào?", rồi im lặng.
  Bằng chứng tốt nghiệp: người học tự học một mục **chưa gặp**, giải thích được,
  và qua một lần kiểm tra muộn mà không có gợi ý.

## 5. Worked Execution Transcript (biên soạn, không phải ca quan sát)

Bối cảnh: người lớn đang học Python, muốn hiểu `for…else`.

- Người học: "Em đọc mục 4.5 ba lần rồi, em hiểu rồi."
- Tutor (AL2): "Đóng tab tài liệu. Dự đoán ba trường hợp này." *(đưa đoạn code ở
  mục 2)*
- Người học: "`[1, 3, 5]` in 'no even number'. `[1, 4, 5]` in 'found even 4' rồi
  in 'no even number'. `[]` không in gì vì không lặp lần nào."
- Tutor: "Giữ nguyên dự đoán. Giờ mở mục 4.5 và tìm câu quyết định khi nào `else`
  chạy."
- Người học: "...nếu không có `break`. Vậy `[1, 4, 5]` có `break` nên không in
  dòng thứ hai."
- Tutor: "Còn `[]`?"
- Người học: "Không có `break`... nên `else` vẫn chạy? Em đọc 'lần lặp cuối' nên
  tưởng phải có lặp."
- Tutor: "Chạy thử để kiểm." — Kết quả: `no even number`, `found even 4`,
  `no even number`.
- Tutor: "Điền bảng bao gồm / loại trừ / ca biên. Thêm một dòng: `return` trong
  vòng lặp thì sao?" — Người học dự đoán `else` bị bỏ qua, chạy thử, đúng.
- Tutor ghi: `assistance_level: AL2`, `independent_check_status: not-yet-observed`
  (vì có probe). Hẹn ôn: lần sau mở đầu bằng một bài mới, ví dụ dùng `while…else`
  tìm số chia, không mở tài liệu trước.

**Đáp án mục 2:** `no even number`; `found even 4`; `no even number`. Dòng
"found even 4" không đi kèm dòng `else`, và danh sách rỗng vẫn chạy `else`.

> *Điểm then chốt:* "em đọc ba lần rồi" là tự báo cáo sau đọc lại. Chỉ ba dự đoán
> đóng tài liệu mới lộ ra hai ngộ nhận: `else` gắn với `if`, và "phải có lần lặp".

## 6. Superficial / Pathological Implementation

| Cách làm hỏng | Vì sao hỏng | Sửa |
| :--- | :--- | :--- |
| Đọc lại nhiều lượt làm vòng chính | Quen mặt chữ, tự tin tăng; không đo được trí nhớ | Mỗi lượt kết thúc bằng truy hồi đóng tài liệu |
| Đọc "từng chữ" bằng cách đọc chậm lại lần nữa | Vẫn là đọc lại; bỏ sót vẫn không lộ ra | Biến từng chữ thành một dự đoán có thể chạy thử |
| AI tóm tắt cả trang docs cho người học | Uỷ thác đúng phần cần luyện | Ở AL0–AL2, AI hỏi probe, không tóm tắt |
| Hoãn luyện cho đến khi "đọc hiểu hết" | Mất truy hồi sớm | Luyện ngay trên ví dụ nhỏ ở lượt 2 |
| Bỏ lượt 4 | Không có giãn cách; dễ quên | Mỗi mục học xong có lịch ôn |
| Bắt người mới hoàn toàn tự đọc docs | Quá tải; nản | Ví dụ mẫu có hướng dẫn trước, docs sau |

**Ngộ nhận cần bác bỏ:**
- *"Tự học bằng docs nghĩa là không ai được giúp."* Mục tiêu là giảm dần hỗ trợ,
  không phải bỏ hỗ trợ ngay từ đầu.
- *"Hỏi AI là xấu."* Hỏi một câu chính xác sau khi đã tìm là kỹ năng. Vấn đề là
  uỷ thác phần đọc và truy hồi.
- *"Docs khó đọc thì tại người học kém."* Docs chính thức ưu tiên đầy đủ và chính
  xác; người mới cần cầu nối.

## 7. Diagnostic Hinge Question for Instructional Decision-Making

```yaml
hinge_question:
  stem: >
    Người học nói: "Em đọc mục 4.5 về for…else ba lần rồi, em hiểu rồi."
    Tutor đang ở giai đoạn We Do. Nước đi tiếp theo phù hợp nhất là gì?
  options:
    A: "Chuyển sang mục tiếp theo vì người học đã đọc kỹ"
    B: "Yêu cầu đọc lần thứ tư, chậm, từng chữ"
    C: "Đóng tài liệu, cho dự đoán output của vài biến thể (có break, không break, danh sách rỗng), rồi mở lại để tìm câu quyết định"
    D: "Tutor tự giảng lại for…else rõ hơn và đưa ví dụ mẫu"
  target: C
  distractor_analysis:
    A: "Có thể coi tự báo cáo là bằng chứng. Hoặc bị áp lực thời gian. Probe: 'Bằng chứng nào cho thấy người học dự đoán đúng được trường hợp danh sách rỗng?'"
    B: "Có thể hiểu 'đọc từng chữ' là đọc chậm lại. Hoặc tin rằng lặp lại tự sinh hiểu. Probe: 'Lần đọc thứ tư tạo ra quan sát nào mà ba lần trước không có?'"
    C: "Truy hồi đóng tài liệu, ca biên biến định nghĩa thành dự đoán, rồi đối chiếu với nguyên văn."
    D: "Có thể muốn giúp nhanh. Hoặc nhầm 'tôi giải thích rõ' với 'người học hiểu'. Ở We Do, việc này đẩy hỗ trợ lên AL4 khi chưa có bằng chứng cần đến. Probe: 'Người học đã thử điều gì trước khi bạn giảng?'"
  remediation_routing:
    A: "Xem mục 6, ngộ nhận về tự báo cáo; thêm một kiểm tra độc lập trước khi chuyển mục"
    B: "Xem lượt 3 ở mục 4: biến từng chữ thành một dự đoán chạy được"
    C: "Tiếp lượt 4 và hẹn ôn giãn cách"
    D: "Xem bậc AL2–AL4 trong AI Assistance Ladder; chỉ tăng hỗ trợ khi probe đã thất bại"
  insufficient_evidence: "Nếu người chọn không nêu lý do, hỏi lý do trước khi định tuyến."
```

## 8. Adaptation Matrix

| Người học / bối cảnh | Lượt bản đồ | Truy hồi & soi định nghĩa | Hỗ trợ |
| :--- | :--- | :--- | :--- |
| Người mới có nền tối thiểu | Tutor làm mẫu trên một mục ngắn | Bảng ba cột có sẵn khung | Bắt đầu AL4, hạ dần |
| Trung cấp | Người học tự làm, tutor kiểm sổ | Người học tự viết ca biên | AL2–AL1 |
| Nâng cao | Tự chọn tài liệu, kể cả đặc tả và mã nguồn | Đối chiếu nhiều nguồn chính thức | AL0; tutor chỉ kiểm tra muộn |
| Nhóm / cặp | Chia mục, mỗi người vẽ bản đồ một phần | Một người đóng tài liệu và giải thích, người kia đối chiếu nguyên văn | Giáo viên chỉ đưa probe |
| AI tutor | Hỏi "định nghĩa này nằm ở đâu?" thay vì trả lời | Sinh ca biên để người học dự đoán; không đưa đáp án trước dự đoán | Ghi `assistance_level` mỗi lượt; không tóm tắt cả trang ở AL0–AL2 trừ khi là điều chỉnh tiếp cận |

## 9. Fidelity Checklist & Failure Mode Recovery

- [ ] Có mục tiêu một câu trước lượt 1.
- [ ] Đã kiểm số phiên bản tài liệu.
- [ ] Mỗi lượt 2 kết thúc bằng viết/nói từ trí nhớ trước khi mở lại.
- [ ] Mỗi thuật ngữ then chốt có bảng bao gồm / loại trừ / ca biên, và ca biên
      được chạy thử.
- [ ] Có ít nhất một lần ôn giãn cách bắt đầu bằng truy hồi.
- [ ] Câu hỏi gửi người khác hoặc AI có mục tiêu, mục đã đọc, ví dụ tối thiểu.
- [ ] Mức hỗ trợ được ghi lại; tuyên bố "tự học được" chỉ dựa trên một mục chưa
      gặp và một kiểm tra muộn.

| Sự cố | Phục hồi |
| :--- | :--- |
| Người học kẹt ở lượt 1 vì quá nhiều thuật ngữ lạ | Tài liệu quá tầm; lùi về ví dụ mẫu có hướng dẫn, quay lại sau |
| Truy hồi trống rỗng | Cho đáp án, đánh dấu, hẹn ôn sớm hơn; đây chưa phải thất bại |
| Tài liệu mơ hồ thật | Chạy thử để kiểm; tìm đặc tả hoặc mã nguồn; ghi câu hỏi chính xác |
| Người học chỉ muốn AI trả lời | Thoả thuận rõ mục tiêu tốt nghiệp; cho phép hỏi sau khi đã tìm |
| Hỗ trợ không hạ được | Giữ mức hiện tại, đổi biểu diễn; không ép AL0 khi chưa có bằng chứng |

## 10. Evidence & Boundary Conditions

**Chưa kiểm được:** chưa đọc được nghiên cứu nào đánh giá trực tiếp quy trình bốn
lượt này, hay việc dạy người học tự đọc tài liệu kỹ thuật như một can thiệp. Đây
là thiết kế tác giả (`U`).

**Thành phần có nguồn (chỉ đọc abstract, ngày 2026-10-29):**
- Dunlosky et al. (2013): kiểm tra luyện tập và giãn cách được xếp mức hữu dụng
  cao; đọc lại và tóm tắt được xếp thấp. →
  [nguồn](../../60-evidence/sources/evidence-dunlosky-2013-learning-techniques.md)
- Karpicke & Blunt (2011): luyện truy hồi cho kết quả học có ý nghĩa tốt hơn học
  bằng lập bản đồ khái niệm, kể cả với câu hỏi suy luận. →
  [nguồn](../../60-evidence/sources/evidence-karpicke-2011-retrieval-vs-concept-mapping.md)
- Roediger & Karpicke (2006): kiểm tra hơn đọc lại ở bài kiểm tra muộn; đọc lại
  làm tăng tự tin. →
  [nguồn](../../60-evidence/sources/evidence-roediger-2006-test-enhanced-learning.md)
- Cepeda et al. (2006): khoảng giãn cách tốt nhất phụ thuộc thời gian cần nhớ. →
  [nguồn](../../60-evidence/sources/evidence-cepeda-2006-distributed-practice.md)
- Ví dụ `for…else` dựa trên The Python Tutorial mục 4.5 và đã chạy thử trên
  Python 3.14 trong lần biên soạn này.
- Quy tắc "tìm trước khi hỏi" dựa trên bài luận của Raymond & Moen, là hướng dẫn
  nghề nghiệp, không phải bằng chứng.

**Giới hạn áp dụng:** các nghiên cứu trên dùng văn bản học thuật hoặc nhiệm vụ nhớ
từ ngữ, không dùng tài liệu lập trình. Việc chuyển sang đọc docs là suy luận cần
pilot. Không có ngưỡng số cho thời lượng lượt, số lần ôn hay thời điểm hạ bậc AL.
Lộ trình hạ hỗ trợ dùng thang AL, vốn là khung thiết kế chưa được xác thực.

**Không lấy từ sách nguồn:**
- Đọc lại nhiều lượt làm vòng chính. Thay bằng truy hồi đóng tài liệu sau mỗi lượt.
- "Đọc từng chữ" hiểu là đọc chậm lại. Ở đây từng chữ thành dự đoán chạy thử được.
- Hoãn mọi luyện tập ở giai đoạn đọc. Ở đây luyện ngay trên ví dụ nhỏ.
- Không có lịch giãn cách. Ở đây lượt 4 là bắt buộc.
- Mở rộng "chỉ cần đọc là học được" sang kỹ năng vận động. Ở đây đó là chống chỉ
  định.

**Dòng ý tưởng (idea lineage):** ý "tài liệu chính thức là sách giáo khoa thật",
"đọc lướt để có bản đồ rồi đọc từng chữ", ví dụ `for…else`, và "tìm trước khi
hỏi" lấy cảm hứng từ Lý Tiếu Lai (xiaolai), *自学是门手艺 / The Craft of
Self-Teaching*, <https://github.com/xiaolai/the-craft-of-selfteaching>, chương
`Part.1.F`, `Part.1.G`, `Part.3.G`. Sách dùng giấy phép CC BY-NC-ND 3.0. Module
này không dịch hay chép đoạn nào; chỉ diễn giải ý tưởng. Sách là nguồn Tier 4/5
theo [chính sách bằng chứng](../../00-system/epistemic-policy.md) và không được
dùng làm bằng chứng.
