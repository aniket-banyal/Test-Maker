function createQuestion(question_type, q_inp_value = null, r_inps_checked = null, o_inps_value = null, points_inp_value = 1, number_of_choices = 4) {
    const { question, q_inp } = createQuestionLabelAndInput(q_inp_value)

    createOptions(number_of_choices, question_type, r_inps_checked, o_inps_value, question)

    createQuestionFooter(points_inp_value, question_type, question)

    q_number++

    q_inp.focus()
    question.scrollIntoView()
}

function createQuestionLabelAndInput(q_inp_value) {
    const question = document.createElement('div')
    question.classList.add("question")

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

    return { question, q_inp }
}

function createOptions(number_of_choices, question_type, r_inps_checked, o_inps_value, question) {

    if (question_type == 'short') {
        createShortAnswerOption(question_type, number_of_choices, o_inps_value, question)
        return
    }

    for (let i = 1; i < number_of_choices + 1; i++) {
        div = document.createElement('div')
        div.classList.add('quiz-form__ans')

        if (question_type == 'mcq') {
            r_inp = document.createElement('input')
            r_inp.type = 'radio'
            r_inp.name = `${q_number}_radio_option`
            r_inp.value = i
            r_inp.required = true
            if (r_inps_checked != null) r_inp.checked = r_inps_checked[i - 1]

            span = document.createElement('span')
            span.classList.add('design')

            div.appendChild(r_inp)
            div.appendChild(span)
        }
        else if (question_type == 'checkbox') {
            c_inp = document.createElement('input')
            c_inp.type = 'checkbox'
            c_inp.name = `${q_number}_checkbox_${i}`
            if (r_inps_checked != null) c_inp.checked = r_inps_checked[i - 1]
            div.appendChild(c_inp)
        }

        o_inp = document.createElement('input')
        o_inp.type = 'text'
        o_inp.name = `${q_number}_option${i}`
        o_inp.placeholder = `Option ${i}`
        o_inp.required = true
        if (o_inps_value != null) o_inp.value = o_inps_value[i - 1]

        div.appendChild(o_inp)

        div.appendChild(createDeleteChoiceSvg(question_type))

        question.appendChild(div)
    }

    question.appendChild(createAddChoiceDiv(question_type))
}

function createShortAnswerOption(question_type, number_of_choices, t_inps_value, question) {
    for (let i = 1; i < number_of_choices + 1; i++) {
        div = document.createElement('div')
        div.classList.add('quiz-form__ans')

        t_inp = document.createElement('input')
        t_inp.type = 'text'
        t_inp.name = `${q_number}_short_${i}`
        t_inp.placeholder = `Answer ${i}`
        t_inp.required = true
        if (t_inps_value != null) t_inp.value = t_inps_value[i - 1]

        div.appendChild(t_inp)

        div.appendChild(createDeleteChoiceSvg(question_type))
        question.appendChild(div)
    }

    question.appendChild(createAddChoiceDiv(question_type))
}

function createQuestionFooter(points_inp_value, question_type, question) {
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

    createFooterButtons(question_type)

    footer.appendChild(point)
    footer.appendChild(div)
    question.appendChild(footer)

    form.appendChild(question)
}

function createFooterButtons(question_type) {
    div = document.createElement('div')
    div.classList.add('footerBtns')

    const duplicateBtn = document.createElement('button')
    duplicateBtn.type = 'button'
    duplicateBtn.classList.add('duplicateBtn')
    duplicateBtn.innerHTML = 'Duplicate'

    if (question_type == 'mcq') {
        duplicateBtn.classList.add('mcqDuplicateBtn')
        duplicateBtn.addEventListener('click', duplicateMcqQuestion)
    }
    else if (question_type == 'checkbox') {
        duplicateBtn.classList.add('checkboxDuplicateBtn')
        duplicateBtn.addEventListener('click', duplicateCheckboxQuestion)
    }
    else if (question_type == 'short') {
        duplicateBtn.classList.add('shortDuplicateBtn')
        duplicateBtn.addEventListener('click', duplicateShortQuestion)
    }

    const deleteBtn = document.createElement('button')
    deleteBtn.type = 'button'
    deleteBtn.classList.add('deleteBtn')
    deleteBtn.innerHTML = 'Delete'
    deleteBtn.addEventListener('click', deleteQuestion)

    div.appendChild(duplicateBtn)
    div.appendChild(deleteBtn)
}


function createAddChoiceDiv(question_type) {
    const div = document.createElement('div')
    div.classList.add('quiz-form__ans')

    if (question_type == 'short') return createAddShortAnswerDiv(div)

    if (question_type == 'mcq') {
        const r_inp = document.createElement('input')
        r_inp.type = 'radio'
        r_inp.addEventListener('click', addMcqChoice)

        const span = document.createElement('span')
        span.classList.add('design')

        div.appendChild(r_inp)
        div.appendChild(span)
    }
    else if (question_type == 'checkbox') {
        const c_inp = document.createElement('input')
        c_inp.type = 'checkbox'
        c_inp.addEventListener('click', addCheckboxChoice)

        div.appendChild(c_inp)
    }

    const o_inp = document.createElement('input')
    o_inp.type = 'text'
    o_inp.placeholder = 'Add Option'

    if (question_type == 'mcq') {
        o_inp.classList.add('add_mcq_choice')
        o_inp.addEventListener('click', addMcqChoice)
        o_inp.addEventListener('input', addMcqChoice)
    }
    else if (question_type == 'checkbox') {
        o_inp.classList.add('add_checkbox_choice')
        o_inp.addEventListener('click', addCheckboxChoice)
        o_inp.addEventListener('input', addCheckboxChoice)
    }

    div.appendChild(o_inp)
    return div
}

function createAddShortAnswerDiv(div) {
    const t_inp = document.createElement('input')
    t_inp.type = 'text'
    t_inp.placeholder = 'Add Answer'
    t_inp.addEventListener('click', addShortChoice)
    t_inp.addEventListener('input', addShortChoice)

    div.appendChild(t_inp)
    return div
}

function createDeleteChoiceSvg(question_type) {
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
    svg.setAttribute('width', '24')
    svg.setAttribute('height', '24')
    svg.setAttribute('viewBox', '0 0 24 24')
    svg.classList.add('delete_choice')
    svg.setAttribute('fill', '#5c626f')
    if (question_type == 'mcq')
        svg.addEventListener('click', deleteMcqChoice)
    else if (question_type == 'checkbox')
        svg.addEventListener('click', deleteCheckboxChoice)
    else if (question_type == 'short')
        svg.addEventListener('click', deleteShortChoice)

    path1 = document.createElementNS('http://www.w3.org/2000/svg', 'path')
    path1.setAttribute('d', 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z')

    path2 = document.createElementNS('http://www.w3.org/2000/svg', 'path')
    path2.setAttribute('d', 'M0 0h24v24H0z')
    path2.setAttribute('fill', 'none')

    svg.appendChild(path1)
    svg.appendChild(path2)

    return svg
}