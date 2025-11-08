let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");

// Abre/fecha ao clicar no botão
closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
});

// Abre ao passar o mouse
sidebar.addEventListener("mouseenter", () => {
    sidebar.classList.add("open");
    menuBtnChange();
});

// Fecha ao sair com o mouse
sidebar.addEventListener("mouseleave", () => {
    sidebar.classList.remove("open");
    menuBtnChange();
});

function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    }
}

