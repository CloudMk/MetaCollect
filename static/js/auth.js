document.getElementById("get-code-btn").addEventListener("click", function() {
    let email = document.getElementById("email").value.trim();

    if (!email) {
        alert("Veuillez entrer votre adresse email.");
        return;
    }

    // Optionnel : vérification basique du format email
    if (!/^\S+@\S+\.\S+$/.test(email)) {
        alert("Veuillez entrer un email valide.");
        return;
    }

    // Désactiver le bouton pendant l'envoi
    let btn = this;
    btn.disabled = true;
    btn.innerText = "Envoi...";

    // Envoi AJAX vers ton API
    fetch("/send-code", { // ← À remplacer par la route réelle dans Flask/PHP
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Code de confirmation envoyé à " + email);
        } else {
            alert("Erreur : " + data.message);
        }
    })
    .catch(error => {
        console.error("Erreur :", error);
        alert("Une erreur est survenue.");
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerText = "Get code";
    });
});
