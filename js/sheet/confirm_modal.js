export function confirmModal({ title, description }) {
  return new Promise((resolve) => {
    const modal = document.querySelector("#confirm_modal")
    const titleEl = document.querySelector("#confirm_modal_title")
    const descEl = document.querySelector("#confirm_modal_description")
    const btnConfirm = document.querySelector("#confirm_modal_confirm_button")
    const btnCancel = document.querySelector("#confirm_modal_cancell_button")
    const btnClose = document.querySelector("#confirm_modal_x_button")

    // seta conteúdo
    titleEl.textContent = title
    descEl.textContent = description

    // mostra modal
    modal.classList.remove("hidden")

    function cleanup(result) {
      modal.classList.add("hidden")

      btnConfirm.removeEventListener("click", onConfirm)
      btnCancel.removeEventListener("click", onCancel)
      btnClose.removeEventListener("click", onCancel)

      resolve(result)
    }

    function onConfirm() {
      cleanup(true)
    }

    function onCancel() {
      cleanup(false)
    }

    btnConfirm.addEventListener("click", onConfirm)
    btnCancel.addEventListener("click", onCancel)
    btnClose.addEventListener("click", onCancel)
  })
}