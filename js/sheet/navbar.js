import { getGameData, getPlayerData } from "./main.js"
import { sendAlert } from "./toast.js"

const navbar = document.querySelector("#navbar")
const notes_button = document.querySelector("#navbar_notes_button")
const xp_text = document.querySelector("#navbar_xp_text")
const search_button = document.querySelector("#navbar_search_button")

let player_data = null
let game_data = null

export function startNavbar(){
    player_data = getPlayerData()
    game_data = getGameData()

    xp_text.textContent = player_data.xp

    notes_button.addEventListener("click", () => {
        sendAlert("As anotações estarão disponíveis em breve. Estamos trabalhando nisso.")
    })

    search_button.addEventListener("click", () => {
        sendAlert("A pesquisa estará disponível em breve. Estamos trabalhando nisso.")
    })
}