/**
 * usersettings.js — Load + Update user settings
 * URLs: /settings/get/  and  /settings/update/
 */

$(document).ready(function () {
    console.log("UserSettings JS loaded.");

    if (!$('#settingsForm').length) return;   // only run on settings page

    // ── LOAD SETTINGS ─────────────────────────────────────
    function loadSettings() {
        $.get('/settings/get/', function (res) {
            if (res.success && res.data) {
                $('#currency').val(res.data.currency    || '₹');
                $('#date_format').val(res.data.date_format || 'YYYY-MM-DD');
            }
        }).fail(function () {
            showMessage('Failed to load settings.', 'error');
        });
    }

    loadSettings();

    // ── SAVE SETTINGS ─────────────────────────────────────
    $('#settingsForm').submit(function (e) {
        e.preventDefault();

        var btn = $(this).find('button[type=submit]');
        btn.prop('disabled', true).text('Saving...');

        $.post('/settings/update/', $(this).serialize(), function (res) {
            if (res.success) {
                showMessage(res.message, 'success');
            } else {
                showMessage(res.message || 'Failed to save settings.', 'error');
            }
        }).fail(function () {
            showMessage('Error saving settings.', 'error');
        }).always(function () {
            btn.prop('disabled', false).text('Save Changes');
        });
    });

});