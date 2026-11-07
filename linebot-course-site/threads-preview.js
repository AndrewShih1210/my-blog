// Load the third-party embed only after an explicit visitor action.
document.querySelectorAll('[data-threads-preview]').forEach((section) => {
  const button = section.querySelector('button');
  const status = section.querySelector('[role="status"]');
  const host = section.querySelector('[data-embed-host]');
  const english = document.documentElement.lang === 'en';
  button.addEventListener('click', () => {
    button.disabled = true;
    const quote = document.createElement('blockquote');
    quote.className = 'text-post-media';
    quote.dataset.textPostPermalink = 'https://www.threads.com/@andrewshih1210/post/DfYGB0Tk_IO';
    quote.dataset.textPostVersion = '0';
    const link = document.createElement('a');
    link.href = quote.dataset.textPostPermalink;
    link.textContent = english ? 'View the original post on Threads' : '在Threads查看原文';
    quote.append(link);
    host.append(quote);
    status.textContent = english ? 'Loading Threads. If no preview appears, use the original-post link.' : '正在載入Threads；若未顯示預覽，請使用原文連結。';
    const script = document.createElement('script');
    script.src = 'https://www.threads.com/embed.js';
    script.async = true;
    script.onerror = () => { status.textContent = english ? 'Preview unavailable. The original-post link remains available.' : '無法載入貼文預覽，仍可使用原文連結。'; };
    document.body.append(script);
  }, {once: true});
});
