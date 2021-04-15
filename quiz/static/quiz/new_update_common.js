const saveBtn = document.querySelector('#save')
const addBtn = document.querySelector('#add')
const submitBtn = document.querySelector('#submit')
const form = document.querySelector('form')

let q_number = document.querySelectorAll('.question').length + 1

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

addBtn.onclick = () => { createQuestion(question_type = 'mcq') }

document.querySelector('#addMcq').addEventListener('click', () => createQuestion(question_type = 'mcq'))
document.querySelector('#addCheckbox').addEventListener('click', () => createQuestion(question_type = 'checkbox'))
document.querySelector('#addShort').addEventListener('click', () => createQuestion(question_type = 'short'))
