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

        //options.length-1 cuz we don't want to modify the Add Option inputs
        for (i = 0; i < options.length - 1; i++) {
            option = options[i]

            r_inp = option.querySelector('input[type="radio"]')
            r_inp.name = `${q_number}_radio_option`

            o_inp = option.querySelector('input[type="text"]')
            o_inp.name = `${q_number}_option${i}`
        }

        points_inp = question.querySelector('.footer input[type="number"]')
        points_inp.name = `${q_number}_point`

        q_number++
    }
}
