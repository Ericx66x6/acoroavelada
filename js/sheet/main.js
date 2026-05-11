import { Player } from "./player.js";
import { GameData } from "./gamedata.js"
import { startSheet } from "./start.js"
import { sendAlert } from "./toast.js";

import { upgradeBloodPotency } from "./upgrade.js";
import { upgradeDiscipline } from "./upgrade.js";
import { upgradeSkill } from "./upgrade.js";

import { showOverlay } from "./overlay.js";
import { hideOverlay } from "./overlay.js";

import { updateStatus } from "./section_update.js";
import { addItem } from "./section_update.js";
import { removeItem } from "./section_update.js";
import { editItem } from "./section_update.js";
import { updateAmbition } from "./section_update.js";
import { updateWish } from "./section_update.js";

import { openUpgradeModal as openUpgradeSkillModal } from "./skill_modal.js";
import { closeUpgradeModal } from "./skill_modal.js";
import { refreshModalData as refreshSkillModalData } from "./skill_modal.js";
import { updateModalData as updateSkillModalData } from "./skill_modal.js";

import { openDisciplineModal, resetModalData } from "./discipline_modal.js";
import { closeDisciplineModal } from "./discipline_modal.js";

import { changeMoney } from "./money_input.js";

import { openSidebar } from "./sidebar.js";
import { closeSidebar } from "./sidebar.js";
import { closeConfirmUpgradeModal } from "./upgrade_modal.js";

import { changeStatusEvents } from "./status.js";
import { closeEditGoalsModal } from "./edit_goals.js";
import { openEditGoalsModal } from "./edit_goals.js";
import { closeItemsModal, openItemsModal } from "./item_modal.js";
import { closeCreateModal } from "./create_modal.js";
import { closeRitualModal, openRitualModal, ShowDescriptiveModal } from "./ritual_modal.js";

import { saveJson } from "./save_server.js";
import { closeNotesModal, deleteNote, editNoteDescription, editNoteTitle } from "./notes_modal.js";

let player_data = null;
let game_data = null;

export const base_url = "https://acoroavelada.onrender.com"
//export const base_url = "http://localhost:5000"

const params = new URLSearchParams(window.location.search)
const playerId = params.get("id")
const playerToken = params.get("token")

Promise.all([
    fetch(`${base_url}/get/game_data`).then(r => r.json()),
    fetch(`${base_url}/get/player_data?id=${playerId}&token=${playerToken}`)
        .then(r => r.json())
]).then(([gData, pData]) => {

    player_data = new Player(pData)
    game_data = new GameData(gData)

    startSheet(player_data, game_data);
    changeStatusEvents()
});

document.addEventListener("overlay:click",() => {
    closeSidebar()
    closeUpgradeModal()
    closeDisciplineModal()
    closeConfirmUpgradeModal()
    closeEditGoalsModal()
    closeItemsModal()
    closeCreateModal()
    closeRitualModal()
    closeNotesModal()
    hideOverlay()
})

document.addEventListener("click", (e) => {
    if (e.target.dataset.refresh !== undefined) {
        openEditGoalsModal(e.target.dataset.refresh)
    }

    if (e.target.dataset.upgrade !== undefined) {
        switch(e.target.dataset.upgrade){
            case("disciplines"):
                resetModalData()
                openDisciplineModal(Number(e.target.dataset.id))
                break
            case("rituals"):
                openRitualModal(Number(e.target.dataset.id))
                break
            case("items"):
                openItemsModal(Number(e.target.dataset.id))
                break
            case("notes"):
                console.log("clicou em uma anotação")
                break
            case("morality"):
                sendAlert("A moralidade do personagem é permanente e não pode ser alterada!")
                break
            case("caracteristic"):
                let carac = game_data.caracteristics.find(c => c.id === Number(e.target.dataset.id))
                ShowDescriptiveModal(carac.name, carac.type + ": " + carac.description, carac.value)
                break
            case("note"):
                let note = player_data.notes.find(n => n.id === Number(e.target.dataset.id))
                switch(e.target.dataset.type){
                    case("delete"):
                        deleteNote(Number(e.target.dataset.id))
                        break
                    case("title"):
                        editNoteTitle(note.id, note.name)
                        break
                    case("description"):
                        editNoteDescription(note.id, note.description)
                        break
                    case("expand"):
                        console.log("expandir, n faz nada por hora")
                        break
                }
                break
            default:
                openUpgradeSkillModal()
                updateSkillModalData(e.target)
                refreshSkillModalData()    
                break
        }
    }
})

export function getGameData(){
    return game_data
}

export function getPlayerData(){
    return player_data
}
