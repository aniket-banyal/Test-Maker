saveBtn = document.querySelector('#save')
addBtn = document.querySelector('#add')
submitBtn = document.querySelector('#submit')
form = document.querySelector('form')

//to prevent form from submitting when enter is pressed in settings modal
form.addEventListener('keydown', (e) => {
    if (e.keyCode == 13) {
        if (e.target.nodeName == 'INPUT') {
            e.preventDefault()
            return false
        }
    }
})

let q_number = document.querySelectorAll('.quiz-form__quiz').length + 1

saveBtn.onclick = () => {
    submitBtn.click()
}

addBtn.onclick = () => {
    quiz = document.createElement('div')
    quiz.classList.add("quiz-form__quiz")

    label = document.createElement('label')
    label.setAttribute('for', `q_${q_number}`)
    label.innerHTML = `${q_number}.`

    q_inp = document.createElement('input')
    q_inp.type = 'text'
    q_inp.name = `q_${q_number}`
    q_inp.id = `q_${q_number}`
    q_inp.classList.add('quiz-form__question')
    q_inp.required = true

    quiz.appendChild(label)
    quiz.appendChild(q_inp)

    for (let i = 1; i < 4 + 1; i++) {
        div = document.createElement('div')
        div.classList.add('quiz-form__ans')

        r_inp = document.createElement('input')
        r_inp.type = 'radio'
        r_inp.name = `${q_number}_radio_option`
        r_inp.value = i
        r_inp.required = true

        span = document.createElement('span')
        span.classList.add('design')

        o_inp = document.createElement('input')
        o_inp.type = 'text'
        o_inp.name = `${q_number}_option${i}`
        o_inp.placeholder = `Option ${i}`
        o_inp.required = true

        div.appendChild(r_inp)
        div.appendChild(span)
        div.appendChild(o_inp)
        quiz.appendChild(div)
    }

    footer = document.createElement('div')
    footer.classList.add('footer')

    point = document.createElement('div')
    point.classList.add('point')

    inp = document.createElement('input')
    inp.type = 'number'
    inp.name = `${q_number}_point`
    inp.value = 1
    inp.required = true
    inp.min = 0

    span = document.createElement('span')
    span.innerHTML = 'points'

    point.appendChild(inp)
    point.appendChild(span)
    footer.appendChild(point)
    quiz.appendChild(footer)

    form.appendChild(quiz)

    q_number++

    q_inp.focus()
    quiz.scrollIntoView();
}

//to make autofocus work in settings modal
$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus();
});

//settings
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
        saveSettingsBtn.disabled = true
    }
    else {
        timerDiv.style.display = 'none'
        saveSettingsBtn.disabled = false
    }
    validate()
})

//only enable save button when all inputs have some value
function validate() {
    let isIncomplete = inputs.some(input => !input.value);
    saveSettingsBtn.disabled = isIncomplete;
}

timerDiv.addEventListener('input', validate);

//save and cancel button in settings 
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

//save data in variables when SAVE btn is clicked
saveSettingsBtn.addEventListener('click', () => {
    checked = timerEnabled.checked
    timerDuration = timerDurationInp.value
    timerStartDate = timerStartDateInp.value
    timerStartTime = timerStartTimeInp.value
})

//not allowing to type - on numpad, - on number row, e and +
timerDurationInp.onkeydown = e => {
    if (e.keyCode == 109 || e.keyCode == 189 || e.keyCode == 69 || e.keyCode == 107 || e.keyCode == 187) return false
}

//allow only positive numbers to be pasted
timerDurationInp.addEventListener('paste', e => {
    e.preventDefault()
    //regex to replace all characters expect number
    let paste = parseInt(e.clipboardData.getData('text').replace(/[^\d]/g, ''))
    e.target.value = Math.abs(paste)
})