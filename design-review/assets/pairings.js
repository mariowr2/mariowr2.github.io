// Main artwork follows its visible intro; the different header scene follows reading.
(() => {
  const scene = document.querySelector('[data-pair]');
  if (!scene) return;
  const header = document.querySelector('.paired-header');
  const mainSvg = scene.querySelector('svg');
  const headerSvg = header.querySelector('svg');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const body = document.body;
  const getRoute = (svg, prefix) => {
    const path = svg.querySelector(`[data-${prefix}-route]`);
    return path ? { path, length: path.getTotalLength(), progress: svg.querySelector(`[data-${prefix}-progress]`), marker: svg.querySelector(`[data-${prefix}-marker]`) } : null;
  };
  const mainRoute = getRoute(mainSvg, 'main');
  const headerRoute = getRoute(headerSvg, 'header');
  const clamp = value => Math.max(0, Math.min(1, value));
  let introEnd = 300;
  const drawRoute = (route, value, isHeader) => {
    if (!route) return;
    const distance = route.length * value;
    const point = route.path.getPointAtLength(distance);
    route.progress?.setAttribute('stroke-dasharray', `${distance} ${route.length}`);
    if (route.marker) {
      const kind = route.marker.dataset.kind;
      let angle = 0;
      let scale = 1;
      if (kind === 'cyclist') {
        const before = route.path.getPointAtLength(Math.max(0, distance - 1));
        const after = route.path.getPointAtLength(Math.min(route.length, distance + 1));
        angle = Math.atan2(after.y - before.y, after.x - before.x) * 180 / Math.PI;
        scale = scene.dataset.pair === 'window' && !isHeader ? .47 : isHeader ? .88 : .75;
      }
      route.marker.setAttribute('transform', `translate(${point.x} ${point.y}) rotate(${angle}) scale(${scale})`);
      const phase = value * Math.PI * (isHeader ? 38 : 18);
      route.marker.querySelectorAll('[data-wheel]').forEach(wheel => {
        const x = wheel.dataset.wheel === 'rear' ? -12 : 13;
        wheel.setAttribute('transform', `rotate(${value * (isHeader ? 3100 : 1500)} ${x} -7)`);
      });
      const hikerLegs = route.marker.querySelector('[data-main-legs]');
      if (hikerLegs) {
        const stride = Math.sin(phase) * 2;
        hikerLegs.setAttribute('d', `M-2-6L${-6 + stride} 0M-2-6L${3 - stride} -1`);
      }
      const runnerLegs = route.marker.querySelector('[data-runner-legs]');
      if (runnerLegs) {
        const stride = Math.sin(phase) * 5;
        runnerLegs.setAttribute('d', `M-3-9L${-8 + stride} -3L${-13 + stride} -5M-3-9L${3 - stride} -3L${6 - stride} 1`);
      }
    }
    return point;
  };
  const drawCat = value => {
    const cat = headerSvg.querySelector('[data-header-cat]');
    if (!cat) return;
    if (cat.dataset.kind === 'walk') {
      const stride = Math.sin(value * Math.PI * 30) * 4;
      cat.setAttribute('transform', `translate(${24 + value * 116} 39)`);
      cat.querySelector('[data-cat-legs]').setAttribute('d', `M-8-1L${-10 + stride} 10M-2-1L${0 - stride} 10M10-1L${7 - stride} 10M14-1L${17 + stride} 10`);
      cat.querySelector('[data-cat-tail]').setAttribute('transform', `rotate(${Math.sin(value * 9) * 9} -12 -7)`);
    } else {
      header.dataset.awake = String(value > .22);
      const stretch = Math.sin(value * Math.PI) * .09;
      cat.querySelector('[data-cat-stretch]').setAttribute('transform', `translate(${-stretch * 15} 0) scale(${1 + stretch} 1)`);
      cat.querySelector('[data-cat-tail]').setAttribute('transform', `rotate(${Math.sin(value * 5) * 13} 52 26)`);
    }
  };
  const update = () => {
    const disabled = reduced.matches;
    const distance = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const reading = disabled ? 0 : clamp(scrollY / distance);
    const local = disabled ? 0 : clamp(scrollY / Math.max(200, introEnd - 110));
    body.classList.toggle('paired-reduced', disabled);
    body.classList.toggle('is-reading', !disabled && scrollY > introEnd - 95);
    body.dataset.mainProgress = local.toFixed(4);
    body.dataset.headerProgress = reading.toFixed(4);
    const point = drawRoute(mainRoute, local, false);
    drawRoute(headerRoute, reading, true);
    drawCat(reading);
    mainSvg.querySelectorAll('[data-parallax]').forEach(layer => {
      const back = layer.dataset.parallax === 'back';
      layer.setAttribute('transform', `translate(${local * (back ? -7 : -3)} ${local * (back ? 4 : -2)})`);
    });
    const lamp = mainSvg.querySelector('[data-lamp]');
    if (lamp && point) { lamp.setAttribute('cx', point.x); lamp.setAttribute('cy', point.y - 16); }
    const gaze = mainSvg.querySelector('[data-cat-gaze]');
    if (gaze) gaze.setAttribute('transform', `translate(${local * 2} ${-local})`);
    const tail = mainSvg.querySelector('[data-window-tail]');
    if (tail) tail.setAttribute('transform', `rotate(${Math.sin(local * Math.PI) * 4} 80 53)`);
  };
  let pending = false;
  const schedule = () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; update(); });
  };
  const measure = () => {
    introEnd = document.querySelector('.intro').getBoundingClientRect().bottom + scrollY;
    update();
  };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', measure, { passive: true });
  reduced.addEventListener('change', measure);
  document.fonts.ready.then(measure);
  addEventListener('load', measure, { once: true });
  measure();
})();
