const add_choice_text_inps = document.querySelectorAll('.add_choice')
add_choice_text_inps.forEach(add_choice_text_inp => {
    add_choice_text_inp.addEventListener('click', addChoice)
    add_choice_text_inp.addEventListener('input', addChoice)

    add_choice_radio_inp = add_choice_text_inp.parentElement.querySelector('input[type="radio"]')
    add_choice_radio_inp.addEventListener('click', addChoice)
})

function addChoice(e) {
    if (e.target.type == 'text') {
        add_choice_text_inp = e.target
        choice = add_choice_text_inp.parentElement
        add_choice_radio_inp = choice.querySelector('input[type="radio"]')
    }
    else {
        add_choice_radio_inp = e.target
        choice = add_choice_radio_inp.parentElement
        add_choice_text_inp = choice.querySelector('input[type="text"]')
    }

    const question = choice.parentElement
    const t_q_number = parseInt(question.querySelector('label').innerText)

    const i = question.querySelectorAll('.quiz-form__ans').length

    add_choice_text_inp.name = `${t_q_number}_option${i}`
    add_choice_text_inp.required = true
    add_choice_text_inp.placeholder = `Option ${i}`
    add_choice_text_inp.classList.remove('add_choice')

    add_choice_radio_inp.name = `${t_q_number}_radio_option`
    add_choice_radio_inp.value = i
    add_choice_radio_inp.required = true

    choice.appendChild(createDeleteChoiceSvg())

    choice.insertAdjacentElement('afterend', createAddChoiceDiv())

    add_choice_text_inp.removeEventListener('click', addChoice)
    add_choice_text_inp.removeEventListener('input', addChoice)
    add_choice_radio_inp.removeEventListener('click', addChoice)
}