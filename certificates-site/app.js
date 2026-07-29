(function () {
  const items = Array.isArray(window.CERTIFICATE_ITEMS) ? window.CERTIFICATE_ITEMS : [];
  const pageLang = document.documentElement.lang === "en" ? "en" : "zh";

  const i18n = {
    zh: {
      total: "公開項目",
      categories: "分類數",
      years: "可辨識年份",
      featured: "代表類群",
      all: "全部",
      open: "開啟預覽",
      browse: "開啟原圖",
      issuer: "頒發或主辦單位",
      noItems: "目前沒有符合此篩選條件的項目。",
      yearLabel: "年份",
      descriptionLabel: "說明",
    },
    en: {
      total: "Public-facing items",
      categories: "Categories",
      years: "Identifiable years",
      featured: "Featured group",
      all: "All",
      open: "Open preview",
      browse: "Open image",
      issuer: "Issuing or hosting body",
      noItems: "No items match this filter.",
      yearLabel: "Year",
      descriptionLabel: "Description",
    },
  }[pageLang];

  const categoryInfo = {
    google: {
      zh: "Google 技能與認證",
      en: "Google Credentials and Skills",
      groupZh: "國際技能認證",
      groupEn: "Global Skills Credentials",
      descZh: "與 Google、Google Cloud、Gemini 及教育應用數位能力相關的完成證明與技能認證。",
      descEn: "Credentials and completion records related to Google, Google Cloud, Gemini, and educator-facing digital skills.",
    },
    license: {
      zh: "專業證照",
      en: "Professional Certifications",
      groupZh: "專業能力",
      groupEn: "Professional Capability",
      descZh: "涵蓋資料庫、程式設計、架構框架與教育科技等面向的專業證照。",
      descEn: "Professional certifications covering databases, programming, architecture frameworks, and educational technology.",
    },
    training: {
      zh: "研習與工作坊",
      en: "Training and Workshop Records",
      groupZh: "持續專業成長",
      groupEn: "Continuous Professional Learning",
      descZh: "與 AI、數位學習、EMI 與教學創新相關的研習、論壇及工作坊紀錄。",
      descEn: "Records of workshops, forums, and training events related to AI, digital learning, EMI, and teaching innovation.",
    },
    lecture: {
      zh: "演講與教學分享",
      en: "Lectures and Teaching Talks",
      groupZh: "公開演講",
      groupEn: "Public Lectures",
      descZh: "校園、教師社群與公開分享場合的演講、教學示範與應用推廣紀錄。",
      descEn: "Lecture, workshop-sharing, and teaching demonstration records delivered in schools, educator communities, and public events.",
    },
    presentation: {
      zh: "論文發表與學術成果",
      en: "Presentations and Scholarly Outputs",
      groupZh: "研究與發表",
      groupEn: "Research and Dissemination",
      descZh: "論文發表、參與證明、獲獎紀錄與期刊相關的學術成果證明。",
      descEn: "Presentation records, participation certificates, awards, and journal-related evidence.",
    },
    appointment: {
      zh: "聘書與教學服務",
      en: "Appointment Letters and Teaching Service",
      groupZh: "教學服務",
      groupEn: "Teaching Service",
      descZh: "與授課、支援課程及教學服務相關的聘任與服務證明。",
      descEn: "Appointment letters and service records related to teaching and course support.",
    },
    appreciation: {
      zh: "感謝狀與推廣肯定",
      en: "Appreciation and Outreach Recognition",
      groupZh: "社群參與",
      groupEn: "Community Engagement",
      descZh: "因演講、推廣與教學貢獻所獲得的感謝狀與肯定紀錄。",
      descEn: "Letters of appreciation received for talks, outreach, and instructional contributions.",
    },
    patent: {
      zh: "專利與智慧財產",
      en: "Patent and Intellectual Property",
      groupZh: "代表成果",
      groupEn: "Featured Output",
      descZh: "專利登錄與代表性創新成果的正式證明。",
      descEn: "Formal evidence of patent registration and featured innovation output.",
    },
    status: {
      zh: "學術身分證明",
      en: "Academic Status Documentation",
      groupZh: "學術里程碑",
      groupEn: "Academic Milestones",
      descZh: "用於證明學術身分與博士階段進程的正式文件。",
      descEn: "Formal documents that verify academic status and doctoral-stage milestones.",
    },
  };

  function cleanText(value) {
    if (typeof value !== "string") return "";
    return value
      .replace(/[\uE000-\uF8FF]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function textFor(item, field) {
    const primaryKey = pageLang === "en" ? `${field}En` : `${field}Zh`;
    const secondaryKey = pageLang === "en" ? `${field}Zh` : `${field}En`;
    const primary = item[primaryKey];
    const secondary = item[secondaryKey];
    return cleanText(primary) || cleanText(secondary) || "-";
  }

  function categoryLabel(key) {
    const info = categoryInfo[key] || categoryInfo.status;
    return pageLang === "en" ? info.en : info.zh;
  }

  function categoryGroup(key) {
    const info = categoryInfo[key] || categoryInfo.status;
    return pageLang === "en" ? info.groupEn : info.groupZh;
  }

  function categoryDescription(key) {
    const info = categoryInfo[key] || categoryInfo.status;
    return pageLang === "en" ? info.descEn : info.descZh;
  }

  const byId = (id) => document.getElementById(id);
  const statsRoot = byId("stats");
  const filterRoot = byId("filters");
  const galleryRoot = byId("gallery");
  const modal = byId("modal");
  const modalTitle = byId("modal-title");
  const modalMeta = byId("modal-meta");
  const modalImg = byId("modal-image");
  const modalLink = byId("modal-link");
  const modalDesc = byId("modal-description");
  const modalClose = byId("modal-close");

  const categoryOrder = ["google", "license", "training", "lecture", "presentation", "appreciation", "appointment", "patent", "status"];
  const categories = [...new Map(items.map((item) => [item.categoryKey, item])).values()]
    .sort((a, b) => {
      const indexA = categoryOrder.indexOf(a.categoryKey);
      const indexB = categoryOrder.indexOf(b.categoryKey);
      const safeA = indexA === -1 ? Number.MAX_SAFE_INTEGER : indexA;
      const safeB = indexB === -1 ? Number.MAX_SAFE_INTEGER : indexB;
      return safeA - safeB;
    });

  let activeCategory = "all";

  function createStat(number, label) {
    const card = document.createElement("article");
    card.className = "stat";
    card.innerHTML = `<div class="num">${number}</div><p>${label}</p>`;
    return card;
  }

  function renderStats() {
    const yearCount = new Set(items.map((item) => item.year).filter(Boolean)).size;
    statsRoot.innerHTML = "";
    statsRoot.append(
      createStat(items.length, i18n.total),
      createStat(categories.length, i18n.categories),
      createStat(yearCount, i18n.years),
      createStat(categoryGroup(categories[0]?.categoryKey || "status"), i18n.featured)
    );
  }

  function renderFilters() {
    filterRoot.innerHTML = "";

    const allBtn = document.createElement("button");
    allBtn.className = "filter-btn active";
    allBtn.type = "button";
    allBtn.textContent = i18n.all;
    allBtn.dataset.filter = "all";
    filterRoot.appendChild(allBtn);

    categories.forEach((category) => {
      const btn = document.createElement("button");
      btn.className = "filter-btn";
      btn.type = "button";
      btn.dataset.filter = category.categoryKey;
      btn.textContent = categoryLabel(category.categoryKey);
      filterRoot.appendChild(btn);
    });

    filterRoot.addEventListener("click", (event) => {
      const button = event.target.closest(".filter-btn");
      if (!button) return;
      activeCategory = button.dataset.filter;
      [...filterRoot.querySelectorAll(".filter-btn")].forEach((el) => {
        el.classList.toggle("active", el === button);
      });
      renderGallery();
    });
  }

  function openModal(item) {
    modalTitle.textContent = textFor(item, "title");
    modalMeta.innerHTML = `
      <p><strong>${i18n.issuer}:</strong> ${textFor(item, "issuer")}</p>
      <p><strong>${i18n.yearLabel}:</strong> ${item.year || "-"}</p>
    `;
    modalDesc.innerHTML = `<p><strong>${i18n.descriptionLabel}:</strong> ${categoryDescription(item.categoryKey)}</p>`;
    modalImg.src = item.image;
    modalImg.alt = textFor(item, "title");
    modalLink.href = item.image;
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }

  function closeModal() {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
  }

  function renderGallery() {
    const current = activeCategory === "all"
      ? items
      : items.filter((item) => item.categoryKey === activeCategory);

    const ordered = [...current].sort((a, b) => {
      const yearA = Number.parseInt(a.year || "0", 10) || 0;
      const yearB = Number.parseInt(b.year || "0", 10) || 0;
      if (yearA !== yearB) return yearB - yearA;
      return (b.sort || 0) - (a.sort || 0);
    });

    galleryRoot.innerHTML = "";
    if (!ordered.length) {
      galleryRoot.innerHTML = `<div class="empty">${i18n.noItems}</div>`;
      return;
    }

    ordered.forEach((item) => {
      const card = document.createElement("article");
      card.className = "card";
      card.innerHTML = `
        <a class="thumb" href="${item.image}" target="_blank" rel="noreferrer">
          <img src="${item.image}" alt="${textFor(item, "title")}" loading="lazy" />
        </a>
        <div class="card-body">
          <div class="chip-row" style="margin-bottom:10px;">
            <span class="tag">${categoryLabel(item.categoryKey)}</span>
            ${item.year ? `<span class="chip">${item.year}</span>` : ""}
          </div>
          <h3>${textFor(item, "title")}</h3>
          <p class="meta">${textFor(item, "issuer")}</p>
          <p class="muted">${categoryDescription(item.categoryKey)}</p>
          <div class="button-row">
            <button class="button primary preview-btn" type="button">${i18n.open}</button>
            <a class="button" href="${item.image}" target="_blank" rel="noreferrer">${i18n.browse}</a>
          </div>
        </div>
      `;
      card.querySelector(".preview-btn").addEventListener("click", () => openModal(item));
      galleryRoot.appendChild(card);
    });
  }

  modalClose.addEventListener("click", closeModal);
  modal.addEventListener("click", (event) => {
    if (event.target === modal) closeModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeModal();
  });

  renderStats();
  renderFilters();
  renderGallery();
})();
