export const phases = {probe: 'Tìm dấu hiệu', interpret: 'Đặt giả thuyết', teach: 'Thử cách dạy', check: 'Kiểm tra lại', review: 'Nhìn lại', transfer: 'Chuyển giao', reflect: 'Phản tư', complete: 'Hoàn thành'};
export const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = value => { try {const u = new URL(value); return u.protocol === 'https:' ? esc(u.href) : '#';} catch {return '#';} };

export function sourceList(sources) {
  return '<details class="sources"><summary>Nguồn và giới hạn áp dụng</summary>' + sources.map(s => '<article><a href="' + safeUrl(s.url) + '" target="_blank" rel="noopener noreferrer">' + esc(s.title) + '</a><p>' + esc(s.scope) + '</p><small>Vị trí: ' + esc(s.locator) + ' · Đã đối chiếu metadata và abstract.</small></article>').join('') + '</details>';
}

export function sessionList(items, selected) {
  if (!items.length) return '<p class="muted">Chưa có phiên. Chọn một tình huống để bắt đầu.</p>';
  return items.map(s => '<a class="session-link' + (s.id === selected ? ' selected' : '') + '" href="#session/' + esc(s.id) + '"' + (s.id === selected ? ' aria-current="page"' : '') + '><strong>' + esc(s.title) + '</strong><small>' + esc(phases[s.phase]) + ' · Bản ' + s.revision + '</small></a>').join('');
}

export function home(catalog) {
  return '<section class="hero"><div class="eyebrow">BỘ BÀI 01 · PHÂN SỐ</div><h1>Một câu hỏi tốt.<br>Một cách dạy phù hợp.</h1><p class="lead">Luyện cách đọc bài làm, hỏi thêm và điều chỉnh cách hướng dẫn. Bắt đầu bằng một tình huống nhỏ.</p><div class="hero-equation" aria-label="So sánh một phần tám và một phần năm"><span>1/8</span><span class="question-mark">?</span><span>1/5</span></div></section>' +
    '<section aria-labelledby="cases-title"><div class="section-title"><h2 id="cases-title">Bạn muốn thử tình huống nào?</h2><span>' + catalog.cases.length + ' tình huống biên soạn</span></div><div class="case-grid">' + catalog.cases.map((c, i) => '<article class="case-card"><span class="case-number">0' + (i + 1) + '</span><div class="tag">Phân số · ' + esc(c.stage) + '</div><h3>' + esc(c.title) + '</h3><p>' + esc(c.summary) + '</p><button class="button secondary start-case" data-case="' + esc(c.id) + '">Luyện tình huống này</button></article>').join('') + '</div></section>' +
    '<section class="notice"><h2>Biết rõ mình đang luyện gì</h2><p>' + esc(catalog.notice) + '</p><p>Các nhận xét nối với lựa chọn và diễn biến đã lưu. Bạn có thể xuất phiên cho một coach đọc lại.</p></section>' + sourceList(catalog.sources);
}

function fractionsDiagram(fractions) {
  const valid = fractions.every(f => Array.isArray(f) && f.length === 2 && f.every(Number.isFinite) && f[1] > 0 && f[0] >= 0 && f[0] <= f[1] && f[1] <= 20);
  if (!valid) return '';
  const rows = fractions.map(([n, d], index) => {
    const y = 42 + index * 58, x = 54, width = 420;
    let ticks = '';
    for (let i = 0; i <= d; i++) ticks += '<line x1="' + (x + width * i / d) + '" y1="' + (y - 5) + '" x2="' + (x + width * i / d) + '" y2="' + (y + 5) + '"/>';
    return '<g class="number-line"><line x1="54" y1="' + y + '" x2="474" y2="' + y + '"/>' + ticks + '<circle class="fraction-dot" cx="' + (x + width * n / d) + '" cy="' + y + '" r="6"/><text x="' + (x + width * n / d) + '" y="' + (y - 15) + '" text-anchor="middle">' + n + '/' + d + '</text><text x="54" y="' + (y + 22) + '" text-anchor="middle">0</text><text x="474" y="' + (y + 22) + '" text-anchor="middle">1</text></g>';
  }).join('');
  return '<figure class="diagram"><svg viewBox="0 0 530 142" role="img" aria-label="Hai trục số cùng đơn vị từ 0 đến 1; vị trí phân số được đánh dấu chính xác">' + rows + '</svg><figcaption>Cùng một đơn vị. Mỗi trục được chia thành các phần bằng nhau theo mẫu số.</figcaption></figure>';
}

function feedback(s) {
  if (!s.review || !s.review.observations) return '';
  return '<section class="feedback"><div class="eyebrow">NHÌN LẠI LỰA CHỌN</div><h2>Điều có thể quan sát</h2>' + s.review.observations.map(o => '<article><h3>' + esc(phases[o.phase]) + '</h3><blockquote>' + esc(o.quote) + '</blockquote><p>' + esc(o.observation) + '</p></article>').join('') + '<p class="case-note">' + esc(s.review.case_note) + '</p><p><strong>Thử cách khác:</strong> ' + esc(s.review.next_try) + '</p><p class="muted">' + esc(s.review.limit) + '</p></section>';
}

export function sessionView(s, draft, archivedDraft) {
  const progress = Object.keys(phases).map((p, i) => '<li class="' + (p === s.phase ? 'current' : i < Object.keys(phases).indexOf(s.phase) ? 'done' : '') + '"' + (p === s.phase ? ' aria-current="step"' : '') + '><span>' + (i + 1) + '</span>' + esc(phases[p]) + '</li>').join('');
  const roles = {teacher: 'Bạn · Người dạy', learner: 'Học sinh mô phỏng', coach: 'Gợi ý biên soạn'};
  const transcript = s.transcript.map((t, i) => '<article class="turn ' + esc(t.role) + '" id="turn-' + i + '"><small>' + roles[t.role] + '</small><p>' + esc(t.text) + '</p></article>').join('');
  const stale = draft && (draft.revision !== s.revision || draft.phase !== s.phase);
  const stored = draft && !stale ? draft : {};
  const previous = stale ? draft : archivedDraft;
  let form = '<div class="completed"><div class="eyebrow">ĐÃ LƯU PHIÊN</div><h2>Mang một thay đổi vào lần dạy tiếp theo.</h2><p>' + esc(s.reflection) + '</p><button class="button primary start-case" data-case="' + esc(s.case_id) + '">Luyện lại tình huống</button><a class="button secondary" href="#">Chọn tình huống khác</a></div>';
  if (s.prompt) {
    const options = s.prompt.options.map(o => '<label class="option"><input type="radio" name="choice" value="' + esc(o.id) + '" required' + (stored.choice === o.id ? ' checked' : '') + '><span>' + esc(o.label) + '</span></label>').join('');
    form = '<form id="move-form"><div class="eyebrow">BƯỚC ' + (Object.keys(phases).indexOf(s.phase) + 1) + '</div><h2 id="step-title">' + esc(s.prompt.title) + '</h2><p>' + esc(s.prompt.question) + '</p><fieldset><legend class="sr-only">Chọn hành động</legend>' + options + '</fieldset><label class="text-label" for="teacher-text">' + (s.phase === 'reflect' ? 'Điều bạn sẽ thay đổi' : 'Lời bạn sẽ nói hoặc lý do lựa chọn') + '</label><textarea id="teacher-text" name="text" rows="4" maxlength="4000"' + (s.phase === 'reflect' ? ' required' : '') + ' placeholder="Viết theo cách của bạn…">' + esc(stored.text || '') + '</textarea><p class="input-help">Lưu nguyên văn để bạn hoặc coach đọc lại. Chưa chấm tự động câu chữ.</p><button class="button primary" type="submit">' + (s.phase === 'reflect' ? 'Lưu và hoàn thành' : s.phase === 'review' ? 'Mở bài chuyển giao' : 'Ghi lựa chọn và tiếp tục') + '</button><span id="save-state" class="save-state">Bản nháp được giữ trên trình duyệt này.</span></form>';
  }
  const recovery = previous ? '<details class="draft-recovery" open><summary>Bản nháp trước được giữ lại</summary><p>Bản nháp chưa được gửi lại tự động. Đọc phiên mới rồi chọn hành động phù hợp; bạn có thể sao chép nội dung bên dưới.</p><textarea readonly aria-label="Bản nháp được giữ lại">' + esc(previous.text || previous.choice || '') + '</textarea><button class="button secondary" id="discard-draft">Bỏ bản nháp cũ</button></details>' : '';
  return '<div class="workspace-title"><div><div class="eyebrow">PHIÊN LUYỆN DẠY · MÔ PHỎNG BIÊN SOẠN</div><h1>' + esc(s.title) + '</h1><span class="muted">Đã lưu bản ' + s.revision + ' · ' + esc(phases[s.phase]) + '</span></div><div class="toolbar"><button class="button quiet" id="reload-session">Tải bản đã lưu</button><button class="button quiet" id="replay-session">Đối chiếu diễn biến</button><a class="button quiet" href="/api/sessions/' + esc(s.id) + '/export?format=md">Xuất Markdown</a><a class="button quiet" href="/api/sessions/' + esc(s.id) + '/export?format=json">JSON</a></div></div><ol class="progress" aria-label="Tiến trình luyện tập">' + progress + '</ol>' + recovery + '<div class="workspace-grid"><section class="conversation" aria-label="Tình huống và diễn biến"><div class="context-card"><h2>Bối cảnh</h2><p>' + esc(s.scenario.context) + '</p></div>' + transcript + (s.choices.teach ? fractionsDiagram(s.scenario.fractions) : '') + '</section><section class="action-panel" aria-label="Hành động tiếp theo">' + form + '</section></div>' + feedback(s) + (s.transfer_feedback ? '<section class="transfer-feedback"><div class="eyebrow">BÀI CHUYỂN GIAO</div><h2>' + (s.transfer_feedback.matched_authored_key ? 'Lựa chọn khớp gợi ý biên soạn' : 'Một cách nhìn khác để cân nhắc') + '</h2><p>' + esc(s.transfer_feedback.explanation) + '</p><p class="muted">' + esc(s.transfer_feedback.limit) + '</p></section>' : '') + sourceList(s.sources);
}
