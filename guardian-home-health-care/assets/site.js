'use strict';
(() => {
  const header=document.querySelector('.site-header');
  const toggle=document.querySelector('.menu-toggle');
  const nav=document.getElementById('main-nav');
  const closeNav=()=>{nav?.classList.remove('open');toggle?.setAttribute('aria-expanded','false');};
  toggle?.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});
  document.querySelectorAll('.nav-group>button').forEach(button=>button.addEventListener('click',()=>{const open=button.parentElement.classList.toggle('open');button.setAttribute('aria-expanded',String(open));}));
  document.addEventListener('click',event=>{if(!event.target.closest('.nav-group')) document.querySelectorAll('.nav-group.open').forEach(group=>{group.classList.remove('open');group.querySelector('button').setAttribute('aria-expanded','false');});if(!event.target.closest('.site-header'))closeNav();});
  nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeNav));
  window.addEventListener('resize',()=>{if(window.innerWidth>950)closeNav();},{passive:true});
  window.addEventListener('scroll',()=>header?.classList.toggle('scrolled',window.scrollY>20),{passive:true});
  let currentModal=null,previousFocus=null;
  const focusables=modal=>Array.from(modal.querySelectorAll('button,a[href],input:not([type=hidden]),select,textarea,[tabindex="0"]')).filter(el=>el.offsetParent!==null&&!el.disabled);
  const markSeen=()=>{try{sessionStorage.setItem('guardian-care-popup','seen');}catch{}};
  function openModal(modal){if(!modal)return;if(currentModal)closeModal();previousFocus=document.activeElement;modal.hidden=false;document.body.classList.add('locked');currentModal=modal;closeNav();focusables(modal)[0]?.focus();if(modal.id==='care-modal')markSeen();}
  function closeModal(){if(!currentModal)return;currentModal.hidden=true;document.body.classList.remove('locked');currentModal=null;previousFocus?.focus();}
  document.querySelectorAll('[data-open-care]').forEach(btn=>btn.addEventListener('click',()=>openModal(document.getElementById('care-modal'))));
  document.querySelectorAll('.modal').forEach(modal=>{modal.addEventListener('click',event=>{if(event.target===modal||event.target.closest('[data-close-modal]'))closeModal();});});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'){closeModal();closeNav();document.querySelectorAll('.nav-group.open').forEach(group=>{group.classList.remove('open');group.querySelector('button').setAttribute('aria-expanded','false');});}if(event.key==='Tab'&&currentModal){const items=focusables(currentModal);const first=items[0],last=items[items.length-1];if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}}});
  document.querySelectorAll('[data-gallery]').forEach(btn=>btn.addEventListener('click',()=>{const box=document.getElementById('photo-modal');if(!box)return;const source=btn.querySelector('img');box.querySelector('img').src=source.src;box.querySelector('img').alt=source.alt;box.querySelector('figcaption').textContent=btn.querySelector('span')?.textContent||source.alt;openModal(box);}));
  let interaction=false;document.querySelectorAll('.care-form input,.care-form select,.care-form textarea').forEach(field=>field.addEventListener('focus',()=>{interaction=true;markSeen();},{once:true}));
  if(document.body.dataset.popup==='true')window.addEventListener('scroll',()=>{let seen=false;try{seen=sessionStorage.getItem('guardian-care-popup')==='seen';}catch{seen=interaction;}const range=document.documentElement.scrollHeight-window.innerHeight;if(!seen&&!interaction&&!currentModal&&range>0&&window.scrollY/range>.48)openModal(document.getElementById('care-modal'));},{passive:true});
  const PHONE='(321) 977-3169';
  const started=Date.now();
  document.querySelectorAll('.care-form').forEach(form=>{form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(form.dataset.sending==='true')return;
    if(!form.reportValidity())return;
    const message=form.querySelector('.form-message');const button=form.querySelector('button[type="submit"]');const original=button.innerHTML;
    form.dataset.sending='true';button.disabled=true;button.textContent='Sending...';message.textContent='';message.className='form-message';
    const controller=new AbortController();const timer=window.setTimeout(()=>controller.abort(),25000);
    try{
      const elapsed=form.querySelector('input[name="elapsed"]');if(elapsed)elapsed.value=String(Math.round((Date.now()-started)/1000));
      const data=new FormData(form);data.set('action','cw_form_submit');
      const response=await fetch(form.getAttribute('action')||'send-form.php',{method:'POST',body:data,headers:{Accept:'application/json'},credentials:'same-origin',signal:controller.signal});
      let result=null;try{result=JSON.parse(await response.text());}catch{result=null;}
      if(!result)throw new Error('We could not send your request right now. Please call '+PHONE+'.');
      if(!response.ok||!result.success)throw new Error(result.data?.message||'We could not send your request right now. Please call '+PHONE+'.');
      form.reset();markSeen();interaction=true;
      message.textContent=result.data?.message||'Thank you! Your request has been sent successfully.';message.classList.add('success');
    }catch(error){
      message.textContent=error.name==='AbortError'?'Your request timed out. Please call '+PHONE+' before sending again.':error instanceof TypeError?'We could not connect. Please check your internet connection, try again or call '+PHONE+'.':error.message||'Something went wrong. Please try again.';
      message.classList.add('error');
    }finally{window.clearTimeout(timer);form.dataset.sending='false';button.disabled=false;button.innerHTML=original;}
  });});
  /* Hero "Find Care" box: carry the city/ZIP into the contact form. */
  try{const city=new URLSearchParams(window.location.search).get('city');const cityField=document.getElementById('contact-care-city');if(city&&cityField){cityField.value=city.trim().slice(0,80);document.getElementById('contact-care-name')?.focus({preventScroll:true});}}catch{}
  if('IntersectionObserver' in window&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){document.documentElement.classList.add('js-motion');const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));}
})();
