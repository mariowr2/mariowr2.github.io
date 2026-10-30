document.querySelector('#copy-prompt').addEventListener('click', async () => {
  const prompt = document.querySelector('#agent-prompt');
  const status = document.querySelector('#copy-status');
  try { await navigator.clipboard.writeText(prompt.value); status.textContent = 'Copied.'; }
  catch { prompt.focus(); prompt.select(); status.textContent = 'Text selected. Press Control+C or Command+C to copy.'; }
});
