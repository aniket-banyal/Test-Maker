document.querySelectorAll('.add_mcq_choice').forEach(add_mcq_choice_text_inp => {
    add_mcq_choice_text_inp.addEventListener('click', addMcqChoice)
    add_mcq_choice_text_inp.addEventListener('input', addMcqChoice)

    add_choice_radio_inp = add_mcq_choice_text_inp.parentElement.querySelector('input[type="radio"]')
    add_choice_radio_inp.addEventListener('click', addMcqChoice)
})

document.querySelectorAll('.add_checkbox_choice').forEach(add_checkbox_choice_text_inp => {
    add_checkbox_choice_text_inp.addEventListener('click', addCheckboxChoice)
    add_checkbox_choice_text_inp.addEventListener('input', addCheckboxChoice)

    add_choice_checkbox_inp = add_checkbox_choice_text_inp.parentElement.querySelector('input[type="checkbox"]')
    add_choice_checkbox_inp.addEventListener('click', addCheckboxChoice)
})

document.querySelectorAll('.add_short_choice').forEach(add_short_choice_text_inp => {
    add_short_choice_text_inp.addEventListener('click', addShortChoice)
    add_short_choice_text_inp.addEventListener('input', addShortChoice)
})

function addMcqChoice(e) {
    _addChoice(e, question_type = 'mcq')
}

function addCheckboxChoice(e) {
    _addChoice(e, question_type = 'checkbox')
}

function addShortChoice(e) {
    const add_choice_text_inp = e.target
    const choice = add_choice_text_inp.parentElement

    const question = choice.parentElement
    const t_q_number = parseInt(question.querySelector('label').innerText)

    const i = question.querySelectorAll('.quiz-form__ans').length

    add_choice_text_inp.name = `${t_q_number}_short_${i}`
    add_choice_text_inp.required = true
    add_choice_text_inp.placeholder = `Answer ${i}`
    add_choice_text_inp.classList.remove('add_short_choice')

    add_choice_text_inp.removeEventListener('click', addShortChoice)
    add_choice_text_inp.removeEventListener('input', addShortChoice)

    choice.appendChild(createDeleteChoiceSvg(question_type = 'short'))

    choice.insertAdjacentElement('afterend', createAddChoiceDiv(question_type = 'short'))
}

function _addChoice(e, question_type) {
    if (e.target.type == 'text') {
        add_choice_text_inp = e.target
        choice = add_choice_text_inp.parentElement

        if (question_type == 'mcq')
            add_choice_radio_inp = choice.querySelector('input[type="radio"]')
        else if (question_type == 'checkbox')
            add_choice_checkbox_inp = choice.querySelector('input[type="checkbox"]')
    }
    else {
        if (question_type == 'mcq') {
            add_choice_radio_inp = e.target
            choice = add_choice_radio_inp.parentElement
        }
        else if (question_type == 'checkbox') {
            add_choice_checkbox_inp = e.target
            choice = add_choice_checkbox_inp.parentElement
        }

        add_choice_text_inp = choice.querySelector('input[type="text"]')
    }

    const question = choice.parentElement
    const t_q_number = parseInt(question.querySelector('label').innerText)

    const i = question.querySelectorAll('.quiz-form__ans').length

    add_choice_text_inp.name = `${t_q_number}_option${i}`
    add_choice_text_inp.required = true
    add_choice_text_inp.placeholder = `Option ${i}`
    add_choice_text_inp.classList.remove('add_mcq_choice')

    if (question_type == 'mcq') {
        add_choice_radio_inp.name = `${t_q_number}_radio_option`
        add_choice_radio_inp.value = i
        add_choice_radio_inp.required = true

        add_choice_text_inp.removeEventListener('click', addMcqChoice)
        add_choice_text_inp.removeEventListener('input', addMcqChoice)
        add_choice_radio_inp.removeEventListener('click', addMcqChoice)
    }
    else if (question_type == 'checkbox') {
        add_choice_checkbox_inp.name = `${t_q_number}_checkbox_${i}`

        add_choice_text_inp.removeEventListener('click', addCheckboxChoice)
        add_choice_text_inp.removeEventListener('input', addCheckboxChoice)
        add_choice_checkbox_inp.removeEventListener('click', addCheckboxChoice)
    }
    choice.appendChild(createDeleteChoiceSvg(question_type))

    choice.insertAdjacentElement('afterend', createAddChoiceDiv(question_type))
}