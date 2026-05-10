import { getPlayerData } from "./main.js";
import { base_url } from "./main.js";

export async function saveJson() {
    const player_data = getPlayerData()

    const res = await fetch(`${base_url}/save`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: player_data.token,
            data: player_data,
            id: player_data.id
        })
    });

    const data = await res.json();

    if (!res.ok) {
        console.error("Erro ao salvar:", data);
        return;
    }

    console.log("Salvo com sucesso:", data);
}