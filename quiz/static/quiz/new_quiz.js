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

let q_number = 2

saveBtn.onclick = () => {
    submitBtn.click()
}

addBtn.onclick = () => {
    createQuestion()
}

function createQuestion(q_inp_value = null, r_inps_checked = null, o_inps_value = null, points_inp_value = 1) {
    question = document.createElement('div')
    question.classList.add("quiz-form__quiz")

    label = document.createElement('label')
    label.setAttribute('for', `q_${q_number}`)
    label.innerHTML = `${q_number}.`

    q_inp = document.createElement('input')
    q_inp.type = 'text'
    q_inp.name = `q_${q_number}`
    q_inp.id = `q_${q_number}`
    q_inp.classList.add('quiz-form__question')
    q_inp.required = true
    q_inp.value = q_inp_value

    question.appendChild(label)
    question.appendChild(q_inp)

    for (let i = 1; i < 4 + 1; i++) {
        div = document.createElement('div')
        div.classList.add('quiz-form__ans')

        r_inp = document.createElement('input')
        r_inp.type = 'radio'
        r_inp.name = `${q_number}_radio_option`
        r_inp.value = i
        r_inp.required = true
        if (r_inps_checked != null) r_inp.checked = r_inps_checked[i - 1]

        span = document.createElement('span')
        span.classList.add('design')

        o_inp = document.createElement('input')
        o_inp.type = 'text'
        o_inp.name = `${q_number}_option${i}`
        o_inp.placeholder = `Option ${i}`
        o_inp.required = true
        if (o_inps_value != null) o_inp.value = o_inps_value[i - 1]

        div.appendChild(r_inp)
        div.appendChild(span)
        div.appendChild(o_inp)
        question.appendChild(div)
    }

    footer = document.createElement('div')
    footer.classList.add('footer')

    point = document.createElement('div')
    point.classList.add('point')

    points_inp = document.createElement('input')
    points_inp.type = 'number'
    points_inp.name = `${q_number}_point`
    points_inp.value = points_inp_value
    points_inp.required = true
    points_inp.min = 0

    span = document.createElement('span')
    span.innerHTML = 'points'

    point.appendChild(points_inp)
    point.appendChild(span)

    duplicateBtn = document.createElement('button')
    duplicateBtn.type = 'button'
    duplicateBtn.classList.add('duplicateBtn')
    duplicateBtn.innerHTML = 'Duplicate'
    duplicateBtn.addEventListener('click', duplicateQuestion)

    footer.appendChild(point)
    footer.appendChild(duplicateBtn)
    question.appendChild(footer)

    form.appendChild(question)

    q_number++

    q_inp.focus()
    question.scrollIntoView()
}


//duplicate question
duplicateBtns = document.querySelectorAll('.duplicateBtn')
duplicateBtns.forEach(duplicateBtn => duplicateBtn.addEventListener('click', duplicateQuestion))

function duplicateQuestion(e) {
    const parentQuestion = e.target.parentElement.parentElement
    const q_inp_value = parentQuestion.querySelector('.quiz-form__question').value
    let r_inps_checked = []
    let o_inps_value = []

    for (r_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="radio"]'))
        r_inps_checked.push(r_inp.checked)

    for (o_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="text"]'))
        o_inps_value.push(o_inp.value)

    points_inp_value = parentQuestion.querySelector('.footer input[type="number"]').value

    createQuestion(q_inp_value, r_inps_checked, o_inps_value, points_inp_value)
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
let checked = false, timerDuration = '', timerStartDate = '', timerStartTime = ''

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