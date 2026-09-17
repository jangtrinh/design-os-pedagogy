import {home, sessionView, sessionList} from './views.js';
const main=document.querySelector('#main'), message=document.querySelector('#message'), nav=document.querySelector('#sessions');
let catalog,current=null,items=[],busy=false,navToken=0;
const pending=new Map(), draftKey=id=>'agent-teacher.draft.'+id, archiveKey=id=>'agent-teacher.previous-draft.'+id;
document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();main.focus();});

function notice(text,error=false){
  message.replaceChildren();if(!text)return;
  const p=document.createElement('p');p.className=error?'alert error':'alert';p.setAttribute('role',error?'alert':'status');p.textContent=text;message.append(p);
}
function localGet(key){try{return JSON.parse(localStorage.getItem(key)||'null');}catch{return null;}}
function localSet(key,value){try{value===null?localStorage.removeItem(key):localStorage.setItem(key,JSON.stringify(value));}catch{notice('Chưa lưu được bản nháp trong trình duyệt. Hãy sao chép lời bạn viết trước khi đóng trang.',true);}}
async function api(path,body){
  const controller=new AbortController(), timeout=setTimeout(()=>controller.abort(),10000);
  try{
    const response=await fetch(path,{signal:controller.signal,cache:'no-store',...(body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{})});
    let value;try{value=await response.json();}catch{throw new Error('Máy chủ chưa trả về nội dung hợp lệ. Bản nháp vẫn được giữ.');}
    if(!response.ok){const error=new Error(value.error?.message||'Không hoàn tất được yêu cầu.');error.status=response.status;throw error;}
    return value;
  }catch(error){
    if(error.name==='AbortError')throw new Error('Yêu cầu quá thời gian chờ. Bản nháp vẫn được giữ; bạn có thể thử lại.');
    if(error instanceof TypeError)throw new Error('Chưa kết nối được máy chủ trên máy này. Bản nháp vẫn được giữ.');
    throw error;
  }finally{clearTimeout(timeout);}
}
function draw(){main.innerHTML=current?sessionView(current,localGet(draftKey(current.id)),localGet(archiveKey(current.id))):home(catalog);nav.innerHTML=sessionList(items,current?.id);}
function setBusy(value){busy=value;main.setAttribute('aria-busy',String(value));main.querySelectorAll('button').forEach(b=>{b.disabled=value;});}
async function refreshList(){try{items=(await api('/api/sessions')).items;nav.innerHTML=sessionList(items,current?.id);}catch{notice('Danh sách phiên chưa tải lại được. Hãy dùng “Tải bản đã lưu” để kiểm tra.',true);}}
async function openHash(){
  const token=++navToken,match=location.hash.match(/^#session\/([a-f0-9-]{36})$/);
  try{const result=match?await api('/api/sessions/'+match[1]):null;if(token!==navToken)return;current=result?.session||null;notice('');draw();main.focus({preventScroll:true});}
  catch(error){notice(error.message,true);}
}
function stableRequest(key,payload){
  const previous=pending.get(key),content=JSON.stringify(payload);
  if(previous?.content===content)return previous.body;
  const body={...payload,request_id:crypto.randomUUID()};pending.set(key,{content,body});return body;
}
function preserveDraft(value){
  const key=draftKey(current.id),old=localGet(key);
  if(old&&(old.phase!==current.phase||old.revision!==current.revision))localSet(archiveKey(current.id),old);
  localSet(key,value);
}
function captureDraft(){
  const form=document.querySelector('#move-form');if(!form||!current)return;
  const data=new FormData(form);preserveDraft({phase:current.phase,revision:current.revision,choice:data.get('choice')||'',text:data.get('text')||''});
}
main.addEventListener('input',captureDraft);main.addEventListener('change',captureDraft);
main.addEventListener('click',async event=>{
  const start=event.target.closest('.start-case');
  if(start&&!busy){
    setBusy(true);notice('');
    const key='agent-teacher.create.'+start.dataset.case,body=localGet(key)||{case_id:start.dataset.case,request_id:crypto.randomUUID()};localSet(key,body);
    try{const result=await api('/api/sessions',body);localSet(key,null);current=result.session;await refreshList();location.hash='session/'+current.id;draw();}
    catch(error){notice(error.message+' Thử lại cùng tình huống để tránh tạo phiên trùng.',true);}finally{setBusy(false);}
  }
  if(event.target.closest('#reload-session')&&!busy)await openHash();
  if(event.target.closest('#discard-draft')&&current){
    const d=localGet(draftKey(current.id));if(d&&(d.phase!==current.phase||d.revision!==current.revision))localSet(draftKey(current.id),null);
    localSet(archiveKey(current.id),null);draw();
  }
  if(event.target.closest('#replay-session')&&current&&!busy){
    setBusy(true);try{const r=await api('/api/sessions/'+current.id+'/replay');notice(r.matches_saved_state?'Đã đối chiếu '+r.event_count+' sự kiện; diễn biến khớp bản đã lưu.':'Diễn biến không khớp bản đã lưu. Hãy giữ bản xuất để kiểm tra.',!r.matches_saved_state);}
    catch(error){notice(error.message,true);}finally{setBusy(false);}
  }
});
main.addEventListener('submit',async event=>{
  if(event.target.id!=='move-form')return;event.preventDefault();if(busy||!current)return;
  const data=new FormData(event.target),id=current.id,payload={revision:current.revision,type:current.phase,choice:data.get('choice')||'',text:data.get('text')||''};
  preserveDraft({phase:current.phase,revision:current.revision,choice:payload.choice,text:payload.text});
  const body=stableRequest(id,payload);setBusy(true);notice('Đang lưu lựa chọn…');
  try{const result=await api('/api/sessions/'+id+'/events',body);pending.delete(id);localSet(draftKey(id),null);if(current?.id===id){current=result.session;draw();main.focus({preventScroll:true});}notice('Đã lưu lựa chọn.');await refreshList();}
  catch(error){notice(error.message+(error.status===409?' Dùng “Tải bản đã lưu” để đối chiếu trước khi gửi lại.':' Nội dung bạn viết vẫn được giữ.'),true);}finally{setBusy(false);}
});
window.addEventListener('hashchange',()=>{if(catalog)openHash();});
try{catalog=await api('/api/catalog');items=(await api('/api/sessions')).items;await openHash();}
catch(error){main.replaceChildren();const title=document.createElement('h1');title.textContent='Chưa mở được buổi luyện';const retry=document.createElement('button');retry.className='button primary';retry.textContent='Thử tải lại';retry.addEventListener('click',()=>location.reload());main.append(title,retry);notice(error.message,true);}
