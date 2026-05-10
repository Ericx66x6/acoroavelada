import { confirmModal } from "./confirm_modal.js"
import { editModal } from "./edit_modal.js"
import { getGameData, getPlayerData } from "./main.js"
import { showOverlay } from "./overlay.js"
import { hideOverlay } from "./overlay.js"
import { addItem, editItem, removeItem } from "./section_update.js"
import { startItems } from "./start.js"

const items_modal = document.querySelector("#items_modal")

const items_modal_title = document.querySelector("#items_modal_title")
const items_modal_description = document.querySelector("#items_modal_description")

const items_modal_x_button = document.querySelector("#items_modal_x_button")
const items_modal_delete_button = document.querySelector("#items_modal_delete_button")

let player_data = null
let game_data = null

let modal_data = {
    title: "TITLE",
    description: "DESCRIPTION",
    id: null,
}

function resetModalData(){
    modal_data = {
        title: "TITLE",
        description: "DESCRIPTION",
        id: null,
    }
}

export function openItemsModal(id){
    updateItemsModalData(id)

    items_modal.classList.remove("hidden")
    showOverlay()
}

export function closeItemsModal(){
    items_modal.classList.add("hidden")
    hideOverlay()
    resetModalData()
}

export async function deleteItemsModalItem(){
    const text = await confirmModal({
        title: "APAGAR ITEM?",
        description: "Essa ação não pode ser desfeita!"
    })

    if(text){
        removeItem(modal_data.id)
        startItems()
        closeItemsModal()
    }
}

export async function editItemsModalTitle(){
    const text = await editModal({
        title: "EDITAR NOME",
        initialValue: modal_data.title,
    })

    if(text !== null){
        modal_data.title = text
        items_modal_title.textContent = text.toUpperCase()

        editItem(modal_data.id, modal_data.title, modal_data.description)
        startItems()
        closeItemsModal()
    }
}

export async function editItemsModalDescription(){
    const text = await editModal({
        title: "EDITAR DESCRIÇÃO",
        initialValue: modal_data.description,
    })

    if(text !== null){
        modal_data.description = text
        items_modal_description.textContent = text

        editItem(modal_data.id, modal_data.title, modal_data.description)
        startItems()
        closeItemsModal()
    }
}

function updateItemsModalData(id){
    
    player_data = getPlayerData()  
    game_data = getGameData()

    const item = player_data.items.find(i => i.id === id)

    if(!item) return

    modal_data.title = item.name.toUpperCase()
    modal_data.description = item.description
    modal_data.id = item.id

    renderItemsModalData()
}

function renderItemsModalData(){
    items_modal_title.textContent = modal_data.title
    items_modal_description.textContent = modal_data.description
}

items_modal_delete_button.addEventListener("click", () => {
    deleteItemsModalItem()
})

items_modal_title.addEventListener("click", () => {
    editItemsModalTitle()
})

items_modal_description.addEventListener("click", () => {
    editItemsModalDescription()
})

items_modal_x_button.addEventListener("click", () => {
    closeItemsModal()
})