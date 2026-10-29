// Decorative SVG only. Normal scrolling, keyboard navigation, and links stay native.
(() => {
  const body = document.body;
  const mode = ['bike', 'summit', 'trail'].find(name => body.classList.contains(`scroll-${name}`));
  if (!mode || !document.querySelector('[data-scroll-mountain]')) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const ns = 'http://www.w3.org/2000/svg';
  const make = (name, attrs = {}) => {
    const element = document.createElementNS(ns, name);
    Object.entries(attrs).forEach(([key, value]) => element.setAttribute(key, value));
    return element;
  };
  const mountain = document.querySelector('[data-scroll-mountain]');
  const mountainSvg = mountain?.querySelector('svg');
  const mountainCopies = mountainSvg ? [mountainSvg] : [];
  // The selected mountain scene remains a static illustration in the other options.
  mountainCopies.forEach(svg => svg.querySelector('.summit-travelled').setAttribute('stroke-dasharray', `0 ${svg.querySelector('.summit-route').getTotalLength()}`));
  let rail, svg, path, active, marker, wheels = [], routeLength = 1;
  let introBottom = 0, trailTop = 0, trailHeight = 1;
  if (mode === 'summit' && mountainSvg) {
    const holder = document.createElement('div');
    holder.className = 'header-summit';
    holder.setAttribute('aria-hidden', 'true');
    const miniature = mountainSvg.cloneNode(true);
    miniature.querySelector('title')?.remove();
    miniature.removeAttribute('aria-labelledby');
    miniature.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
    holder.append(miniature);
    document.querySelector('.site-head').append(holder);
    mountainCopies.push(miniature);
  } else {
    rail = document.createElement('div');
    rail.className = `scroll-rail${mode === 'trail' ? ' scroll-trail-rail' : ''}`;
    rail.setAttribute('aria-hidden', 'true');
    svg = make('svg', { 'aria-hidden': 'true' });
    path = make('path', { class: 'scroll-track' });
    active = make('path', { class: 'scroll-track-active' });
    svg.append(path, active);
    marker = make('g', { class: mode === 'bike' ? 'scroll-bike-art' : 'trail-runner' });
    if (mode === 'bike') {
      marker.innerHTML = '<circle cx="-12" cy="-7" r="8"/><circle cx="13" cy="-7" r="8"/><g class="wheel-spokes"><path d="M-20-7H-4M-12-15V1"/></g><g class="wheel-spokes"><path d="M5-7H21M13-15V1"/></g><path d="M-12-7L-3-22L2-7ZM-3-22H8L13-7M2-7L8-22L6-26H13M-7-24H1M-1-32L-6-24L4-19L1-8M-1-32L9-28L10-24" fill="none"/><circle cx="3" cy="-38" r="3"/><path d="M-1-40Q3-45 7-39" fill="none"/>';
      wheels = [...marker.querySelectorAll('.wheel-spokes')];
    } else {
      marker.innerHTML = '<circle cx="0" cy="-13" r="2.3"/><path d="M0-9L-2-3L-7 1M-2-3L4 1M0-8L4-5L7-8M0-8L-4-7L-6-3"/>';
    }
    svg.append(marker);
    rail.append(svg);
    body.prepend(rail);
  }
  const progress = () => {
    const distance = document.documentElement.scrollHeight - innerHeight;
    return distance > 0 ? Math.max(0, Math.min(1, scrollY / distance)) : 0;
  };
  const drawMountain = value => mountainCopies.forEach(scene => {
    const route = scene.querySelector('.summit-route');
    const length = route.getTotalLength();
    const point = route.getPointAtLength(length * value);
    scene.querySelector('.hiker-marker').setAttribute('transform', `translate(${point.x} ${point.y})`);
    scene.querySelector('.summit-travelled').setAttribute('stroke-dasharray', `${length * value} ${length}`);
  });
  const update = () => {
    if (reduced.matches) {
      body.classList.add('motion-reduced');
      body.classList.remove('has-left-intro');
      drawMountain(0);
      return;
    }
    body.classList.remove('motion-reduced');
    const value = progress();
    body.dataset.scrollProgress = value.toFixed(4);
    if (mode === 'summit') {
      drawMountain(value);
      body.classList.toggle('has-left-intro', scrollY > introBottom - 95);
    } else {
      const fraction = mode === 'trail' ? Math.max(0, Math.min(1, (scrollY + innerHeight * .43 - trailTop) / trailHeight)) : value;
      const distance = routeLength * fraction;
      const point = path.getPointAtLength(distance);
      marker.setAttribute('transform', mode === 'bike' ? `translate(${point.x} ${point.y}) rotate(80) scale(${innerWidth <= 760 ? .4 : .72})` : `translate(${point.x} ${point.y}) scale(${innerWidth <= 760 ? .65 : .9})`);
      active.setAttribute('stroke-dasharray', `${distance} ${routeLength}`);
      if (mode === 'bike') {
        const rotation = value * 2400;
        wheels[0].setAttribute('transform', `rotate(${rotation} -12 -7)`);
        wheels[1].setAttribute('transform', `rotate(${rotation} 13 -7)`);
      }
    }
  };
  const measure = () => {
    introBottom = document.querySelector('.intro')?.getBoundingClientRect().bottom + scrollY || 0;
    if (rail) {
      if (mode === 'bike') {
        const box = rail.getBoundingClientRect();
        svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
        const x = box.width / 2 - (innerWidth <= 760 ? 6 : 10);
        path.setAttribute('d', `M${x} 35C${x + 4} ${box.height * .3} ${x - 4} ${box.height * .7} ${x} ${box.height - 35}`);
      } else {
        trailTop = document.querySelector('.columns').getBoundingClientRect().top + scrollY;
        const end = document.querySelector('.foot').getBoundingClientRect().top + scrollY - 18;
        trailHeight = Math.max(100, end - trailTop);
        rail.style.top = `${trailTop}px`;
        rail.style.height = `${trailHeight}px`;
        const width = rail.getBoundingClientRect().width;
        svg.setAttribute('viewBox', `0 0 ${width} ${trailHeight}`);
        const x = width / 2;
        let d = `M${x} 8`;
        const steps = Math.ceil(trailHeight / 140);
        for (let i = 0; i < steps; i++) {
          const y = Math.min(trailHeight - 8, (i + 1) * trailHeight / steps);
          const previous = i * trailHeight / steps;
          const offset = i % 2 ? -8 : 8;
          d += `C${x + offset} ${previous + 35} ${x - offset} ${y - 35} ${x} ${y}`;
        }
        path.setAttribute('d', d);
        svg.querySelectorAll('.trail-waypoint').forEach(dot => dot.remove());
        document.querySelectorAll('.post').forEach(post => {
          const y = post.getBoundingClientRect().top + scrollY - trailTop + 14;
          const waypoint = make('circle', { class: 'trail-waypoint', cx: x, cy: y, r: 2.5 });
          svg.insertBefore(waypoint, marker);
        });
      }
      active.setAttribute('d', path.getAttribute('d'));
      routeLength = path.getTotalLength();
    }
    update();
  };
  let pending = false;
  const schedule = () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; update(); });
  };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', measure, { passive: true });
  reduced.addEventListener('change', measure);
  document.fonts.ready.then(measure);
  addEventListener('load', measure, { once: true });
  measure();
})();
