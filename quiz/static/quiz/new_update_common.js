const saveBtn = document.querySelector('#save')
const addBtn = document.querySelector('#add')
const submitBtn = document.querySelector('#submit')
const form = document.querySelector('form')

let q_number = document.querySelectorAll('.quiz-form__quiz').length + 1

//to prevent form from submitting when enter is pressed in settings modal
form.addEventListener('keydown', (e) => {
    if (e.key == 'Enter') {
        if (e.target.nodeName == 'INPUT') {
            e.preventDefault()
            return false
        }
    }
})

saveBtn.onclick = () => { submitBtn.click() }

addBtn.onclick = () => { createQuestion() }


function createQuestion(q_inp_value = null, r_inps_checked = null, o_inps_value = null, points_inp_value = 1, number_of_choices = 4) {
    const question = document.createElement('div')
    question.classList.add("quiz-form__quiz")

    const label = document.createElement('label')
    label.setAttribute('for', `q_${q_number}`)
    label.innerHTML = `${q_number}.`

    const q_inp = document.createElement('input')
    q_inp.type = 'text'
    q_inp.name = `q_${q_number}`
    q_inp.id = `q_${q_number}`
    q_inp.classList.add('quiz-form__question')
    q_inp.required = true
    q_inp.value = q_inp_value

    question.appendChild(label)
    question.appendChild(q_inp)

    for (let i = 1; i < number_of_choices + 1; i++) {
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

    question.appendChild(createAddChoiceDiv())

    const footer = document.createElement('div')
    footer.classList.add('footer')

    const point = document.createElement('div')
    point.classList.add('point')

    const points_inp = document.createElement('input')
    points_inp.type = 'number'
    points_inp.name = `${q_number}_point`
    points_inp.value = points_inp_value
    points_inp.required = true
    points_inp.min = 0

    span = document.createElement('span')
    span.innerHTML = 'points'

    point.appendChild(points_inp)
    point.appendChild(span)

    div = document.createElement('div')
    div.classList.add('footerBtns')

    const duplicateBtn = document.createElement('button')
    duplicateBtn.type = 'button'
    duplicateBtn.classList.add('duplicateBtn')
    duplicateBtn.innerHTML = 'Duplicate'
    duplicateBtn.addEventListener('click', duplicateQuestion)

    const deleteBtn = document.createElement('button')
    deleteBtn.type = 'button'
    deleteBtn.classList.add('deleteBtn')
    deleteBtn.innerHTML = 'Delete'
    deleteBtn.addEventListener('click', deleteQuestion)

    div.appendChild(duplicateBtn)
    div.appendChild(deleteBtn)
    footer.appendChild(point)
    footer.appendChild(div)
    question.appendChild(footer)

    form.appendChild(question)

    q_number++

    q_inp.focus()
    question.scrollIntoView()
}

//add new choice
const add_choice_text_inps = document.querySelectorAll('.add_choice')
add_choice_text_inps.forEach(add_choice_text_inp => {
    add_choice_text_inp.addEventListener('click', addOptionClickHandler)
    add_choice_text_inp.addEventListener('input', addOptionClickHandler)

    add_choice_radio_inp = add_choice_text_inp.parentElement.querySelector('input[type="radio"]')
    add_choice_radio_inp.addEventListener('click', addOptionClickHandler)
})

function addOptionClickHandler(e) {
    if (e.target.type == 'text') {
        add_choice_text_inp = e.target
        parentAnswer = add_choice_text_inp.parentElement
        add_choice_radio_inp = parentAnswer.querySelector('input[type="radio"]')
    }
    else {
        add_choice_radio_inp = e.target
        parentAnswer = add_choice_radio_inp.parentElement
        add_choice_text_inp = parentAnswer.querySelector('input[type="text"]')
    }

    const parentQuestion = parentAnswer.parentElement
    const t_q_number = parseInt(parentQuestion.querySelector('label').innerText)

    const i = parentQuestion.querySelectorAll('.quiz-form__ans').length

    add_choice_text_inp.name = `${t_q_number}_option${i}`
    add_choice_text_inp.required = true
    add_choice_text_inp.placeholder = `Option ${i}`
    add_choice_text_inp.classList.remove('add_choice')

    add_choice_radio_inp.name = `${t_q_number}_radio_option`
    add_choice_radio_inp.value = i
    add_choice_radio_inp.required = true

    parentAnswer.insertAdjacentElement('afterend', createAddChoiceDiv())

    add_choice_text_inp.removeEventListener('click', addOptionClickHandler)
    add_choice_text_inp.removeEventListener('input', addOptionClickHandler)
    add_choice_radio_inp.removeEventListener('click', addOptionClickHandler)
}

function createAddChoiceDiv() {
    const div = document.createElement('div')
    div.classList.add('quiz-form__ans')

    const r_inp = document.createElement('input')
    r_inp.type = 'radio'
    r_inp.addEventListener('click', addOptionClickHandler)

    const span = document.createElement('span')
    span.classList.add('design')

    const o_inp = document.createElement('input')
    o_inp.type = 'text'
    o_inp.placeholder = 'Add Option'
    o_inp.classList.add('add_choice')
    o_inp.addEventListener('click', addOptionClickHandler)
    o_inp.addEventListener('input', addOptionClickHandler)

    div.appendChild(r_inp)
    div.appendChild(span)
    div.appendChild(o_inp)
    return div
}

//duplicate question
duplicateBtns = document.querySelectorAll('.duplicateBtn')
duplicateBtns.forEach(duplicateBtn => duplicateBtn.addEventListener('click', duplicateQuestion))

function duplicateQuestion(e) {
    const parentQuestion = e.target.parentElement.parentElement.parentElement
    const q_inp_value = parentQuestion.querySelector('.quiz-form__question').value
    let r_inps_checked = []
    let o_inps_value = []

    for (r_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="radio"]'))
        r_inps_checked.push(r_inp.checked)

    for (o_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="text"]'))
        o_inps_value.push(o_inp.value)

    const points_inp_value = parentQuestion.querySelector('.footer input[type="number"]').value
    const number_of_choices = parentQuestion.querySelectorAll('.quiz-form__ans input[type="radio"]').length - 1
    createQuestion(q_inp_value, r_inps_checked, o_inps_value, points_inp_value, number_of_choices)
}


//delete question
const deleteBtns = document.querySelectorAll('.deleteBtn')
deleteBtns.forEach(deleteBtn => deleteBtn.addEventListener('click', deleteQuestion))

function deleteQuestion(e) {
    const parentQuestion = e.target.parentElement.parentElement.parentElement
    parentQuestion.remove()

    //dont make this let cuz we wanna acess global q_number
    q_number = 1
    questions = document.querySelectorAll('.quiz-form__quiz')
    for (question of questions) {
        label = question.querySelector('label')
        label.setAttribute('for', `q_${q_number}`)
        label.innerHTML = `${q_number}.`

        q_inp = question.querySelector('.quiz-form__question')
        q_inp.name = `q_${q_number}`
        q_inp.id = `q_${q_number}`

        for (r_inp of question.querySelectorAll('.quiz-form__ans input[type="radio"]')) {
            r_inp.name = `${q_number}_radio_option`
        }

        let i = 1
        for (o_inp of question.querySelectorAll('.quiz-form__ans input[type="text"]')) {
            o_inp.name = `${q_number}_option${i}`
            i++
        }

        points_inp = question.querySelector('.footer input[type="number"]')
        points_inp.name = `${q_number}_point`

        q_number++
    }
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
    const paste = parseInt(e.clipboardData.getData('text').replace(/[^\d]/g, ''))
    e.target.value = Math.abs(paste)
})