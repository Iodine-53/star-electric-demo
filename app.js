/* STAR ELECTRIC — interactions */
(function(){
"use strict";
var $=function(s,c){return (c||document).querySelector(s)};
var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

/* ---- live Tampa clock + open chip ---- */
function tickClock(){
  try{
    var t=new Date().toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit',hour12:true});
    var parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',hour:'numeric',hour12:false}).format(new Date());
    var h=parseInt(parts,10);
    var el=$('#tampaTime'); if(el) el.textContent=t.replace(' ','')+' ET';
    var chip=$('#openChip');
    if(chip){
      var open=h>=7&&h<19;
      chip.textContent=open?'OPEN NOW':'NEXT DISPATCH 7 AM';
      chip.classList.toggle('open',open);
    }
    var mc=$('#mbarChip'); if(mc) mc.style.color=(h>=7&&h<19)?'#7ee2a0':'#e2a07e';
  }catch(e){}
}
tickClock(); setInterval(tickClock,1000);

/* ---- mobile nav ---- */
var burger=$('#burger'),mnav=$('#mnav');
if(burger) burger.addEventListener('click',function(){
  var open=mnav.classList.toggle('open');
  burger.setAttribute('aria-expanded',open?'true':'false');
});
$$('#mnav a').forEach(function(a){a.addEventListener('click',function(){mnav.classList.remove('open');burger.setAttribute('aria-expanded','false')})});

/* ---- one-shot reveals ----
   NOTE (2026-10-05 lesson): a fully clip-path-hidden element reports
   intersection ratio 0 to IntersectionObserver forever, so the wipe
   elements are observed via their unclipped parent instead. */
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){
    if(e.isIntersecting){
      var t=e.target._wipe||e.target;
      t.classList.add('in'); io.unobserve(e.target);
    }
  });
},{threshold:.12});
$$('.blur-in').forEach(function(el){io.observe(el)});
$$('.wipe-in').forEach(function(el){ el.parentElement._wipe=el; io.observe(el.parentElement); });

/* ---- FAQ ---- */
$$('.faq-item').forEach(function(item){
  var q=$('.faq-q',item),a=$('.faq-a',item);
  q.addEventListener('click',function(){
    var open=item.classList.toggle('open');
    q.setAttribute('aria-expanded',open?'true':'false');
    a.style.maxHeight=open?a.scrollHeight+'px':'0px';
  });
});

/* ---- LOAD CHECK ---- */
var chips=$$('.lc-chips .chip[data-amps]'),panels=$$('.panelpick'),
    fill=$('#lcFill'),cap=$('#lcCap'),readout=$('#lcReadout'),
    verdict=$('#lcVerdict'),lcCta=$('#lcCta');
var panelAmps=100;
function lcUpdate(){
  var sum=0;
  chips.forEach(function(c){ if(c.classList.contains('on')) sum+=parseInt(c.dataset.amps,10); });
  var pct=Math.min(100,Math.round(sum/panelAmps*100));
  fill.style.width=pct+'%';
  fill.classList.toggle('over',sum>panelAmps*0.8&&sum>0);
  cap.style.left='80%';
  if(sum===0){
    readout.textContent='Tap your appliances above — most Clearwater homes land between 90A and 150A.';
    verdict.hidden=true; lcCta.hidden=true; return;
  }
  readout.textContent='Your selected load ≈ '+sum+'A against a '+panelAmps+'A panel. (Electricians size to 80% of the panel — that is the white line.)';
  verdict.hidden=false; lcCta.hidden=false;
  if(sum>panelAmps*0.8){
    verdict.className='lc-verdict bad';
    verdict.textContent='OVER THE LINE. '+sum+'A of load on a '+panelAmps+'A panel — that is exactly why the breaker trips. A 200A service change ends it.';
  }else{
    verdict.className='lc-verdict good';
    verdict.textContent='ROOM TO SPARE — for now. '+sum+'A fits today, but add an EV charger and the math flips. Worth a free look before you buy the car.';
  }
}
chips.forEach(function(c){c.addEventListener('click',function(){
  c.classList.toggle('on'); c.setAttribute('aria-pressed',c.classList.contains('on')?'true':'false'); lcUpdate();
})});
panels.forEach(function(p){p.addEventListener('click',function(){
  panels.forEach(function(q){q.classList.remove('on');q.setAttribute('aria-pressed','false')});
  p.classList.add('on'); p.setAttribute('aria-pressed','true');
  panelAmps=parseInt(p.dataset.panel,10); lcUpdate();
})});
if(lcCta) lcCta.addEventListener('click',function(){
  var s=$('#sService');
  if(s){ for(var i=0;i<s.options.length;i++){ if(s.options[i].text.indexOf('Panel upgrade')===0){ s.selectedIndex=i; break; } } }
});

/* ---- 4-STEP ESTIMATE STEPPER ---- */
var stepper=$('#stepper');
if(stepper){
  var cur=1, picks={};
  var pFill=$('#pFill'),stepCount=$('#stepCount'),back=$('#stepBack'),next=$('#stepNext'),err=$('#stepErr');
  function show(n){
    cur=n;
    $$('.step',stepper).forEach(function(s){s.classList.toggle('on',parseInt(s.dataset.step,10)===n)});
    pFill.style.width=(Math.min(n,4)/4*100)+'%';
    stepCount.textContent=n<=4?('STEP '+n+' OF 4'):'READY TO SEND';
    back.hidden=(n===1||n===5); next.hidden=(n===5);
    next.textContent=(n===4)?'See my summary →':'Continue →';
    err.hidden=true;
  }
  function fail(msg){ err.textContent=msg; err.hidden=false; }
  $$('.pick',stepper).forEach(function(p){p.addEventListener('click',function(){
    var grp=p.parentElement;
    $$('.pick',grp).forEach(function(q){q.classList.remove('on')});
    p.classList.add('on');
    picks[grp.getAttribute('aria-label')]=p.dataset.v;
    err.hidden=true;
  })});
  back.addEventListener('click',function(){show(Math.max(1,cur-1))});
  next.addEventListener('click',function(){
    if(cur===1){
      var s=$('#sService');
      if(!s.value){fail('Pick a service first — it takes two seconds.');s.focus();return;}
      picks.service=s.options[s.selectedIndex].text;
    }
    if(cur===2){
      var z=$('#sZip').value.trim();
      if(!/^\d{5}$/.test(z)){fail('Enter your 5-digit ZIP so we route you to the right day.');$('#sZip').focus();return;}
      picks.zip=z;
    }
    if(cur===3&&!picks['Home size']){fail('Tap your home size — it changes the price.');return;}
    if(cur===4&&!picks['Callback time']){fail('Pick a callback time and we will call exactly then.');return;}
    if(cur===4){
      $('#doneSummary').textContent=picks.service+' · ZIP '+picks.zip+' · '+picks['Home size']+' · call '+picks['Callback time']+'.';
      var body=encodeURIComponent('Hi Star Electric,\n\nService: '+picks.service+'\nZIP: '+picks.zip+'\nHome size: '+picks['Home size']+'\nCall me: '+picks['Callback time']+'\n\nThanks!');
      $('#mailtoBtn').href='mailto:jerry@starelectricservices.com?subject='+encodeURIComponent('Estimate request — '+picks.service)+'&body='+body;
    }
    show(cur+1);
    if(cur<=4) $('.step[data-step="'+cur+'"]',stepper).scrollIntoView({block:'nearest',behavior:'smooth'});
  });
  show(1);
}

/* ---- sticky mobile bar: after hero, hide at final CTA ---- */
var mbar=$('#mbar'),hero=$('#hero'),book=$('#book');
function barCheck(){
  if(!mbar||window.innerWidth>640) return;
  var pastHero=window.scrollY>(hero?hero.offsetHeight:600);
  var r=book?book.getBoundingClientRect():null;
  var atFinal=r&&r.top<window.innerHeight*0.6;
  mbar.classList.toggle('show',pastHero&&!atFinal);
}
window.addEventListener('scroll',barCheck,{passive:true});
window.addEventListener('resize',barCheck);
barCheck();
})();
