const overlay = document.getElementById("overlay")

overlay.addEventListener("click", () => {
    document.dispatchEvent(new CustomEvent("overlay:click"))
})

export function showOverlay(){
    overlay.classList.add("active")
}

export function hideOverlay(){
    overlay.classList.remove("active")
}
