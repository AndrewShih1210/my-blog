"use strict";

const NS = "http://www.w3.org/2000/svg";
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
const uid = () => `layer-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;

const els = {
  stage: $("#stage"),
  stageFrame: $("#stageFrame"),
  canvasViewport: $("#canvasViewport"),
  projectTitle: $("#projectTitle"),
  projectDuration: $("#projectDuration"),
  durationDisplay: $("#durationDisplay"),
  timecode: $("#timecode"),
  playhead: $("#playhead"),
  rulerTrack: $("#rulerTrack"),
  trackArea: $("#trackArea"),
  layerList: $("#layerList"),
  saveState: $("#saveState"),
  toast: $("#toast"),
  exportDialog: $("#exportDialog"),
  helpDialog: $("#helpDialog"),
  recordProgress: $("#recordProgress"),
  recordStatus: $("#recordStatus"),
  recordPercent: $("#recordPercent"),
  recordCanvas: $("#recordCanvas")
};

let browserVoices = [];
let speechStopRequested = false;

const state = {
  projectTitle: "水循環教學動畫",
  template: "water",
  aspect: "16:9",
  duration: 12,
  background: "#ffffff",
  selectedId: "cloud",
  currentTime: 6.2,
  playing: false,
  recording: false,
  cancelRecording: false,
  zoom: 1,
  layers: [],
  history: [],
  animationFrame: null,
  playStartedAt: 0,
  playStartTime: 0,
  narration: {
    text: "水循環包含蒸發、降水與匯集。太陽加熱水面形成水蒸氣，水氣凝結成雲，最後以雨水回到地表。",
    voice: "",
    rate: 0,
    audioUrl: "",
    subtitleUrl: "",
    duration: 0
  }
};

const templateFactories = {
  water() {
    return {
      title: "水循環教學動畫",
      duration: 12,
      background: "#ffffff",
      layers: [
        { id: "title", name: "標題", kind: "text", text: "水循環的過程", x: 640, y: 72, color: "#163865", size: 42, scale: 1, opacity: 1, start: 0, duration: 1.8, animation: "slide-up", easing: "ease-out" },
        { id: "cloud", name: "雲朵", kind: "cloud", x: 500, y: 172, color: "#4c92e8", scale: 1, opacity: 1, start: 1.2, duration: 2.4, animation: "slide-right", easing: "ease-in-out" },
        { id: "rain", name: "雨滴", kind: "rain", x: 880, y: 245, color: "#348be1", scale: 1, opacity: 1, start: 4.4, duration: 2.2, animation: "slide-up", easing: "ease-out" },
        { id: "labels", name: "說明文字", kind: "labels", text: "蒸發　降水　匯集", x: 0, y: 0, color: "#163865", scale: 1, opacity: 1, start: 1.1, duration: 8.5, animation: "fade", easing: "ease-in-out" }
      ]
    };
  },
  intro() {
    return {
      title: "課程片頭動畫",
      duration: 8,
      background: "#102754",
      layers: [
        { id: "intro-ring", name: "動態圓環", kind: "rings", x: 640, y: 360, color: "#32d0c5", scale: 1, opacity: .75, start: 0, duration: 6.5, animation: "pop", easing: "spring" },
        { id: "intro-title", name: "課程標題", kind: "text", text: "生成式 AI 教學設計", x: 640, y: 330, color: "#ffffff", size: 56, scale: 1, opacity: 1, start: .5, duration: 2.1, animation: "slide-up", easing: "ease-out" },
        { id: "intro-subtitle", name: "單元資訊", kind: "text", text: "從概念到教室實踐", x: 640, y: 405, color: "#b9d8ff", size: 27, scale: 1, opacity: 1, start: 1.2, duration: 2, animation: "fade", easing: "ease-in-out" },
        { id: "intro-line", name: "裝飾線", kind: "line", x: 640, y: 370, color: "#32d0c5", scale: 1, opacity: 1, start: .9, duration: 2.4, animation: "slide-right", easing: "ease-out" }
      ]
    };
  },
  steps() {
    return {
      title: "三步驟解說動畫",
      duration: 12,
      background: "#f6f9ff",
      layers: [
        { id: "steps-title", name: "標題", kind: "text", text: "三步驟完成學習任務", x: 640, y: 120, color: "#17355f", size: 48, scale: 1, opacity: 1, start: 0, duration: 1.7, animation: "slide-up", easing: "ease-out" },
        { id: "step-1", name: "步驟一", kind: "step", text: "理解概念", number: "1", x: 290, y: 360, color: "#1463df", scale: 1, opacity: 1, start: 1.1, duration: 2, animation: "pop", easing: "spring" },
        { id: "step-2", name: "步驟二", kind: "step", text: "動手練習", number: "2", x: 640, y: 360, color: "#0ab9ad", scale: 1, opacity: 1, start: 3.1, duration: 2, animation: "pop", easing: "spring" },
        { id: "step-3", name: "步驟三", kind: "step", text: "反思應用", number: "3", x: 990, y: 360, color: "#f09a2d", scale: 1, opacity: 1, start: 5.1, duration: 2, animation: "pop", easing: "spring" }
      ]
    };
  },
  outro() {
    return {
      title: "影片片尾動畫",
      duration: 8,
      background: "#eefbfa",
      layers: [
        { id: "outro-shape", name: "外框", kind: "outro-shape", x: 640, y: 330, color: "#0ab9ad", scale: 1, opacity: 1, start: 0, duration: 5.8, animation: "float", easing: "ease-in-out" },
        { id: "outro-title", name: "結束標題", kind: "text", text: "謝謝觀看", x: 640, y: 328, color: "#17355f", size: 65, scale: 1, opacity: 1, start: .4, duration: 2.1, animation: "pop", easing: "spring" },
        { id: "outro-subtitle", name: "提醒文字", kind: "text", text: "別忘了整理今天的學習重點", x: 640, y: 420, color: "#477086", size: 26, scale: 1, opacity: 1, start: 1.4, duration: 2.2, animation: "fade", easing: "ease-in-out" },
        { id: "outro-credit", name: "署名", kind: "text", text: "教學設計｜您的名字", x: 640, y: 560, color: "#2e6670", size: 20, scale: 1, opacity: 1, start: 2.1, duration: 2, animation: "slide-up", easing: "ease-out" }
      ]
    };
  }
};

function svgEl(name, attrs = {}, text = "") {
  const node = document.createElementNS(NS, name);
  Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
  if (text) node.textContent = text;
  return node;
}

function setGroupMeta(group, layer) {
  group.dataset.layerId = layer.id;
  group.setAttribute("role", "button");
  group.setAttribute("aria-label", `選取${layer.name}圖層`);
  group.addEventListener("click", event => {
    event.stopPropagation();
    selectLayer(layer.id);
  });
  return group;
}

function createLayerGraphic(layer) {
  const g = setGroupMeta(svgEl("g"), layer);
  g.dataset.baseX = layer.x;
  g.dataset.baseY = layer.y;

  if (layer.kind === "text") {
    const text = svgEl("text", {
      x: 0, y: 0, fill: layer.color, "text-anchor": "middle",
      "font-size": layer.size || 42, "font-weight": layer.size > 45 ? 750 : 650,
      "font-family": "'Microsoft JhengHei', 'Noto Sans TC', sans-serif"
    }, layer.text);
    g.append(text);
  } else if (layer.kind === "cloud") {
    g.append(
      svgEl("path", { d: "M-112 42C-143 42-160 22-154-4c5-23 26-37 49-34 9-31 37-52 70-52 39 0 70 28 74 66 30-5 59 18 59 50 0 9-2 16-6 23H-112Z", fill: "#f9fcff", stroke: layer.color, "stroke-width": 5, "stroke-linejoin": "round" }),
      svgEl("path", { d: "M-115 74C-40 106 41 101 116 62", class: "motion-path" }),
      svgEl("path", { d: "m105 54 19 5-14 14", fill: "none", stroke: "#80a4d8", "stroke-width": 4 })
    );
  } else if (layer.kind === "rain") {
    g.append(svgEl("path", { d: "M-58-46c-24 0-38-15-34-35 4-16 19-27 36-25 7-22 27-36 51-36 28 0 50 20 53 47 22-4 43 13 43 36 0 5-1 10-3 13H-58Z", fill: "#6785a5", stroke: "#29496c", "stroke-width": 4 }));
    [-55, -20, 15, 50].forEach((x, i) => g.append(svgEl("path", { d: `M${x} 2q-20 30-4 39c18 2 21-17 4-39Z`, fill: i % 2 ? "#348be1" : "#5aa9ef" })));
  } else if (layer.kind === "labels") {
    g.append(
      svgEl("text", { x: 300, y: 405, fill: layer.color, "font-size": 31, "font-weight": 700 }, "蒸發"),
      svgEl("text", { x: 927, y: 317, fill: layer.color, "font-size": 31, "font-weight": 700 }, "降水"),
      svgEl("text", { x: 620, y: 643, fill: layer.color, "font-size": 31, "font-weight": 700 }, "匯集")
    );
  } else if (layer.kind === "rings") {
    g.append(
      svgEl("circle", { cx: 0, cy: 0, r: 245, fill: "none", stroke: layer.color, "stroke-width": 3, opacity: .45 }),
      svgEl("circle", { cx: 0, cy: 0, r: 180, fill: "none", stroke: "#4c8fe9", "stroke-width": 2, opacity: .45 }),
      svgEl("circle", { cx: 0, cy: 0, r: 105, fill: "#173b72", opacity: .5 })
    );
  } else if (layer.kind === "line") {
    g.append(svgEl("rect", { x: -105, y: -3, width: 210, height: 6, rx: 3, fill: layer.color }));
  } else if (layer.kind === "step") {
    g.append(
      svgEl("circle", { cx: 0, cy: -30, r: 78, fill: layer.color }),
      svgEl("circle", { cx: 0, cy: -30, r: 61, fill: "none", stroke: "white", "stroke-width": 2, opacity: .4 }),
      svgEl("text", { x: 0, y: -7, fill: "white", "text-anchor": "middle", "font-size": 58, "font-weight": 750 }, layer.number),
      svgEl("text", { x: 0, y: 100, fill: "#17355f", "text-anchor": "middle", "font-size": 30, "font-weight": 700 }, layer.text)
    );
  } else if (layer.kind === "outro-shape") {
    g.append(
      svgEl("rect", { x: -270, y: -105, width: 540, height: 210, rx: 34, fill: "none", stroke: layer.color, "stroke-width": 4, transform: "rotate(-3)" }),
      svgEl("circle", { cx: -280, cy: -135, r: 8, fill: "#1463df" }),
      svgEl("circle", { cx: 290, cy: 130, r: 12, fill: "#ffb13b" })
    );
  } else if (layer.kind === "shape") {
    if (layer.shape === "circle") g.append(svgEl("circle", { cx: 0, cy: 0, r: 65, fill: layer.color }));
    if (layer.shape === "square") g.append(svgEl("rect", { x: -65, y: -65, width: 130, height: 130, rx: 10, fill: layer.color }));
    if (layer.shape === "triangle") g.append(svgEl("path", { d: "M0-75 78 65H-78Z", fill: layer.color }));
    if (layer.shape === "arrow") g.append(svgEl("path", { d: "M-90-24H28v-42l68 66-68 66V24H-90Z", fill: layer.color }));
  } else if (layer.kind === "icon") {
    const label = { idea: "💡", question: "？", check: "✓", book: "▤" }[layer.icon] || "✓";
    g.append(
      svgEl("circle", { cx: 0, cy: 0, r: 62, fill: layer.color }),
      svgEl("text", { x: 0, y: 23, fill: "white", "text-anchor": "middle", "font-size": 64, "font-weight": 750 }, label)
    );
  } else if (layer.kind === "iconify") {
    const icon = svgEl("svg", {
      x: -72, y: -72, width: 144, height: 144,
      viewBox: layer.viewBox || "0 0 24 24",
      color: layer.color, fill: "currentColor",
      "aria-label": layer.iconName || layer.name
    });
    icon.innerHTML = layer.iconSvg || "";
    g.append(icon);
  }
  return g;
}

function renderBackground() {
  const bg = svgEl("rect", { id: "stageBackground", x: 0, y: 0, width: 1280, height: 720, fill: state.background });
  els.stage.append(bg);
  if (state.template === "water") {
    const defs = svgEl("defs");
    const lakeGradient = svgEl("linearGradient", { id: "lakeGradient", x1: "0", y1: "0", x2: "0", y2: "1" });
    lakeGradient.append(
      svgEl("stop", { offset: "0", "stop-color": "#72c8f6" }),
      svgEl("stop", { offset: "1", "stop-color": "#49abea" })
    );
    const riverGradient = svgEl("linearGradient", { id: "riverGradient", x1: "0", y1: "0", x2: "1", y2: "1" });
    riverGradient.append(
      svgEl("stop", { offset: "0", "stop-color": "#87d8ff" }),
      svgEl("stop", { offset: "1", "stop-color": "#3d9ff0" })
    );
    defs.append(lakeGradient, riverGradient);

    const landscape = svgEl("g", { "aria-hidden": "true" });
    const sun = svgEl("g");
    sun.append(svgEl("circle", { cx: 160, cy: 154, r: 42, fill: "#ffc138" }));
    [
      [160, 92, 160, 68], [160, 216, 160, 240], [98, 154, 74, 154], [222, 154, 246, 154],
      [116, 110, 99, 93], [204, 110, 221, 93], [116, 198, 99, 215], [204, 198, 221, 215]
    ].forEach(points => sun.append(svgEl("path", {
      d: `M${points[0]} ${points[1]}L${points[2]} ${points[3]}`,
      stroke: "#ffb100", "stroke-width": 5, "stroke-linecap": "round"
    })));

    const lake = svgEl("path", {
      d: "M0 556C116 546 235 562 344 554c87-7 151-5 220 7 54 10 81 42 74 78-6 30-27 57-62 81H0Z",
      fill: "url(#lakeGradient)"
    });
    const bankShadow = svgEl("path", {
      d: "M474 567c58-35 111-40 164-32 68 10 94-9 139-35 73-43 156-58 246-39 46 10 88 33 141 48 31 9 57 17 75 33-4 17-21 24-49 24-47 0-77 4-112 22-32 17-48 34-91 33-86-2-125-7-202 12-70 17-121 17-170-2-44-17-91-26-143-23Z",
      fill: "#94602f"
    });
    const island = svgEl("path", {
      d: "M470 550c61-37 114-42 170-33 66 11 93-7 138-35 72-44 155-60 246-39 45 10 88 34 140 49 33 9 61 19 78 36-13 15-36 20-69 19-51-2-79 3-116 21-32 16-47 33-90 32-83-2-123-8-196 10-68 17-117 17-165-1-45-18-88-27-138-25-15-8-15-17 2-27Z",
      fill: "#8cc969", stroke: "#4b8a42", "stroke-width": 3, "stroke-linejoin": "round"
    });

    const mountains = svgEl("g");
    mountains.append(
      svgEl("path", { d: "M565 528 718 352 846 528Z", fill: "#55ad6b", stroke: "#277b50", "stroke-width": 3, "stroke-linejoin": "round" }),
      svgEl("path", { d: "M666 528 810 266 965 528Z", fill: "#4da665", stroke: "#277b50", "stroke-width": 3, "stroke-linejoin": "round" }),
      svgEl("path", { d: "M829 528 951 328 1095 528Z", fill: "#62b977", stroke: "#277b50", "stroke-width": 3, "stroke-linejoin": "round" }),
      svgEl("path", { d: "m753 370 57-104 42 71 21-27 44 75-31-12-25 26-25-30-25 20-25-28Z", fill: "#f5f8fb" }),
      svgEl("path", { d: "m908 398 43-70 31 51 17-15 30 51-24-8-18 20-19-21-21 16-18-18Z", fill: "#f4f8fc" }),
      svgEl("path", { d: "M718 352 756 430 690 493", fill: "none", stroke: "#398d5a", "stroke-width": 3, opacity: ".8" }),
      svgEl("path", { d: "M951 328 1001 423 945 496", fill: "none", stroke: "#3a915d", "stroke-width": 3, opacity: ".75" })
    );

    const river = svgEl("path", {
      d: "M842 326c-30 45 29 51-18 89-39 31 16 43-39 76-55 34-11 58-81 83-57 21-72 42-106 77-17 18-42 42-78 69h166c25-31 46-59 79-76 76-38 82-74 68-100-16-30 69-47 52-86-15-34 38-63 12-91-14-16-5-28 7-44Z",
      fill: "url(#riverGradient)", stroke: "#176ec9", "stroke-width": 4, "stroke-linejoin": "round"
    });
    const riverHighlight = svgEl("path", {
      d: "M862 360c3 22-22 35-16 53 7 18 30 25 3 47-19 16-54 22-43 48 10 23-30 40-64 53-39 15-65 50-87 79",
      fill: "none", stroke: "#a9e7ff", "stroke-width": 5, "stroke-linecap": "round", opacity: ".75"
    });

    function tree(x, y, scale = 1, color = "#2f9951") {
      const treeGroup = svgEl("g", { transform: `translate(${x} ${y}) scale(${scale})` });
      treeGroup.append(
        svgEl("rect", { x: -4, y: 12, width: 8, height: 27, rx: 3, fill: "#76502b" }),
        svgEl("path", { d: "M0-35C-20-26-22-2-12 13c7 10 18 10 25 0 11-16 7-40-13-48Z", fill: color, stroke: "#237443", "stroke-width": 2 })
      );
      return treeGroup;
    }
    [
      [545, 523, .75, "#45a45d"], [574, 512, .95, "#31964d"], [608, 518, .72, "#52ad63"],
      [649, 500, 1.08, "#2f9650"], [690, 520, .76, "#3da358"], [732, 504, .88, "#2d9550"],
      [927, 504, .72, "#3ba158"], [968, 493, 1.04, "#2d914c"], [1010, 505, .86, "#43a65c"],
      [1053, 492, 1.08, "#318f4d"], [1093, 505, .82, "#3aa157"], [1132, 497, .95, "#329950"]
    ].forEach(values => landscape.append(tree(...values)));
    landscape.append(
      svgEl("path", { d: "M0 556H485c42 5 75 27 94 59 13 23 16 55 7 105H0Z", fill: "url(#lakeGradient)" }),
      svgEl("path", { d: "M230 568c90-30 150-91 231-127M247 564l-22-3 12-18", fill: "none", stroke: "#1463df", "stroke-width": 5, "stroke-linecap": "round" }),
      svgEl("path", { d: "M1001 335c75 60 83 145 41 210m-8-7 7 22 18-14", fill: "none", stroke: "#1463df", "stroke-width": 5, "stroke-linecap": "round" }),
      svgEl("path", { d: "M500 660c84 35 184 22 250-19m-6-9 18 2-8 16", fill: "none", stroke: "#1463df", "stroke-width": 5, "stroke-linecap": "round" })
    );

    els.stage.append(defs, sun, lake, bankShadow, island, mountains, river, riverHighlight, landscape);
    [
      [76, 602, 24], [126, 631, 22], [181, 588, 28], [252, 655, 24], [322, 606, 30], [386, 676, 26]
    ].forEach(([x, y, width], i) => els.stage.append(svgEl("path", {
      d: `M${x} ${y}q${width / 2} -10 ${width} 0t${width} 0`,
      fill: "none", stroke: i % 2 ? "#2b9fe4" : "#168bd6", "stroke-width": 3, "stroke-linecap": "round", opacity: ".78"
    })));
  }
}

function renderStage() {
  els.stage.innerHTML = "";
  renderBackground();
  state.layers.forEach(layer => els.stage.append(createLayerGraphic(layer)));
  applyFrame(state.currentTime);
  drawSelection();
}

function drawSelection() {
  $$(".selection-ui", els.stage).forEach(node => node.remove());
  const target = els.stage.querySelector(`[data-layer-id="${CSS.escape(state.selectedId)}"]`);
  if (!target || state.playing || state.recording) return;
  try {
    const box = target.getBBox();
    const ui = svgEl("g", { class: "selection-ui" });
    const targetTransform = target.getAttribute("transform");
    if (targetTransform) ui.setAttribute("transform", targetTransform);
    ui.append(svgEl("rect", { class: "selection-box", x: box.x - 12, y: box.y - 12, width: box.width + 24, height: box.height + 24 }));
    [[box.x - 12, box.y - 12], [box.x + box.width + 12, box.y - 12], [box.x - 12, box.y + box.height + 12], [box.x + box.width + 12, box.y + box.height + 12]].forEach(([cx, cy]) => ui.append(svgEl("rect", { class: "selection-handle", x: cx - 6, y: cy - 6, width: 12, height: 12 })));
    target.parentNode.append(ui);
  } catch { /* SVG can be briefly detached during export. */ }
}

function ease(progress, type) {
  const p = clamp(progress, 0, 1);
  if (type === "linear") return p;
  if (type === "ease-out") return 1 - Math.pow(1 - p, 3);
  if (type === "spring") return 1 - Math.cos(p * Math.PI * 2.5) * Math.exp(-p * 5);
  return p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
}

function layerFrame(layer, time) {
  if (layer.animation === "none") return { opacity: layer.opacity, dx: 0, dy: 0, scale: layer.scale, rotation: 0 };
  const raw = (time - layer.start) / Math.max(.01, layer.duration);
  const p = ease(raw, layer.easing);
  if (raw < 0) return { opacity: 0, dx: 0, dy: 0, scale: layer.scale, rotation: 0 };
  const opacity = layer.opacity * clamp(raw / .35, 0, 1);
  if (layer.animation === "slide-right") return { opacity, dx: -150 * (1 - p), dy: 0, scale: layer.scale, rotation: 0 };
  if (layer.animation === "slide-left") return { opacity, dx: 150 * (1 - p), dy: 0, scale: layer.scale, rotation: 0 };
  if (layer.animation === "slide-up") return { opacity, dx: 0, dy: 100 * (1 - p), scale: layer.scale, rotation: 0 };
  if (layer.animation === "slide-down") return { opacity, dx: 0, dy: -100 * (1 - p), scale: layer.scale, rotation: 0 };
  if (layer.animation === "pop") return { opacity, dx: 0, dy: 0, scale: layer.scale * (.42 + .58 * p), rotation: 0 };
  if (layer.animation === "zoom-out") return { opacity, dx: 0, dy: 0, scale: layer.scale * (1.65 - .65 * p), rotation: 0 };
  if (layer.animation === "rotate-in") return { opacity, dx: 0, dy: 0, scale: layer.scale * (.75 + .25 * p), rotation: -18 * (1 - p) };
  if (layer.animation === "bounce") {
    const bounce = raw >= 1 ? 0 : Math.abs(Math.sin(p * Math.PI * 2.5)) * 75 * (1 - p);
    return { opacity, dx: 0, dy: -bounce, scale: layer.scale, rotation: 0 };
  }
  if (layer.animation === "swing") {
    const rotation = raw >= 1 ? Math.sin((time - layer.start) * 2.2) * 2 : Math.sin(p * Math.PI * 4) * 16 * (1 - p);
    return { opacity, dx: 0, dy: 0, scale: layer.scale, rotation };
  }
  if (layer.animation === "float") return { opacity, dx: 0, dy: raw >= 1 ? Math.sin((time - layer.start) * 1.6) * 12 : 28 * (1 - p), scale: layer.scale, rotation: 0 };
  return { opacity, dx: 0, dy: 0, scale: layer.scale, rotation: 0 };
}

function applyFrame(time) {
  state.currentTime = clamp(time, 0, state.duration);
  state.layers.forEach(layer => {
    const node = els.stage.querySelector(`[data-layer-id="${CSS.escape(layer.id)}"]`);
    if (!node) return;
    const frame = layerFrame(layer, state.currentTime);
    const x = Number(layer.x || 0) + frame.dx;
    const y = Number(layer.y || 0) + frame.dy;
    node.setAttribute("transform", `translate(${x} ${y}) rotate(${frame.rotation || 0}) scale(${frame.scale})`);
    node.setAttribute("opacity", frame.opacity);
  });
  const ratio = state.duration ? state.currentTime / state.duration : 0;
  els.playhead.style.left = `${ratio * 100}%`;
  els.timecode.textContent = formatTime(state.currentTime);
}

function play(fromStart = false) {
  if (state.recording) return;
  if (fromStart || state.currentTime >= state.duration) applyFrame(0);
  state.playing = true;
  state.playStartedAt = performance.now();
  state.playStartTime = state.currentTime;
  drawSelection();
  const tick = now => {
    if (!state.playing) return;
    const next = state.playStartTime + (now - state.playStartedAt) / 1000;
    applyFrame(next);
    if (next >= state.duration) {
      pause();
      applyFrame(state.duration);
      drawSelection();
      return;
    }
    state.animationFrame = requestAnimationFrame(tick);
  };
  state.animationFrame = requestAnimationFrame(tick);
}

function pause() {
  state.playing = false;
  if (state.animationFrame) cancelAnimationFrame(state.animationFrame);
  state.animationFrame = null;
  drawSelection();
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60).toString().padStart(2, "0");
  const secs = Math.floor(seconds % 60).toString().padStart(2, "0");
  const hundredths = Math.floor((seconds % 1) * 100).toString().padStart(2, "0");
  return `${mins}:${secs}.${hundredths}`;
}

function selectLayer(id) {
  if (!state.layers.some(layer => layer.id === id)) return;
  state.selectedId = id;
  renderTimeline();
  syncInspector();
  drawSelection();
}

function selectedLayer() {
  return state.layers.find(layer => layer.id === state.selectedId);
}

function syncInspector() {
  const layer = selectedLayer();
  if (!layer) return;
  $("#layerName").value = layer.name;
  $("#layerText").value = layer.text || "";
  $("#layerText").disabled = !("text" in layer);
  $("#positionX").value = Math.round(layer.x || 0);
  $("#positionY").value = Math.round(layer.y || 0);
  $("#layerColor").value = normalizeHex(layer.color || "#1463df");
  $("#layerColorText").value = (layer.color || "#1463df").toUpperCase();
  $("#layerOpacity").value = Math.round((layer.opacity ?? 1) * 100);
  $("#opacityValue").value = `${$("#layerOpacity").value}%`;
  $("#layerScale").value = Math.round((layer.scale ?? 1) * 100);
  $("#scaleValue").value = `${$("#layerScale").value}%`;
  $("#animationType").value = layer.animation || "fade";
  $("#layerDuration").value = layer.duration;
  $("#layerDurationValue").value = `${Number(layer.duration).toFixed(1)} 秒`;
  $("#layerDelay").max = state.duration;
  $("#layerDelay").value = layer.start;
  $("#layerDelayValue").value = `${Number(layer.start).toFixed(1)} 秒`;
  $("#easing").value = layer.easing || "ease-in-out";
}

function normalizeHex(value) {
  if (/^#[0-9a-f]{6}$/i.test(value)) return value;
  return "#1463df";
}

function updateSelected(patch, record = true) {
  const layer = selectedLayer();
  if (!layer) return;
  if (record) pushHistory();
  Object.assign(layer, patch);
  markChanged();
  renderStage();
  renderTimeline();
  syncInspector();
}

function renderTimeline() {
  els.layerList.innerHTML = "";
  $$(".track-row", els.trackArea).forEach(row => row.remove());
  state.layers.forEach(layer => {
    const row = document.createElement("div");
    row.className = `layer-row${layer.id === state.selectedId ? " selected" : ""}`;
    row.dataset.id = layer.id;
    row.innerHTML = `<button type="button" aria-label="顯示或隱藏圖層"><svg viewBox="0 0 24 24"><path d="M3 12s3-5 9-5 9 5 9 5-3 5-9 5-9-5-9-5Z"/><circle cx="12" cy="12" r="2"/></svg></button><span>${escapeHtml(layer.name)}</span><button type="button" aria-label="鎖定圖層"><svg viewBox="0 0 24 24"><rect x="6" y="10" width="12" height="10" rx="2"/><path d="M9 10V7a3 3 0 0 1 6 0v3"/></svg></button>`;
    row.addEventListener("click", () => selectLayer(layer.id));
    els.layerList.append(row);

    const track = document.createElement("div");
    track.className = `track-row${layer.id === state.selectedId ? " selected" : ""}`;
    const clip = document.createElement("button");
    clip.className = "clip";
    clip.type = "button";
    clip.textContent = layer.text || layer.name;
    clip.style.left = `${(layer.start / state.duration) * 100}%`;
    clip.style.width = `${Math.max(2.5, (layer.duration / state.duration) * 100)}%`;
    clip.addEventListener("click", event => { event.stopPropagation(); selectLayer(layer.id); });
    track.append(clip);
    track.addEventListener("click", event => {
      const rect = track.getBoundingClientRect();
      applyFrame(((event.clientX - rect.left) / rect.width) * state.duration);
      selectLayer(layer.id);
    });
    els.trackArea.insertBefore(track, els.playhead);
  });
  renderRuler();
}

function renderRuler() {
  els.rulerTrack.innerHTML = "";
  const divisions = 10;
  for (let i = 0; i <= divisions; i += 1) {
    const label = document.createElement("span");
    label.className = "ruler-label";
    label.style.left = `${i * 10}%`;
    label.textContent = formatTime((state.duration / divisions) * i).slice(0, 5);
    els.rulerTrack.append(label);
  }
}

function applyTemplate(name, shouldConfirm = true) {
  if (shouldConfirm && !confirm("套用範本會取代目前畫面。要繼續嗎？")) return;
  pushHistory();
  const data = templateFactories[name]();
  state.template = name;
  state.projectTitle = data.title;
  state.duration = data.duration;
  state.background = data.background;
  state.layers = structuredClone(data.layers);
  state.selectedId = state.layers[0].id;
  state.currentTime = Math.min(state.duration, { water: 6.2, intro: 3.2, steps: 6.2, outro: 3.2 }[name] || state.duration * .52);
  els.projectTitle.value = state.projectTitle;
  els.projectDuration.value = state.duration;
  updateDurationLabels();
  $$(".template-card").forEach(card => card.classList.toggle("selected", card.dataset.template === name));
  renderAll();
  markChanged();
  showToast("已套用動畫範本");
}

function renderAll() {
  renderStage();
  renderTimeline();
  syncInspector();
  setAspect(state.aspect);
}

function addText(style = "body") {
  pushHistory();
  const presets = {
    heading: { text: "輸入標題", size: 52, y: 250 },
    body: { text: "輸入說明文字", size: 30, y: 360 },
    caption: { text: "重點提示", size: 24, y: 520 }
  };
  const preset = presets[style] || presets.body;
  const layer = { id: uid(), name: preset.text, kind: "text", text: preset.text, x: 640, y: preset.y, color: state.background === "#12213d" ? "#ffffff" : "#163865", size: preset.size, scale: 1, opacity: 1, start: state.currentTime, duration: 2, animation: "slide-up", easing: "ease-out" };
  state.layers.push(layer);
  state.selectedId = layer.id;
  renderAll();
  markChanged();
}

function addShape(shape) {
  pushHistory();
  const names = { circle: "圓形", square: "方形", triangle: "三角形", arrow: "箭頭" };
  const layer = { id: uid(), name: names[shape], kind: "shape", shape, x: 640, y: 360, color: "#1463df", scale: 1, opacity: 1, start: state.currentTime, duration: 2, animation: "pop", easing: "spring" };
  state.layers.push(layer);
  state.selectedId = layer.id;
  renderAll();
  markChanged();
}

function addIcon(icon) {
  pushHistory();
  const names = { idea: "概念圖示", question: "提問圖示", check: "重點圖示", book: "閱讀圖示" };
  const layer = { id: uid(), name: names[icon], kind: "icon", icon, x: 640, y: 360, color: "#0ab9ad", scale: 1, opacity: 1, start: state.currentTime, duration: 2, animation: "pop", easing: "spring" };
  state.layers.push(layer);
  state.selectedId = layer.id;
  renderAll();
  markChanged();
}

function iconifySvgUrl(iconName) {
  const [prefix, name] = String(iconName).split(":");
  return `https://api.iconify.design/${encodeURIComponent(prefix)}/${encodeURIComponent(name)}.svg`;
}

async function searchIconLibrary(query) {
  const status = $("#iconLibraryStatus");
  const results = $("#iconLibraryResults");
  const keyword = String(query || "").trim();
  if (!keyword) {
    status.textContent = "請輸入英文關鍵字，例如 mountain、water 或 education。";
    status.dataset.state = "error";
    return;
  }
  status.textContent = "正在搜尋免費 SVG 素材…";
  status.dataset.state = "loading";
  results.innerHTML = "";
  try {
    const endpoint = `https://api.iconify.design/search?query=${encodeURIComponent(keyword)}&prefixes=tabler,mdi&limit=32`;
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error("素材庫暫時無法連線");
    const data = await response.json();
    const icons = Array.isArray(data.icons) ? data.icons.slice(0, 18) : [];
    if (!icons.length) {
      status.textContent = "找不到符合的素材，請改用較簡短的英文關鍵字。";
      status.dataset.state = "error";
      return;
    }
    icons.forEach(iconName => {
      const [prefix, name] = iconName.split(":");
      const license = data.collections?.[prefix]?.license?.spdx || (prefix === "tabler" ? "MIT" : "Apache-2.0");
      const button = document.createElement("button");
      button.type = "button";
      button.className = "library-item";
      button.title = `${iconName}｜${license}`;
      button.innerHTML = `<img src="${iconifySvgUrl(iconName)}?color=%231463df" alt=""><span>${escapeHtml(name)}</span>`;
      button.addEventListener("click", () => addIconifyAsset(iconName, license, button));
      results.append(button);
    });
    status.textContent = `找到 ${data.total || icons.length} 個結果，顯示前 ${icons.length} 個。點選即可加入畫布。`;
    status.dataset.state = "ready";
  } catch (error) {
    console.error(error);
    status.textContent = "無法連線 Iconify。請確認網路後再試一次。";
    status.dataset.state = "error";
  }
}

async function addIconifyAsset(iconName, license, button) {
  button.disabled = true;
  const original = button.innerHTML;
  button.innerHTML = "<span>載入中…</span>";
  try {
    const response = await fetch(iconifySvgUrl(iconName));
    if (!response.ok) throw new Error("SVG 下載失敗");
    const rawSvg = await response.text();
    const documentSvg = new DOMParser().parseFromString(rawSvg, "image/svg+xml");
    const rootSvg = documentSvg.documentElement;
    if (rootSvg.nodeName.toLowerCase() !== "svg" || documentSvg.querySelector("parsererror")) throw new Error("SVG 格式不正確");
    rootSvg.querySelectorAll("script,foreignObject,image,a,use").forEach(node => node.remove());
    rootSvg.querySelectorAll("*").forEach(node => {
      [...node.attributes].forEach(attribute => {
        if (/^on/i.test(attribute.name) || /(?:href|src)$/i.test(attribute.name)) node.removeAttribute(attribute.name);
      });
    });
    const [, name] = iconName.split(":");
    pushHistory();
    const layer = {
      id: uid(), name: `免費素材｜${name}`, kind: "iconify",
      iconName, iconSvg: rootSvg.innerHTML, viewBox: rootSvg.getAttribute("viewBox") || "0 0 24 24",
      license, x: 640, y: 360, color: "#1463df", scale: 1, opacity: 1,
      start: state.currentTime, duration: 2, animation: "pop", easing: "spring"
    };
    state.layers.push(layer);
    state.selectedId = layer.id;
    renderAll();
    markChanged();
    showToast(`已加入 ${name} SVG 素材`);
  } catch (error) {
    console.error(error);
    showToast(error.message || "素材加入失敗");
  } finally {
    button.disabled = false;
    button.innerHTML = original;
  }
}

function deleteSelected() {
  if (state.layers.length <= 1) return showToast("至少需要保留一個圖層");
  const index = state.layers.findIndex(layer => layer.id === state.selectedId);
  if (index < 0) return;
  pushHistory();
  state.layers.splice(index, 1);
  state.selectedId = state.layers[Math.max(0, index - 1)].id;
  renderAll();
  markChanged();
  showToast("已刪除圖層");
}

function pushHistory() {
  state.history.push(JSON.stringify(projectData()));
  if (state.history.length > 25) state.history.shift();
}

function undo() {
  const snapshot = state.history.pop();
  if (!snapshot) return showToast("目前沒有可復原的操作");
  loadProjectData(JSON.parse(snapshot), false);
  showToast("已復原上一個操作");
}

function projectData() {
  return {
    version: 1,
    projectTitle: els.projectTitle.value || state.projectTitle,
    template: state.template,
    aspect: state.aspect,
    duration: state.duration,
    background: state.background,
    layers: state.layers,
    narration: state.narration
  };
}

function loadProjectData(data, record = true) {
  if (!data || !Array.isArray(data.layers) || !data.layers.length) throw new Error("專案格式不正確");
  if (record) pushHistory();
  state.projectTitle = String(data.projectTitle || "未命名動畫");
  state.template = String(data.template || "custom");
  state.aspect = ["16:9", "9:16", "1:1", "4:3"].includes(data.aspect) ? data.aspect : "16:9";
  state.duration = clamp(Number(data.duration) || 12, 3, 60);
  state.background = normalizeHex(data.background || "#ffffff");
  state.layers = data.layers.map(layer => ({
    id: String(layer.id || uid()), name: String(layer.name || "未命名圖層"), kind: String(layer.kind || "text"),
    text: layer.text == null ? undefined : String(layer.text), x: Number(layer.x) || 0, y: Number(layer.y) || 0,
    color: normalizeHex(layer.color || "#1463df"), size: Number(layer.size) || 36, scale: Number(layer.scale) || 1,
    opacity: Number.isFinite(Number(layer.opacity)) ? clamp(Number(layer.opacity), .1, 1) : 1,
    start: clamp(Number(layer.start) || 0, 0, state.duration), duration: clamp(Number(layer.duration) || 2, .3, state.duration),
    animation: String(layer.animation || "fade"), easing: String(layer.easing || "ease-in-out"),
    shape: layer.shape, icon: layer.icon, number: layer.number,
    iconSvg: layer.iconSvg, viewBox: layer.viewBox, iconName: layer.iconName, license: layer.license
  }));
  state.narration = {
    ...state.narration,
    ...(data.narration || {})
  };
  state.selectedId = state.layers[0].id;
  state.currentTime = state.duration * .52;
  els.projectTitle.value = state.projectTitle;
  els.projectDuration.value = state.duration;
  $("#aspectRatio").value = state.aspect;
  updateDurationLabels();
  renderAll();
  syncNarrationUI();
  markChanged();
}

function syncNarrationUI() {
  state.narration.audioUrl = "";
  state.narration.subtitleUrl = "";
  state.narration.duration = 0;
  $("#narrationText").value = state.narration.text || "";
  $("#narrationCount").value = String((state.narration.text || "").length);
  $("#narrationRate").value = Number(state.narration.rate) || 0;
  $("#narrationRateValue").value = `${Number(state.narration.rate) || 0}%`;
  populateBrowserVoices();
}

function saveProject() {
  state.projectTitle = els.projectTitle.value.trim() || "未命名動畫";
  downloadBlob(new Blob([JSON.stringify(projectData(), null, 2)], { type: "application/json" }), `${safeName(state.projectTitle)}.json`);
  localStorage.setItem("motionStudioProject", JSON.stringify(projectData()));
  markSaved();
  showToast("專案 JSON 已下載");
}

function openProject(file) {
  const reader = new FileReader();
  reader.onload = () => {
    try {
      loadProjectData(JSON.parse(reader.result));
      showToast("專案已開啟");
    } catch (error) {
      showToast(error.message || "無法開啟專案");
    }
  };
  reader.readAsText(file);
}

function markChanged() {
  els.saveState.textContent = "儲存中…";
  clearTimeout(markChanged.timer);
  markChanged.timer = setTimeout(() => {
    localStorage.setItem("motionStudioProject", JSON.stringify(projectData()));
    markSaved();
  }, 350);
}

function markSaved() {
  els.saveState.textContent = "已自動儲存";
}

function safeName(value) {
  return value.replace(/[<>:"/\\|?*\x00-\x1F]/g, "_").trim() || "animation";
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}

function serializeStage(clean = true) {
  const clone = els.stage.cloneNode(true);
  if (clean) $$(".selection-ui, .motion-path", clone).forEach(node => node.remove());
  clone.setAttribute("xmlns", NS);
  clone.setAttribute("width", "1280");
  clone.setAttribute("height", "720");
  return new XMLSerializer().serializeToString(clone);
}

function downloadSvg() {
  pause();
  applyFrame(state.currentTime);
  downloadBlob(new Blob([serializeStage()], { type: "image/svg+xml;charset=utf-8" }), `${safeName(els.projectTitle.value)}-${formatTime(state.currentTime).replace(/[:.]/g, "-")}.svg`);
  showToast("SVG 畫面已下載");
}

function downloadStandaloneHtml() {
  pause();
  const data = JSON.stringify(projectData()).replace(/</g, "\\u003c");
  const html = `<!doctype html>
<html lang="zh-Hant-TW"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${escapeHtml(els.projectTitle.value)}</title>
<style>html,body{margin:0;height:100%;background:#111;display:grid;place-items:center}svg{width:100vw;height:100vh;max-width:calc(100vh * 16 / 9);font-family:"Microsoft JhengHei",sans-serif}.controls{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);display:flex;gap:8px}.controls button{border:0;border-radius:7px;padding:9px 16px;font:600 14px "Microsoft JhengHei";cursor:pointer}.controls button:first-child{background:#1463df;color:#fff}</style>
<body><div id="mount"></div><div class="controls"><button id="play">播放</button><button id="restart">重播</button></div>
<script>const project=${data};const mount=document.getElementById("mount");mount.innerHTML=\`${serializeStage().replace(/`/g, "\\`").replace(/<\/script/gi, "<\\/script")}\`;const svg=mount.querySelector("svg");const layers=[...svg.querySelectorAll("[data-layer-id]")];let raf,start;
const ease=(p,t)=>t==="linear"?p:t==="ease-out"?1-Math.pow(1-p,3):p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
function frame(time){project.layers.forEach((l,i)=>{const n=layers[i];if(!n)return;const raw=(time-l.start)/Math.max(.01,l.duration),p=ease(Math.max(0,Math.min(1,raw)),l.easing),o=raw<0?0:(l.opacity??1)*Math.max(0,Math.min(1,raw/.35));let dx=0,dy=0,s=l.scale??1,r=0;if(l.animation==="slide-right")dx=-150*(1-p);if(l.animation==="slide-left")dx=150*(1-p);if(l.animation==="slide-up")dy=100*(1-p);if(l.animation==="slide-down")dy=-100*(1-p);if(l.animation==="pop")s*=.42+.58*p;if(l.animation==="zoom-out")s*=1.65-.65*p;if(l.animation==="rotate-in"){s*=.75+.25*p;r=-18*(1-p)}if(l.animation==="bounce")dy=-Math.abs(Math.sin(p*Math.PI*2.5))*75*(1-p);if(l.animation==="swing")r=raw>=1?Math.sin((time-l.start)*2.2)*2:Math.sin(p*Math.PI*4)*16*(1-p);if(l.animation==="float")dy=raw>=1?Math.sin((time-l.start)*1.6)*12:28*(1-p);n.setAttribute("opacity",l.animation==="none"?(l.opacity??1):o);n.setAttribute("transform",\`translate(\${(l.x||0)+dx} \${(l.y||0)+dy}) rotate(\${r}) scale(\${s})\`)})}
function play(){cancelAnimationFrame(raf);start=performance.now();const tick=n=>{const t=(n-start)/1000;frame(t);if(t<project.duration)raf=requestAnimationFrame(tick)};raf=requestAnimationFrame(tick)}document.getElementById("play").onclick=play;document.getElementById("restart").onclick=play;frame(0);play();<\\/script>`;
  downloadBlob(new Blob([html], { type: "text/html;charset=utf-8" }), `${safeName(els.projectTitle.value)}.html`);
  showToast("獨立 HTML 已下載");
}

async function svgToCanvas(svgText, canvas) {
  const context = canvas.getContext("2d");
  const blob = new Blob([svgText], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  try {
    const image = await new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
  } finally {
    URL.revokeObjectURL(url);
  }
}

async function loadSvgImage(svgText) {
  const blob = new Blob([svgText], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  try {
    return await new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = reject;
      image.src = url;
    });
  } finally {
    URL.revokeObjectURL(url);
  }
}

function serializeSvgNode(node) {
  node.setAttribute("xmlns", NS);
  node.setAttribute("width", "1280");
  node.setAttribute("height", "720");
  return new XMLSerializer().serializeToString(node);
}

async function prepareRecordingAssets() {
  const backgroundSvg = els.stage.cloneNode(true);
  $$("[data-layer-id], .selection-ui, .motion-path", backgroundSvg).forEach(node => node.remove());
  const backgroundImage = await loadSvgImage(serializeSvgNode(backgroundSvg));
  const layers = [];
  for (const layer of state.layers) {
    const source = els.stage.querySelector(`[data-layer-id="${CSS.escape(layer.id)}"]`);
    if (!source) continue;
    const layerSvg = els.stage.cloneNode(false);
    const graphic = source.cloneNode(true);
    graphic.setAttribute("transform", `translate(${layer.x || 0} ${layer.y || 0}) scale(${layer.scale || 1})`);
    graphic.setAttribute("opacity", "1");
    $$(".motion-path", graphic).forEach(node => node.remove());
    layerSvg.append(graphic);
    layers.push({ layer, image: await loadSvgImage(serializeSvgNode(layerSvg)) });
  }
  return { backgroundImage, layers };
}

function drawRecordingFrame(assets, canvas, time) {
  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(assets.backgroundImage, 0, 0, canvas.width, canvas.height);
  assets.layers.forEach(({ layer, image }) => {
    const frame = layerFrame(layer, time);
    const baseScale = layer.scale || 1;
    context.save();
    context.globalAlpha = frame.opacity;
    context.translate((layer.x || 0) + frame.dx, (layer.y || 0) + frame.dy);
    context.rotate((frame.rotation || 0) * Math.PI / 180);
    context.scale(frame.scale / baseScale, frame.scale / baseScale);
    context.drawImage(image, -(layer.x || 0), -(layer.y || 0), canvas.width, canvas.height);
    context.restore();
  });
}

async function recordVideo() {
  if (!window.MediaRecorder || !HTMLCanvasElement.prototype.captureStream) {
    return showToast("此瀏覽器不支援錄影，請改用最新版 Chrome 或 Edge");
  }
  pause();
  state.recording = true;
  state.cancelRecording = false;
  els.recordProgress.hidden = false;
  $("#recordWebmBtn").disabled = true;
  const progress = $("progress", els.recordProgress);
  const canvas = els.recordCanvas;
  let stream;
  try {
    els.recordStatus.textContent = "正在準備 SVG 圖層…";
    const recordingAssets = await prepareRecordingAssets();
    drawRecordingFrame(recordingAssets, canvas, 0);
    stream = canvas.captureStream(30);

    const mimeCandidates = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"];
    const mimeType = mimeCandidates.find(type => MediaRecorder.isTypeSupported(type)) || "";
    const recorder = new MediaRecorder(stream, { mimeType, videoBitsPerSecond: 8_000_000 });
    const chunks = [];
    recorder.ondataavailable = event => { if (event.data.size) chunks.push(event.data); };
    const completed = new Promise(resolve => { recorder.onstop = resolve; });
    recorder.start(250);
    const started = performance.now();

    while (!state.cancelRecording) {
      const elapsed = (performance.now() - started) / 1000;
      const time = Math.min(elapsed, state.duration);
      applyFrame(time);
      drawRecordingFrame(recordingAssets, canvas, time);
      const percent = Math.round((time / state.duration) * 100);
      progress.value = percent;
      els.recordPercent.value = `${percent}%`;
      els.recordStatus.textContent = `正在錄製 ${formatTime(time)} / ${formatTime(state.duration)}`;
      if (time >= state.duration) break;
      await new Promise(resolve => requestAnimationFrame(resolve));
    }
    recorder.stop();
    await completed;

    if (state.cancelRecording) {
      els.recordStatus.textContent = "錄製已取消";
      showToast("已取消錄製");
      return;
    }

    const webmBlob = new Blob(chunks, { type: mimeType || "video/webm" });
    downloadBlob(webmBlob, `${safeName(els.projectTitle.value)}.webm`);
    els.recordStatus.textContent = "錄製完成，WebM 已下載";
    showToast("WebM 影片已下載");
    els.recordPercent.value = "100%";
  } catch (error) {
    console.error(error);
    els.recordStatus.textContent = `輸出失敗：${error.message}`;
    showToast(error.message || "影片輸出失敗");
  } finally {
    stream?.getTracks().forEach(track => track.stop());
    state.recording = false;
    $("#recordWebmBtn").disabled = false;
    setTimeout(() => { els.recordProgress.hidden = true; progress.value = 0; }, 1600);
    applyFrame(0);
    drawSelection();
  }
}

function populateBrowserVoices() {
  const status = $("#ttsRuntimeStatus");
  const select = $("#narrationVoice");
  if (!("speechSynthesis" in window) || !window.SpeechSynthesisUtterance) {
    select.disabled = true;
    $("#generateNarrationBtn").disabled = true;
    status.textContent = "此瀏覽器不支援 Web Speech API，請改用最新版 Chrome 或 Edge。";
    status.dataset.ready = "false";
    return;
  }
  browserVoices = window.speechSynthesis.getVoices();
  const previous = state.narration.voice || select.value;
  select.replaceChildren(new Option("自動選擇（繁體中文優先）", ""));
  browserVoices
    .sort((a, b) => {
      const score = voice => voice.lang.toLowerCase() === "zh-tw" ? 0 : voice.lang.toLowerCase().startsWith("zh") ? 1 : 2;
      return score(a) - score(b) || a.lang.localeCompare(b.lang) || a.name.localeCompare(b.name);
    })
    .forEach(voice => select.add(new Option(`${voice.name}｜${voice.lang}`, voice.voiceURI)));
  const matched = browserVoices.find(voice => voice.voiceURI === previous || voice.name === previous);
  select.value = matched?.voiceURI || "";
  state.narration.voice = select.value;
  status.textContent = browserVoices.length
    ? `已讀取 ${browserVoices.length} 個裝置語音；語音只供即時預覽，不會寫入 WebM。`
    : "語音清單仍在載入；若沒有聲音，請稍後再按一次播放。";
  status.dataset.ready = "true";
}

function previewBrowserNarration() {
  const text = $("#narrationText").value.trim();
  if (!text) return showToast("請先輸入旁白文字");
  if (!("speechSynthesis" in window) || !window.SpeechSynthesisUtterance) {
    return showToast("此瀏覽器不支援語音預覽");
  }
  const button = $("#generateNarrationBtn");
  speechStopRequested = false;
  const utterance = new SpeechSynthesisUtterance(text);
  const selected = browserVoices.find(voice => voice.voiceURI === $("#narrationVoice").value);
  const preferred = selected
    || browserVoices.find(voice => voice.lang.toLowerCase() === "zh-tw")
    || browserVoices.find(voice => voice.lang.toLowerCase().startsWith("zh"));
  if (preferred) utterance.voice = preferred;
  utterance.lang = preferred?.lang || "zh-TW";
  utterance.rate = clamp(1 + Number($("#narrationRate").value) / 100, .5, 2);
  utterance.volume = Number($("#previewVolume").value) / 100;
  utterance.onstart = () => {
    button.disabled = true;
    $("#ttsRuntimeStatus").textContent = "正在播放瀏覽器語音預覽…";
  };
  utterance.onend = () => {
    speechStopRequested = false;
    button.disabled = false;
    $("#ttsRuntimeStatus").textContent = "預覽結束；下載的 WebM 不含此語音。";
  };
  utterance.onerror = event => {
    button.disabled = false;
    if (speechStopRequested || event.error === "canceled" || event.error === "interrupted") {
      speechStopRequested = false;
      $("#ttsRuntimeStatus").textContent = "語音預覽已停止；下載的 WebM 不含旁白。";
      return;
    }
    $("#ttsRuntimeStatus").textContent = "語音預覽未完成，請確認瀏覽器語音權限與裝置音量。";
    showToast("瀏覽器語音播放失敗");
  };
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}

function stopBrowserNarration() {
  speechStopRequested = true;
  window.speechSynthesis?.cancel();
  $("#generateNarrationBtn").disabled = false;
  const status = $("#ttsRuntimeStatus");
  status.textContent = "語音預覽已停止；下載的 WebM 不含旁白。";
}

function setAspect(aspect) {
  state.aspect = aspect;
  const ratios = { "16:9": "16 / 9", "9:16": "9 / 16", "1:1": "1 / 1", "4:3": "4 / 3" };
  els.stageFrame.style.aspectRatio = ratios[aspect];
  if (aspect === "9:16") els.stageFrame.style.width = "min(42%, 450px)";
  else if (aspect === "1:1") els.stageFrame.style.width = "min(70%, 650px)";
  else if (aspect === "4:3") els.stageFrame.style.width = "min(82%, 760px)";
  else els.stageFrame.style.width = "min(100%, 900px)";
  markChanged();
}

function setZoom(value) {
  state.zoom = clamp(value, .5, 1.5);
  els.stageFrame.style.transform = `scale(${state.zoom})`;
  $("#zoomLabel").textContent = `${Math.round(state.zoom * 100)}%`;
}

function updateDurationLabels() {
  els.durationDisplay.textContent = formatTime(state.duration);
  $("#layerDelay").max = state.duration;
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.add("show");
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => els.toast.classList.remove("show"), 1900);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}

function bindEvents() {
  $("#playBtn").addEventListener("click", () => play());
  $("#pauseBtn").addEventListener("click", pause);
  $("#replayBtn").addEventListener("click", () => play(true));
  $("#fullscreenBtn").addEventListener("click", () => els.stageFrame.requestFullscreen?.());
  $("#exportBtn").addEventListener("click", () => els.exportDialog.showModal());
  $("#helpBtn").addEventListener("click", () => els.helpDialog.showModal());
  $("#recordWebmBtn").addEventListener("click", recordVideo);
  $("#downloadSvgBtn").addEventListener("click", downloadSvg);
  $("#downloadHtmlBtn").addEventListener("click", downloadStandaloneHtml);
  $("#cancelRecordBtn").addEventListener("click", () => { state.cancelRecording = true; });
  $("#saveProjectBtn").addEventListener("click", saveProject);
  $("#projectFile").addEventListener("change", event => { if (event.target.files[0]) openProject(event.target.files[0]); event.target.value = ""; });
  $("#newProjectBtn").addEventListener("click", () => applyTemplate("water"));
  $("#undoBtn").addEventListener("click", undo);
  $("#deleteLayerBtn").addEventListener("click", deleteSelected);
  $("#deleteLayerFooterBtn").addEventListener("click", deleteSelected);
  $("#addLayerBtn").addEventListener("click", () => { switchAssetPanel("text"); });
  $("#fitTimelineBtn").addEventListener("click", () => { applyFrame(0); showToast("時間軸已符合影片長度"); });
  $("#fitBtn").addEventListener("click", () => setZoom(1));
  $("#zoomOut").addEventListener("click", () => setZoom(state.zoom - .1));
  $("#zoomIn").addEventListener("click", () => setZoom(state.zoom + .1));
  $("#aspectRatio").addEventListener("change", event => setAspect(event.target.value));
  els.stage.addEventListener("click", () => drawSelection());
  els.trackArea.addEventListener("click", event => {
    if (event.target.closest(".track-row")) return;
    const rect = els.trackArea.getBoundingClientRect();
    applyFrame(((event.clientX - rect.left) / rect.width) * state.duration);
    drawSelection();
  });

  $$(".tool").forEach(button => button.addEventListener("click", () => switchAssetPanel(button.dataset.panel)));
  $$(".template-card").forEach(card => card.addEventListener("click", () => applyTemplate(card.dataset.template)));
  $$(".asset-action").forEach(button => button.addEventListener("click", () => addText(button.dataset.add)));
  $$("[data-shape]").forEach(button => button.addEventListener("click", () => addShape(button.dataset.shape)));
  $$("[data-icon]").forEach(button => button.addEventListener("click", () => addIcon(button.dataset.icon)));
  $("#iconLibraryForm").addEventListener("submit", event => {
    event.preventDefault();
    searchIconLibrary($("#iconLibraryQuery").value);
  });
  $$("#backgroundSwatches button").forEach(button => button.addEventListener("click", () => {
    pushHistory(); state.background = button.dataset.color; renderStage(); markChanged();
  }));
  $("#templateSearch").addEventListener("input", event => {
    const query = event.target.value.trim().toLowerCase();
    $$(".template-card").forEach(card => { card.hidden = query && !card.textContent.toLowerCase().includes(query); });
  });
  $$(".tabs button").forEach(button => button.addEventListener("click", () => {
    $$(".tabs button").forEach(tab => tab.classList.toggle("active", tab === button));
    $$(".tab-panel").forEach(panel => panel.classList.toggle("active", panel.dataset.tabPanel === button.dataset.tab));
  }));

  els.projectTitle.addEventListener("input", () => { state.projectTitle = els.projectTitle.value; markChanged(); });
  els.projectDuration.addEventListener("change", () => {
    pushHistory();
    state.duration = clamp(Number(els.projectDuration.value) || 12, 3, 60);
    els.projectDuration.value = state.duration;
    state.layers.forEach(layer => {
      layer.start = Math.min(layer.start, state.duration - .3);
      layer.duration = Math.min(layer.duration, state.duration - layer.start);
    });
    updateDurationLabels(); renderTimeline(); syncInspector(); markChanged();
  });

  $("#layerName").addEventListener("change", event => updateSelected({ name: event.target.value.trim() || "未命名圖層" }));
  $("#layerText").addEventListener("input", event => updateSelected({ text: event.target.value }, false));
  $("#positionX").addEventListener("change", event => updateSelected({ x: clamp(Number(event.target.value) || 0, -500, 1800) }));
  $("#positionY").addEventListener("change", event => updateSelected({ y: clamp(Number(event.target.value) || 0, -500, 1200) }));
  $("#layerColor").addEventListener("input", event => updateSelected({ color: event.target.value }, false));
  $("#layerOpacity").addEventListener("input", event => updateSelected({ opacity: Number(event.target.value) / 100 }, false));
  $("#layerScale").addEventListener("input", event => updateSelected({ scale: Number(event.target.value) / 100 }, false));
  $("#animationType").addEventListener("change", event => updateSelected({ animation: event.target.value }));
  $("#layerDuration").addEventListener("input", event => updateSelected({ duration: Number(event.target.value) }, false));
  $("#layerDelay").addEventListener("input", event => updateSelected({ start: Number(event.target.value) }, false));
  $("#easing").addEventListener("change", event => updateSelected({ easing: event.target.value }));
  $("#narrationText").addEventListener("input", event => {
    state.narration.text = event.target.value;
    $("#narrationCount").value = String(event.target.value.length);
    markChanged();
  });
  $("#narrationVoice").addEventListener("change", event => {
    state.narration.voice = event.target.value;
    markChanged();
  });
  $("#narrationRate").addEventListener("input", event => {
    state.narration.rate = Number(event.target.value);
    $("#narrationRateValue").value = `${event.target.value}%`;
    markChanged();
  });
  $("#generateNarrationBtn").addEventListener("click", previewBrowserNarration);
  $("#stopNarrationBtn").addEventListener("click", stopBrowserNarration);
  if ("speechSynthesis" in window) window.speechSynthesis.addEventListener?.("voiceschanged", populateBrowserVoices);
  window.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") { event.preventDefault(); saveProject(); }
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "z") { event.preventDefault(); undo(); }
    if (event.code === "Space" && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { event.preventDefault(); state.playing ? pause() : play(); }
    if ((event.key === "Delete" || event.key === "Backspace") && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) deleteSelected();
  });
}

function switchAssetPanel(name) {
  $$(".tool").forEach(tool => tool.classList.toggle("active", tool.dataset.panel === name));
  $$(".asset-view").forEach(view => view.classList.toggle("active", view.dataset.view === name));
}

function init() {
  bindEvents();
  let restored = null;
  try { restored = JSON.parse(localStorage.getItem("motionStudioProject")); } catch { /* ignore invalid local state */ }
  if (restored?.layers?.length) {
    loadProjectData(restored, false);
    markSaved();
  } else {
    const data = templateFactories.water();
    state.layers = structuredClone(data.layers);
    state.duration = data.duration;
    state.background = data.background;
    renderAll();
    updateDurationLabels();
    syncNarrationUI();
  }
  populateBrowserVoices();
}

init();
