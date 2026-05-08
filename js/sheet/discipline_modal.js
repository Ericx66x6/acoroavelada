import { getGameData, getPlayerData } from "./main.js"

import { hideOverlay } from "./overlay.js"
import { showOverlay } from "./overlay.js"

const discipline_modal = document.querySelector("#discipline_modal")

const discipline_modal_title = document.querySelector("#discipline_modal_title")
const discipline_modal_subtitle = document.querySelector("#discipline_modal_subtitle")
const discipline_modal_description = document.querySelector("#discipline_modal_description")

const discipline_modal_x_button = document.querySelector("#discipline_modal_x_button")
const discipline_modal_previous_button = document.querySelector("#discipline_modal_previous_button")
const discipline_modal_next_button = document.querySelector("#discipline_modal_next_button")
const discipline_modal_unlock_button = document.querySelector("#discipline_modal_unlock_button")

const discipline_modal_iconballcontainer = document.querySelector("#discipline_modal_iconballcontainer")
const discipline_modal_nivel_text = document.querySelector("#discipline_modal_nivel_text")

let player_data = null
let game_data = null

let modal_data = {
    title: "TITLE",
    subtitle: "SUBTITLE",
    description: "DESCRIPTION",
    id: null,
    nivel: 0,
    display_nivel: 1,
    max_nivel: 0,
}

export function openDisciplineModal(id){
    discipline_modal.classList.remove("hidden")

    updateDisciplineModalData(id)
    renderDisciplineModalData()
    showOverlay()
}

export function closeDisciplineModal(){
    discipline_modal.classList.add("hidden")

    hideOverlay()
}

export function resetModalData(){
    modal_data = {
        title: "TITLE",
        subtitle: "SUBTITLE",
        description: "DESCRIPTION",
        id: null,
        nivel: 0,
        display_nivel: 1,
        max_nivel: 0,
    }
}

export function updateDisciplineModalData(id){
    player_data = getPlayerData()
    game_data = getGameData()

    let discipline = game_data.disciplines.find(i => i.id === id)

    modal_data.id = id

    modal_data.title = discipline.name
    modal_data.subtitle = discipline.nivels.find(d => modal_data.display_nivel === d.nivel).subname
    modal_data.description = discipline.nivels.find(d => modal_data.display_nivel === d.nivel).description

    modal_data.nivel = player_data.disciplines.find(d => id === d.id).nivel
    modal_data.max_nivel = game_data.maxvalue_generation[player_data.generation]
}

function renderDisciplineModalData(){
    discipline_modal_title.textContent = modal_data.title
    discipline_modal_subtitle.textContent = modal_data.subtitle
    discipline_modal_description.textContent = modal_data.description

    const map = {
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
    }

    discipline_modal_nivel_text.textContent = map[modal_data.display_nivel]

    modalStateControler()
    updateIconBallContainer(discipline_modal_iconballcontainer, modal_data.display_nivel, modal_data.max_nivel)
}

function modalStateControler(){
    if(modal_data.display_nivel === modal_data.nivel + 1){
        discipline_modal_unlock_button.classList.remove("unavailable")
    }
    else{
        discipline_modal_unlock_button.classList.add("unavailable")
    }

    if(modal_data.nivel < modal_data.display_nivel){
        discipline_modal.classList.add("locked")
        discipline_modal.classList.remove("unlocked")
    }
    else{
        discipline_modal.classList.remove("locked")
        discipline_modal.classList.add("unlocked")
    }
}

function updateIconBallContainer(container, display_nivel, max_nivel){
    container.innerHTML = ""

    for(let i = 0; i < max_nivel; i++){
        const iconball = document.createElement("div")
        iconball.classList.add("iconball")
        container.appendChild(iconball)
    }

    for(let i = 0; i < display_nivel; i++){
        container.children[i].classList.add("active")
    }
}

// Ao clicar em ADQUIRIR
discipline_modal_unlock_button.addEventListener("click", () => {
    document.dispatchEvent(new CustomEvent("upgrade", {
        detail: {
            title: modal_data.title,
            key: "disciplines",
            id: modal_data.id,
            act_nivel: modal_data.nivel,
            display_nivel: modal_data.display_nivel,
            xp_cost: (modal_data.nivel + 1) * game_data.xp_cost["disciplines"],
            up_levels: 1,
        }
    }))
})

// Ao clicar no >
discipline_modal_next_button.addEventListener("click", () => {
    if(modal_data.display_nivel < modal_data.max_nivel){
        modal_data.display_nivel++
        updateDisciplineModalData(modal_data.id)
        renderDisciplineModalData()
    }
})

// Ao clicar no <
discipline_modal_previous_button.addEventListener("click", () => {
    if(modal_data.display_nivel > 1){
        modal_data.display_nivel--
        updateDisciplineModalData(modal_data.id)
        renderDisciplineModalData()
    }
})

// Ao clicar no X
discipline_modal_x_button.addEventListener("click", () => {
    closeDisciplineModal()
})