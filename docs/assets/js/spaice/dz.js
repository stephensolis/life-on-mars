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
      formData.append("model", "photo1");
    });
    this.on("success", function(file, responseText) {
      document.getElementById('output_image').src = 'data:image/jpeg;base64, ' + responseText;
    });
  }
};
