const button = document.querySelector('[data-copy-brief]');
button?.addEventListener('click', async () => {
  const prompt = document.querySelector('#agent-prompt');
  const status = document.querySelector('[data-copy-status]');
  try {
    await navigator.clipboard.writeText(prompt.value);
    status.textContent = 'Prompt copied. Attach the files you want it to read.';
  } catch {
    prompt.focus();
    prompt.select();
    status.textContent = 'Text selected. Press Command+C or Ctrl+C to copy.';
  }
});
