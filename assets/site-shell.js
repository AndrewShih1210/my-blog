document.querySelectorAll('.unified-header').forEach((header) => {
  const menus = [...header.querySelectorAll('details')];
  const close = () => menus.forEach(menu => { menu.open = false; });
  header.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('click', event => { if (!header.contains(event.target)) close(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      const active = menus.find(menu => menu.open);
      close();
      if (active) active.querySelector('summary').focus();
    }
  });
  window.matchMedia('(max-width:1180px)').addEventListener('change', close);
});
