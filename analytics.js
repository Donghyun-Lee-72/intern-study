+(() => {
  const endpoint = "https://collect.donghyunlee.me/collect";
  const key = "site-analytics-session";
  let sessionId = sessionStorage.getItem(key);
  if (!sessionId) { sessionId = crypto.randomUUID(); sessionStorage.setItem(key, sessionId); }
  const seen = new Set();
  const base = () => ({ eventId: crypto.randomUUID(), sessionId, path: location.pathname + location.search, referrerHost: (() => { try { return document.referrer ? new URL(document.referrer).hostname : ""; } catch { return ""; } })(), language: navigator.language, screen: `${screen.width}x${screen.height}` });
  const send = (eventType, extra = {}) => { const payload = JSON.stringify({ ...base(), eventType, ...extra }); if (!navigator.sendBeacon(endpoint, payload)) fetch(endpoint, { method: "POST", body: payload, headers: { "content-type": "text/plain" }, keepalive: true, mode: "cors" }).catch(() => {}); };
  send("pageview");
  document.addEventListener("click", event => { const link = event.target.closest("a[href]"); if (!link) return; if (link.href.startsWith("mailto:")) send("email_click", { target: link.href.replace(/\\?.*$/, "") }); else if (link.hostname && link.hostname !== location.hostname) send("outbound_click", { target: link.href.slice(0, 500) }); });
  const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (!entry.isIntersecting || !entry.target.id || seen.has(entry.target.id)) return; seen.add(entry.target.id); send("section_view", { target: entry.target.id }); }), { threshold: 0.55 });
  document.querySelectorAll("section[id], article[id], h2[id]").forEach(node => observer.observe(node));
})();

