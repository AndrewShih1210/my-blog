(function () {
  const sourceItems = Array.isArray(window.CERTIFICATE_ITEMS) ? window.CERTIFICATE_ITEMS : [];
  const lang = document.documentElement.lang === "en" ? "en" : "zh";
  const root = document.getElementById("credential-list");
  const search = document.getElementById("credential-search");
  const filters = document.getElementById("credential-filters");
  const summary = document.getElementById("credential-summary");

  const text = {
    zh: {
      all: "全部",
      google: "Google 證照與技能",
      professional: "專業證照",
      name: "證照或證明名稱",
      issuer: "發照單位",
      date: "發照或取得日期",
      evidence: "證書影像",
      open: "查看",
      noDate: "證書未載明",
      noResult: "沒有符合條件的證照。",
      total: "清單項目",
      dated: "可辨識日期",
      issuers: "發照單位",
      types: {
        formal: "專業認證",
        course: "課程完成證明",
        attendance: "研習參與證明",
        aggregate: "彙整紀錄",
      },
    },
    en: {
      all: "All",
      google: "Google credentials",
      professional: "Professional certifications",
      name: "Credential or record",
      issuer: "Issuing organization",
      date: "Issue or completion date",
      evidence: "Evidence",
      open: "View",
      noDate: "Not shown on the certificate",
      noResult: "No credential matches the current filters.",
      total: "List entries",
      dated: "Entries with dates",
      issuers: "Issuing organizations",
      types: {
        formal: "Professional credential",
        course: "Course certificate",
        attendance: "Attendance record",
        aggregate: "Aggregate record",
      },
    },
  }[lang];

  const formalIds = new Set([
    "cert-001", "cert-002", "cert-010",
    "cert-091", "cert-092", "cert-093", "cert-094", "cert-095", "cert-096",
  ]);
  const attendanceIds = new Set(["cert-006"]);
  const aggregateIds = new Set(["cert-009", "cert-011", "cert-015"]);

  const items = sourceItems
    .filter((item) => item.categoryKey === "google" || item.categoryKey === "license")
    .map((item) => ({
      ...item,
      credentialType: formalIds.has(item.id)
        ? "formal"
        : attendanceIds.has(item.id)
          ? "attendance"
          : aggregateIds.has(item.id)
            ? "aggregate"
            : "course",
    }));

  let active = "all";

  function localized(item, key) {
    return item[`${key}${lang === "en" ? "En" : "Zh"}`]
      || item[`${key}${lang === "en" ? "Zh" : "En"}`]
      || "";
  }

  function renderSummary() {
    const dated = items.filter((item) => item.issuedDate).length;
    const issuers = new Set(items.map((item) => localized(item, "issuer")).filter(Boolean)).size;
    summary.innerHTML = `
      <article class="summary-card"><strong>${items.length}</strong><span>${text.total}</span></article>
      <article class="summary-card"><strong>${dated}</strong><span>${text.dated}</span></article>
      <article class="summary-card"><strong>${issuers}</strong><span>${text.issuers}</span></article>
    `;
  }

  function renderFilters() {
    const options = [
      ["all", text.all],
      ["google", text.google],
      ["license", text.professional],
    ];
    filters.innerHTML = options.map(([key, label]) => `
      <button class="filter-btn${active === key ? " active" : ""}" type="button" data-filter="${key}">${label}</button>
    `).join("");
  }

  function filteredItems() {
    const query = search.value.trim().toLocaleLowerCase();
    return items
      .filter((item) => active === "all" || item.categoryKey === active)
      .filter((item) => {
        if (!query) return true;
        return [
          localized(item, "title"),
          localized(item, "issuer"),
          item.issuedDate || "",
          text.types[item.credentialType],
        ].join(" ").toLocaleLowerCase().includes(query);
      })
      .sort((a, b) => {
        const dateA = (a.issuedDate || "0000").slice(0, 10);
        const dateB = (b.issuedDate || "0000").slice(0, 10);
        return dateB.localeCompare(dateA) || a.sort - b.sort;
      });
  }

  function renderTable() {
    const visible = filteredItems();
    if (!visible.length) {
      root.innerHTML = `<p class="empty">${text.noResult}</p>`;
      return;
    }

    const rows = visible.map((item) => {
      const note = localized(item, "issuedDateNote");
      return `
        <tr>
          <td><a href="${item.image}" target="_blank" rel="noreferrer"><img class="credential-thumb" src="${item.image}" alt="${localized(item, "title")}" loading="lazy"></a></td>
          <td class="credential-name">${localized(item, "title")}<span class="credential-note">${text.types[item.credentialType]}</span></td>
          <td>${localized(item, "issuer")}</td>
          <td class="date-cell">${item.issuedDate || text.noDate}${note ? `<span class="credential-note">${note}</span>` : ""}</td>
          <td><a class="button" href="${item.image}" target="_blank" rel="noreferrer">${text.open}</a></td>
        </tr>
      `;
    }).join("");

    root.innerHTML = `
      <div class="credential-table-wrap">
        <table class="credential-table">
          <thead><tr><th>${text.evidence}</th><th>${text.name}</th><th>${text.issuer}</th><th>${text.date}</th><th></th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;
  }

  filters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    active = button.dataset.filter;
    renderFilters();
    renderTable();
  });
  search.addEventListener("input", renderTable);

  renderSummary();
  renderFilters();
  renderTable();
})();
