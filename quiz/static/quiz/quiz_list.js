//enalbe tooltips
$(function () {
    options = { 'trigger': 'manual' }
    $('[data-toggle="tooltip"]').tooltip(options)
})

//delete popup
$(function () {
    $('[data-toggle="confirm"]').jConfirm({ 'theme': 'bootstrap-4-white', size: 'medium' }).on('confirm', function (e) {
        e.preventDefault()
        id = $(this).data('id')
        form = document.getElementById(id)
        form.submit()
    })
})

//Share functionality
shareBtns = document.querySelectorAll('.share')
shareBtns.forEach(btn => {
    btn.onclick = e => {
        e.preventDefault()
        if (btn.getAttribute('data-timer-set') == 1) {
            const aux = document.createElement("input")
            aux.setAttribute("value", `https://ani-quiz-maker.herokuapp.com/take-quiz/${btn.getAttribute('data-value')}/register/`)
            document.body.appendChild(aux)
            aux.select()
            document.execCommand("copy")
            document.body.removeChild(aux)
            $(btn).tooltip('show')

            setTimeout(() => {
                $(btn).tooltip('hide')
            }, 1600)
        }
        else {
            $(btn).attr("data-original-title", "Please set the timer duration, Start Date and Start Time by going into Edit->Settings");
            $(btn).tooltip('show')

            setTimeout(() => {
                $(btn).tooltip('hide')
            }, 6000)
        }
    }
})

//3dot context menu
const menuBtns = document.querySelectorAll('svg')
let visible = false
let hideMenu

menuBtns.forEach(menuBtn => {
    menuBtn.addEventListener('click', (e) => {
        const el = e.currentTarget
        const parent = el.parentElement
        const menu = parent.querySelector('.more-menu')

        e.preventDefault()

        if (!visible) {
            visible = true
            parent.classList.add('show-more-menu')
            menu.setAttribute('aria-hidden', false)
            document.addEventListener('mousedown', hideMenu = function (e) { _hideMenu(e, parent) })
            // console.log('mousedown added')
        }
    })
})


function _hideMenu(e, el) {
    const menu = el.querySelector('.more-menu')

    if (menu.contains(e.target)) return

    if (visible) {
        visible = false
        el.classList.remove('show-more-menu')
        menu.setAttribute('aria-hidden', true)
        document.removeEventListener('mousedown', hideMenu)
    }
}

//duplicate functionality
form = document.querySelector('#duplicate_form')
submitBtn = document.querySelector('#submit')
duplicateDoneBtn = document.querySelector('#duplicateDone')

duplicateBtns = document.querySelectorAll('.duplicate')
duplicateBtns.forEach(btn => {
    btn.onclick = (e) => {
        id = e.srcElement.getAttribute('data-id')

        //handling the case if enter key is pressed
        form.onsubmit = () => {
            form.action = `/quiz/${id}/duplicate/`
            return true
        }

        duplicateDoneBtn.onclick = () => {
            submitBtn.click()
        }
    }
});

//clear modal form when cancel is pressed
$('#duplicateModal').on('hidden.bs.modal', function () {
    $(this).find('form').trigger('reset');
})

//to make autofocus work in duplicate modal
$('.modal').on('shown.bs.modal', function () {
    $(this).find('[autofocus]').focus();
});


//results
// resultBtn = document.querySelector('#resultBtn')
// resultBtn.onclick = (e) => {
//     // id = e.srcElement.getAttribute('data-id')




// }