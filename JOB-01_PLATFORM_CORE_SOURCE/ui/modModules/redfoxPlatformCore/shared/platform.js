(function () {
  "use strict";

  const CONTRACT = "job01.platform.v1";
  const host = document.body.dataset.host === "pc" ? "pc" : "phone";
  const root = document.getElementById("app");
  const fallbackDestination = {
    id: "redfox.home",
    owner: "JOB-01",
    name: "IceFox Home",
    description: "Shared RedFox FoxNet front door.",
    category: "Platform",
    iconPath: "/ui/modModules/redfoxPlatformCore/assets/icefox.svg",
    entryPath: "internal:redfox.home",
    order: 0,
    version: "0.1.0",
    phone: true,
    pc: true,
    enabled: true,
    permissions: [],
  };

  const state = {
    browserOpen: host === "phone",
    activeId: "redfox.home",
    history: [],
    registry: [fallbackDestination],
    registryStatus: "Waiting for the platform registry",
  };

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function safeAssetPath(value, fallback) {
    const path = String(value || "");
    if (path.startsWith("/ui/modModules/") && !path.includes("..")) return path;
    return fallback;
  }

  function normalizeDestination(value) {
    if (!value || typeof value !== "object") return null;
    if (!/^[a-z0-9][a-z0-9._-]{2,79}$/.test(String(value.id || ""))) return null;
    const entryPath = String(value.entryPath || "");
    if (entryPath !== "internal:redfox.home" && safeAssetPath(entryPath, "") === "") return null;
    return {
      id: String(value.id),
      owner: String(value.owner || "UNKNOWN"),
      name: String(value.name || value.id),
      description: String(value.description || ""),
      category: String(value.category || "Other"),
      iconPath: safeAssetPath(value.iconPath, fallbackDestination.iconPath),
      entryPath,
      order: Number.isFinite(Number(value.order)) ? Number(value.order) : 9999,
      version: String(value.version || "0.0.0"),
      phone: value.phone !== false,
      pc: value.pc !== false,
      enabled: value.enabled !== false,
      permissions: Array.isArray(value.permissions)
        ? value.permissions.filter((item) => typeof item === "string")
        : [],
      bridgeContract: value.bridgeContract ? String(value.bridgeContract) : "",
    };
  }

  function setRegistry(payload) {
    if (!payload || payload.contract !== CONTRACT || !Array.isArray(payload.destinations)) {
      state.registryStatus = "Registry response rejected: expected " + CONTRACT;
      render();
      return;
    }
    const items = payload.destinations
      .map(normalizeDestination)
      .filter(Boolean)
      .filter((item) => item.enabled && item[host])
      .sort((a, b) => a.order - b.order || a.name.localeCompare(b.name));
    state.registry = items.length ? items : [fallbackDestination];
    state.registryStatus = "Shared registry connected · " + state.registry.length + " destination(s)";
    if (!state.registry.some((item) => item.id === state.activeId)) state.activeId = "redfox.home";
    render();
  }

  function requestRegistry() {
    window.parent.postMessage({ type: "RedFoxPlatformRequestRegistry", contract: CONTRACT, host }, "*");
  }

  function activeDestination() {
    return state.registry.find((item) => item.id === state.activeId) || fallbackDestination;
  }

  function openBrowser() {
    state.browserOpen = true;
    state.activeId = "redfox.home";
    render();
    requestRegistry();
  }

  function openDestination(id, saveHistory) {
    if (!state.registry.some((item) => item.id === id)) return;
    if (saveHistory !== false && state.activeId !== id) state.history.push(state.activeId);
    state.activeId = id;
    state.browserOpen = true;
    render();
  }

  function goBack() {
    if (state.history.length) {
      state.activeId = state.history.pop();
      render();
      return;
    }
    if (state.activeId !== "redfox.home") {
      openDestination("redfox.home", false);
      return;
    }
    leaveHost();
  }

  function leaveHost() {
    if (host === "phone") {
      window.parent.postMessage({ type: "RedFoxPlatformReturnToPhone", contract: CONTRACT }, "*");
    } else {
      state.browserOpen = false;
      state.activeId = "redfox.home";
      state.history = [];
      render();
    }
  }

  function returnToComputer() {
    window.parent.postMessage({ type: "RedFoxPlatformReturnToComputer", contract: CONTRACT }, "*");
  }

  function appCards() {
    return state.registry
      .map(
        (item) => `
          <button class="destination-card" type="button" data-destination="${escapeHtml(item.id)}">
            <img src="${escapeHtml(item.iconPath)}" alt="">
            <span class="destination-copy">
              <strong>${escapeHtml(item.name)}</strong>
              <small>${escapeHtml(item.category)} · ${escapeHtml(item.owner)}</small>
              <span>${escapeHtml(item.description)}</span>
            </span>
          </button>`,
      )
      .join("");
  }

  function homeContent() {
    return `
      <section class="icefox-home">
        <div class="hero-mark">
          <img src="${fallbackDestination.iconPath}" alt="">
          <div><span>REDFOX NETWORK</span><h1>ICEFOX</h1><p>One front door. The same registered destinations on phone and PC.</p></div>
        </div>
        <div class="contract-line"><strong>${CONTRACT}</strong><span>${escapeHtml(state.registryStatus)}</span></div>
        <section class="destination-section">
          <div class="section-heading"><h2>Registered destinations</h2><button id="refreshRegistry" type="button">Refresh</button></div>
          <div class="destination-grid">${appCards()}</div>
        </section>
        <aside class="boundary-note">
          <strong>Platform boundary</strong>
          <span>IceFox handles registration and navigation. Career transactions remain with RLS through the JOB-02 bridge.</span>
        </aside>
      </section>`;
  }

  function destinationContent() {
    const item = activeDestination();
    if (item.entryPath === "internal:redfox.home") return homeContent();
    return `<iframe class="destination-frame" src="${escapeHtml(item.entryPath)}" title="${escapeHtml(item.name)}"></iframe>`;
  }

  function browserWindow() {
    const item = activeDestination();
    return `
      <section class="browser-window ${host === "phone" ? "phone-browser" : "pc-browser"}">
        <header class="browser-titlebar">
          <div class="browser-brand"><img src="${fallbackDestination.iconPath}" alt=""><strong>IceFox</strong></div>
          <div class="window-actions">
            ${host === "pc" ? '<button id="minimizeBrowser" type="button" aria-label="Minimize">—</button>' : ""}
            <button id="closeBrowser" type="button" aria-label="Close">×</button>
          </div>
        </header>
        <nav class="browser-toolbar">
          <button id="browserBack" type="button" aria-label="Back">←</button>
          <button id="browserHome" type="button" aria-label="Home">⌂</button>
          <div class="address-field"><span>◆</span><code>icefox://${escapeHtml(item.id)}</code></div>
          <span class="host-pill">${host.toUpperCase()}</span>
        </nav>
        <main class="browser-content">${destinationContent()}</main>
      </section>`;
  }

  function desktop() {
    return `
      <main class="desktop-shell">
        <header class="desktop-menubar"><strong>RedFox Workstation</strong><span>RLS Career · JOB-01</span></header>
        <section class="desktop-icons">
          <button id="icefoxDesktopIcon" class="desktop-icon" type="button">
            <img src="${fallbackDestination.iconPath}" alt="">
            <span>IceFox</span>
          </button>
        </section>
        ${state.browserOpen ? browserWindow() : ""}
        <footer class="desktop-taskbar">
          <button id="startIceFox" type="button"><img src="${fallbackDestination.iconPath}" alt="">IceFox</button>
          <span class="taskbar-spacer"></span>
          <button id="returnComputer" type="button">Return to RLS Computer</button>
        </footer>
      </main>`;
  }

  function wireBrowser() {
    const back = document.getElementById("browserBack");
    const home = document.getElementById("browserHome");
    const close = document.getElementById("closeBrowser");
    const minimize = document.getElementById("minimizeBrowser");
    const refresh = document.getElementById("refreshRegistry");
    if (back) back.addEventListener("click", goBack);
    if (home) home.addEventListener("click", () => openDestination("redfox.home"));
    if (close) close.addEventListener("click", leaveHost);
    if (minimize) minimize.addEventListener("click", leaveHost);
    if (refresh) refresh.addEventListener("click", requestRegistry);
    document.querySelectorAll("[data-destination]").forEach((button) => {
      button.addEventListener("click", () => openDestination(button.dataset.destination));
    });
  }

  function render() {
    if (host === "pc") {
      root.innerHTML = desktop();
      const desktopIcon = document.getElementById("icefoxDesktopIcon");
      const start = document.getElementById("startIceFox");
      const returnButton = document.getElementById("returnComputer");
      if (desktopIcon) desktopIcon.addEventListener("click", openBrowser);
      if (start) start.addEventListener("click", openBrowser);
      if (returnButton) returnButton.addEventListener("click", returnToComputer);
    } else {
      root.innerHTML = browserWindow();
    }
    wireBrowser();
  }

  window.addEventListener("message", (event) => {
    const data = event && event.data ? event.data : {};
    if (data.type === "RedFoxPlatformRegistry") setRegistry(data.payload);
  });

  window.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    event.preventDefault();
    if (host === "pc" && state.browserOpen) leaveHost();
    else goBack();
  });

  render();
  requestRegistry();
  window.setTimeout(requestRegistry, 750);
})();
