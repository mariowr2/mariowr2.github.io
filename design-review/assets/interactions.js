// Optional enhancement: every article remains a normal HTML link without JS.
document.querySelectorAll('[data-filter-group]').forEach(group => {
  const scope = document.querySelector('[data-filter-items]');
  const items = [...scope.querySelectorAll('[data-topics]')];
  group.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
    group.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    const topic = button.dataset.topic;
    items.forEach(item => { item.hidden = topic !== 'all' && !item.dataset.topics.split(' ').includes(topic); });
    document.querySelector('[data-filter-count]').textContent = `${items.filter(i => !i.hidden).length} published entries`;
  }));
});
