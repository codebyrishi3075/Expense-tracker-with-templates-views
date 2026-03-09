/**
 * expense.js — Full CRUD with inline Edit Panel
 */
$(document).ready(function () {
    console.log("Expense JS loaded.");

    if (!$('#expenseForm').length) return;

    // ── LOAD CATEGORIES into both dropdowns ───────────────
    function loadCategoriesForExpense() {
        $.get('/budget/categories/list/', function (res) {
            if (!res.data) return;
            var opts = '<option value="">Select a category</option>';
            res.data.forEach(function (c) {
                opts += '<option value="' + c.id + '">' + c.name + '</option>';
            });
            $('#categorySelect').html(opts);
            $('#editCategorySelect').html(opts);
        });
    }
    loadCategoriesForExpense();
    loadExpenses();

    // ── CREATE ────────────────────────────────────────────
    $('#expenseForm').submit(function (e) {
        e.preventDefault();
        var amount   = $('input[name=amount]', this).val();
        var expDate  = $('input[name=date]', this).val();
        var category = $('#categorySelect').val();

        if (!amount || parseFloat(amount) <= 0) { showMessage('Please enter a valid amount.', 'error'); return; }
        if (!expDate)  { showMessage('Please select a date.', 'error'); return; }
        if (!category) { showMessage('Please select a category.', 'error'); return; }

        $.post('/expenses/create/', $(this).serialize(), function (res) {
            if (res.success) {
                showMessage(res.message, 'success');
                $('#expenseForm')[0].reset();
                loadExpenses();
            } else {
                showMessage(res.message, 'error');
            }
        }).fail(function () { showMessage('Error creating expense.', 'error'); });
    });

    // ── LOAD LIST ─────────────────────────────────────────
    function loadExpenses(page) {
        page = page || 1;
        $.get('/expenses/list/', { page: page, search: $('#searchInput').val() || '' }, function (res) {
            var html = '';
            if (!res.data || res.data.length === 0) {
                html = '<p class="empty-msg">No expenses found.</p>';
            } else {
                res.data.forEach(function (exp) {
                    html +=
                        '<div class="item-row expense-row">' +
                            '<div class="expense-info">' +
                                '<span class="item-name">' + (exp.category || 'Uncategorized') + '</span>' +
                                '<span class="item-meta">' +
                                    '₹' + parseFloat(exp.amount).toFixed(2) +
                                    ' &nbsp;|&nbsp; ' + exp.date +
                                    (exp.notes ? ' &nbsp;|&nbsp; ' + exp.notes : '') +
                                '</span>' +
                            '</div>' +
                            '<div class="expense-actions">' +
                                '<button class="btn-warning-sm edit-expense-btn"' +
                                    ' data-id="'          + exp.id          + '"' +
                                    ' data-category_id="' + (exp.category_id || '') + '"' +
                                    ' data-amount="'      + exp.amount      + '"' +
                                    ' data-date="'        + exp.date        + '"' +
                                    ' data-notes="'       + (exp.notes || '') + '">Edit</button>' +
                                '<button class="btn-danger-sm delete-expense-btn" data-id="' + exp.id + '">Delete</button>' +
                            '</div>' +
                        '</div>';
                });
            }
            $('#expenseList').html(html);
            renderPagination(res.num_pages, res.current_page);
        }).fail(function () { showMessage('Failed to load expenses.', 'error'); });
    }

    // ── OPEN EDIT PANEL ───────────────────────────────────
    $(document).on('click', '.edit-expense-btn', function () {
        $('#editExpenseId').val($(this).data('id'));
        $('#editCategorySelect').val($(this).data('category_id') || '');
        $('#editAmount').val($(this).data('amount'));
        $('#editDate').val($(this).data('date'));
        $('#editNotes').val($(this).data('notes') || '');

        $('#editPanel').show();
        $('#searchPanel').hide();
        $('html, body').animate({ scrollTop: $('#editPanel').offset().top - 20 }, 300);
    });

    // ── CANCEL EDIT ───────────────────────────────────────
    $('#cancelEditBtn').click(function () {
        $('#editPanel').hide();
        $('#searchPanel').show();
        $('#editExpenseForm')[0].reset();
    });

    // ── SUBMIT EDIT ───────────────────────────────────────
    $('#editExpenseForm').submit(function (e) {
        e.preventDefault();
        var id = $('#editExpenseId').val();

        $.post('/expenses/update/' + id + '/', $(this).serialize(), function (res) {
            if (res.success) {
                showMessage(res.message, 'success');
                $('#editPanel').hide();
                $('#searchPanel').show();
                $('#editExpenseForm')[0].reset();
                loadExpenses();
            } else {
                showMessage(res.message, 'error');
            }
        }).fail(function () { showMessage('Error updating expense.', 'error'); });
    });

    // ── DELETE ────────────────────────────────────────────
    $(document).on('click', '.delete-expense-btn', function () {
        if (!confirm('Delete this expense?')) return;
        $.post('/expenses/delete/' + $(this).data('id') + '/', function (res) {
            if (res.success) { showMessage(res.message, 'success'); loadExpenses(); }
            else { showMessage(res.message, 'error'); }
        }).fail(function () { showMessage('Error deleting expense.', 'error'); });
    });

    // ── PAGINATION ────────────────────────────────────────
    function renderPagination(total, current) {
        if (!total || total <= 1) { $('#pagination').html(''); return; }
        var html = '<div class="pagination">';
        for (var i = 1; i <= total; i++) {
            html += '<button class="page-btn' + (i === current ? ' active' : '') + '" data-page="' + i + '">' + i + '</button>';
        }
        $('#pagination').html(html + '</div>');
    }
    $(document).on('click', '.page-btn', function () { loadExpenses($(this).data('page')); });

    // ── SEARCH ────────────────────────────────────────────
    $('#searchBtn').click(function () { loadExpenses(); });
    $('#searchInput').keypress(function (e) { if (e.which === 13) { e.preventDefault(); loadExpenses(); } });
});