import { sendAlert } from "./toast.js"
import { getGameData } from "./main.js"
import { getPlayerData } from "./main.js"
import { saveJson } from "./save_server.js"

export function upgradeBloodPotency(up_levels){
    const player_data = getPlayerData()
    const game_data = getGameData()

    const act_nivel = player_data.bloodpotency
    const display_nivel = act_nivel + up_levels
    const xp_cost = getXpCost(act_nivel, display_nivel, game_data.xp_cost["bloodpotency"])

    const max_bp_gen = game_data.bloodpotency_generation[player_data.generation].max 

    if(display_nivel > max_bp_gen || xp_cost > player_data.xp){
        return
    }

    player_data.bloodpotency = display_nivel
    player_data.xp -= xp_cost;
    
    refreshXpViewer()
    refreshBloodPotency()
    saveJson()
}

export function upgradeSkill(id, key, up_levels){
    //Atributes and Skills
    const player_data = getPlayerData()
    const game_data = getGameData()
    const max_nivel = game_data.maxvalue_generation[player_data.generation]

    let keys = [
        "knowledges",
        "expertises",
        "talents",
        "atributes"
    ]

    if(!keys.includes(key)) return

    //---------------------------------
    const playerSkill = player_data[key]?.find(s => s.id === id)
    const act_nivel = playerSkill.value
    const display_nivel = act_nivel + up_levels
    const xp_cost = getXpCost(act_nivel, display_nivel, game_data.xp_cost[key])

    if(display_nivel > max_nivel || player_data.xp < xp_cost) return

    playerSkill.value = display_nivel
    player_data.xp -= xp_cost

    refreshXpViewer()
    refreshSkill(key, id)
    saveJson()
}

export function upgradeDiscipline(id){
    const player_data = getPlayerData()
    const game_data = getGameData()
    const max_nivel = game_data.maxvalue_generation[player_data.generation]

    const discipline = player_data.disciplines.find(discipline => discipline.id === id)
    const act_nivel = discipline.nivel
    const display_nivel = act_nivel + 1
    const xp_cost = getXpCost(act_nivel, display_nivel, game_data.xp_cost["disciplines"])

    if(display_nivel > max_nivel || player_data.xp < xp_cost) return

    discipline.nivel = display_nivel
    player_data.xp -= xp_cost;

    refreshXpViewer()
    refreshDiscipline(id)
    saveJson()
}

export function updateIconBallContainer(container, max_nivel, act_nivel){
    for(let i = 0; i < max_nivel; i++){
        container.children[i].classList.remove("active")
    }

    for(let i = 0; i < act_nivel; i++){
        container.children[i].classList.add("active")
    }
}

export function refreshXpViewer(){
    const player_data = getPlayerData()

    document.getElementById("xp").textContent = player_data.xp + "xp"
}

function refreshDiscipline(id){
    const player_data = getPlayerData()
    const game_data = getGameData()
    const max_nivel = game_data.maxvalue_generation[player_data.generation]
    const iconballcontainer = document.getElementById("discipline_"+id).querySelector(".iconballcontainer")
    
    updateIconBallContainer(iconballcontainer, max_nivel, player_data.disciplines.find(d => d.id === id).nivel)
}

function refreshBloodPotency(){
    const player_data = getPlayerData()
    const game_data = getGameData()

    const keys = [
        "bloodsurge",
        "sheal",
        "aheal",
        "hungerdices",
        "consumablebloods"
    ]

    keys.forEach((key) => {
        document.getElementById(key).textContent = game_data.bloodpotency.find(i => i.nivel === player_data.bloodpotency)[key]
    })

    const iconballcontainer = document.getElementById("bloodpotencycontainer")
    updateIconBallContainer(iconballcontainer, 10, player_data.bloodpotency)
}

function refreshSkill(key, id){
    let keys = [
        "knowledges",
        "expertises",
        "talents",
        "precedents",
        "atributes"
    ]

    if(!keys.includes(key)) return

    const player_data = getPlayerData()
    const game_data = getGameData()
    const max_nivel = game_data.maxvalue_generation[player_data.generation]
    
    let iconballcontainer = null

    switch(key){
        case("atributes"):
            iconballcontainer = document.getElementById("atribute_"+id).querySelector(".iconballcontainer")
            break
        default:
            iconballcontainer = document.getElementById(game_data[key][id].name).querySelector(".iconballcontainer")
            break
    }

    updateIconBallContainer(iconballcontainer, max_nivel, player_data[key].find(s => s.id === id).value) 
}

function getXpCost(act_nivel, display_nivel, multiplier){
    let xp_cost = 0

    const diff = display_nivel - act_nivel

    if(diff <= 0){
        return 0
    }

    for(let i = 0; i < diff; i++){
      const grow = (act_nivel + i) * multiplier
      xp_cost += grow > 0 ? grow : multiplier
    }

    return xp_cost
}