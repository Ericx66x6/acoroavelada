import { getPlayerData } from "./main.js"
import { sendAlert } from "./toast.js"
import { saveJson } from "./save_server.js"

const input = document.querySelector("#money_input")

export function changeMoney(value){
    const player_data = getPlayerData()
    const num = Number(value)

    if(player_data.money + num >= 0){
        player_data.money += num

        const money = document.querySelector("#money")
        money.textContent = "$ " + player_data.money
        saveJson()

        if(num > 0){
            sendAlert("O Narrador será notificado dessa alteração !")
        }
    }
}

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        changeMoney(input.value)
        input.value = ""
    }
})