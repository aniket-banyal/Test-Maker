document.querySelectorAll('.mcqDuplicateBtn').forEach(duplicateBtn => duplicateBtn.addEventListener('click', duplicateMcqQuestion))

document.querySelectorAll('.checkboxDuplicateBtn').forEach(duplicateBtn => duplicateBtn.addEventListener('click', duplicateCheckboxQuestion))

document.querySelectorAll('.shortDuplicateBtn').forEach(duplicateBtn => duplicateBtn.addEventListener('click', duplicateShortQuestion))


function duplicateMcqQuestion(e) {
    _duplicateQuestion(e, question_type = 'mcq')
}


function duplicateCheckboxQuestion(e) {
    _duplicateQuestion(e, question_type = 'checkbox')
}


function duplicateShortQuestion(e) {
    _duplicateQuestion(e, question_type = 'short')
}

function _duplicateQuestion(e, question_type) {
    const parentQuestion = e.target.parentElement.parentElement.parentElement
    const q_inp_value = parentQuestion.querySelector('.quiz-form__question').value
    let r_inps_checked = []
    let o_inps_value = []

    if (question_type == 'mcq') {
        for (r_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="radio"]'))
            r_inps_checked.push(r_inp.checked)
    }
    else if (question_type == 'checkbox') {
        for (c_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="checkbox"]'))
            r_inps_checked.push(c_inp.checked)
    }

    for (o_inp of parentQuestion.querySelectorAll('.quiz-form__ans input[type="text"]'))
        o_inps_value.push(o_inp.value)

    const points_inp_value = parentQuestion.querySelector('.footer input[type="number"]').value

    // - 1 cuz we don't want to include the Add Option input
    const number_of_choices = parentQuestion.querySelectorAll('.quiz-form__ans input[type="text"]').length - 1

    createQuestion(question_type, q_inp_value, r_inps_checked, o_inps_value, points_inp_value, number_of_choices)
}
