import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const descriptions = {
  "index.html": "施育廷學術網站，整理生成式 AI 與 AI 教育應用研究、雙語教材、LINE Bot 實作課程、演講紀錄及專業證明，呈現國立臺中教育大學相關教學與研究實務。",
  "index_en.html": "Yu-Ting Shih's academic website presents research, bilingual course materials, LINE Bot projects, talks, and professional records in generative AI, AI education, educational technology, and learning analytics at NTCU.",
  "author-works/index.html": "施育廷第一作者與獨立作者著作專區，收錄生成式 AI、AI 教育應用、教育科技與學習分析研究，並提供代表專利、研究圖表及 APA 格式著作清單。",
  "author-works/index_en.html": "Explore Yu-Ting Shih's first-author and sole-author works in generative AI, AI education, educational technology, and learning analytics, with a representative patent, research visuals, and an APA bibliography.",
  "ai-course-site/index.html": "施育廷製作的雙語生成式 AI 教材，透過概念說明、教學案例、實作活動與專題任務，引導教師及學習者將 AI 工具融入教學、研究與工作流程。",
  "ai-course-site/index_en.html": "A bilingual generative AI course site by Yu-Ting Shih, offering concepts, teaching cases, hands-on activities, and projects for integrating AI tools into education, research, and professional workflows.",
  "certificates-site/index.html": "施育廷專業成果與證明專區，分類整理證照、研習紀錄、論文發表、獲獎、演講、聘書、感謝狀、專利及其他學術文件，提供教學與研究經歷查閱。",
  "certificates-site/index_en.html": "Yu-Ting Shih's professional record archive, organized by certifications, training, conference presentations, awards, talks, appointments, appreciation letters, patents, and academic documents.",
  "linebot-course-site/index.html": "施育廷製作的 LINE Bot 實作教材，依序說明 LINE Messaging API、Google Apps Script、Google Sheets、Webhook 與 Gemini 的建置及整合流程。",
  "linebot-course-site/index_en.html": "A bilingual LINE Bot course by Yu-Ting Shih covering LINE Messaging API, Google Apps Script, Google Sheets, webhooks, Gemini integration, and practical automation workflows.",
  "sitemap.html": "施育廷學術網站導覽，集中連結研究成果、APA 著作清單、生成式 AI 教材、LINE Bot 課程、演講、證照與中英文頁面。",
  "sitemap_en.html": "A complete guide to Yu-Ting Shih's academic website, linking research outputs, APA publications, generative AI materials, LINE Bot courses, talks, credentials, and bilingual pages.",

  "01-探討學習者對AI教育應用之科技認知與態度、整合性科技接受度及使用意願之分析/index.html": "探討學習者對 AI 教育應用的科技認知、態度、整合性科技接受度與使用意願，分析影響 AI 教育工具採用及教學策略設計的重要因素。",
  "01-探討學習者對AI教育應用之科技認知與態度、整合性科技接受度及使用意願之分析/index_en.html": "This study examines learners' technological cognition, attitudes, integrated technology acceptance, and intention to use AI educational applications, identifying factors relevant to adoption and teaching design.",
  "02-AI-輔助程式設計與數據分析學習中的人機互動行為分析/index.html": "分析非資訊背景大學生使用 AI 輔助程式設計與數據分析時的人機互動行為，呈現生成式 AI 在問題解決、學習支持與能力培養上的應用。",
  "02-AI-輔助程式設計與數據分析學習中的人機互動行為分析/index_en.html": "This study analyzes human-AI interaction among non-computing majors using AI support for programming and data analysis, with attention to problem solving, learning support, and skill development.",
  "03-Enhancing-learning-outcomes-and-reducing-anxiety-in-programming-courses-through-AI-integration/index.html": "探討程式設計課程導入 AI 輔助對學習成效與學習焦慮的影響，說明生成式 AI 如何支援非資訊背景學生理解程式概念與完成任務。",
  "03-Enhancing-learning-outcomes-and-reducing-anxiety-in-programming-courses-through-AI-integration/index_en.html": "This study evaluates whether AI integration in programming courses can improve learning outcomes and reduce anxiety, particularly for students without a computing background.",
  "04-From-Traditional-Semantic-Analysis-to-Generative-AI-Research-on-Cybersecurity-and-Privacy-Challenges-in-Cloud-Based-Educational-Task-Automation/index.html": "探討雲端教育任務自動化從傳統語意分析走向生成式 AI 時的資安與隱私挑戰，涵蓋對話代理人、資料處理、系統部署及風險管理。",
  "04-From-Traditional-Semantic-Analysis-to-Generative-AI-Research-on-Cybersecurity-and-Privacy-Challenges-in-Cloud-Based-Educational-Task-Automation/index_en.html": "This research examines cybersecurity and privacy challenges as cloud-based educational task automation moves from traditional semantic analysis to generative AI and conversational agents.",
  "05-優化學習工作流輕量級無伺服器AI代理人之開發與成效分析/index.html": "介紹用於優化學習工作流的輕量級無伺服器 AI 代理人，分析其系統設計、任務自動化流程與實施成效，呈現低維護部署的教育應用價值。",
  "05-優化學習工作流輕量級無伺服器AI代理人之開發與成效分析/index_en.html": "This study develops and evaluates a lightweight serverless AI agent for learning workflows, examining system design, task automation, implementation outcomes, and low-maintenance deployment.",
  "06-優化教學場域與學習效率之輕量級無伺服器AI代理人應用/index.html": "探討輕量級無伺服器 AI 代理人在教學場域的應用，整理資訊查詢、內容生成、紀錄與通知等工作流程，並分析其對教學及學習效率的影響。",
  "06-優化教學場域與學習效率之輕量級無伺服器AI代理人應用/index_en.html": "This research applies a lightweight serverless AI agent to teaching contexts, integrating information retrieval, content generation, records, and notifications to improve teaching and learning efficiency.",
  "07-探討-GenAI人機協作評量之信度與差異分析/index.html": "探討生成式 AI 與教師進行人機協作評量時的評分信度、差異與一致性，分析 AI 評分標準、偏誤及校準在教育評量實務中的應用。",
  "07-探討-GenAI人機協作評量之信度與差異分析/index_en.html": "This study investigates reliability, differences, and agreement in GenAI human-machine collaborative assessment, with attention to scoring criteria, bias, calibration, and educational use.",
  "08-數位閱讀策略工具「英語閱讀小舵手」對學生英語閱讀素養影響之準實驗研究企劃/index.html": "提出生成式 AI 數位閱讀策略工具「英語閱讀小舵手」的準實驗研究企劃，評估策略引導對大學生英語閱讀素養與學習表現的影響。",
  "08-數位閱讀策略工具「英語閱讀小舵手」對學生英語閱讀素養影響之準實驗研究企劃/index_en.html": "This quasi-experimental research proposal evaluates how the generative AI reading strategy tool English Reading Helmsman may influence university students' English reading literacy and performance.",
  "09-從心盲到心流-運算思維在生成式AI互動中的認知補償與效益/index.html": "探討運算思維在生成式 AI 互動中對心盲症使用者的認知補償與學習效益，分析提示設計、人機協作及 Vibe Coding 經驗。",
  "09-從心盲到心流-運算思維在生成式AI互動中的認知補償與效益/index_en.html": "This study explores how computational thinking may provide cognitive compensation for users with aphantasia during generative AI interaction, prompt design, collaboration, and Vibe Coding.",
  "10-生成式AI自動評分與回饋系統之滿意度與需求分析/index.html": "分析大學生使用生成式 AI 自動評分與回饋系統的滿意度、接受情形及功能需求，檢視其在降低教師負擔與提供個人化學習指引上的價值。",
  "10-生成式AI自動評分與回饋系統之滿意度與需求分析/index_en.html": "This study analyzes student satisfaction, acceptance, and needs regarding a generative AI automated grading and feedback system designed to support personalized learning and reduce teacher workload.",
  "11-生成式AI於資料科學課程的導入時長效應-比較不同介入週數對非資訊背景大學生學習成效之影響/index.html": "比較生成式 AI 在資料科學課程中不同介入週數的學習成效，分析導入時長對非資訊背景大學生知識理解、任務表現與學習支持的影響。",
  "11-生成式AI於資料科學課程的導入時長效應-比較不同介入週數對非資訊背景大學生學習成效之影響/index_en.html": "This study compares different durations of generative AI intervention in a data science course and evaluates effects on knowledge, task performance, and learning support for non-computing majors.",
  "12-生成式AI於霸凌情境模擬多重虛擬學生進行正向反思活動/index.html": "運用生成式 AI 模擬霸凌情境中的多重虛擬學生，設計正向反思活動，探討情境互動、觀點轉換、同理理解與社會情緒學習的教育應用。",
  "12-生成式AI於霸凌情境模擬多重虛擬學生進行正向反思活動/index_en.html": "This study uses generative AI to simulate multiple virtual students in bullying scenarios, supporting positive reflection, perspective taking, and social-emotional learning activities.",
  "13-運用智慧對話系統於心理與社會情緒評量之應用/index.html": "探討智慧對話系統在心理與社會情緒評量中的應用，分析互動式篩檢、回應紀錄與初步支持如何補充傳統靜態量表、學生求助流程及有限輔導人力。",
  "13-運用智慧對話系統於心理與社會情緒評量之應用/index_en.html": "This study examines intelligent dialogue systems for psychological and social-emotional assessment, including interactive screening, response records, and preliminary support alongside traditional scales.",
};

function escapeAttribute(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function replaceMeta(html, selector, content) {
  const escaped = escapeAttribute(content);
  const pattern = new RegExp(`(<meta\\s+${selector}\\s+content=")[^"]*("\\s*\\/?>)`, "i");
  return pattern.test(html) ? html.replace(pattern, `$1${escaped}$2`) : html;
}

let updated = 0;
let unchanged = 0;
const validation = [];
for (const [relativePath, description] of Object.entries(descriptions)) {
  const filePath = path.join(repoRoot, ...relativePath.split("/"));
  if (!fs.existsSync(filePath)) {
    throw new Error(`Missing target: ${relativePath}`);
  }

  const original = fs.readFileSync(filePath, "utf8");
  if (!/<meta\s+name="description"\s+content="[^"]*"\s*\/?>/i.test(original)) {
    throw new Error(`Missing meta description: ${relativePath}`);
  }
  if (!/<meta\s+property="og:description"\s+content="[^"]*"\s*\/?>/i.test(original)) {
    throw new Error(`Missing Open Graph description: ${relativePath}`);
  }

  let html = replaceMeta(original, 'name="description"', description);
  html = replaceMeta(html, 'property="og:description"', description);
  html = replaceMeta(html, 'name="twitter:description"', description);

  if (html !== original) {
    fs.writeFileSync(filePath, html, "utf8");
    updated += 1;
  } else {
    unchanged += 1;
  }

  const current = fs.readFileSync(filePath, "utf8");
  const meta = current.match(/<meta\s+name="description"\s+content="([^"]*)"\s*\/?>/i)?.[1];
  const og = current.match(/<meta\s+property="og:description"\s+content="([^"]*)"\s*\/?>/i)?.[1];
  const metaCount = [...current.matchAll(/<meta\s+name="description"\s+content="[^"]*"\s*\/?>/gi)].length;
  const ogCount = [...current.matchAll(/<meta\s+property="og:description"\s+content="[^"]*"\s*\/?>/gi)].length;
  const suspicious = metaCount !== 1 || ogCount !== 1 || !meta || meta !== escapeAttribute(description) || og !== meta || /…|\.\.\.|(?:[\u3400-\u9fff]\s+){4,}/u.test(meta);
  validation.push({ relativePath, length: meta?.length ?? 0, suspicious });
}

const issues = validation.filter((item) => item.suspicious || item.length < 60 || item.length > 240);
console.log(`Updated ${updated} HTML files; ${unchanged} already current.`);
console.log(`Validated ${validation.length} descriptions; ${issues.length} issues.`);
if (issues.length) {
  for (const issue of issues) console.error(`${issue.relativePath}: length=${issue.length}, suspicious=${issue.suspicious}`);
  process.exitCode = 1;
}
