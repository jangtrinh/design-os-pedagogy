---
schema_version: "2.0.0"
id: method-forward-reference-management
type: practice
title: "Quản lý tham chiếu trước: dùng khái niệm trước khi giải thích mà vẫn khép vòng bằng truy hồi"
locale: vi
stage: [S3, S4, S5, S6]
axes: [AX-01, AX-03, AX-04]
capabilities: [CAP-02, CAP-03, CAP-04]
context: [tutoring, course-sequencing, technical-skill-learning]
evidence_grade: U
claim_status: unreviewed
review_status: unreviewed
provenance:
  kind: authored
  citations:
    - url: https://pubmed.ncbi.nlm.nih.gov/16507066/
      locator: "Roediger & Karpicke (2006), PubMed abstract: testing vs restudying, delayed retention, confidence"
    - url: https://pubmed.ncbi.nlm.nih.gov/19586265/
      locator: "Kornell, Hays & Bjork (2009), PubMed abstract: unsuccessful retrieval attempts followed by the answer"
    - url: https://pubmed.ncbi.nlm.nih.gov/16719566/
      locator: "Cepeda et al. (2006), PubMed abstract: inter-study interval and retention interval act jointly"
    - url: https://pubmed.ncbi.nlm.nih.gov/26173288/
      locator: "Dunlosky et al. (2013), PubMed abstract: utility ratings, rereading rated low"
    - url: https://github.com/xiaolai/the-craft-of-selfteaching
      locator: "Idea lineage only (Tier 4/5, CC BY-NC-ND 3.0): markdown/Part.1.F.deal-with-forward-references.md, read 2026-10-29"
prerequisites: [concept-cognitive-load-theory, spaced-practice-retrieval]
leads_to: [runtime-pedagogical-state-machine, method-learning-from-primary-docs]
source_ids: [evidence-roediger-2006-test-enhanced-learning, evidence-kornell-2009-unsuccessful-retrieval, evidence-cepeda-2006-distributed-practice, evidence-dunlosky-2013-learning-techniques]
---

# Quản lý tham chiếu trước (forward references)

> Đây là protocol do tác giả biên soạn, chưa được thử nghiệm như một can thiệp
> trọn gói. Từng thành phần có nguồn riêng ở mục 10; toàn bộ quy trình vẫn ở
> `evidence_grade: U` và cần pilot.

## 1. Capability Contract

Sau module này, giáo viên hoặc AI tutor có thể:

1. **Phát hiện** một tham chiếu trước: thuật ngữ, ký hiệu hay cấu trúc người học
   buộc phải gặp hoặc dùng *bây giờ* nhưng lời giải thích đầy đủ nằm ở bài sau.
2. **Gắn cờ** nó bằng một câu nói rõ ba điều: phần cần biết ngay, phần được hoãn,
   và lúc sẽ quay lại.
3. **Giữ sổ tham chiếu mở** (open-reference ledger) và đưa mỗi mục đến hạn khép.
4. **Khép vòng** bằng câu hỏi truy hồi đóng sách, giải thích phần đã hoãn, một bài
   mới phân biệt đúng phần đó, rồi lên lịch ôn giãn cách. Không khép bằng đọc lại.
5. **Quyết định** khi nào nên đổi trình tự thay vì gắn thêm cờ.

## 2. Instructional Problem Solved

Nhiều lĩnh vực không xếp được theo kiểu "định nghĩa trước, dùng sau". Lập trình,
luật, y khoa, ngoại ngữ và tài liệu kỹ thuật thật đầy khái niệm xuất hiện trước
khi được giải thích. Hai phản xạ phổ biến đều hỏng:

- **Giấu hoặc lờ đi:** người học tự đoán nghĩa, dễ đoán sai, và tốn chú ý vào
  việc giải mã thứ chưa cần.
- **Hứa suông:** "sau này sẽ hiểu". Không ai ghi lại lời hứa, nên vòng không bao
  giờ khép. Người học mang theo một lỗ hổng mà không biết.

**Dự đoán trước khi đọc tiếp.** Buổi 1, tutor cho người học chạy `print(len("abc"))`
và nói "hàm sẽ học ở buổi 3". Đến buổi 3, cách khép vòng nào giúp nhớ lâu hơn sau
một tuần? (a) cho đọc lại đoạn buổi 1; (b) giải thích kỹ rồi hỏi "hiểu chưa?";
(c) yêu cầu nhớ lại, không mở tài liệu, rằng buổi 1 đã hoãn điều gì, rồi mới giải
thích. Ghi lựa chọn của bạn, rồi đối chiếu với mục 4 và mục 10.

## 3. Preconditions & Contraindications

**Dùng khi:**
- Không thể dạy khái niệm đầy đủ trước mà không làm quá tải bài hiện tại, ví dụ
  dạy "hàm" trước khi người học in được một dòng chữ.
- Người học phải làm việc với tài liệu thật (docs, văn bản luật, phác đồ) vốn
  không được viết theo thứ tự sư phạm.
- Có thể nói một nghĩa tối thiểu *đúng nhưng chưa đủ* cho bài hiện tại.

**Không dùng, hoặc dùng hạn chế, khi:**
- Có thể đổi trình tự với chi phí thấp. Khi đó đổi trình tự, không gắn cờ.
- Khái niệm bị hoãn chính là mục tiêu đang được đánh giá.
- Nghĩa tối thiểu buộc phải nói sai (một "lời nói dối tạm" sẽ phải gỡ sau). Hãy
  nói một phiên bản đúng nhưng hẹp.
- Trẻ nhỏ (S1–S2): ưu tiên đổi trình tự. Lời hứa "sẽ quay lại" cần năng lực theo
  dõi thời gian và tự điều chỉnh mà module này chưa kiểm tra ở lứa tuổi đó.
- Sổ đã có quá nhiều mục mở mà người học không còn theo dõi được. Dấu hiệu là họ
  hỏi lại cùng một cờ, hoặc lo lắng về "những thứ chưa hiểu". Khi đó dừng gắn
  thêm cờ và sắp lại bài. Module không đặt một ngưỡng số; ngưỡng cần quan sát
  trong bối cảnh.

## 4. Method Anatomy & Expert Think-Aloud

Protocol có ba nhịp: gắn cờ, giữ sổ, khép vòng. Khi luyện cho giáo viên hoặc
cấu hình AI tutor, đi theo I Do → We Do → You Do:
- **I Do:** người hướng dẫn làm mẫu một câu cờ và một mục sổ, nói to quyết định.
- **We Do:** người học nghề cùng viết câu cờ cho tham chiếu trước tiếp theo trong
  bài, đối chiếu ba phần (dùng ngay / hoãn / hẹn).
- **You Do:** người học nghề tự lập danh sách cờ và kế hoạch khép vòng cho một bài
  của mình; đồng nghiệp chấm bằng checklist ở mục 9.

### 4.1 Gắn cờ (flag)

Câu gắn cờ có ba phần:
1. **Dùng ngay:** "Hôm nay chỉ cần biết `len(...)` trả về độ dài của thứ trong
   ngoặc."
2. **Hoãn:** "Vì sao viết có ngoặc, và tự tạo hàm ra sao, chưa cần."
3. **Hẹn:** "Ta quay lại ở buổi 3. Mục này nằm trong sổ."

> *Think-aloud của tutor:* "Nếu giải thích 'hàm' ngay, người học phải giữ cùng
> lúc cú pháp gọi, giá trị trả về và khái niệm tham số. Với người mới, số phần tử
> tương tác này quá nhiều so với mục tiêu hôm nay là in ra một kết quả. Nhưng
> nếu tôi chỉ nói 'đừng để ý', họ vẫn sẽ tốn sức đoán. Câu cờ phải cho phép họ
> *thôi giải mã*: nói rõ phần nào không cần hiểu."

Đây là ứng dụng trực tiếp của [Cognitive Load Theory](../../10-foundations/learning-science/cognitive-load-theory.md):
hoãn phần giải thích để giảm tải nội tại lúc này. Cờ không làm tải biến mất; nó
chỉ hiệu quả khi người học thật sự được phép bỏ qua phần hoãn.

### 4.2 Sổ tham chiếu mở (ledger)

Người giữ sổ là tutor, không phải người học. Người học được xem sổ khi muốn.

```yaml
open_references:
  - ref_id: fr-001
    term: "hàm (function)"
    first_seen: "buổi 1, print(len('abc'))"
    usable_meaning_now: "len(x) trả về độ dài của x"
    deferred_part: "định nghĩa hàm, tham số, giá trị trả về"
    payoff_planned: "buổi 3"
    status: open            # open → due → closing → closed | reopened
    learner_questions: ["tại sao có ngoặc?"]
    retrieval_evidence: []  # điền khi khép vòng và mỗi lần ôn
```

> *Think-aloud:* "Sổ là để tôi giữ lời hứa. Không có sổ, lời hứa phụ thuộc vào
> trí nhớ của tôi, và với một AI tutor là phụ thuộc vào độ dài ngữ cảnh. Câu hỏi
> người học đặt ra lúc gặp cờ là dữ liệu quý: buổi khép vòng phải trả lời đúng
> câu đó."

### 4.3 Khép vòng (payoff)

Thứ tự ở buổi hẹn:
1. **Truy hồi đóng sách:** "Buổi 1 ta dùng `len` mà chưa giải thích. Không mở
   lại bài, hãy viết: nó làm gì, và ta đã hoãn điều gì?" Nếu người học không nhớ,
   vẫn tiếp tục. Một lần truy hồi thất bại, sau đó có đáp án, vẫn có ích (mục 10).
2. **Giải thích phần đã hoãn,** nối với câu trả lời vừa viết và với câu hỏi cũ
   trong sổ.
3. **Bài mới phân biệt:** một nhiệm vụ chỉ làm đúng được khi hiểu phần đã hoãn,
   ví dụ tự viết hàm `dem_nguyen_am(s)` rồi giải thích vì sao `len` và hàm này
   cùng một dạng.
4. **Lên lịch ôn giãn cách:** đặt ít nhất một lần ôn ở buổi sau và một lần ở xa
   hơn. Mỗi lần ôn mở đầu bằng truy hồi, không bằng đọc lại. Khoảng cách chọn
   theo việc người học cần nhớ bao lâu; module không đưa lịch tối ưu.
5. Cập nhật `status: closed` chỉ khi có bằng chứng ở bước 3. Nếu bước 3 hỏng,
   chuyển `reopened` và hẹn lại.

> *Think-aloud:* "Tôi không hỏi 'nhớ không?' hay 'hiểu chưa?'. Đó là tự báo cáo.
> Đọc lại bài cũ sẽ làm người học thấy quen, mà cảm giác quen không phải bằng
> chứng nhớ được sau một tuần."

**Nối với lý thuyết.** Câu cờ cùng sơ đồ "những gì sẽ quay lại" đóng vai trò gần
với *advance organizer* của Ausubel: một khung đặt trước để gắn kiến thức sau.
Việc hẹn quay lại sâu hơn mang tinh thần *spiral curriculum* của Bruner. Cả hai
là dòng lý thuyết Tier 3 (Grade E), không được đọc lại trong lần biên soạn này.
Lịch ôn dựa trên module [Spaced Practice & Retrieval](../../10-foundations/learning-science/spaced-practice-retrieval.md).

## 5. Worked Execution Transcript (biên soạn, không phải ca quan sát)

Bối cảnh: người lớn tự học Python với AI tutor, ba buổi trong hai tuần.

**Buổi 1**
- Tutor: "Gõ `print(len("abc"))` và chạy." — Người học: "Ra 3."
- Tutor: "Đúng. Hôm nay chỉ cần biết `len(...)` trả về độ dài thứ trong ngoặc.
  Vì sao có ngoặc và làm sao tự tạo một hàm như `len` thì để buổi 3. Tôi ghi vào
  sổ, bạn không cần nhớ hộ."
- Người học: "Tại sao `print` cũng có ngoặc?"
- Tutor: "Câu hỏi hay. `print` cùng loại với `len`. Tôi thêm câu hỏi của bạn vào
  mục này; buổi 3 sẽ trả lời đúng câu đó." *(Ghi `learner_questions`.)*
- Phần còn lại của buổi: luyện chuỗi và số. Người học vẫn luyện bình thường; cờ
  không phải lý do hoãn luyện tập.

**Buổi 3**
- Tutor: "Đóng tab bài cũ. Buổi 1 ta dùng hai thứ có ngoặc mà chưa giải thích.
  Bạn nhớ đó là gì, và ta hoãn điều gì?"
- Người học: "`len` với... `input`? Hoãn vì sao có ngoặc."
- Tutor: "Một nửa đúng. Thứ hai là `print`. Bạn nhớ đúng phần bị hoãn." *(Ghi
  bằng chứng: nhớ phần hoãn, nhầm tên hàm thứ hai.)*
- Tutor giải thích: hàm nhận đầu vào trong ngoặc và có thể trả về giá trị; rồi
  trả lời câu hỏi cũ về `print`.
- Bài phân biệt: "Viết `dem_nguyen_am(s)` trả về số nguyên âm trong `s`. Rồi giải
  thích: `print(dem_nguyen_am("hello"))` chạy theo thứ tự nào?"
- Người học làm đúng hàm, nhưng nói `print` chạy trước. Tutor không đóng mục;
  đặt `status: reopened`, cho một ví dụ lồng hàm, hẹn ôn ở buổi 4 bằng một câu
  dự đoán thứ tự chạy.

**Buổi 4 (ôn):** mở đầu bằng câu dự đoán, không mở bài buổi 3. Người học dự đoán
đúng thứ tự và giải thích được. Mục chuyển `closed`; một lần ôn xa hơn vẫn được
xếp lịch.

> *Điểm then chốt:* buổi 3 đã phát hiện lỗi thứ tự thực thi nhờ bài phân biệt.
> Nếu chỉ hỏi "hiểu chưa?", lỗi này đã bị bỏ qua.

## 6. Superficial / Pathological Implementation

| Cách làm hỏng | Vì sao hỏng | Sửa |
| :--- | :--- | :--- |
| "Đừng lo, sau sẽ hiểu" nhưng không có sổ | Lời hứa không ai giữ; vòng không khép | Mỗi cờ phải có một mục trong sổ và một buổi hẹn |
| Gắn cờ cho mọi thứ | Người học thấy toàn bộ bài là "chưa hiểu", tăng lo lắng | Đổi trình tự nếu rẻ; chỉ gắn cờ khi thật cần |
| Khép vòng bằng "đọc lại bài 1" | Tạo cảm giác quen; không cho bằng chứng nhớ lâu | Truy hồi đóng sách trước, giải thích sau |
| Hoãn mọi bài luyện cho đến khi hết cờ | Mất cơ hội luyện và truy hồi sớm | Luyện phần đã dùng được; cờ chỉ hoãn phần giải thích |
| Khép bằng một lời giảng hay, không có bài kiểm | Tutor làm hết việc; không có bằng chứng độc lập | Bắt buộc bài phân biệt mới trước khi `closed` |
| Nghĩa tối thiểu nói sai | Phải gỡ niềm tin sai sau này | Nói phiên bản đúng nhưng hẹp |

**Ngộ nhận cần bác bỏ:**
- *"Người học dùng đúng rồi thì đã hiểu."* Dùng đúng trong một mẫu quen không cho
  thấy họ hiểu phần đã hoãn. Kiểm bằng nhiệm vụ mới.
- *"Đọc nhiều lần sẽ tự thấm."* Nguồn đọc ở mục 10 cho thấy kiểm tra hơn đọc lại
  ở các bài kiểm tra muộn, dù đọc lại làm tăng tự tin.
- *"Không nhớ được lúc khép vòng là thất bại."* Một lần truy hồi hỏng rồi được
  biết đáp án vẫn có ích; ghi lại và hẹn ôn.

## 7. Diagnostic Hinge Question for Instructional Decision-Making

```yaml
hinge_question:
  stem: >
    Buổi 1 tutor gắn cờ "đối tượng (object)" khi người học gọi "abc".upper().
    Buổi 5 là buổi hẹn. Người học đã dùng .upper() đúng nhiều lần từ buổi 1.
    Tutor nên làm gì đầu tiên ở buổi 5?
  options:
    A: "Cho người học đọc lại đoạn buổi 1 rồi giảng về đối tượng"
    B: "Giảng kỹ về đối tượng rồi hỏi: bạn hiểu chưa?"
    C: "Không mở tài liệu: hỏi người học nhớ gì về chỗ đã gặp và phần đã hoãn; rồi giảng, cho bài mới phân biệt, xếp lịch ôn"
    D: "Bỏ qua khép vòng vì người học đã dùng .upper() đúng; xóa mục khỏi sổ"
  target: C
  distractor_analysis:
    A: "Có thể tin rằng tiếp xúc lại là đủ để khép vòng. Hoặc chỉ muốn khởi động nhẹ. Probe: 'Sau khi đọc lại, bằng chứng nào cho thấy họ sẽ nhớ sau một tuần?'"
    B: "Có thể coi tự báo cáo là bằng chứng. Hoặc thiếu sẵn bài phân biệt. Probe: 'Câu trả lời nào ở bước này sẽ khiến bạn mở lại mục?'"
    C: "Truy hồi trước, giải thích sau, kiểm bằng nhiệm vụ mới, có lịch ôn."
    D: "Có thể nhầm dùng đúng trong mẫu quen với hiểu phần đã hoãn. Hoặc sổ bị quá tải. Probe: 'Người học có giải thích được vì sao .upper() đứng sau chuỗi không?'"
  remediation_routing:
    A: "Đọc mục 4.3 bước 1; chạy lại transcript mục 5 với phiên bản đọc lại và so sánh bằng chứng thu được"
    B: "Viết một bài phân biệt cho 'đối tượng' trước khi giảng"
    C: "Chuyển sang luyện tập mục 8 với nhóm hoặc AI tutor"
    D: "Xem ngộ nhận 1 ở mục 6; nếu sổ quá dài, xem mục 3 về đổi trình tự"
  insufficient_evidence: "Nếu chọn mà không nêu lý do, hỏi lý do trước khi định tuyến."
```

Một lựa chọn chưa xác định duy nhất một niềm tin. Hỏi lý do trước khi can thiệp.

## 8. Adaptation Matrix

| Người học / bối cảnh | Gắn cờ | Sổ | Khép vòng |
| :--- | :--- | :--- | :--- |
| Người mới (S3–S6, chưa có nền) | Ít cờ, câu cờ ngắn; ưu tiên đổi trình tự | Tutor giữ; người học không cần nhìn | Truy hồi có gợi ý nhẹ (AL1–AL2), bài phân biệt nhỏ |
| Người đã có nền | Có thể nhiều cờ hơn; người học tự đề xuất phần hoãn | Người học cùng giữ sổ | Truy hồi không gợi ý; bài chuyển giao xa hơn |
| Nhóm / lớp | Cờ chung trên bảng "sẽ quay lại" | Một sổ lớp, công khai | Mọi người viết câu trả lời truy hồi cùng lúc (bảng con, phiếu), rồi mới giảng |
| AI tutor | Câu cờ đủ ba phần; không tự giải thích phần hoãn khi chưa đến hẹn, trừ khi người học thật sự cần để làm tiếp | Lưu ngoài ngữ cảnh hội thoại, có `payoff_planned` | Trạng thái `due` kích hoạt truy hồi trước giải thích (xem [state machine](../../90-agent-runtime/workflows/pedagogical-state-machine.md)) |
| Người học lo âu cao | Sổ ngắn, hiển thị; nói rõ "chưa hiểu là bình thường ở bước này" | Cho xem sổ để thấy lời hứa được giữ | Truy hồi ít rủi ro, không chấm điểm |

## 9. Fidelity Checklist & Failure Mode Recovery

- [ ] Mỗi cờ có đủ ba phần: dùng ngay / hoãn / hẹn.
- [ ] Nghĩa tối thiểu đúng (dù hẹp).
- [ ] Mỗi cờ có một mục trong sổ với `payoff_planned`.
- [ ] Bài luyện không bị hoãn chỉ vì có cờ.
- [ ] Buổi hẹn mở đầu bằng truy hồi đóng sách, không bằng đọc lại.
- [ ] Có bài mới phân biệt trước khi `closed`.
- [ ] Có ít nhất một lần ôn giãn cách sau khi khép.
- [ ] Câu hỏi người học đặt lúc gặp cờ được trả lời ở buổi khép.

| Sự cố | Phục hồi |
| :--- | :--- |
| Người học không nhớ gì lúc truy hồi | Cho đáp án, vẫn giảng; ghi bằng chứng; xếp ôn sớm hơn |
| Tutor quên hẹn | Kiểm tra mục `due` ở đầu mỗi buổi; khép muộn vẫn hơn không khép |
| Người học đòi hiểu ngay | Cho một giải thích ngắn, đúng; nếu cần cho việc đang làm, khép sớm luôn |
| Sổ phình to | Dừng gắn cờ; sắp lại trình tự bài |
| Bài phân biệt hỏng | `reopened`, đổi cách biểu diễn, hẹn lại |

## 10. Evidence & Boundary Conditions

**Chưa kiểm được:** chưa đọc được nghiên cứu nào đánh giá trực tiếp quy trình
"cờ + sổ + khép vòng" như một gói. Đây là thiết kế tác giả (`U`).

**Thành phần có nguồn (chỉ đọc abstract, ngày 2026-10-29):**
- Roediger & Karpicke (2006): ôn bằng kiểm tra cho kết quả tốt hơn đọc lại ở các
  bài kiểm tra sau 2 ngày và 1 tuần. Ở mốc 5 phút thì ngược lại. Đọc lại làm tăng
  tự tin. → [nguồn](../../60-evidence/sources/evidence-roediger-2006-test-enhanced-learning.md)
- Kornell, Hays & Bjork (2009): truy hồi thất bại rồi được xem đáp án vẫn cải
  thiện việc học, với tài liệu từ vựng và câu hỏi hư cấu. →
  [nguồn](../../60-evidence/sources/evidence-kornell-2009-unsuccessful-retrieval.md)
- Cepeda et al. (2006): khoảng giãn cách tốt nhất tăng theo thời gian cần nhớ;
  tổng hợp trên nhiệm vụ nhớ từ ngữ. →
  [nguồn](../../60-evidence/sources/evidence-cepeda-2006-distributed-practice.md)
- Dunlosky et al. (2013): đọc lại được xếp mức hữu dụng thấp; kiểm tra luyện tập
  và giãn cách được xếp cao. →
  [nguồn](../../60-evidence/sources/evidence-dunlosky-2013-learning-techniques.md)
- Ausubel (advance organizer) và Bruner (spiral curriculum): dòng lý thuyết
  Tier 3, Grade E; chỉ nêu tên, không đọc lại trong lần này.

**Giới hạn áp dụng:** các nguồn trên dùng văn bản, từ vựng hoặc kiến thức khoa
học, không dùng việc học lập trình hay đọc tài liệu kỹ thuật. Việc áp dụng sang
khái niệm kỹ thuật là suy luận cần kiểm chứng. Không có ngưỡng số cho số cờ hay
lịch ôn.

**Không lấy từ sách nguồn:**
- Đọc lại là vòng lặp chính. Sách khuyên đọc hết dù chưa hiểu rồi lặp nhiều lần
  (nguyên văn: "读不懂也要读完，然后重复很多遍", Lý Tiếu Lai, chương `Part.1.F`). Module này giữ ý "đọc lướt hết để
  có bản đồ", nhưng thay vòng lặp đọc lại bằng truy hồi đóng sách.
- Để việc tự viết chương trình sau khi đã đọc được code cơ bản (sách vẫn khuyên
  sửa và chạy code mẫu trong lúc đọc). Ở đây luyện truy hồi bắt đầu ngay; chỉ phần giải
  thích bị hoãn.
- Không có lịch giãn cách. Ở đây mọi mục đã khép đều có lịch ôn.
- Quy việc quên cho sự lười biếng. Quên là bình thường; sổ và lịch ôn tồn tại vì
  lẽ đó.

**Dòng ý tưởng (idea lineage):** khái niệm "tham chiếu trước" (过早引用) và chiến
lược gắn cờ "chưa cần hiểu, sẽ quay lại" lấy cảm hứng từ Lý Tiếu Lai (xiaolai),
*自学是门手艺 / The Craft of Self-Teaching*, <https://github.com/xiaolai/the-craft-of-selfteaching>,
chương `Part.1.F`. Sách dùng giấy phép CC BY-NC-ND 3.0. Module này không dịch hay
chép đoạn nào; chỉ diễn giải ý tưởng bằng lời của tác giả module. Sách là nguồn
Tier 4/5 theo [chính sách bằng chứng](../../00-system/epistemic-policy.md) và
không được dùng làm bằng chứng.

Module liên quan: [Học từ tài liệu gốc](learning-from-primary-docs.md).
