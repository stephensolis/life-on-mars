Dropzone.options.DropZoneFiddle = {
  url: this.location,
  paramName: "image",
  clickable: true,
  maxFilesize: 10, //in mb
  uploadMultiple: false,
  maxFiles: 1,
  addRemoveLinks: true,
  acceptedFiles: '.png,.jpg,.gif,.jpeg,.bmp',
  url: 'https://server.artifyearth.co/infer',
  init: function() {
    window.dropzone = this;
    this.on("sending", function(file, xhr, formData) {
      formData.append("model", window.selected_model);
    });
    this.on("success", function(file, responseText) {
      var fr = new FileReader();
      fr.onload = function () {
        $('#input_image').attr('src', fr.result);
        $('#output_image').attr('src', 'data:image/jpeg;base64, ' + responseText);

        var target_height = $(window).height() * 0.7;
        var target_width = $('#input_image').prop('naturalWidth') * $(window).height() * 0.7 / $('#input_image').prop('naturalHeight');

        $('#input_image').prop('height', target_height);
        $('#input_image').prop('width', target_width);
        $('#output_image').prop('height', target_height);
        $('#output_image').prop('width', target_width);

        $('#compare_image').twentytwenty();
      };
      fr.readAsDataURL(file);
      $('#output_download').attr('href', 'data:image/jpeg;base64, ' + responseText);

      $('#DropZoneFiddle').hide();
      $('#output_div').show();
    });
  }
};
