(function($) {
    $(document).ready(function() {
        // Atualizar os campos de coordenador e membros ao mudar a startup
        $('#id_startup').change(function() {
            var startupId = $(this).val();
            var coordenadorField = $('#id_coordenador');
            var membrosField = $('#id_membros');

            // Atualizar coordenador
            $.ajax({
                url: '/admin/get-coordenadores/',  // URL da sua view para coordenadores
                data: {
                    'startup_id': startupId
                },
                success: function(data) {
                    coordenadorField.empty();
                    $.each(data.coordenadores, function(index, coordenador) {
                        coordenadorField.append('<option value="' + coordenador.id + '">' + coordenador.nome + '</option>');
                    });
                }
            });

            // Atualizar membros
            $.ajax({
                url: '/admin/get-membros/',  // URL da sua view para membros
                data: {
                    'startup_id': startupId
                },
                success: function(data) {
                    membrosField.empty();
                    $.each(data.membros, function(index, membro) {
                        membrosField.append('<option value="' + membro.id + '">' + membro.nome + '</option>');
                    });
                }
            });
        });
    });
})(django.jQuery);
