import { showOverlay } from "./overlay.js"
import { hideOverlay } from "./overlay.js"
import { getPlayerData } from "./main.js"
import { getGameData } from "./main.js"
import { upgradeBloodPotency } from "./upgrade.js"
import { upgradeSkill } from "./upgrade.js"
import { upgradeDiscipline } from "./upgrade.js"
import { sendAlert } from "./toast.js"

import { openConfirmUpgradeModal } from "./upgrade_modal.js"
import { closeConfirmUpgradeModal } from "./upgrade_modal.js"
import { renderConfirmModal } from "./upgrade_modal.js"

const upg_modal = document.querySelector("#upg_modal")
const upg_modal_title = document.querySelector("#upg_modal_title")
const upg_modal_x_button = document.querySelector("#upg_modal_x_button")
const upg_modal_upgrade_button = document.querySelector("#upg_modal_upg_button")
const upg_modal_lessbutton = document.querySelector("#upg_modal_lessbutton")
const upg_modal_plusbutton = document.querySelector("#upg_modal_plusbutton")
const upg_modal_description = document.querySelector("#upg_modal_description")
const upg_modal_options_container = document.querySelector("#upg_modal_options_container")
const upg_modal_act_xp = document.querySelector("#upg_modal_act_xp")
const upg_modal_cost_xp = document.querySelector("#upg_modal_cost_xp")
const upg_modal_remain_xp = document.querySelector("#upg_modal_remain_xp")

const iconball_container = document.querySelector("#upg_modal_iconballcontainer")

let player_data = null
let game_data = null

let modal_data = {
    title: "title",
    description: "description",
    
    key: null,
    id: null,

    max_nivel: 5,
    act_nivel: 0,
    display_nivel: 0,
    
    xp_cost: 0,
    multiplier: 0,

    up_levels: 0,

    is_locked: false,
}

export function openUpgradeModal(){
    showOverlay()
    upg_modal.classList.remove("hidden")
}

export function closeUpgradeModal(){
    hideOverlay()
    upg_modal.classList.add("hidden")
}

function resetModalData(){
    modal_data.title = "HABILIDADE"
    modal_data.description = "Descrição da habilidade"
    
    modal_data.key = null
    modal_data.id = null

    modal_data.max_nivel = 0
    modal_data.act_nivel = 0
    modal_data.display_nivel = 0
    
    modal_data.xp_cost = 0
    modal_data.multiplier = 0

    modal_data.up_levels = 0

    modal_data.is_locked = false
}

export function updateModalData(element){
    // Usado somente para puxar infos pro modal ao clicar
    resetModalData()

    modal_data.key = element.dataset.upgrade
    modal_data.id = Number(element.dataset.id)

    player_data ??= getPlayerData()
    game_data ??= getGameData()
    
    modal_data.multiplier = game_data.xp_cost[modal_data.key]
    modal_data.is_locked = modal_data.key === "precedents"

    switch(modal_data.key){
        case("bloodpotency"):
            modal_data.title = "POTÊNCIA DE SANGUE"
            modal_data.description = game_data.bloodpotency[0].description
            modal_data.max_nivel = 10
            modal_data.act_nivel = modal_data.display_nivel = player_data.bloodpotency
            break
        default:
            modal_data.title = game_data[modal_data.key][modal_data.id].name
            modal_data.description = game_data[modal_data.key][modal_data.id].description
            modal_data.max_nivel = game_data.maxvalue_generation[player_data.generation]
            modal_data.act_nivel = modal_data.display_nivel = player_data[modal_data.key][modal_data.id].value
            break
    }
}

function updateXpCostData(){
    // Atualiza o custo de XP no modal com base no nivel que está sendo mostrado

    modal_data.xp_cost = 0

    const diff = modal_data.display_nivel - modal_data.act_nivel

    for(let i = 0; i < diff; i++){
      const grow = (modal_data.act_nivel + i) * modal_data.multiplier
      modal_data.xp_cost += grow > 0 ? grow : modal_data.multiplier
    }
}

function renderUpgradeModal(){
    upg_modal_title.textContent = modal_data.title
    upg_modal_description.textContent = modal_data.description

    iconball_container.innerHTML = ""

    for(let i = 0; i < modal_data.max_nivel; i++){
        const iconball = document.createElement("div")
        iconball.classList.add("iconball")
        iconball_container.appendChild(iconball)
    }

    for(let i = 0; i < modal_data.display_nivel; i++){
        iconball_container.children[i].classList.add("active")
    }

    upg_modal_act_xp.textContent = player_data.xp + " XP"
    upg_modal_cost_xp.textContent = modal_data.xp_cost + " XP"
    upg_modal_remain_xp.textContent = (player_data.xp - modal_data.xp_cost) + " XP"
}

function controllUpgradeButton(){
    const bp_rules = modal_data.key === "bloodpotency" && modal_data.display_nivel > game_data.bloodpotency_generation[player_data.generation].max

    if(bp_rules){
        sendAlert("Limite de Geração atingido. Diminua sua Geração para continuar evoluindo a Potência de Sangue")
    }

    if(modal_data.is_locked || player_data.xp < modal_data.xp_cost || modal_data.act_nivel === modal_data.display_nivel || bp_rules){
        upg_modal_upgrade_button.classList.add("unavailable")
    }
    else{
        upg_modal_upgrade_button.classList.remove("unavailable")
    }
}

// Ao clicar no X do modal principal
upg_modal_x_button.addEventListener("click", () => {
    closeUpgradeModal()
})

// Ao clicar em EVOLUIR no modal principal
upg_modal_upgrade_button.addEventListener("click", () => {
    document.dispatchEvent(new CustomEvent("upgrade", {
        detail: {
            title: modal_data.title,
            key: modal_data.key,
            id: modal_data.id,
            act_nivel: modal_data.act_nivel,
            display_nivel: modal_data.display_nivel,
            xp_cost: modal_data.xp_cost,
            up_levels: modal_data.up_levels,
        }
    }))
})

upg_modal_lessbutton.addEventListener("click", () => {
    if(modal_data.display_nivel - 1 >= modal_data.act_nivel){
        modal_data.display_nivel--
        refreshModalData()
    }
})

upg_modal_plusbutton.addEventListener("click", () => {
    if(modal_data.display_nivel + 1 <= modal_data.max_nivel){
        modal_data.display_nivel++
        refreshModalData()
        
        if(modal_data.is_locked){
            sendAlert("Os Antecedentes só podem ser evoluídos durante a criação do personagem.")
        }
    }
})

export function refreshModalData(){
    modal_data.up_levels = modal_data.display_nivel - modal_data.act_nivel
    
    updateXpCostData()
    controllUpgradeButton()
    renderUpgradeModal()
}