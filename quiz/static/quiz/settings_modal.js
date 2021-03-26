//to make autofocus work in settings modal
$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus()
})

const timerEnabled = document.querySelector("input[name='timer-enabled']")
const timerDiv = document.querySelector('.timer')
const timerDurationInp = document.querySelector(".timer input[type='number']")
const timerStartDateInp = document.querySelector(".timer input[type='date']")
const timerStartTimeInp = document.querySelector(".timer input[type='time']")
const inputs = [...timerDiv.querySelectorAll('input')]

timerEnabled.addEventListener('change', e => {
    if (e.target.checked) {
        timerDiv.style.display = 'flex'
        timerDurationInp.focus()
        validate()
    }
    else {
        timerDiv.style.display = 'none'
        saveSettingsBtn.disabled = false
    }
})

//only enable save button when all inputs have some value
function validate() {
    let isIncomplete = inputs.some(input => !input.value);
    saveSettingsBtn.disabled = isIncomplete;
}

timerDiv.addEventListener('input', validate);

const saveSettingsBtn = document.querySelector('#saveSettings')
const cancelSettingsBtn = document.querySelector('#cancelSettings')
let checked = timerEnabled.checked
let timerDuration = timerDurationInp.value
let timerStartDate = timerStartDateInp.value
let timerStartTime = timerStartTimeInp.value

cancelSettingsBtn.addEventListener('click', () => {
    checked ? timerDiv.style.display = 'flex' : timerDiv.style.display = 'none'
    timerEnabled.checked = checked
    timerDurationInp.value = timerDuration
    timerStartDateInp.value = timerStartDate
    timerStartTimeInp.value = timerStartTime
})

saveSettingsBtn.addEventListener('click', () => {
    checked = timerEnabled.checked
    timerDuration = timerDurationInp.value
    timerStartDate = timerStartDateInp.value
    timerStartTime = timerStartTimeInp.value
})


//not allowing to type - on numpad, - on number row, e , +, .
timerDurationInp.onkeydown = e => {
    if (e.keyCode == 109 || e.keyCode == 189 || e.keyCode == 69 || e.keyCode == 107 || e.keyCode == 187 || e.keyCode == 190 || e.keyCode == 110) return false
}


//allow only positive numbers to be pasted
timerDurationInp.addEventListener('paste', e => {
    e.preventDefault()
    //regex to extract only digits
    const paste = parseInt(e.clipboardData.getData('text').replace(/[^\d]/g, ''))
    e.target.value = Math.abs(paste)
})