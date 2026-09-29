"use strict";

/* Crónica del reino: todo el estado vive en este pergamino. */
const API_BASE_URL = "http://127.0.0.1:8000";

const state = {
  facciones: [],
  heroes: [],
  faccionActualIndex: 0,
  heroeActualIndex: 0,
  heroSearchQuery: "",
};

/* Heraldo: atajo para invocar elementos del DOM por su sello (id). */
const $ = (id) => document.getElementById(id);

const els = {
  statusText: $("status-text"),
  visorFaccion: $("visor-faccion"),
  heroeDestacado: $("heroe-destacado"),
  formFaccion: $("form-faccion"),
  formHeroe: $("form-heroe"),
  msg: $("msg"),
};

/* Tinta mágica: escapa texto del usuario para que ningún hechizo rompa el muro. */
function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

/* Oráculo: extrae el mensaje de error que devuelve el Altar (API). */
function getErrorDetail(err, fallback) {
  const detail = err?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (detail) return JSON.stringify(detail);
  return fallback;
}

/* Paloma mensajera: aviso verde de victoria o rojo de derrota (3 segundos). */
function showMsg(text, ok = true) {
  els.msg.textContent = text;
  els.msg.style.color = ok ? "#7CFC00" : "#ff6b6b";
  window.clearTimeout(showMsg._t);
  showMsg._t = window.setTimeout(() => {
    els.msg.textContent = "";
  }, 3000);
}

/* Cuervos mensajeros: traen clanes y héroes del Altar en un solo vuelo. */
async function fetchAll() {
  const [resFacciones, resHeroes] = await Promise.all([
    axios.get(`${API_BASE_URL}/facciones/`),
    axios.get(`${API_BASE_URL}/heroes/`),
  ]);
  return { facciones: resFacciones.data, heroes: resHeroes.data };
}

/* Reclutador: llena el estandarte del formulario con los clanes vivos. */
function poblarSelectFacciones() {
  $("h-faccion").innerHTML = state.facciones
    .map((f) => `<option value="${f.id}">${escapeHtml(f.nombre)}</option>`)
    .join("");
}

/* Atalaya: trae del Altar la facción que ocupa la posición indicada. */
async function fetchFaccionPagina(i) {
  const res = await axios.get(`${API_BASE_URL}/facciones/?skip=${i}&limit=1`);
  return res.data[0];
}

/* Leva: reúne a los héroes que juraron por un clan (y pasan el filtro). */
function heroesDeFaccion(faccionId) {
  const q = state.heroSearchQuery.trim().toLowerCase();
  return state.heroes.filter(
    (h) =>
      h.faccion_id === faccionId &&
      (!q ||
        h.nombre.toLowerCase().includes(q) ||
        h.clase_heroe.toLowerCase().includes(q))
  );
}

/* Estandarte mayor: muestra un clan cada vez con sus botones de mando. */
async function renderVisor() {
  const total = state.facciones.length;
  if (!total) return;
  state.faccionActualIndex =
    ((state.faccionActualIndex % total) + total) % total;
  const f = await fetchFaccionPagina(state.faccionActualIndex);

  let archivoEmblema = "neutral.jpg";
  const nombreLimpio = f.nombre.toLowerCase();
  if (nombreLimpio.includes("horda") || nombreLimpio.includes("orco")) {
    archivoEmblema = "horda.png";
  } else if (nombreLimpio.includes("alianza") || nombreLimpio.includes("humano")) {
    archivoEmblema = "alianza.png";
  } else if (nombreLimpio.includes("muertos") || nombreLimpio.includes("azote")) {
    archivoEmblema = "azote.png";
  } else if (nombreLimpio.includes("elfos")) {
    archivoEmblema = "elfos.png";
  }

  const facImg = $("fac-imagen");
  facImg.style.display = "";
  facImg.alt = f.nombre;
  facImg.onerror = () => {
    facImg.style.display = "none";
  };
  facImg.src = `assets/${archivoEmblema}`;
  $("fac-nombre").textContent = f.nombre;
  $("fac-recurso").textContent = f.recurso_especial || "—";
  $("fac-contador").textContent = `${state.faccionActualIndex + 1} de ${total}`;
  $("fac-acciones").innerHTML =
    `<button type="button" data-action="del-faccion" data-id="${f.id}">🗑️</button> ` +
    `<button type="button" data-action="edit-faccion" data-id="${f.id}">✏️</button>`;
  state.heroeActualIndex = 0;
  renderDestacado(f.id);
}

/* Campeón en el pedestal: el héroe destacado del clan en pantalla. */
function renderDestacado(faccionId) {
  const lista = heroesDeFaccion(faccionId);
  if (!lista.length) {
    $("hero-nombre").textContent = state.heroSearchQuery.trim()
      ? "Sin resultados"
      : "Sin héroes";
    $("hero-detalle").textContent = "—";
    $("hero-contador").textContent = "0 de 0";
    $("hero-acciones").innerHTML = "";
    $("hero-imagen").style.display = "none";
    return;
  }
  state.heroeActualIndex =
    ((state.heroeActualIndex % lista.length) + lista.length) % lista.length;
  const h = lista[state.heroeActualIndex];
  const heroImg = $("hero-imagen");
  heroImg.style.display = "";
  heroImg.alt = h.nombre;
  heroImg.onerror = () => {
    heroImg.style.display = "none";
  };
  heroImg.src = `assets/${h.nombre.toLowerCase()}.png`;
  $("hero-nombre").textContent = h.nombre;
  $("hero-detalle").textContent = `${h.clase_heroe} / ${h.atributo_principal}`;
  $("hero-contador").textContent = `${state.heroeActualIndex + 1} de ${lista.length}`;
  $("hero-acciones").innerHTML =
    `<button type="button" data-action="del-heroe" data-id="${h.id}">🗑️</button> ` +
    `<button type="button" data-action="edit-heroe" data-id="${h.id}">✏️</button>`;
}

/* Cuerno de guerra: avanza o retrocede el estandarte. */
function irFac(d) {
  state.faccionActualIndex += d;
  renderVisor().catch(() => {
    showMsg("No se pudo cargar la facción", false);
  });
}

/* Llamada del oráculo: avanza o retrocede el campeón destacado. */
function irHeroe(d) {
  const f = state.facciones[state.faccionActualIndex];
  if (!f) return;
  state.heroeActualIndex += d;
  renderDestacado(f.id);
}

/* Despertar del reino: carga inicial de clanes, héroes y visor. */
async function init() {
  try {
    const { facciones, heroes } = await fetchAll();
    state.facciones = facciones;
    state.heroes = heroes;
    els.statusText.textContent = `OK - ${facciones.length} facciones, ${heroes.length} héroes`;
    poblarSelectFacciones();
    await renderVisor();
  } catch (err) {
    els.statusText.textContent = "ERROR: arranca backend con uvicorn";
  }
}

/* Gritos de guerra por clan, grabados en español en la armería (assets). */
const SOUND_MAP = [
  { keys: ["horda", "orco"], src: "assets/horda.mp3" },
  { keys: ["alianza", "humano"], src: "assets/alianza.mp3" },
  { keys: ["muertos", "azote"], src: "assets/azote.mp3" },
  { keys: ["elfos"], src: "assets/elfos.mp3" },
];
const SOUND_DEFAULT = "assets/horda.mp3";
const soundBuffers = {};
let audioCtx = null;

/* Intérprete: del nombre del clan al archivo de su grito. */
function resolveSoundSrc(faccionNombre) {
  const nombreLimpio = String(faccionNombre || "").toLowerCase();
  for (const entry of SOUND_MAP) {
    if (entry.keys.some((k) => nombreLimpio.includes(k))) return entry.src;
  }
  return SOUND_DEFAULT;
}

/* Despertar del coro: el navegador exige un gesto para cantar. */
function ensureCtx() {
  if (!audioCtx) {
    const Ctx = window.AudioContext || window.webkitAudioContext;
    if (!Ctx) return null;
    audioCtx = new Ctx();
  }
  if (audioCtx.state === "suspended") void audioCtx.resume();
  return audioCtx;
}

/* Afinación: descarga y decodifica un grito una sola vez. */
async function decodeToBuffer(ctx, src) {
  const res = await fetch(src);
  if (!res.ok) throw new Error("HTTP " + res.status);
  const buf = await ctx.decodeAudioData(await res.arrayBuffer());
  soundBuffers[src] = buf;
  return buf;
}

/* Ensayo general: deja los cuatro gritos listos antes de la batalla. */
async function preloadSounds() {
  const ctx = ensureCtx();
  if (!ctx) return;
  const srcs = [...new Set([SOUND_DEFAULT, ...SOUND_MAP.map((e) => e.src)])];
  for (const src of srcs) {
    try {
      await decodeToBuffer(ctx, src);
    } catch (e) {
      showMsg(`Sonido no disponible: ${src}`, false);
    }
  }
}

/* Primera sangre: el primer clic o tecla despierta al coro. */
function unlockAudioOnce() {
  ensureCtx();
  document.removeEventListener("pointerdown", unlockAudioOnce);
  document.removeEventListener("keydown", unlockAudioOnce);
}
document.addEventListener("pointerdown", unlockAudioOnce);
document.addEventListener("keydown", unlockAudioOnce);

/* Toca el grito del clan usando su partitura ya decodificada. */
async function playBuffer(src) {
  const ctx = ensureCtx();
  if (!ctx) throw new Error("sin AudioContext");
  const buf = soundBuffers[src] || (await decodeToBuffer(ctx, src));
  const node = ctx.createBufferSource();
  node.buffer = buf;
  node.connect(ctx.destination);
  node.start(0);
}

/* Bardo: canta el grito del clan; si falla, lo intenta con cuerno simple. */
function reproducirSonidoFaccion(faccionNombre) {
  const archivoAudio = resolveSoundSrc(faccionNombre);
  ensureCtx();
  playBuffer(archivoAudio).catch(() => {
    try {
      const fallback = new Audio(archivoAudio);
      fallback.volume = 1.0;
      window.__sfxLast = fallback;
      const p = fallback.play();
      if (p && typeof p.catch === "function") {
        p.catch(() => {
          showMsg("El coro está afónico", false);
        });
      }
    } catch (e) {
      showMsg("El coro está afónico", false);
    }
  });
}

/* Fundar un clan: envía el estandarte al Altar y celebra con su himno. */
async function handleCreateFaccion(event) {
  event.preventDefault();
  const nombre = $("f-nombre").value.trim();
  try {
    await axios.post(`${API_BASE_URL}/facciones/`, {
      nombre: nombre,
      recurso_especial: $("f-recurso").value.trim() || null,
    });
    showMsg("Facción creada");
    event.target.reset();
    await init();
    reproducirSonidoFaccion(nombre);
  } catch (err) {
    showMsg(getErrorDetail(err, "Error 400/422"), false);
  }
}

/* Invocar un campeón: lo presenta en el Altar con el grito de su clan. */
async function handleCreateHeroe(event) {
  event.preventDefault();
  let nombreSel = "";
  try {
    const sel = $("h-faccion");
    nombreSel = sel.options[sel.selectedIndex]?.text || "";
  } catch (e) {
    nombreSel = "";
  }
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
    reproducirSonidoFaccion(nombreSel);
  } catch (err) {
    showMsg(getErrorDetail(err, "Error"), false);
  }
}

/* Caída del estandarte: borra un clan y su hueste en silencio. */
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

/* Destierro silencioso: borra un héroe sin trompetas. */
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

/* Escriba: reescribe el nombre y el tributo de un clan. */
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

/* Herrero: reforja el nombre y la clase de un campeón. */
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

/* Plaza del mercado: un solo oído para los botones de cada tarjeta. */
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
  const action = actions[btn.dataset.action];
  if (action) action();
}

/* Pregón: enlaza formularios, flechas y buscador con sus heraldos. */
els.formFaccion.addEventListener("submit", handleCreateFaccion);
els.formHeroe.addEventListener("submit", handleCreateHeroe);
els.visorFaccion.addEventListener("click", handleListClick);
els.heroeDestacado.addEventListener("click", handleListClick);
$("fac-prev").addEventListener("click", () => irFac(-1));
$("fac-next").addEventListener("click", () => irFac(1));
$("hero-prev").addEventListener("click", () => irHeroe(-1));
$("hero-next").addEventListener("click", () => irHeroe(1));
$("hero-search").addEventListener("input", (e) => {
  state.heroSearchQuery = e.target.value;
  state.heroeActualIndex = 0;
  const f = state.facciones[state.faccionActualIndex];
  if (f) renderDestacado(f.id);
});

preloadSounds();
init();
