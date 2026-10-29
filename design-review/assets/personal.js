const cat = document.querySelector('[data-cat]');
if (cat) {
  const button = cat.querySelector('[data-cat-toggle]');
  button.addEventListener('click', () => {
    const awake = cat.dataset.awake !== 'true';
    cat.dataset.awake = String(awake);
    button.setAttribute('aria-pressed', String(awake));
    button.textContent = awake ? 'Let the cat sleep' : 'Wake the cat';
    cat.querySelector('title').textContent = awake ? 'A cat awake beside a window looking onto mountains' : 'A cat napping beside a window looking onto mountains';
    cat.classList.remove('is-waking');
    if (awake) { void cat.offsetWidth; cat.classList.add('is-waking'); }
  });
  cat.addEventListener('pointermove', event => {
    if (cat.dataset.awake !== 'true' || event.pointerType === 'touch') return;
    const box = cat.getBoundingClientRect();
    cat.style.setProperty('--gaze-x', `${Math.max(-2, Math.min(2, (event.clientX - box.left - box.width / 2) / 40))}px`);
    cat.style.setProperty('--gaze-y', `${Math.max(-1.5, Math.min(1.5, (event.clientY - box.top - box.height / 2) / 50))}px`);
  });
  cat.addEventListener('pointerleave', () => {
    cat.style.setProperty('--gaze-x', '0px');
    cat.style.setProperty('--gaze-y', '0px');
  });
}
const route = document.querySelector('[data-route]');
if (route) {
  const path = route.querySelector('#scenic-path');
  const marker = route.querySelector('.rider-marker');
  const travelled = route.querySelector('.route-travelled');
  const input = route.querySelector('input');
  const length = path.getTotalLength();
  const update = () => {
    const distance = length * Number(input.value) / 100;
    const point = path.getPointAtLength(distance);
    const ahead = path.getPointAtLength(Math.min(length, distance + 1));
    const behind = path.getPointAtLength(Math.max(0, distance - 1));
    const angle = Math.atan2(ahead.y - behind.y, ahead.x - behind.x) * 180 / Math.PI;
    marker.setAttribute('transform', `translate(${point.x} ${point.y}) rotate(${angle})`);
    travelled.setAttribute('stroke-dasharray', `${distance} ${length}`);
  };
  input.addEventListener('input', update);
  update();
}
const summit = document.querySelector('[data-summit]');
if (summit) {
  const path = summit.querySelector('#summit-path');
  const marker = summit.querySelector('.hiker-marker');
  const travelled = summit.querySelector('.summit-travelled');
  const button = summit.querySelector('[data-summit-step]');
  const status = summit.querySelector('[data-summit-status]');
  const length = path.getTotalLength();
  const stages = ['At the trailhead', 'Finding a rhythm', 'A little further', 'Still going', 'Near the top', 'At the summit'];
  const update = () => {
    const distance = length * Number(summit.dataset.step) / 5;
    const point = path.getPointAtLength(distance);
    marker.setAttribute('transform', `translate(${point.x} ${point.y})`);
    travelled.setAttribute('stroke-dasharray', `${distance} ${length}`);
    status.textContent = stages[Number(summit.dataset.step)];
    button.textContent = Number(summit.dataset.step) === 5 ? 'Back to the trailhead' : 'Take another step';
  };
  button.addEventListener('click', () => { summit.dataset.step = (Number(summit.dataset.step) + 1) % 6; update(); });
  update();
}
