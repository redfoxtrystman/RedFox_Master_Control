// Parent-side BeamNG app bridge for JOB-13.
// Mirrors the working JOB-09 iframe -> postMessage -> bngApi.engineLua pattern.

(function () {
  'use strict';

  function luaQuote(value) {
    return "'" + String(value == null ? '' : value)
      .replace(/\\/g, '\\\\')
      .replace(/'/g, "\\'")
      .replace(/\r/g, '\\r')
      .replace(/\n/g, '\\n') + "'";
  }

  function callAuctionLua(action, payload) {
    var json = '{}';
    try { json = JSON.stringify(payload || {}); } catch (err) { json = '{}'; }
    bngApi.engineLua(
      'extensions.redfoxCopartAuction.webActionJson(' +
      luaQuote(action) + ',' + luaQuote(json) + ')'
    );
  }

  window.addEventListener('message', function (event) {
    var data = event.data || {};
    if (data.source !== 'redfox-copart-portal') return;
    if (data.type === 'action') callAuctionLua(data.action, data.payload || {});
  });

  window.redfoxCopartCallLua = callAuctionLua;
}());
