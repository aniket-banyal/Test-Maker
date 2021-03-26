const duplicateBtns = document.querySelectorAll('.duplicateBtn')
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

    // - 1 cuz we don't want to include the Add Option input
    const number_of_choices = parentQuestion.querySelectorAll('.quiz-form__ans input[type="radio"]').length - 1

    createQuestion(q_inp_value, r_inps_checked, o_inps_value, points_inp_value, number_of_choices)
}
