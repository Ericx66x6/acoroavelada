import { hideOverlay, showOverlay } from "./overlay.js"
import { addItem } from "./section_update.js"
import { startItems } from "./start.js"

const modal = document.querySelector("#add_modal")

const create_modal_title = document.querySelector("#create_modal_title")

const inputName = document.querySelector("#create_modal_name_textarea")
const inputDesc = document.querySelector("#create_modal_description_textarea")

const btnConfirm = document.querySelector("#create_modal_confirmbutton")
const btnCancel = document.querySelector("#create_modal_cancellbutton")
const btnClose = document.querySelector("#create_modal_x_button")

const addItemButton = document.querySelector("#add_items_button")

export function openCreateModal(title){
    inputName.value = ""
    inputDesc.value = ""

    create_modal_title.textContent = title.toUpperCase()
    modal.classList.remove("hidden")
    showOverlay()
}

export function closeCreateModal(){
    modal.classList.add("hidden")
    hideOverlay()
}

addItemButton.addEventListener("click", () => {
    openCreateModal("CRIAR ITEM")
})

btnCancel.addEventListener("click", () => {
    closeCreateModal()
})

btnClose.addEventListener("click", () => {
    closeCreateModal()
})

btnConfirm.addEventListener("click", () => {
    if(inputName.value == ""){
        inputName.value = "SEM NOME"
    }

    addItem(inputName.value, inputDesc.value)
    startItems()
    closeCreateModal()
})