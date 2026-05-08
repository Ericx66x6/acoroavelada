import { getPlayerData } from "./main.js"
import { showOverlay } from "./overlay.js"
import { hideOverlay } from "./overlay.js"
import { saveJson } from "./save_server.js"

const editgoals_modal = document.getElementById("edit_goals_modal")

const editgoals_title = document.getElementById("editgoals_title")
const editgoals_text = document.getElementById("editgoals_text")
const editgoals_cancellbutton = document.getElementById("editgoals_cancellbutton")
const editgoals_confirmbutton = document.getElementById("editgoals_confirmbutton")
const editgoals_x_button = document.getElementById("editgoals_x_button")

const ambition = document.getElementById("ambition_description")
const wish = document.getElementById("wish_description")

const map = {
    "ambition": ambition,
    "wish": wish,
}

let key = null

export function openEditGoalsModal(_key){
    key = _key

    editgoals_modal.classList.remove("hidden")

    showOverlay()
    updateEditGoalsData()
}

export function closeEditGoalsModal(){
    editgoals_modal.classList.add("hidden")
    hideOverlay()
}

export function updateEditGoalsData(){
    const map = {
        ambition: "ALTERAR AMBIÇÃO",
        wish: "ALTERAR DESEJO",
    }

    editgoals_title.textContent = map[key]
}

export function updateGoal(){
    const player_data = getPlayerData()

    if(!document.getElementById(key+"_description")) return

    let text = editgoals_text.value
    editgoals_text.value = ""

    document.getElementById(key+"_description").textContent = text

    if(key == "wish"){
        player_data.goals.find(g => g.id === 1).description = text
    }
    else if(key == "ambition"){
        player_data.goals.find(g => g.id === 0).description = text
    }

    closeEditGoalsModal()
    hideOverlay()
    saveJson()
}

editgoals_cancellbutton.addEventListener("click", () => {
    closeEditGoalsModal()
    editgoals_text.value = ""
})

editgoals_x_button.addEventListener("click", () => {
    closeEditGoalsModal()
    editgoals_text.value = ""
})

editgoals_confirmbutton.addEventListener("click", () => {
    updateGoal()
})