const deleteBtns = document.querySelectorAll('.deleteBtn')
deleteBtns.forEach(deleteBtn => deleteBtn.addEventListener('click', deleteQuestion))


function deleteQuestion(e) {
    const parentQuestion = e.target.parentElement.parentElement.parentElement
    parentQuestion.remove()

    //dont make this let cuz we wanna acess global q_number
    q_number = 1
    questions = document.querySelectorAll('.question')
    for (question of questions) {
        label = question.querySelector('label')
        label.setAttribute('for', `q_${q_number}`)
        label.innerHTML = `${q_number}.`

        q_inp = question.querySelector('.quiz-form__question')
        q_inp.name = `q_${q_number}`
        q_inp.id = `q_${q_number}`

        options = question.querySelectorAll('.quiz-form__ans')

        question_type = 'mcq'

        if (question.querySelectorAll('.quiz-form__ans input[type="checkbox"]').length > 0)
            question_type = 'checkbox'

        if (question.querySelectorAll('.quiz-form__ans input[type="checkbox"]').length == 0 &&
            question.querySelectorAll('.quiz-form__ans input[type="radio"]').length == 0) {
            question_type = 'short'
        }

        //options.length-1 cuz we don't want to modify the Add Option inputs
        for (i = 0; i < options.length - 1; i++) {
            option = options[i]

            if (question_type == 'mcq') {
                r_inp = option.querySelector('input[type="radio"]')
                r_inp.name = `${q_number}_radio_option`
            }
            else if (question_type == 'checkbox') {
                c_inp = option.querySelector('input[type="checkbox"]')
                c_inp.name = `${q_number}_checkbox_${i + 1}`
            }

            o_inp = option.querySelector('input[type="text"]')

            if (question_type == 'short')
                o_inp.name = `${q_number}_short_${i + 1}`

            else
                o_inp.name = `${q_number}_option${i + 1}`
        }

        points_inp = question.querySelector('.footer input[type="number"]')
        points_inp.name = `${q_number}_point`

        q_number++
    }
}
