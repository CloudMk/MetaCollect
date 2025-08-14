document.addEventListener("DOMContentLoaded", () => {
  const registerPage = document.getElementById("register-page");
  const loginPage = document.getElementById("login-page");
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  const registerError = document.getElementById("register-error");
  const registerSuccess = document.getElementById("register-success");
  const loginError = document.getElementById("login-error");

  const goLogin = document.getElementById("go-login");
  const goRegister = document.getElementById("go-register");

  // ✅ Afficher page de connexion au démarrage
  loginPage.classList.remove("hidden");
  registerPage.classList.add("hidden");

  // Navigation
  goLogin.addEventListener("click", (e) => {
      e.preventDefault();
      registerPage.classList.add("hidden");
      loginPage.classList.remove("hidden");
  });

  goRegister.addEventListener("click", (e) => {
      e.preventDefault();
      loginPage.classList.add("hidden");
      registerPage.classList.remove("hidden");
  });
});
