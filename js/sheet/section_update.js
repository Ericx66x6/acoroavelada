import { getPlayerData } from "./main.js";
import { saveJson } from "./save_server.js";

export function updateStatus(status, value) {
    const keys = {
        hunger: { max: 6 },
        humanity: { max: 5 },
        sdamage: { max: 10 },
        adamage: { max: 10 },
        willpower: { max: 10 },
        inspiration: { max: 1 }
    };

    const key = keys[status];
    if (!key) return;

    const element = document.getElementById(status);
    if (!element) return;

    const current = Number(element.textContent) || 0;
    const next = current + value;

    if (next < 0 || next > key.max) return;

    element.textContent = next;
}

export function addItem(name, description){
    const player_data = getPlayerData()
    
    //Encontrar um ID vazio
    let id = 0
    
    while(player_data.items.some(item => item.id === id)){
        id++
    }
    
    player_data.items.push({
        "id":id,
        "name":name,
        "description":description,
    })

    saveJson()
}

export function removeItem(id){
    const player_data = getPlayerData()

    const index = player_data.items.findIndex(item => item.id === id)
    if (index === -1) return

    player_data.items.splice(index, 1)

    saveJson()
}

export function editItem(id, new_name, new_description){
    const player_data = getPlayerData()

    const item = player_data.items.find(item => item.id === id)

    if(!item){
        console.log("retornou na section_update 1")
        return
    }

    item.name = new_name
    item.description = new_description

    saveJson()
}

export function updateAmbition(new_ambition){
    if(new_ambition.length === 0){
        return
    }

    document.getElementById("ambition_description").textContent = new_ambition

    saveJson()
}

export function updateWish(new_wish){
    if(new_wish.length === 0){
        return
    }

    document.getElementById("wish_description").textContent = 
    
    saveJson()
}