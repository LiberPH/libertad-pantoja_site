// Vista ampliada de la obra. Sin JavaScript, el enlace abre la imagen sola.
(function () {
  var enlaces = Array.prototype.slice.call(document.querySelectorAll('.art-zoom'));
  var visor = document.createElement('dialog');
  if (!enlaces.length || typeof visor.showModal !== 'function') return;

  var t = window.visorTextos || {};
  visor.className = 'visor';
  visor.setAttribute('aria-labelledby', 'visor-titulo');
  visor.innerHTML =
    '<button type="button" class="visor-cerrar" aria-label="' + (t.zoom_close || 'Cerrar') + '">×</button>' +
    '<button type="button" class="visor-anterior" aria-label="' + (t.zoom_prev || 'Obra anterior') + '">‹</button>' +
    '<figure><img alt="">' +
    '<figcaption>' +
    '<span class="visor-titulo" id="visor-titulo"></span>' +
    '<span class="visor-meta"></span>' +
    '<span class="visor-precio"></span>' +
    '<a class="visor-cta"></a>' +
    '<span class="visor-posicion"></span>' +
    '</figcaption></figure>' +
    '<button type="button" class="visor-siguiente" aria-label="' + (t.zoom_next || 'Obra siguiente') + '">›</button>';
  document.body.appendChild(visor);

  var img = visor.querySelector('img');
  var precio = visor.querySelector('.visor-precio');
  var cta = visor.querySelector('.visor-cta');
  var actual = 0;

  function texto(el) {
    return el ? el.textContent.replace(/\s+/g, ' ').trim() : '';
  }

  function mostrar(n) {
    actual = (n + enlaces.length) % enlaces.length;
    var a = enlaces[actual];
    var ficha = a.closest('.art-card');
    img.src = a.getAttribute('href');
    img.alt = a.dataset.title;
    visor.querySelector('.visor-titulo').textContent = a.dataset.title;
    visor.querySelector('.visor-meta').textContent = a.dataset.meta;

    // Estado y precio, tal como aparecen en la ficha.
    var estado = ficha && ficha.querySelector('.status-pill');
    var etiqueta = estado ? texto(estado.lastChild) : '';
    var cifras = [];
    if (ficha) {
      var unica = ficha.querySelector('.art-price');
      if (unica) cifras.push(texto(unica));
      Array.prototype.forEach.call(ficha.querySelectorAll('.price-list div'), function (fila) {
        cifras.push(texto(fila.querySelector('dt')) + ' ' + texto(fila.querySelector('dd')));
      });
    }
    precio.textContent = [etiqueta].concat(cifras).filter(Boolean).join(' · ');

    var boton = ficha && ficha.querySelector('.art-cta');
    cta.hidden = !boton;
    if (boton) {
      cta.href = boton.getAttribute('href');
      cta.textContent = boton.textContent;
    }

    visor.querySelector('.visor-posicion').textContent =
      (actual + 1) + ' ' + (t.zoom_of || 'de') + ' ' + enlaces.length;
  }

  enlaces.forEach(function (a, n) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      mostrar(n);
      visor.showModal();
    });
  });

  visor.querySelector('.visor-cerrar').addEventListener('click', function () { visor.close(); });
  visor.querySelector('.visor-anterior').addEventListener('click', function () { mostrar(actual - 1); });
  visor.querySelector('.visor-siguiente').addEventListener('click', function () { mostrar(actual + 1); });
  visor.addEventListener('click', function (ev) { if (ev.target === visor) visor.close(); });
  visor.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowLeft') mostrar(actual - 1);
    if (ev.key === 'ArrowRight') mostrar(actual + 1);
  });
  visor.addEventListener('close', function () { enlaces[actual].focus(); });
})();
