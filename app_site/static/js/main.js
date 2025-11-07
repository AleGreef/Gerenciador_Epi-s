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

// --- Máscara CPF ---
const cpfInput = document.getElementById('cpf');

cpfInput.addEventListener('input', function(e) {
    // Remove tudo que não for dígito
    let digits = this.value.replace(/\D/g, '').slice(0, 11);

    // Aplica a formatação progressivamente
    digits = digits.replace(/^(\d{3})(\d)/, '$1.$2');                    // 000....
    digits = digits.replace(/^(\d{3}\.\d{3})(\d)/, '$1.$2');             // 000.000....
    digits = digits.replace(/^(\d{3}\.\d{3}\.\d{3})(\d{1,2})/, '$1-$2'); // 000.000.000-00

    this.value = digits;
});

// Evita colar texto com letras/formatos estranhos
cpfInput.addEventListener('paste', function(e) {
    e.preventDefault();
    const pasted = (e.clipboardData || window.clipboardData).getData('text');
    const cleaned = pasted.replace(/\D/g, '').slice(0, 11);
    // Reaplica formatação rápida (mesma lógica)
    let v = cleaned.replace(/^(\d{3})(\d)/, '$1.$2');
    v = v.replace(/^(\d{3}\.\d{3})(\d)/, '$1.$2');
    v = v.replace(/^(\d{3}\.\d{3}\.\d{3})(\d{1,2})/, '$1-$2');
    this.value = v;
});

// --- Máscara Telefone ---
const telInput = document.getElementById('telefone');
telInput.addEventListener('input', function () {
    let v = this.value.replace(/\D/g, '').slice(0, 11);
    
    // Formato para 11 dígitos: (99) 99999-9999
    // Formato para 10 dígitos: (99) 9999-9999
    if (v.length > 10) {
    v = v.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
    } else if (v.length > 5) {
    v = v.replace(/^(\d{2})(\d{4})(\d{0,4})$/, '($1) $2-$3');
    } else if (v.length > 2) {
    v = v.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else {
    v = v.replace(/^(\d*)/, '($1');
    }

    this.value = v;
});

const form = document.getElementById('form-colaborador');
  form.addEventListener('submit', function () {
    const cpf = document.getElementById('cpf');
    const telefone = document.getElementById('telefone');

    // Remove tudo que não for número antes de enviar
    cpf.value = cpf.value.replace(/\D/g, '');
    telefone.value = telefone.value.replace(/\D/g, '');
  });

setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 4000); // desaparece após 4 segundos