// A small indication of effort, rather than a trip played out in the margins.
(() => {
  const scene = document.querySelector('[data-quiet]');
  if (!scene) return;
  const body = document.body;
  const header = document.querySelector('.paired-header');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const scenes = [scene.querySelector('svg'), header.querySelector('svg')];
  const routes = scenes.map(svg => {
    const path = svg.querySelector('[data-quiet-route]');
    return path ? { path, length: path.getTotalLength(), cue: svg.querySelector('[data-quiet-cue]') } : null;
  });
  let introEnd = 300;
  const clamp = value => Math.max(0, Math.min(1,value));
  const draw = (value, index) => {
    const svg = scenes[index];
    const route = routes[index];
    if (route) {
      const maximum = index === 0 ? 16 : 12;
      const distance = route.length * .3 + Math.min(maximum, route.length * .3) * value;
      const point = route.path.getPointAtLength(distance);
      route.cue.setAttribute('transform', `translate(${point.x} ${point.y})`);
      const stone = route.cue.querySelector('[data-quiet-stone]');
      if (stone) stone.setAttribute('transform', `rotate(${-value * 32} ${index === 0 ? '9 -7' : '0 -4'})`);
    }
    svg.querySelectorAll('[data-quiet-level]').forEach(stone => {
      const level = Number(stone.dataset.quietLevel);
      const emphasis = clamp(value * 1.8 - level * .35);
      stone.style.opacity = String(.36 + emphasis * .42);
    });
  };
  const update = () => {
    const disabled = reduced.matches;
    const reading = disabled ? 0 : clamp(scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight));
    const local = disabled ? 0 : clamp(scrollY / Math.max(200,introEnd-110));
    body.classList.toggle('paired-reduced',disabled);
    body.classList.toggle('is-reading',!disabled && scrollY > introEnd - 95);
    body.dataset.quietMainProgress = local.toFixed(4);
    body.dataset.quietHeaderProgress = reading.toFixed(4);
    draw(local,0);draw(reading,1);
  };
  let pending=false;
  const schedule=()=>{
    if(pending)return;
    pending=true;
    requestAnimationFrame(()=>{pending=false;update();});
  };
  const measure=()=>{introEnd=document.querySelector('.intro').getBoundingClientRect().bottom+scrollY;update();};
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',measure,{passive:true});
  reduced.addEventListener('change',measure);
  document.fonts.ready.then(measure);
  addEventListener('load',measure,{once:true});
  measure();
})();
