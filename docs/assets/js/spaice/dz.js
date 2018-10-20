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
      $('#output_image').attr('src', 'data:image/jpeg;base64, ' + responseText);
      $('#DropZoneFiddle').hide();
      $('#output_div').show();
    });
    this.on("complete", function(file) {
      this.removeAllFiles(true);
    });
  }
};
