import os
import tempfile
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from types import SimpleNamespace
from base64 import b64encode

from utils import get_config
from trainer import MUNIT_Trainer
import argparse
from torch.autograd import Variable
import torchvision.utils as vutils
import sys
import torch
import os
from torchvision import transforms
from PIL import Image


#########
# options
#########

all_opts = {
    'model1': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 1,
        'style': '', # style image path
        'checkpoint': 'models/gen_00510000.pt'
    })
}


#############
# load models
#############

def build_munit_model(opts):
    # Load experiment setting
    config = get_config(opts.config)

    # Setup model and data loader
    config['vgg_model_path'] = '/tmp'
    style_dim = config['gen']['style_dim']
    trainer = MUNIT_Trainer(config)

    state_dict = torch.load(opts.checkpoint)
    trainer.gen_a.load_state_dict(state_dict['a'])
    trainer.gen_b.load_state_dict(state_dict['b'])

    trainer.cuda()
    trainer.eval()
    encode = trainer.gen_a.encode if opts.a2b else trainer.gen_b.encode # encode function
    style_encode = trainer.gen_b.encode if opts.a2b else trainer.gen_a.encode # encode function
    decode = trainer.gen_b.decode if opts.a2b else trainer.gen_a.decode # decode function

    if 'new_size' in config:
        new_size = config['new_size']
    else:
        if opts.a2b == 1:
            new_size = config['new_size_a']
        else:
            new_size = config['new_size_b']

    style_image = Variable(transform(Image.open(opts.style).convert('RGB')).unsqueeze(0).cuda()) if opts.style != '' else None

    return (encode, style_encode, decode, new_size, style_image, style_dim)

models = {}
for key in all_opts:
    opts = all_opts[key]
    if opts.type == 'munit':
        models[key] = build_munit_model(opts)


#################
# model inference
#################

def infer_munit(model, input_path, output_path):
    encode, style_encode, decode, new_size, style_image, style_dim = model

    with torch.no_grad():
        transform = transforms.Compose([transforms.Resize(new_size),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        image = Variable(transform(Image.open(input_path).convert('RGB')).unsqueeze(0).cuda())

        # Start testing
        content, _ = encode(image)

        style_rand = Variable(torch.randn(1, style_dim, 1, 1).cuda())
        if style_image:
            _, style = style_encode(style_image)
        else:
            style = style_rand

        s = style[0].unsqueeze(0)
        outputs = decode(content, s)
        outputs = (outputs + 1) / 2.

        vutils.save_image(outputs.data, output_path, padding=0, normalize=True)


#########
# serving
#########

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
CORS(app)

@app.errorhandler(Exception)
def unhandled_exception(exception):
    return jsonify({'error': str(exception)})

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/infer', methods=['POST'])
def infer():
    if 'model' not in request.form:
        return jsonify({'error': 'missing model'})
    opts = all_opts[request.form['model']]
    model = models[request.form['model']]

    with tempfile.NamedTemporaryFile() as input_file:
        input_path = input_file.name
        if 'image' not in request.files:
            return jsonify({'error': 'missing image file'})
        input_file.write(request.files['image'].read())
        input_file.flush()

        with tempfile.NamedTemporaryFile() as output_file:
            output_path = output_file.name + '.jpg'

            if opts.type == 'munit':
                infer_munit(model, input_path, output_path)

            return b64encode(open(output_path, 'rb').read())

app.run(host='0.0.0.0', port=5000)
