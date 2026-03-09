/**
 * utils.js — CSRF setup + global showMessage()
 * Load karo SABSE PEHLE base.html mein
 */

// ── CSRF SETUP ────────────────────────────────────────────
function getCsrfToken() {
    var name  = 'csrftoken';
    var value = null;
    if (document.cookie) {
        document.cookie.split(';').forEach(function (c) {
            c = c.trim();
            if (c.startsWith(name + '=')) {
                value = decodeURIComponent(c.substring(name.length + 1));
            }
        });
    }
    // fallback: hidden input
    if (!value) {
        var inp = document.querySelector('input[name=csrfmiddlewaretoken]');
        if (inp) value = inp.value;
    }
    return value;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', getCsrfToken());
        }
    }
});

// ── GLOBAL showMessage() ──────────────────────────────────
// Used by: expense.js, budget.js, dashboard.js, usersettings.js, account.js
function showMessage(msg, type) {
    type = type || 'info';
    var color = type === 'success' ? 'var(--green)' : type === 'error' ? 'var(--red)' : 'var(--accent2)';
    var icon  = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';

    var $div = $('#messageDiv');
    $div.stop(true, true)
        .html('<span style="color:' + color + '; font-weight:600;">' + icon + ' ' + msg + '</span>')
        .fadeIn(200);

    setTimeout(function () { $div.fadeOut(500); }, 3500);
}

// Alias — some files use showMsg
var showMsg = showMessage;