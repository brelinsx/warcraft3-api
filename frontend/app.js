"use strict";

/* ===== Config y estado ===== */
const API_BASE_URL = "http://127.0.0.1:8000";

const state = {
  facciones: [],
  heroes: [],
};

/* ===== Helpers DOM ===== */
const $ = (id) => document.getElementById(id);

const els = {
  statusText: $("status-text"),
  faccionesList: $("facciones-list"),
  heroesList: $("heroes-list"),
  formFaccion: $("form-faccion"),
  formHeroe: $("form-heroe"),
  msg: $("msg"),
  search: $("search"),
  filterFaccion: $("filter-faccion"),
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function getErrorDetail(err, fallback) {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (detail) return JSON.stringify(detail);
  return fallback;
}

function showMsg(text, ok = true) {
  els.msg.textContent = text;
  els.msg.style.color = ok ? "#7CFC00" : "#ff6b6b";
  window.clearTimeout(showMsg._t);
  showMsg._t = window.setTimeout(() => {
    els.msg.textContent = "";
  }, 3000);
}

/* ===== API ===== */
async function fetchAll() {
  const [resFacciones, resHeroes] = await Promise.all([
    axios.get(`${API_BASE_URL}/facciones/`),
    axios.get(`${API_BASE_URL}/heroes/`),
  ]);
  return { facciones: resFacciones.data, heroes: resHeroes.data };
}

/* ===== Render ===== */
function renderFacciones() {
  els.faccionesList.innerHTML =
    state.facciones
      .map(
        (f) =>
          `<p><b>${escapeHtml(f.nombre)}</b> - ${escapeHtml(f.recurso_especial || "")} ` +
          `(${f.heroes.length} héroes) ` +
          `<button type="button" data-action="del-faccion" data-id="${f.id}">🗑️</button> ` +
          `<button type="button" data-action="edit-faccion" data-id="${f.id}">✏️</button></p>`
      )
      .join("") || "<p>Sin facciones</p>";

  const currentFilter = els.filterFaccion.value;
  const options =
    `<option value="">Todas</option>` +
    state.facciones
      .map((f) => `<option value="${f.id}">${escapeHtml(f.nombre)}</option>`)
      .join("");
  els.filterFaccion.innerHTML = options;
  els.filterFaccion.value = currentFilter;

  $("h-faccion").innerHTML = state.facciones
    .map((f) => `<option value="${f.id}">${escapeHtml(f.nombre)}</option>`)
    .join("");
}

function renderHeroes(list) {
  els.heroesList.innerHTML =
    list
      .map(
        (h) =>
          `<p><b>${escapeHtml(h.nombre)}</b> ` +
          `(${escapeHtml(h.clase_heroe)}/${escapeHtml(h.atributo_principal)}) - ` +
          `${escapeHtml(h.faccion?.nombre || "")} ` +
          `<button type="button" data-action="del-heroe" data-id="${h.id}">🗑️</button> ` +
          `<button type="button" data-action="edit-heroe" data-id="${h.id}">✏️</button></p>`
      )
      .join("") || "<p>Sin héroes</p>";
}

function applyFilters() {
  const query = els.search.value.trim().toLowerCase();
  const faccionId = els.filterFaccion.value;
  const filtered = state.heroes.filter(
    (h) =>
      (!query || h.nombre.toLowerCase().includes(query)) &&
      (!faccionId || String(h.faccion_id) === faccionId)
  );
  renderHeroes(filtered);
}

/* ===== Carga inicial ===== */
async function init() {
  try {
    const { facciones, heroes } = await fetchAll();
    state.facciones = facciones;
    state.heroes = heroes;
    els.statusText.textContent = `OK - ${facciones.length} facciones, ${heroes.length} héroes`;
    renderFacciones();
    applyFilters();
  } catch (err) {
    els.statusText.textContent = "ERROR: arranca backend con uvicorn";
    console.error(err);
  }
}

/* ===== Handlers CRUD ===== */
async function handleCreateFaccion(event) {
  event.preventDefault();
  try {
    await axios.post(`${API_BASE_URL}/facciones/`, {
      nombre: $("f-nombre").value.trim(),
      recurso_especial: $("f-recurso").value.trim() || null,
    });
    showMsg("Facción creada");
    event.target.reset();
    await init();
  } catch (err) {
    console.error(err.response?.data);
    showMsg(getErrorDetail(err, "Error 400/422"), false);
  }
}

async function handleCreateHeroe(event) {
  event.preventDefault();
  try {
    await axios.post(`${API_BASE_URL}/heroes/`, {
      nombre: $("h-nombre").value.trim(),
      clase_heroe: $("h-clase").value.trim(),
      atributo_principal: $("h-atributo").value,
      faccion_id: parseInt($("h-faccion").value, 10),
    });
    showMsg("Héroe creado");
    event.target.reset();
    await init();
  } catch (err) {
    console.error(err.response?.data);
    showMsg(getErrorDetail(err, "Error"), false);
  }
}

async function handleDeleteFaccion(id) {
  if (!window.confirm("¿Borrar facción? También borra sus héroes.")) return;
  try {
    await axios.delete(`${API_BASE_URL}/facciones/${id}`);
    showMsg("Facción eliminada");
    await init();
  } catch (err) {
    showMsg(getErrorDetail(err, "Error al borrar"), false);
  }
}

async function handleDeleteHeroe(id) {
  if (!window.confirm("¿Borrar héroe?")) return;
  try {
    await axios.delete(`${API_BASE_URL}/heroes/${id}`);
    showMsg("Héroe eliminado");
    await init();
  } catch (err) {
    showMsg(getErrorDetail(err, "Error al borrar"), false);
  }
}

async function handleEditFaccion(id) {
  const faccion = state.facciones.find((x) => x.id === id);
  if (!faccion) return;
  const nombre = window.prompt("Nombre:", faccion.nombre);
  if (nombre === null) return;
  const recurso = window.prompt("Recurso especial:", faccion.recurso_especial || "");
  if (recurso === null) return;
  try {
    await axios.put(`${API_BASE_URL}/facciones/${id}`, {
      nombre: nombre.trim(),
      recurso_especial: recurso.trim() || null,
    });
    showMsg("Facción actualizada");
    await init();
  } catch (err) {
    showMsg(getErrorDetail(err, "Error al actualizar"), false);
  }
}

async function handleEditHeroe(id) {
  const heroe = state.heroes.find((x) => x.id === id);
  if (!heroe) return;
  const nombre = window.prompt("Nombre:", heroe.nombre);
  if (nombre === null) return;
  const clase = window.prompt("Clase:", heroe.clase_heroe);
  if (clase === null) return;
  try {
    await axios.put(`${API_BASE_URL}/heroes/${id}`, {
      nombre: nombre.trim(),
      clase_heroe: clase.trim(),
      atributo_principal: heroe.atributo_principal,
      faccion_id: heroe.faccion_id,
    });
    showMsg("Héroe actualizado");
    await init();
  } catch (err) {
    showMsg(getErrorDetail(err, "Error al actualizar"), false);
  }
}

/* Delegación de clics: evita onclick inline y variables globales sueltas */
function handleListClick(event) {
  const btn = event.target.closest("button[data-action]");
  if (!btn) return;
  const id = Number(btn.dataset.id);
  const actions = {
    "del-faccion": () => handleDeleteFaccion(id),
    "edit-faccion": () => handleEditFaccion(id),
    "del-heroe": () => handleDeleteHeroe(id),
    "edit-heroe": () => handleEditHeroe(id),
  };
  actions[btn.dataset.action]?.();
}

/* ===== Eventos ===== */
els.formFaccion.addEventListener("submit", handleCreateFaccion);
els.formHeroe.addEventListener("submit", handleCreateHeroe);
els.search.addEventListener("input", applyFilters);
els.filterFaccion.addEventListener("change", applyFilters);
els.faccionesList.addEventListener("click", handleListClick);
els.heroesList.addEventListener("click", handleListClick);

init();
