const toast = document.querySelector("#toast") 
const toast_h4 = toast.querySelector("h4")

const duration = 2500
let is_alerting = false

export async function sendAlert(msg){
    if(is_alerting) return

    toast_h4.textContent = msg
    toast.classList.add("show")
    is_alerting = true

    await new Promise(r => setTimeout(r, duration))

    toast.classList.remove("show")
    is_alerting = false
}

