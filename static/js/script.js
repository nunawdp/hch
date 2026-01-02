// GLOBAL FUNCTION
// JConfirm request submit reuseable
function confirmFormSubmit(options) {
    $.confirm({
        title: options.title || "Confirmation",
        content: options.content || `<form id="confirm-form" method="post" action="${options.url}">
                ${options.csrf || ""}
                <p>${options.message || "Are you sure?"}</p>
            </form>`,
        type: options.type || "blue",
        columnClass: options.size || 'medium',
        buttons: {
            cancel: {
                text: options.cancelText || "Cancel",
                btnClass: "btn-secondary"
            },
            confirm: {
                text: options.confirmText || "OK",
                btnClass: options.confirmClass || "btn-primary",
                action: function () {
                    this.$content.find("#confirm-form").submit()
                }
            },
        }
    })
}

// init select2 agar bisa digunakan di semua lokasi
// init select2 tanpa ajax
function initSelect2Normal(container = null) {

    const $scope = container || $(document);
    const $modalBox = container ? container.closest('.jconfirm-box') : null;

    $scope.find('.select2:not(.select2-ajax)').each(function () {
        const $select = $(this);

        if ($select.data('select2')) return;

        const options = {
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: $select.data('placeholder'),
        };

        if ($modalBox && $modalBox.length) {
            options.dropdownParent = $modalBox;
        }

        $select.select2(options);
    });
}


// init select2 yang menggunakan ajax
function initSelect2(container = null) {

    const $scope = container || $(document);
    const $modalBox = container ? container.closest('.jconfirm-box') : null;

    $scope.find('.select2-ajax').each(function () {
        const $select = $(this);

        if ($select.data('select2')) return;

        const options = {
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: $select.data('placeholder'),
            // minimumInputLength: 1,
            ajax: {
                url: $select.data('url'),
                dataType: 'json',
                delay: 300,
                data: params => ({ q: params.term }),
                processResults: data => ({
                    results: data.map(item => ({
                        id: item.id,
                        text: item.text
                    }))
                })
            }
        };

        if ($modalBox && $modalBox.length) {
            options.dropdownParent = $(document.body);
        }

        $select.select2(options);
    });
}


// load form & check action
function loadForm(url) {
    const options = {
        url: url,
        method: 'GET',
    };
    return $.ajax(options);
}

async function checkAction(options) {
    try {
        const formHtml = await loadForm(options.url);
        

        $.confirm({
            title: options.title || 'Form',
            content: formHtml,
            columnClass: options.size || 'medium',
            backgroundDismiss: false, // User tidak bisa menutup modal dengan klik background
            backgroundDismissAnimation: 'shake', // Memberi efek getar jika background diklik
            buttons: {
                submit: {
                    text: options.submitText || 'Save',
                    btnClass: options.submitClass || 'btn-primary',
                    action: function () {
                        if (options.data){
                            this.$content.find('form').find('#id_status').val(options.data)
                        }
                        return submitForm(this, options);
                    }
                },
                cancel: {
                    text: 'Cancel'
                }
            },
            onOpenBefore: function () {
                initSelect2Normal(this.$content);
                initSelect2(this.$content)
            },
            // onOpen: function(){
            //     initSelect2Normal(this.$content);
            //     initSelect2(this.$content)
            // },
            // onClose: function () {
            //     // 🔥 destroy SEMUA select2 di modal
            //     this.$content
            //         .find('.select2-hidden-accessible')
            //         .select2('destroy');
            // }
            onDestroy: function () {
                // 🔥 destroy SEMUA select2 di modal
                this.$content
                    .find('select.select2-hidden-accessible')
                    .each(function () {
                        if ($(this).data('select2')) {
                            $(this).select2('destroy')
                        }
                    })
            }
        });

    } catch (err) {
        console.error('Load form failed', err);
    }
}

function submitForm(dialog, options) {
    const form = dialog.$content.find('form');

    return $.ajax({
        url: form.attr('action'),
        method: 'POST',
        data: form.serialize()
    }).done(function (res) {
        dialog.close();

        if (typeof options.onSuccess === 'function') {
            options.onSuccess(res);
        }

    }).fail(function (xhr) {
        // 🔥 bersihkan select2 SEBELUM ganti HTML
        dialog.$content
        .find('.select2-hidden-accessible')
        .select2('destroy');

        dialog.$content.html(xhr.responseText);

        initSelect2Normal(dialog.$content);
        initSelect2(dialog.$content);
        
        return false;
    });
}


$(document).ready(function(){
    const $collapse = $('#navbarSearch');

    // Tutup saat klik di luar collapse
    $(document).on('click', function (e) {
        const $input = $('#navbarSearch input');
        const $menu = $('#navbarMenu .row');
        if (
            $collapse.hasClass('show') &&
            !$input.is(e.target) || !$menu.is(e.target) &&
            $input.has(e.target).length === 0
        ) {
            $collapse.collapse('hide');
        }
    });

    // Tutup saat ESC ditekan
    $(document).on('keydown', function (e) {
        if (e.key === 'Escape' && $collapse.hasClass('show')) {
            $collapse.collapse('hide');
        }
    });

    $('#navbarSearch').on('shown.bs.collapse', function () {
        $(this).find('input').trigger('focus');
    });


    //select2 ajax
    initSelect2()
    initSelect2Normal()
    
    
})