export function editModal({ title, initialValue = "" }) {
  return new Promise((resolve) => {
    const modal = document.querySelector("#edit_modal")
    const titleEl = document.querySelector("#edit_modal_title")
    const textarea = document.querySelector("#edit_modal_textarea")

    const btnConfirm = document.querySelector("#edit_modal_confirmbutton")
    const btnCancel = document.querySelector("#edit_modal_cancellbutton")
    const btnClose = document.querySelector("#edit_modal_x_button")

    // configura conteúdo
    titleEl.textContent = title
    textarea.value = initialValue

    // mostra modal
    modal.classList.remove("hidden")

    // foca no textarea (detalhe nice 👀)
    setTimeout(() => textarea.focus(), 0)

    function cleanup(result) {
      modal.classList.add("hidden")

      btnConfirm.removeEventListener("click", onConfirm)
      btnCancel.removeEventListener("click", onCancel)
      btnClose.removeEventListener("click", onCancel)

      resolve(result)
    }

    function onConfirm() {
      cleanup(textarea.value)
    }

    function onCancel() {
      cleanup(null)
    }

    btnConfirm.addEventListener("click", onConfirm)
    btnCancel.addEventListener("click", onCancel)
    btnClose.addEventListener("click", onCancel)
  })
}