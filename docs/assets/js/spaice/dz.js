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
    this.on("sending", function(file, xhr, formData) {
      formData.append("model", window.selected_model);
    });
    this.on("success", function(file, responseText) {
      var fr = new FileReader();
      fr.onload = function () {
        $('#input_image').attr('src', fr.result);
        $('#compare_image').twentytwenty();
        if ($('#input_image').prop('width') < $('#output_image').prop('width')) {
          $('#input_image').prop('width', $('#output_image').prop('width'));
          $('#input_image').prop('height', $('#output_image').prop('height'));
        } else {
          $('#output_image').prop('width', $('#input_image').prop('width'));
          $('#output_image').prop('height', $('#input_image').prop('height'));
        }
      };
      fr.readAsDataURL(file);
      $('#output_image').attr('src', 'data:image/jpeg;base64, ' + responseText);
      $('#output_download').attr('href', 'data:image/jpeg;base64, ' + responseText);

      $('#DropZoneFiddle').hide();
      $('#output_div').show();
    });
    this.on("complete", function(file) {
      this.removeAllFiles(true);
    });
  }
};
