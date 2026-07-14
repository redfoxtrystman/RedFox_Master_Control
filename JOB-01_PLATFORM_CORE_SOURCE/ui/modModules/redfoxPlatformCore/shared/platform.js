(function () {
  "use strict";

  const CONTRACT = "job01.platform.v1";
  const host = document.body.dataset.host === "pc" ? "pc" : "phone";
  const root = document.getElementById("app");
  const ASSET = "/ui/modModules/redfoxPlatformCore/assets";
  const ICEFOX_LOGO = ASSET + "/brand/icefox_head.svg";

  const fallbackDestination = {
    id: "redfox.home",
    owner: "JOB-01",
    name: "IceFox",
    description: "RedFox legal network and shared browser home.",
    category: "Home",
    iconPath: ICEFOX_LOGO,
    entryPath: "internal:redfox.home",
    order: 0,
    version: "0.2.0",
    phone: true,
    pc: true,
    enabled: true,
    permissions: [],
  };

  const previewListings = [
    ["bruckell_bastion.svg", "2020 Bruckell Bastion", "$17,250"],
    ["gavril_dseries.svg", "2017 Gavril D-Series", "$12,900"],
    ["ibishu_hopper.svg", "2015 Ibishu Hopper", "$6,300"],
    ["civetta_scintilla.svg", "2018 Civetta Scintilla", "$24,750"],
    ["etk_kseries.svg", "2016 ETK K-Series", "$11,100"],
  ];

  const state = {
    browserOpen: host === "phone",
    activeId: "redfox.home",
    history: [],
    forward: [],
    registry: [fallbackDestination],
    registryStatus: "Connecting to the RedFox registry",
    theme: localStorage.getItem("redfox.icefox.theme") === "light" ? "light" : "dark",
    favorite: localStorage.getItem("redfox.icefox.favorite") === "true",
    reloadKey: 0,
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
      iconPath: safeAssetPath(value.iconPath, ICEFOX_LOGO),
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
      state.registryStatus = "Registry response rejected — expected " + CONTRACT;
      render();
      return;
    }
    const items = payload.destinations
      .map(normalizeDestination)
      .filter(Boolean)
      .filter((item) => item.enabled && item[host])
      .sort((a, b) => a.order - b.order || a.name.localeCompare(b.name));
    state.registry = items.length ? items : [fallbackDestination];
    state.registryStatus = "Secure connection · " + state.registry.length + " destination(s) installed";
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
    state.history = [];
    state.forward = [];
    render();
    requestRegistry();
  }

  function openDestination(id, saveHistory) {
    if (!state.registry.some((item) => item.id === id)) return;
    if (saveHistory !== false && state.activeId !== id) {
      state.history.push(state.activeId);
      state.forward = [];
    }
    state.activeId = id;
    state.browserOpen = true;
    render();
  }

  function goBack() {
    if (state.history.length) {
      state.forward.push(state.activeId);
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

  function goForward() {
    if (!state.forward.length) return;
    state.history.push(state.activeId);
    state.activeId = state.forward.pop();
    render();
  }

  function reloadPage() {
    state.reloadKey += 1;
    render();
    requestRegistry();
  }

  function leaveHost() {
    if (host === "phone") {
      window.parent.postMessage({ type: "RedFoxPlatformReturnToPhone", contract: CONTRACT }, "*");
    } else {
      state.browserOpen = false;
      state.activeId = "redfox.home";
      state.history = [];
      state.forward = [];
      render();
    }
  }

  function returnToComputer() {
    window.parent.postMessage({ type: "RedFoxPlatformReturnToComputer", contract: CONTRACT }, "*");
  }

  function toggleTheme() {
    state.theme = state.theme === "dark" ? "light" : "dark";
    localStorage.setItem("redfox.icefox.theme", state.theme);
    render();
  }

  function toggleFavorite() {
    state.favorite = !state.favorite;
    localStorage.setItem("redfox.icefox.favorite", String(state.favorite));
    render();
  }

  function searchInstalled(value) {
    const query = String(value || "").trim().toLowerCase();
    if (!query) return;
    const normalized = query.replace(/^https?:\/\//, "").replace(/^icefox:\/\//, "");
    const match = state.registry.find((item) =>
      item.id.toLowerCase() === normalized ||
      item.id.toLowerCase().includes(normalized) ||
      item.name.toLowerCase().includes(normalized),
    );
    if (match) openDestination(match.id);
    else {
      state.registryStatus = "No installed RedFox destination matched “" + query + "”";
      render();
    }
  }

  function navTabs() {
    return state.registry
      .map((item) => `
        <button class="favorite-tab ${item.id === state.activeId ? "active" : ""}" type="button" data-destination="${escapeHtml(item.id)}">
          <img src="${escapeHtml(item.iconPath)}" alt=""><span>${escapeHtml(item.name)}</span>
        </button>`)
      .join("");
  }

  function destinationCards() {
    return state.registry
      .map((item) => `
        <button class="quick-card" type="button" data-destination="${escapeHtml(item.id)}">
          <span class="quick-card-image"><img src="${escapeHtml(item.iconPath)}" alt=""></span>
          <strong>${escapeHtml(item.name)}</strong>
          <small>${escapeHtml(item.category)}</small>
        </button>`)
      .join("");
  }

  function listingCards() {
    return previewListings
      .map((item) => `
        <article class="listing-card">
          <img src="${ASSET}/vehicles/${item[0]}" alt="">
          <div><span>${escapeHtml(item[1])}</span><strong>${escapeHtml(item[2])}</strong></div>
        </article>`)
      .join("");
  }

  function homeContent() {
    return `
      <section class="icefox-home">
        <section class="hero-panel">
          <div class="hero-copy">
            <h1>ICE<span>FOX</span></h1>
            <p>Your portal for legal services, auctions, and more.</p>
            <form id="heroSearch" class="hero-search">
              <input id="heroSearchInput" autocomplete="off" placeholder="Search IceFox or type an installed destination">
              <button type="submit">Search</button>
            </form>
          </div>
          <img class="hero-car" src="${ASSET}/vehicles/hero_car.svg" alt="">
          <div class="hero-brand-card"><img src="${ICEFOX_LOGO}" alt="IceFox"><strong>ICEFOX</strong><span>REDFOX LEGAL NETWORK</span></div>
          <aside class="weather-card"><small>Leaf Springs, CA</small><strong>☀ 72°F</strong><span>Sunny<br>H 74° · L 55°</span></aside>
          <aside class="news-card"><strong>RedFox News Feed</strong><ul><li>IceFox platform core online.</li><li>${escapeHtml(state.registry.length)} destinations installed.</li><li>Phone and PC share one registry.</li></ul></aside>
        </section>

        <section class="content-panel quick-panel">
          <div class="panel-heading"><h2>Quick Access</h2><span>${escapeHtml(state.registryStatus)}</span></div>
          <div class="quick-grid">${destinationCards()}</div>
        </section>

        <section class="advert-row" aria-label="RedFox network advertising previews">
          <img class="loan-ad" src="${ASSET}/ads/top/loan_banner.svg" alt="RedFox Finance preview">
          <img class="listing-ad" src="${ASSET}/ads/sidebar/list_ride.svg" alt="Vehicle listing preview">
        </section>

        <section class="content-panel listings-panel">
          <div class="panel-heading"><h2>Featured Listings — FoxNet Preview</h2><span>Visual preview only · JOB-02 transactions not connected</span></div>
          <div class="listing-grid">${listingCards()}</div>
        </section>
      </section>`;
  }

  function destinationContent() {
    const item = activeDestination();
    if (item.entryPath === "internal:redfox.home") return homeContent();
    const separator = item.entryPath.includes("?") ? "&" : "?";
    const src = item.entryPath + separator + "redfoxReload=" + state.reloadKey;
    return `<iframe class="destination-frame" src="${escapeHtml(src)}" title="${escapeHtml(item.name)}"></iframe>`;
  }

  function browserWindow() {
    const item = activeDestination();
    return `
      <section class="browser-window ${host === "phone" ? "phone-browser" : "pc-browser"}">
        <header class="browser-titlebar">
          <div class="browser-brand"><img src="${ICEFOX_LOGO}" alt=""><strong>ICEFOX</strong></div>
          <div class="window-actions">
            ${host === "pc" ? '<button id="minimizeBrowser" type="button" aria-label="Minimize">—</button><button type="button" aria-label="Maximize">□</button>' : ""}
            <button id="closeBrowser" class="close-window" type="button" aria-label="Close">×</button>
          </div>
        </header>
        <div class="browser-toolbar">
          <button id="browserBack" type="button" aria-label="Back" ${state.history.length ? "" : "disabled"}>←</button>
          <button id="browserForward" type="button" aria-label="Forward" ${state.forward.length ? "" : "disabled"}>→</button>
          <button id="browserReload" type="button" aria-label="Reload">↻</button>
          <button id="browserHome" type="button" aria-label="Home">⌂</button>
          <form id="addressForm" class="address-field"><span>🔒</span><input id="addressInput" value="https://icefox.redfox/${escapeHtml(item.id)}" aria-label="IceFox address"></form>
          <button id="favoriteButton" class="favorite-button ${state.favorite ? "selected" : ""}" type="button" aria-label="Favorite">★</button>
          <button type="button" aria-label="Privacy">🛡</button>
          <button id="themeButton" type="button" aria-label="Theme">${state.theme === "dark" ? "☾" : "☀"}</button>
          <button type="button" aria-label="Menu">☰</button>
        </div>
        <nav class="favorites-row"><button class="home-tab active-home" id="navHome" type="button">⌂ Home</button>${navTabs()}</nav>
        <main class="browser-content">${destinationContent()}</main>
      </section>`;
  }

  function desktopCards() {
    return state.registry
      .map((item) => `
        <button class="desktop-launch-card" type="button" data-destination="${escapeHtml(item.id)}">
          <img src="${escapeHtml(item.iconPath)}" alt="">
          <strong>${escapeHtml(item.name)}</strong>
          <small>${escapeHtml(item.description)}</small>
        </button>`)
      .join("");
  }

  function desktop() {
    return `
      <main class="desktop-shell">
        <header class="desktop-menubar"><div><img src="${ICEFOX_LOGO}" alt=""><strong>REDFOX WORKSTATION</strong></div><span>${escapeHtml(state.registryStatus)}</span></header>
        <section class="start-screen">
          <header><h1>Welcome back, Driver</h1><p>What are we doing today?</p></header>
          <div class="desktop-launch-grid">${desktopCards()}</div>
          <footer><span>RED FOX INTERNET SYSTEMS</span><span>v0.2</span><strong>● Secure Connection</strong></footer>
        </section>
        ${state.browserOpen ? browserWindow() : ""}
        <footer class="desktop-taskbar">
          <button id="startIceFox" type="button"><img src="${ICEFOX_LOGO}" alt="">IceFox</button>
          <span class="taskbar-spacer"></span>
          <button id="returnComputer" type="button">Return to RLS Computer</button>
        </footer>
      </main>`;
  }

  function wireDestinationButtons() {
    document.querySelectorAll("[data-destination]").forEach((button) => {
      button.addEventListener("click", () => {
        state.browserOpen = true;
        openDestination(button.dataset.destination);
      });
    });
  }

  function wireBrowser() {
    const actions = {
      browserBack: goBack,
      browserForward: goForward,
      browserReload: reloadPage,
      browserHome: () => openDestination("redfox.home"),
      navHome: () => openDestination("redfox.home"),
      closeBrowser: leaveHost,
      minimizeBrowser: leaveHost,
      favoriteButton: toggleFavorite,
      themeButton: toggleTheme,
    };
    Object.entries(actions).forEach(([id, action]) => {
      const element = document.getElementById(id);
      if (element) element.addEventListener("click", action);
    });

    const address = document.getElementById("addressForm");
    if (address) address.addEventListener("submit", (event) => {
      event.preventDefault();
      searchInstalled(document.getElementById("addressInput").value);
    });

    const hero = document.getElementById("heroSearch");
    if (hero) hero.addEventListener("submit", (event) => {
      event.preventDefault();
      searchInstalled(document.getElementById("heroSearchInput").value);
    });
    wireDestinationButtons();
  }

  function render() {
    document.body.classList.toggle("light-theme", state.theme === "light");
    if (host === "pc") {
      root.innerHTML = desktop();
      const start = document.getElementById("startIceFox");
      const returnButton = document.getElementById("returnComputer");
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
