document.querySelectorAll('.delete_mcq_choice').forEach(delete_choice_btn => delete_choice_btn.addEventListener('click', deleteMcqChoice))

document.querySelectorAll('.delete_checkbox_choice').forEach(delete_choice_btn => delete_choice_btn.addEventListener('click', deleteCheckboxChoice))

document.querySelectorAll('.delete_short_choice').forEach(delete_choice_btn => delete_choice_btn.addEventListener('click', deleteShortChoice))


function deleteMcqChoice(e) {
    _deleteChoice(e, question_type = 'mcq')
}


function deleteCheckboxChoice(e) {
    _deleteChoice(e, question_type = 'checkbox')
}


function deleteShortChoice(e) {
    if (e.target.classList.contains('delete_choice')) delete_choice_btn = e.target
    else delete_choice_btn = e.target.parentElement

    option = delete_choice_btn.parentElement
    const question = option.parentElement
    const t_q_number = parseInt(question.querySelector('label').innerText)

    option.remove()

    const options = question.querySelectorAll('.quiz-form__ans')

    //options.length-1 cuz we don't wanna modify the Add Option inputs
    for (i = 0; i < options.length - 1; i++) {
        option = options[i]

        t_inp = option.querySelector('input[type="text"]')
        t_inp.name = `${t_q_number}_short_${i + 1}`
        t_inp.placeholder = `Answer ${i + 1}`
    }
}


function _deleteChoice(e, question_type) {
    if (e.target.classList.contains('delete_choice')) delete_choice_btn = e.target
    else delete_choice_btn = e.target.parentElement

    option = delete_choice_btn.parentElement
    const question = option.parentElement
    const t_q_number = parseInt(question.querySelector('label').innerText)

    option.remove()

    const options = question.querySelectorAll('.quiz-form__ans')

    //options.length-1 cuz we don't wanna modify the Add Option inputs
    for (i = 0; i < options.length - 1; i++) {
        option = options[i]

        if (question_type == 'mcq') {
            r_inp = option.querySelector('input[type="radio"]')
            r_inp.value = i + 1
        }
        else if (question_type == 'checkbox') {
            c_inp = option.querySelector('input[type="checkbox"]')
            c_inp.name = `${t_q_number}_checkbox_${i + 1}`
        }

        o_inp = option.querySelector('input[type="text"]')
        o_inp.name = `${t_q_number}_option${i + 1}`
        o_inp.placeholder = `Option ${i + 1}`
    }
}
