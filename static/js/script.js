// Gestion de l'affichage des pages
document.getElementById('go-register').addEventListener('click', function(e) {
  e.preventDefault();
  document.getElementById('login-page').classList.add('hidden');
  document.getElementById('register-page').classList.remove('hidden');
});

document.getElementById('go-login').addEventListener('click', function(e) {
  e.preventDefault();
  document.getElementById('register-page').classList.add('hidden');
  document.getElementById('login-page').classList.remove('hidden');
});