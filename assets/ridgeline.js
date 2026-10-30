// A short on-screen scroll window, rather than progress through a long ascent.
(() => {
  const scene = document.querySelector('[data-mountain]');
  if (!scene) return;
  const body = document.body;
  const header = document.querySelector('.paired-header');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const graphics = [scene.querySelector('svg'), header.querySelector('svg')];
  const mode = scene.dataset.mountain;
  const clamp = value => Math.max(0,Math.min(1,value));
  let start=0, range=80, handoff=150;
  const draw=(svg,p,small)=>{
    const scale = small ? .45 : 1;
    const back=svg.querySelector('[data-mountain-layer=back]');
    const front=svg.querySelector('[data-mountain-layer=front]');
    if(mode==='contour'){
      back.setAttribute('transform',`translate(${-p*4*scale} ${p*scale})`);
      front.setAttribute('transform',`translate(${p*4*scale} ${-p*2*scale})`);
    }else{
      back.setAttribute('transform',`translate(${-p*2*scale} ${p*scale})`);
      front.setAttribute('transform',`translate(${p*scale} ${-p*4*scale})`);
    }
    front.style.opacity=String(.72+p*.18);
  };
  const update=()=>{
    const disabled=reduced.matches;
    const local=disabled?0:clamp((scrollY-start)/range);
    const reading=disabled?0:clamp(scrollY/Math.max(1,document.documentElement.scrollHeight-innerHeight));
    body.classList.toggle('paired-reduced',disabled);
    body.classList.toggle('is-reading',!disabled && scrollY>=handoff);
    body.dataset.mountainMainProgress=local.toFixed(4);
    body.dataset.mountainHeaderProgress=reading.toFixed(4);
    draw(graphics[0],local,false);draw(graphics[1],reading,true);
  };
  let pending=false;
  const schedule=()=>{
    if(pending)return;
    pending=true;
    requestAnimationFrame(()=>{pending=false;update();});
  };
  const measure=()=>{
    const rect=scene.getBoundingClientRect();
    const sceneTop=rect.top+scrollY;
    const sceneBottom=sceneTop+rect.height;
    const headerHeight=document.querySelector('.site-head').getBoundingClientRect().height;
    start=Math.max(0,sceneBottom+24-innerHeight);
    const visibleRoom=Math.max(48,sceneTop-headerHeight-15-start);
    range=Math.min(96,visibleRoom);
    handoff=Math.max(start+range,sceneBottom-headerHeight-6);
    body.dataset.mountainStart=String(start);
    body.dataset.mountainRange=String(range);
    update();
  };
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',measure,{passive:true});
  reduced.addEventListener('change',measure);
  document.fonts.ready.then(measure);
  addEventListener('load',measure,{once:true});
  measure();
})();
