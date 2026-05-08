import { getPlayerData } from "./main.js"
import { saveJson } from "./save_server.js"

export function changeStatusEvents(){
    const keys = [
        "hunger",
        "humanity",
        "sdamage",
        "adamage",
        "willpower",
        "inspiration",
    ]

    keys.forEach((key) => {
        const player_data = getPlayerData()

        const lessButton = document.getElementById(key)
        const plusButton = document.getElementById(key+"_max")
        
        plusButton.addEventListener("click", () => {
            const value = Number(lessButton.textContent)
            const max_value = Number(plusButton.textContent.replace("/", ""))
            const new_value = value - 1

            if(value == 0) return

            lessButton.textContent = new_value
            player_data.status[key] = new_value

            saveJson()
        })

        lessButton.addEventListener("click", () => {
            const value = Number(lessButton.textContent)
            const max_value = Number(plusButton.textContent.replace("/", ""))
            const new_value = value + 1

            if(value == max_value) return

            lessButton.textContent = new_value
            player_data.status[key] = new_value

            saveJson()
        })
    })
}