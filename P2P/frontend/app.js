const API_BASE = "http://localhost:8000";

function render(box, data) {
  box.innerHTML = `
<pre class="bg-slate-900 border border-slate-700 rounded-lg p-3 overflow-x-auto">
${JSON.stringify(data, null, 2)}
</pre>`;
}

/* ================= UPLOAD ================= */
async function uploadFile() {
  const input = document.getElementById("uploadFileInput");
  const box = document.getElementById("uploadResult");

  if (!input.files.length) {
    box.innerHTML = "⚠️ Select a file first.";
    return;
  }

  const fd = new FormData();
  fd.append("file", input.files[0]);

  box.innerHTML = "⏳ Uploading & registering on-chain…";

  const res = await fetch(`${API_BASE}/upload_with_file`, {
    method: "POST",
    body: fd
  });

  render(box, await res.json());
}

/* ================= VERIFY ================= */
async function verifyHash() {
  const hash = document.getElementById("verifyInput").value.trim();
  const box = document.getElementById("verifyResult");

  if (!hash) {
    box.innerHTML = "⚠️ Hash required.";
    return;
  }

  box.innerHTML = "⏳ Verifying on-chain…";
  const res = await fetch(`${API_BASE}/verify/${hash}`);
  render(box, await res.json());
}

/* ================= REGISTER NODE ================= */
async function registerNode() {
  const addr = document.getElementById("nodeAddressInput").value.trim();
  const box = document.getElementById("nodeResult");

  if (!addr) {
    box.innerHTML = "⚠️ Node ID required.";
    return;
  }

  const fd = new FormData();
  fd.append("address", addr);

  box.innerHTML = "⏳ Registering node…";
  const res = await fetch(`${API_BASE}/register_node`, {
    method: "POST",
    body: fd
  });

  render(box, await res.json());
}

/* ================= SUMMARY ================= */
async function loadSummary() {
  const box = document.getElementById("summaryBox");
  box.innerHTML = "⏳ Loading ledger…";

  const res = await fetch(`${API_BASE}/summary`);
  const data = await res.json();

  box.innerHTML = `
<div class="grid grid-cols-2 gap-4">
  <div class="bg-slate-900 border border-slate-700 rounded-lg p-4">
    <p class="text-xs text-slate-400">Total Files</p>
    <p class="text-2xl font-bold">${data.files_registered}</p>
  </div>
  <div class="bg-slate-900 border border-slate-700 rounded-lg p-4">
    <p class="text-xs text-slate-400">Sample Keys</p>
    <pre class="text-xs">${JSON.stringify(data.files_keys_sample, null, 2)}</pre>
  </div>
</div>`;
}

/* ================= DOWNLOAD ================= */
async function downloadFile() {
  const hash = document.getElementById("downloadHashInput").value.trim();
  const box = document.getElementById("downloadResult");

  if (!hash) {
    box.innerHTML = "⚠️ Hash required.";
    return;
  }

  box.innerHTML = "⏳ Rebuilding file from network…";

  const res = await fetch(`${API_BASE}/download/${hash}`);
  if (!res.ok) {
    const err = await res.json();
    box.innerHTML = "❌ " + err.detail;
    return;
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  document.body.appendChild(a);
  a.click();
  a.remove();

  box.innerHTML = "✅ File downloaded.";
}
