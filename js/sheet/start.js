import { getPlayerData } from "./main.js"
import { getGameData } from "./main.js"
import { startNavbar } from "./navbar.js"

let player_data = null
let game_data = null
let max_value = null

export function startSheet() {
    player_data = getPlayerData()
    game_data = getGameData()
    max_value = game_data.maxvalue_generation[player_data.generation]

    startSkills();
    startOverview();
    startStatus();
    startBloodPotency();
    startAtributes();
    startDisciplines();
    startRituals();
    startItems();
    startGoals();
    startMorality();
    startNavbar();
    startCaracteristics();
}

function startSkills(){

    const talents_container = document.querySelector("#talentscontainer");
    const expertises_container = document.querySelector("#expertisescontainer");
    const knowledges_container = document.querySelector("#knowledgescontainer");
    const precedents_container = document.querySelector("#precedentscontainer");

    let knowledges_array = game_data.knowledges.map(item => item.name)
    let expertises_array = game_data.expertises.map(item => item.name)
    let talents_array = game_data.talents.map(item => item.name)
    let precedents_array = game_data.precedents.map(item => item.name)

    createSkillsByList(talents_container, talents_array, "talents");
    createSkillsByList(expertises_container, expertises_array, "expertises");
    createSkillsByList(knowledges_container, knowledges_array, "knowledges");
    createSkillsByList(precedents_container, precedents_array, "precedents");
}

function startOverview(){
    const map = {
        charname: player_data.char.toUpperCase(),
        playername: player_data.player,
        cla: player_data.cla,
        generation: `${player_data.generation}th Geração`,
        xp: `${player_data.xp}xp`
    };

    for (let key in map) {
        document.querySelector(`#${key}`).textContent = map[key];
    }

    document.querySelector("#profilepicture").src = player_data.profilepicture;
}

function startStatus(){

    const status = player_data.status;

    const map = {
        hunger: "#hunger",
        humanity: "#humanity",
        sdamage: "#sdamage",
        adamage: "#adamage",
        willpower: "#willpower",
        inspiration: "#inspiration"
    };

    for (let key in map) {
        document.querySelector(map[key]).textContent = status[key];
    }
}

function startBloodPotency(){

    const bpcontainer = document.querySelector("#bloodpotencycontainer");
    const bp_nivel = player_data.bloodpotency;
    const bp_game_data = game_data.bloodpotency.find(item => item.nivel === bp_nivel);

    [...bpcontainer.children].forEach((el, i) => {
        el.classList.toggle("active", i < bp_nivel);
        el.dataset.upgrade = "bloodpotency"
        el.dataset.nivel = bp_nivel
    });

    const map = {
        bloodsurge: "#bloodsurge",
        sheal: "#sheal",
        aheal: "#aheal",
        hungerdices: "#hungerdices",
        consumablebloods: "#consumablebloods"
    };

    for (let key in map) {
        document.querySelector(map[key]).textContent = bp_game_data[key];
    }
}

function startAtributes(){

    for(let i = 0; i < 9; i++){

        const container = document.querySelector(`#atribute_${i} .iconballcontainer`);
        const h3_container = document.querySelector(`#atribute_${i} .elementtitlecontainer`)
        const h3 = h3_container.querySelector(".elementtitle")

        const level = player_data.atributes[i].value;

        for(let i = 0; i < max_value; i++){
            const iconball = document.createElement("div");
            iconball.classList.add("iconball");
            container.appendChild(iconball);
        }

        for(let ball of container.children){
            ball.classList.remove("active");
            ball.dataset.upgrade = "atributes"
            ball.dataset.nivel = level
            ball.dataset.id = i
        }

        for(let j = 0; j < level; j++){
            container.children[j].classList.add("active");
        }

        h3_container.dataset.upgrade = "atributes"
        h3_container.dataset.nivel = level
        h3_container.dataset.id = i

        h3.dataset.upgrade = "atributes"
        h3.dataset.nivel = level
        h3.dataset.id = i
    }
}

function startDisciplines(){
    let count = player_data.disciplines.length

    for(let i = 0; i < count; i++){
        let discipline = game_data.disciplines[player_data.disciplines[i].id]
        createDiscipline(discipline.id, discipline.name, discipline.description, player_data.disciplines[i].nivel)
    }
}

function startRituals(){
    let count = player_data.rituals.length

    for(let i = 0; i < count; i++){
        let ritual = game_data.rituals[player_data.rituals[i].id]
        createRitual(ritual.id, ritual.name, ritual.short_description, ritual.nivel)
    }
}

export function startItems(){
    const items_container = document.querySelector("#items_container")     

    while (items_container.querySelectorAll(".elementcard").length > 1) {
        items_container.removeChild(items_container.querySelectorAll(".elementcard")[items_container.querySelectorAll(".elementcard").length - 1])
    }

    let items = player_data.items.length

    for(let i = 0; i < items; i++){
        createItem(player_data.items[i].name.toUpperCase(), player_data.items[i].description, player_data.items[i].id)
    }

    const money = document.querySelector("#money")
    money.textContent = "$ " + player_data.money
}

function startGoals(){
    const wish = document.querySelector("#wish_description")
    const ambition = document.querySelector("#ambition_description")

    ambition.textContent = player_data.goals[0].description
    wish.textContent = player_data.goals[1].description
}

function startMorality(){
    const principle = document.querySelector("#principle")
    const conviction_1 = document.querySelector("#conviction_1")
    const conviction_2 = document.querySelector("#conviction_2")
    const conviction_3 = document.querySelector("#conviction_3")

    principle.textContent = player_data.moralityes[0].description
    conviction_1.textContent = player_data.moralityes[1].description
    conviction_2.textContent = player_data.moralityes[2].description
    conviction_3.textContent = player_data.moralityes[3].description

}

function startCaracteristics(){
    const caracteristicsContainer = document.querySelector("#caracteristics_container")

    console.log(player_data)

    let count = player_data.caracteristics.length

    for(let i = 0; i < count; i++){
        let id = player_data.caracteristics[i].id

        createCaracteristic(id)
    }
}

export function createCaracteristic(id){
    const caracteristicsContainer = document.querySelector("#caracteristics_container")

    const elementcard = document.createElement("div")
    const elementheader = document.createElement("div")
    const elementtitle = document.createElement("h3")
    const expandicon = document.createElement("h5")
    const elementsubtitle = document.createElement("h3")
    const iconballcontainer = document.createElement("div")

    const elementList = [elementcard, elementheader, elementtitle, expandicon, elementsubtitle]

    elementList.forEach((item) => {
        item.dataset.upgrade = "caracteristic"
        item.dataset.id = id
    })

    elementheader.appendChild(elementtitle)
    elementheader.appendChild(expandicon)

    elementcard.appendChild(elementheader)
    elementcard.appendChild(elementsubtitle)
    elementcard.appendChild(iconballcontainer)

    elementcard.classList.add("elementcard")
    elementheader.classList.add("elementheader")
    expandicon.classList.add("expandicon")
    elementsubtitle.classList.add("elementsubtitle")
    iconballcontainer.classList.add("iconballcontainer")

    let caracteristic = game_data[caracteristics].find(c => c.id === id)

    elementtitle.textContent = caracteristic.name
    elementsubtitle.textContent = caracteristic.type.toUpperCase()

    let value = caracteristic.value

    for(let i = 0; i < max_value; i++){
        const iconball = document.createElement("div");
        iconball.classList.add("iconball");
        iconballcontainer.appendChild(iconball);

        iconball.dataset.upgrade = "caracteristic"
        iconball.dataset.id = id

        if(value > 0){
            iconball.classList.add("active")
            value--
        }
    }

    caracteristicsContainer.appendChild(elementcard)
}

export function createItem(name, description, id){
    const items_container = document.querySelector("#items_container")

    const elementcard = document.createElement("div")
    const elementheader = document.createElement("div")
    const img = document.createElement("img")
    const h3 = document.createElement("h3")
    const expandicon = document.createElement("h5")
    const divider = document.createElement("div")
    const elementdescription = document.createElement("p")

    const elementsList = [elementcard, elementheader, h3, img, expandicon, divider, elementdescription]

    elementsList.forEach((item) => {
        item.dataset.upgrade = "items"
        item.dataset.id = id
    })

    elementheader.appendChild(h3)
    elementheader.appendChild(expandicon)

    elementcard.appendChild(elementheader)
    
    elementcard.classList.add("elementcard")
    elementheader.classList.add("elementheader")
    img.classList.add("threshicon")
    img.src="img/threshicon.svg"
    expandicon.classList.add("expandicon")
    divider.classList.add("divider")
    elementdescription.classList.add("elementdescription")
    h3.classList.add("fullsize")

    h3.textContent = name
    elementdescription.textContent = description

    items_container.insertBefore(elementcard, items_container.children[1])
}

function createRitual(id, title, description, nivel){
    const rituals_container = document.querySelector("#rituals_container");
    
    const elementcard = document.createElement("div");
    const elementheader = document.createElement("div");
    const h3 = document.createElement("h3");
    const expandicon = document.createElement("h5");
    const elementsubtitle = document.createElement("h3");
    const divider = document.createElement("div");
    const elementdescription = document.createElement("p");

    const elementList = [elementcard, elementheader, h3, expandicon, elementdescription, elementsubtitle, divider]

    elementList.forEach((item) => {
        item.dataset.upgrade = "rituals"
        item.dataset.id = id
    })

    elementcard.classList.add("elementcard");
    elementheader.classList.add("elementheader");
    expandicon.classList.add("expandicon");
    elementsubtitle.classList.add("elementsubtitle");
    divider.classList.add("divider");
    elementdescription.classList.add("elementdescription");

    elementheader.appendChild(h3);
    elementheader.appendChild(expandicon);

    elementcard.appendChild(elementheader);
    elementcard.appendChild(elementsubtitle);
    elementcard.appendChild(divider);
    elementcard.appendChild(elementdescription);

    elementcard.id = id
    h3.textContent = title
    expandicon.textContent = "+"
    elementdescription.textContent = description
    elementsubtitle.textContent = "NIVEL "+nivel

    rituals_container.appendChild(elementcard)
}

function createDiscipline(id, title, description, nivel){

    const disciplines_container = document.querySelector("#disciplines_container");

    const elementcard = document.createElement("div");
    const elementheader = document.createElement("div");
    const h3 = document.createElement("h3");
    const expandicon = document.createElement("h5");
    const elementdescription = document.createElement("p");
    const iconballcontainer = document.createElement("div");

    const elementList = [elementcard, elementheader, h3, expandicon, elementdescription, iconballcontainer]

    elementList.forEach((item) => {
        item.dataset.upgrade = "disciplines"
        item.dataset.id = id
    })

    elementheader.classList.add("elementheader");
    expandicon.classList.add("expandicon");
    elementdescription.classList.add("elementdescription");
    iconballcontainer.classList.add("iconballcontainer");
    elementcard.classList.add("elementcard");

    h3.textContent = title;
    expandicon.textContent = "+";
    elementdescription.textContent = description;

    elementheader.appendChild(h3);
    elementheader.appendChild(expandicon);

    for(let i = 0; i < max_value; i++){
        const iconball = document.createElement("div");
        iconball.classList.add("iconball");
        iconballcontainer.appendChild(iconball);

        iconball.dataset.upgrade = "disciplines"
        iconball.dataset.id = id

        if(nivel > 0){
            iconball.classList.add("active")
            nivel--
        }
    }

    elementcard.appendChild(elementheader);
    elementcard.appendChild(elementdescription);
    elementcard.appendChild(iconballcontainer);

    elementcard.id = "discipline_"+id

    disciplines_container.appendChild(elementcard);
}

function createSkillsByList(container, list, key){

    for(let i = 0; i < list.length; i++){
        let element = document.createElement("div");
        let h3_container = document.createElement("div");
        let h3 = document.createElement("h3");
        let icon_ball_container = document.createElement("div");

        h3.textContent = list[i];

        h3_container.classList.add("elementtitlecontainer")
        h3.classList.add("elementtitle")
        element.classList.add("element");
        icon_ball_container.classList.add("iconballcontainer");

        h3_container.appendChild(h3);
        element.appendChild(h3_container);
        element.appendChild(icon_ball_container);

        let skill = player_data[key].find(a => a.id === (i));
        let level = skill ? skill.value : 0;

        for(let j = 0; j < max_value; j++){
            let icon_ball = document.createElement("div");
            icon_ball.classList.add("iconball");
            icon_ball.dataset.upgrade = key
            icon_ball.dataset.id = i
            icon_ball.dataset.nivel = level

            if(j < level){
                icon_ball.classList.add("active");
            }

            icon_ball_container.appendChild(icon_ball);
        }

        element.id = list[i];
        element.dataset.id = i;

        h3_container.dataset.upgrade = key
        h3_container.dataset.id = i
        h3_container.dataset.nivel = level
        h3.dataset.upgrade = key
        h3.dataset.id = i
        h3.dataset.nivel = level
        

        container.appendChild(element);
    }
}

