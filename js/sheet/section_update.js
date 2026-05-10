import { getPlayerData } from "./main.js";
import { saveJson } from "./save_server.js";

/* ---------------- STATUS ---------------- */

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

/* ---------------- NOTES ---------------- */

export function addNote(name, description) {
    const now = new Date();

    const day = String(now.getDate()).padStart(2, "0");
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");

    const date = `${day}/${month}`;
    const time = `${hours}:${minutes}`;

    const player_data = getPlayerData();

    let id = 0;
    while (player_data.notes.some(item => item.id === id)) {
        id++;
    }

    player_data.notes.push({
        id,
        name,
        description,
        date,
        time
    });

    saveJson();
}

export function removeNote(id) {
    const player_data = getPlayerData();

    const index = player_data.notes.findIndex(note => note.id === id);
    if (index === -1) return;

    player_data.notes.splice(index, 1);

    saveJson();
}

export function editNote(id, new_name, new_description) {
    const player_data = getPlayerData();

    const note = player_data.notes.find(note => note.id === id);
    if (!note) return;

    if (new_name !== null && new_name !== undefined) {
        note.name = new_name;
    }

    if (new_description !== null && new_description !== undefined) {
        note.description = new_description;
    }

    saveJson();
}

/* ---------------- ITEMS ---------------- */

export function addItem(name, description) {
    const player_data = getPlayerData();

    let id = 0;
    while (player_data.items.some(item => item.id === id)) {
        id++;
    }

    player_data.items.push({
        id,
        name,
        description
    });

    saveJson();
}

export function removeItem(id) {
    const player_data = getPlayerData();

    const index = player_data.items.findIndex(item => item.id === id);
    if (index === -1) return;

    player_data.items.splice(index, 1);

    saveJson();
}

export function editItem(id, new_name, new_description) {
    const player_data = getPlayerData();

    const item = player_data.items.find(item => item.id === id);
    if (!item) return;

    if (new_name !== null && new_name !== undefined) {
        item.name = new_name;
    }

    if (new_description !== null && new_description !== undefined) {
        item.description = new_description;
    }

    saveJson();
}

/* ---------------- GOALS ---------------- */

export function updateAmbition(new_ambition) {
    if (!new_ambition || new_ambition.length === 0) return;

    document.getElementById("ambition_description").textContent = new_ambition;

    saveJson();
}

export function updateWish(new_wish) {
    if (!new_wish || new_wish.length === 0) return;

    document.getElementById("wish_description").textContent = new_wish;

    saveJson();
}