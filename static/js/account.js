/**
 * ============================================================
 *  account.js — Register, Login, OTP, Profile, Password Reset
 * ============================================================
 */

$(document).ready(function () {
    console.log("Account JS Loaded.");


    // ── REGISTER ──────────────────────────────────────────

    $('#registerForm').submit(function (e) {
        e.preventDefault();
        console.log('Register form submitted.');

        $.ajax({
            url: '/register/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'OTP sent to your email.', 'success');
                setTimeout(function () {
                    window.location.href = '/verify-otp/';
                }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Registration failed.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── VERIFY OTP (Email Verification) ───────────────────

    $('#verifyOtpForm').submit(function (e) {
        e.preventDefault();
        console.log('Verify OTP submitted.');

        $.ajax({
            url: '/verify-otp/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'Email verified successfully.', 'success');
                setTimeout(function () {
                    window.location.href = '/login/';
                }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Invalid OTP.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── LOGIN ─────────────────────────────────────────────

    $('#loginForm').submit(function (e) {
        e.preventDefault();
        console.log('Login form submitted.');

        $.ajax({
            url: '/login/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'Login successful.', 'success');
                setTimeout(function () {
                    window.location.href = '/dashboard/';
                }, 1000);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Invalid credentials.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── UPDATE PROFILE ────────────────────────────────────

    $('#updateProfileForm').submit(function (e) {
        e.preventDefault();
        console.log('Update profile submitted.');

        $.ajax({
            url: '/update-profile/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'Profile updated successfully.', 'success');
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Update failed.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── UPLOAD AVATAR ─────────────────────────────────────
    // NOTE: form id must be "avatarUploadForm" in upload_avatar.html

    $('#avatarUploadForm').submit(function (e) {
        e.preventDefault();
        console.log('Avatar upload submitted.');

        var formData = new FormData(this);

        $.ajax({
            url: '/upload-avatar/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (res) {
                showMsg(res.message || 'Avatar uploaded successfully.', 'success');
                setTimeout(function () { location.reload(); }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Upload failed.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── PASSWORD RESET — Request OTP ──────────────────────

    $('#passwordResetRequestForm').submit(function (e) {
        e.preventDefault();
        console.log('Password reset request submitted.');

        $.ajax({
            url: '/password-reset/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'OTP sent to your email.', 'success');
                setTimeout(function () {
                    window.location.href = '/password-reset-verify/';
                }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'User not found.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── PASSWORD RESET — Verify OTP ───────────────────────

    $('#passwordResetVerifyForm').submit(function (e) {
        e.preventDefault();
        console.log('Password reset OTP verify submitted.');

        $.ajax({
            url: '/password-reset-verify/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'OTP verified.', 'success');
                setTimeout(function () {
                    window.location.href = '/password-reset-confirm/';
                }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Invalid OTP.';
                showMsg(msg, 'error');
            }
        });
    });


    // ── PASSWORD RESET — Confirm New Password ─────────────

    $('#passwordResetConfirmForm').submit(function (e) {
        e.preventDefault();
        console.log('Password reset confirm submitted.');

        $.ajax({
            url: '/password-reset-confirm/',
            method: 'POST',
            data: $(this).serialize(),
            success: function (res) {
                showMsg(res.message || 'Password reset successful.', 'success');
                setTimeout(function () {
                    window.location.href = '/login/';
                }, 1200);
            },
            error: function (xhr) {
                var msg = xhr.responseJSON ? xhr.responseJSON.message : 'Password reset failed.';
                showMsg(msg, 'error');
            }
        });
    });

});