import { hideOverlay } from "./overlay.js"
import { showOverlay } from "./overlay.js"

const close_button = document.querySelector("#sidebar_cb")
const open_button = document.querySelector("#sidebar_ob")
const side_bar = document.querySelector("#side_bar")

close_button.addEventListener("click", () => {
    side_bar.classList.add("closed")
    hideOverlay()
})

open_button.addEventListener("click", () => {
    side_bar.classList.remove("closed")
    showOverlay()
})

export function closeSidebar(){
    close_button.click()
}

export function openSidebar(){
    open_button.click()
}

function startLI(){
    const li_list = document.querySelectorAll("li")

    li_list.forEach((li) => {
        li.addEventListener("click", () => {
            const targetId = li.dataset.section;
            const target = document.getElementById(targetId);

            if(target){
                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                })
            }

            closeSidebar();
        })
    })
}

startLI()