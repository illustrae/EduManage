document.querySelectorAll('#copy-icon').forEach(icon => {
    icon.addEventListener('click', (event) => {
        const input=event.target.parentElement.localName == "td" ? event.target.parentElement.previousElementSibling
        :event.target.previousElementSibling
        copyWord(input)
    })
})

const copyWord = input => {
    const savedValue = input.localName == "input" ? input.value : input.innerHTML; 
    navigator.clipboard.writeText(savedValue);
    if(input.localName == "input"){
        input.value = "Copied!"
        setTimeout(()=>input.value = savedValue, 1000);
    }else{
        input.innerHTML = "Copied!"
        setTimeout(()=>input.innerHTML = savedValue, 1000);
    }
}