const delete_choice_btns = document.querySelectorAll('.delete_choice')
delete_choice_btns.forEach(delete_choice_btn => delete_choice_btn.addEventListener('click', deleteChoice))

function deleteChoice(e) {
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

        r_inp = option.querySelector('input[type="radio"]')
        r_inp.value = i + 1

        o_inp = option.querySelector('input[type="text"]')
        o_inp.name = `${t_q_number}_option${i + 1}`
        o_inp.placeholder = `Option ${i + 1}`
    }
}
