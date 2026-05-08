import { getPlayerData } from "./main.js";

export async function saveJson() {
    const player_data = getPlayerData()

    const res = await fetch("http://localhost:5000/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            char: player_data.char,
            token: "acoroavelada2026",
            data: player_data
        })
    });

    const data = await res.json();

    if (!res.ok) {
        console.error("Erro ao salvar:", data);
        return;
    }

    console.log("Salvo com sucesso:", data);
}