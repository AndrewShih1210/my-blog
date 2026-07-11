import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const roots = [
  path.join(repoRoot, "linebot-course-site"),
  path.join(repoRoot, "scripts", "linebot-course-site-templates"),
];

let updated = 0;
let current = 0;

for (const root of roots) {
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith(".html")) continue;
    const filePath = path.join(root, entry.name);
    const original = fs.readFileSync(filePath, "utf8");
    if (!original.includes('<nav class="nav"')) continue;

    const english = entry.name.endsWith("_en.html");
    const label = english ? "Menu" : "選單";
    let html = original;

    if (!html.includes('class="menu-toggle"')) {
      const button = `<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="course-nav"><span>${label}</span><span class="menu-toggle-icon" aria-hidden="true"></span></button>\n      `;
      html = html.replace('<nav class="nav"', `${button}<nav id="course-nav" class="nav"`);
    }

    if (!html.includes('src="nav.js"')) {
      html = html.replace("</head>", '  <script src="nav.js" defer></script>\n</head>');
    }

    if (html !== original) {
      fs.writeFileSync(filePath, html, "utf8");
      updated += 1;
    } else {
      current += 1;
    }
  }
}

console.log(`Updated ${updated} navigation files; ${current} already current.`);
