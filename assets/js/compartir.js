// Botón «Compartir» de cada obra: en el celular abre el menú de compartir;
// si el navegador no lo tiene, copia el enlace directo a la obra.
(function () {
  var t = window.visorTextos || {};
  var aviso = document.createElement('span');
  aviso.className = 'visually-hidden';
  aviso.setAttribute('role', 'status');
  document.body.appendChild(aviso);

  function copiado(boton) {
    var original = boton.textContent;
    boton.textContent = t.share_copied || 'Enlace copiado';
    aviso.textContent = boton.textContent;
    setTimeout(function () { boton.textContent = original; aviso.textContent = ''; }, 2200);
  }

  function compartirObra(id, titulo, boton) {
    var url = location.origin + location.pathname + '#' + id;
    if (navigator.share) {
      navigator.share({ title: titulo, text: '«' + titulo + '» · ' + (t.share_text || ''), url: url })
        .catch(function () {});
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { copiado(boton); },
        function () { window.prompt('', url); });
    } else {
      window.prompt('', url);
    }
  }

  window.compartirObra = compartirObra;
  Array.prototype.forEach.call(document.querySelectorAll('.art-compartir'), function (boton) {
    boton.hidden = false;
    boton.addEventListener('click', function () {
      compartirObra(boton.dataset.obra, boton.dataset.title, boton);
    });
  });
})();
