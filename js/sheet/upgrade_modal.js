import { closeUpgradeModal } from "./skill_modal.js"
import { closeDisciplineModal } from "./discipline_modal.js"

import { openUpgradeModal } from "./skill_modal.js"
import { openDisciplineModal } from "./discipline_modal.js"

import { upgradeBloodPotency } from "./upgrade.js"
import { upgradeSkill } from "./upgrade.js"
import { upgradeDiscipline } from "./upgrade.js"
import { hideOverlay } from "./overlay.js"

const c_upg_modal = document.querySelector("#c_upg_modal")
const c_upg_modal_x_button = document.querySelector("#c_upg_modal_x_button")
const c_upg_modal_confirm_button = document.querySelector("#c_upg_modal_confirm_button")
const c_upg_modal_cancell_button = document.querySelector("#c_upg_modal_cancell_button")
const c_upg_modal_description = document.querySelector("#c_upg_modal_description")

let modal_data = {
    title: null,
    key: null,
    id: null,
    act_nivel: 0,
    display_nivel: 0,
    xp_cost: 0,
    up_levels: 0,
}

function resetModalData(){
    modal_data = [
        title = null,
        key = null,
        id = null,
        act_nivel = 0,
        display_nivel = 0,
        xp_cost = 0,
        up_levels = 0,
    ]
}

export function openConfirmUpgradeModal(){
    c_upg_modal.classList.remove("hidden")
}

export function closeConfirmUpgradeModal(){
    c_upg_modal.classList.add("hidden")
}

export function renderConfirmModal(){
    let msg = `Deseja gastar ${modal_data.xp_cost} XP para evoluir a habilidade ${modal_data.title} do nível ${modal_data.act_nivel} para o nível ${modal_data.display_nivel} ?`

    c_upg_modal_description.textContent = msg
}

export function confirmUpgrade(){
    hideOverlay()
    closeUpgradeModal()
    closeDisciplineModal()
    closeConfirmUpgradeModal()

    switch(modal_data.key){
        case("disciplines"):
            upgradeDiscipline(modal_data.id)
            break
        case("bloodpotency"):
            upgradeBloodPotency(modal_data.up_levels)
            break
        default:
            upgradeSkill(modal_data.id, modal_data.key, modal_data.up_levels)
            break
    }
}

// Ao clicar no X ou no CANCELAR do modal secundário
c_upg_modal_x_button.addEventListener("click", () => {
    closeConfirmUpgradeModal()
})

c_upg_modal_cancell_button.addEventListener("click", () => {
    closeConfirmUpgradeModal()
})

// Ao clicar em CONFIRMAR dentro do modal secundário
c_upg_modal_confirm_button.addEventListener("click", () => {
    confirmUpgrade()
})

document.addEventListener("upgrade", (e) => {
    modal_data = e.detail

    openConfirmUpgradeModal()
    renderConfirmModal()
})