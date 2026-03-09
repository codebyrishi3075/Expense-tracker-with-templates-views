/**
 * dashboard.js — Load dashboard summary data
 */

function loadDashboard() {
    var month = $('#monthFilter').val() || '';
    var url   = '/dashboard/summary/';
    if (month) url += '?month=' + encodeURIComponent(month);

    $('#categoryTable').html('<tr><td colspan="5" class="loading-cell">Loading...</td></tr>');

    $.get(url, function (data) {
        if (!data.success) {
            showMessage('Failed to load dashboard: ' + (data.message || 'Unknown error'), 'error');
            $('#categoryTable').html('<tr><td colspan="5" class="error-msg-td">Failed to load data.</td></tr>');
            return;
        }

        var cur = data.currency || '₹';

        // Update stat cards
        $('#totalExpense').text(cur + ' ' + parseFloat(data.total_expense).toFixed(2));
        $('#remainingBudget').text(cur + ' ' + parseFloat(data.remaining_budget).toFixed(2));

        // Build category rows
        var html = '';
        if (!data.categories || data.categories.length === 0) {
            html = '<tr><td colspan="5" class="loading-cell" style="color:var(--muted);">No data for this period.</td></tr>';
        } else {
            data.categories.forEach(function (cat) {
                var status = cat.exceeded
                    ? '<span class="badge-danger">Exceeded</span>'
                    : '<span class="badge-success">OK</span>';

                var remainingColor = cat.remaining < 0 ? 'style="color:var(--red);"' : '';

                html +=
                    '<tr>' +
                        '<td>' + cat.category + '</td>' +
                        '<td>' + cur + ' ' + parseFloat(cat.spent).toFixed(2) + '</td>' +
                        '<td>' + (cat.budget > 0 ? cur + ' ' + parseFloat(cat.budget).toFixed(2) : '—') + '</td>' +
                        '<td ' + remainingColor + '>' + cur + ' ' + parseFloat(cat.remaining).toFixed(2) + '</td>' +
                        '<td>' + status + '</td>' +
                    '</tr>';
            });
        }

        $('#categoryTable').html(html);

    }).fail(function (xhr) {
        var msg = (xhr.responseJSON && xhr.responseJSON.message) ? xhr.responseJSON.message : 'Server error.';
        showMessage('Dashboard error: ' + msg, 'error');
        $('#categoryTable').html('<tr><td colspan="5" class="error-msg-td">Failed to load data.</td></tr>');
    });
}

$(document).ready(function () {
    console.log("Dashboard JS loaded.");

    // Load on page open
    loadDashboard();

    // Month filter change
    $('#monthFilter').on('change', function () {
        loadDashboard();
    });

    // Clear filter
    $('#clearMonthBtn').on('click', function () {
        $('#monthFilter').val('');
        loadDashboard();
    });
});