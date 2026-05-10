import { confirmModal } from "./confirm_modal.js"
import { openCreateModal } from "./create_modal.js"
import { hideOverlay, showOverlay } from "./overlay.js"
import { removeNote, editNote } from "./section_update.js"
import { editModal } from "./edit_modal.js"
import { startNotes } from "./start.js"

const modal = document.querySelector("#notes_modal")

const close_button = document.querySelector("#notes_modal_x_button")
const add_button = document.querySelector("#notes_addbutton")

export function openNotesModal(){
    modal.classList.remove("hidden")
    refresh()
    showOverlay()
}

export function closeNotesModal(){
    modal.classList.add("hidden")
    hideOverlay()
}

function refresh(){
    startNotes()
}

// --------------------
// CLOSE
// --------------------
close_button.addEventListener("click", closeNotesModal)


// --------------------
// EDIT TITLE
// --------------------
export async function editNoteTitle(id, currentTitle) {
    const result = await editModal({
        title: "EDITAR TÍTULO",
        initialValue: currentTitle
    })

    if (result === null) return

    editNote(id, result, null) // atualiza PLAYER + salva
    refresh()
}


// --------------------
// EDIT DESCRIPTION
// --------------------
export async function editNoteDescription(id, currentDesc) {
    const result = await editModal({
        title: "EDITAR DESCRIÇÃO",
        initialValue: currentDesc
    })

    if (result === null) return

    editNote(id, null, result) // atualiza PLAYER + salva
    refresh()
}


// --------------------
// CREATE NOTE
// --------------------
export function createNote(){
    openCreateModal("CRIAR NOTA", "note")
    closeNotesModal()
}


// --------------------
// DELETE NOTE
// --------------------
export async function deleteNote(id){
    const result = await confirmModal({
        title: "TEM CERTEZA?",
        description: "Quer realmente deletar essa nota?"
    })

    if (!result) return

    removeNote(id) // atualiza PLAYER + salva
    refresh()
}


// --------------------
// ADD BUTTON
// --------------------
add_button.addEventListener("click", createNote)