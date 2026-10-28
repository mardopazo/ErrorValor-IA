/* ErrorValor-IA — comportamiento mínimo: tema, menú móvil, progreso de lectura, copiar plantilla. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");

  /* Tema claro/oscuro (se recuerda por navegador si el almacenamiento está disponible) */
  function temaActual() {
    var t = root.getAttribute("data-tema");
    if (t) return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "oscuro" : "claro";
  }
  var botonTema = document.getElementById("boton-tema");
  if (botonTema) {
    botonTema.addEventListener("click", function () {
      var nuevo = temaActual() === "oscuro" ? "claro" : "oscuro";
      root.setAttribute("data-tema", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) {}
    });
  }

  /* Menú en pantallas chicas */
  var botonMenu = document.getElementById("boton-menu");
  if (botonMenu) {
    botonMenu.addEventListener("click", function () {
      var abierto = document.body.classList.toggle("menu-abierto");
      botonMenu.setAttribute("aria-expanded", abierto ? "true" : "false");
    });
    document.querySelectorAll(".lateral a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("menu-abierto");
        botonMenu.setAttribute("aria-expanded", "false");
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("menu-abierto")) {
        document.body.classList.remove("menu-abierto");
        botonMenu.setAttribute("aria-expanded", "false");
        botonMenu.focus();
      }
    });
  }

  /* Progreso de lectura: las celdas del anillo se encienden a medida que se avanza */
  var secciones = Array.prototype.slice.call(document.querySelectorAll(".prosa section[id]"));
  var celdas = Array.prototype.slice.call(document.querySelectorAll(".anillo path[data-sec]"));
  var enlaces = Array.prototype.slice.call(document.querySelectorAll(".indice a"));
  var pendiente = false;

  function actualizar() {
    pendiente = false;
    if (!secciones.length) return;
    var marca = window.innerHeight * 0.3;
    var actual = 0;
    for (var i = 0; i < secciones.length; i++) {
      if (secciones[i].getBoundingClientRect().top <= marca) actual = i;
    }
    var alFinal = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
    if (alFinal) actual = secciones.length - 1;
    celdas.forEach(function (c) {
      var n = parseInt(c.getAttribute("data-sec"), 10);
      c.classList.toggle("leida", n < actual);
      c.classList.toggle("actual", n === actual);
    });
    enlaces.forEach(function (a, n) {
      if (n === actual) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }
  function pedir() { if (!pendiente) { pendiente = true; window.requestAnimationFrame(actualizar); } }
  window.addEventListener("scroll", pedir, { passive: true });
  window.addEventListener("resize", pedir);
  actualizar();

  /* Copiar plantilla en Markdown (anexos) */
  var botonCopiar = document.getElementById("boton-copiar");
  var fuente = document.getElementById("fuente-md");
  var estado = document.getElementById("estado-copia");
  if (botonCopiar && fuente) {
    botonCopiar.addEventListener("click", function () {
      var texto = fuente.textContent.replace(/^\n/, "");
      function listo(ok) {
        if (estado) {
          estado.textContent = ok ? "Copiado al portapapeles." : "No se pudo copiar. Usá «Descargar .md».";
          window.setTimeout(function () { estado.textContent = ""; }, 3500);
        }
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto).then(function () { listo(true); }, function () { listo(false); });
      } else {
        var ta = document.createElement("textarea");
        ta.value = texto; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta); listo(ok);
      }
    });
  }
})();
