import { getGameData, getPlayerData } from "./main.js"
import { hideOverlay, showOverlay } from "./overlay.js"

const ritual_modal = document.querySelector("#ritual_modal")

const ritual_title = document.querySelector("#ritual_modal_title")
const ritual_close_button = document.querySelector("#ritual_modal_close_button")
const ritual_description = document.querySelector("#ritual_modal_description")
const ritual_nivel = document.querySelector("#ritual_modal_nivel_text")

let player_data = null
let game_data = null

export function openRitualModal(id){
    ritual_modal.classList.remove("hidden")
    renderRitualModal(id)
    showOverlay()
}

export function closeRitualModal(){
    ritual_modal.classList.add("hidden")
    hideOverlay()
}

function renderRitualModal(id){
    player_data = getPlayerData()
    game_data = getGameData()

    const ritual = game_data.rituals.find(r => r.id === id)
    if(!ritual) return

    const map = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
        8: "VIII",
        9: "IX",
        10: "X",
    }

    ritual_title.textContent = ritual.name
    ritual_description.textContent = ritual.description
    ritual_nivel.textContent = map[ritual.nivel]
}

ritual_close_button.addEventListener("click", () => {
    closeRitualModal()
})