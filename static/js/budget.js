/**
 * ============================================================
 *  budget.js — Categories & Budget CRUD + Utilization
 * ============================================================
 */

$(document).ready(function () {
    console.log("Budget JS Loaded.");


    // ── LOAD CATEGORIES ───────────────────────────────────
    // Called on categories page AND budget page (populates dropdown)

    function loadCategories() {
        $.get('/budget/categories/list/', function (res) {
            var listHtml   = '';
            var optionHtml = '<option value="">Select a category</option>';

            if (res.data && res.data.length > 0) {
                res.data.forEach(function (c) {
                    listHtml +=
                        '<div class="item-row">' +
                            '<span class="item-name">' + c.name + '</span>' +
                            '<button class="btn-danger-sm delete-category-btn" data-id="' + c.id + '">Delete</button>' +
                        '</div>';
                    optionHtml += '<option value="' + c.id + '">' + c.name + '</option>';
                });
            } else {
                listHtml = '<p class="empty-msg">No categories created yet.</p>';
            }

            $('#categoryList').html(listHtml);

            // Populate category dropdowns on budget page & expense page
            $('select[name="category"], #categorySelect').html(optionHtml);

        }).fail(function () {
            showMsg('Failed to load categories.', 'error');
        });
    }

    if ($('#categoryList').length || $('#categorySelect').length) {
        loadCategories();
    }


    // ── CREATE CATEGORY ───────────────────────────────────

    $('#categoryForm').submit(function (e) {
        e.preventDefault();
        console.log('Create category submitted.');

        $.ajax({
            url: '/budget/categories/create/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                if (res.success) {
                    showMsg(res.message, 'success');
                    $('#categoryForm')[0].reset();
                    loadCategories();
                } else {
                    showMsg(res.message, 'error');
                }
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Error creating category.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── DELETE CATEGORY ───────────────────────────────────
    // confirm() used only for delete actions

    $(document).on('click', '.delete-category-btn', function () {
        var id = $(this).data('id');

        if (!confirm('Are you sure you want to delete this category?')) return;

        $.ajax({
            url: '/budget/categories/delete/' + id + '/',
            method: 'POST',
            success: function (res) {
                if (res.success) {
                    showMsg(res.message, 'success');
                    loadCategories();
                } else {
                    showMsg(res.message, 'error');
                }
            },
            error: function () {
                showMsg('Error deleting category.', 'error');
            }
        });
    });


    // ── LOAD BUDGETS ──────────────────────────────────────

    function loadBudgets() {
        $.get('/budget/list/', function (res) {
            var html = '';

            if (res.data && res.data.length > 0) {
                res.data.forEach(function (b) {
                    html +=
                        '<div class="item-row">' +
                            '<span class="item-name"><strong>' + b.category + '</strong></span>' +
                            '<span class="item-meta">₹' + parseFloat(b.amount).toFixed(2) + ' &nbsp;|&nbsp; ' + b.month + '</span>' +
                            '<button class="btn-warning-sm edit-budget-btn" data-id="' + b.id + '" data-amount="' + b.amount + '">Edit</button>' +
                            '<button class="btn-danger-sm delete-budget-btn" data-id="' + b.id + '">Delete</button>' +
                        '</div>';
                });
            } else {
                html = '<p class="empty-msg">No budgets created yet.</p>';
            }

            $('#budgetList').html(html);

        }).fail(function () {
            showMsg('Failed to load budgets.', 'error');
        });
    }

    if ($('#budgetList').length) {
        loadBudgets();
    }


    // ── CREATE BUDGET ─────────────────────────────────────

    $('#budgetForm').submit(function (e) {
        e.preventDefault();
        console.log('Create budget submitted.');

        $.ajax({
            url: '/budget/create/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                if (res.success) {
                    showMsg(res.message, 'success');
                    $('#budgetForm')[0].reset();
                    loadBudgets();
                } else {
                    showMsg(res.message, 'error');
                }
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Error creating budget.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── EDIT BUDGET ───────────────────────────────────────

    $(document).on('click', '.edit-budget-btn', function () {
        var id            = $(this).data('id');
        var currentAmount = $(this).data('amount');

        var newAmount = prompt('Enter new budget amount:', currentAmount);
        if (newAmount === null || newAmount === '') return;

        if (isNaN(newAmount) || parseFloat(newAmount) <= 0) {
            showMsg('Please enter a valid positive amount.', 'error');
            return;
        }

        $.ajax({
            url: '/budget/edit/' + id + '/',
            method: 'POST',
            data: { amount: newAmount },
            success: function (res) {
                if (res.success) {
                    showMsg(res.message, 'success');
                    loadBudgets();
                } else {
                    showMsg(res.message, 'error');
                }
            },
            error: function () {
                showMsg('Error updating budget.', 'error');
            }
        });
    });


    // ── DELETE BUDGET ─────────────────────────────────────

    $(document).on('click', '.delete-budget-btn', function () {
        var id = $(this).data('id');

        if (!confirm('Are you sure you want to delete this budget?')) return;

        $.ajax({
            url: '/budget/delete/' + id + '/',
            method: 'POST',
            success: function (res) {
                if (res.success) {
                    showMsg(res.message, 'success');
                    loadBudgets();
                } else {
                    showMsg(res.message, 'error');
                }
            },
            error: function () {
                showMsg('Error deleting budget.', 'error');
            }
        });
    });


    // ── BUDGET UTILIZATION ────────────────────────────────

    $('#loadUtilization').click(function () {
        console.log('Load utilization clicked.');

        $.get('/budget/utilization/', function (res) {
            var html = '';

            if (res.data && res.data.length > 0) {
                res.data.forEach(function (u) {
                    var pct      = u.budget > 0 ? (u.spent / u.budget) * 100 : 0;
                    var barClass = pct > 100 ? 'bar-danger' : pct > 75 ? 'bar-warning' : 'bar-success';

                    html +=
                        '<div class="util-item">' +
                            '<div class="util-header">' +
                                '<strong>' + u.category + '</strong>' +
                                '<span>₹' + parseFloat(u.spent).toFixed(2) + ' / ₹' + parseFloat(u.budget).toFixed(2) + '</span>' +
                            '</div>' +
                            '<div class="progress-track">' +
                                '<div class="progress-fill ' + barClass + '" style="width:' + Math.min(pct, 100) + '%"></div>' +
                            '</div>' +
                            '<small class="util-remaining">Remaining: ₹' + parseFloat(u.remaining).toFixed(2) + '</small>' +
                        '</div>';
                });
            } else {
                html = '<p class="empty-msg">No utilization data for this month.</p>';
            }

            $('#utilizationDiv').html(html);

        }).fail(function () {
            showMsg('Failed to load utilization.', 'error');
        });
    });

});