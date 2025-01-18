let nom = document.getElementById('id_nom');

nom.addEventListener("input", function () {
  nom.value = nom.value.toUpperCase()
})