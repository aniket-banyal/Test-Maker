btn = document.querySelector('#submit')
hiddenBtn = document.querySelector('#hiddenSubmit')
btn.onclick = () => {
    hiddenBtn.click()
}