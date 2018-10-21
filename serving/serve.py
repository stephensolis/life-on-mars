import os
import tempfile
import sys
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from types import SimpleNamespace
from base64 import b64encode

import torch
from utils import get_config
from trainer import MUNIT_Trainer
from torch.autograd import Variable
import torchvision.utils as vutils
from torchvision import transforms
from PIL import Image

import process_stylization
from photo_wct import PhotoWCT


#########
# options
#########

all_opts = {
    'earth': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 1,
        'style': 'styles/earth.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'moon': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/moon.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'mars': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/mars.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'mercury': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/mercury.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'neptune': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/neptune.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'saturn': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/saturn.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'uranus': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/uranus.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'venus': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/venus.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'jupiter': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': 'styles/jupiter.jpg',
        'checkpoint': 'models/generator_planets2earth.pt'
    }),
    'kandinsky2': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 1,
        'style': '',
        'checkpoint': 'models/generator_earth2kandinsky.pt'
    }),
    'mars2earth': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 1,
        'style': '',
        'checkpoint': 'models/generator_mars2earth_landscape.pt'
    }),
    'earth2mars': SimpleNamespace(**{
        'type': 'munit',
        'config': 'configs/mars2earth.yaml',
        'a2b': 0,
        'style': '',
        'checkpoint': 'models/generator_mars2earth_landscape.pt'
    }),
    'kandinsky': SimpleNamespace(**{
        'type': 'photostyle',
        'model': 'models/photo_wct.pth',
        'style_image_path': 'styles/kandinsky.jpg',
        'fast': True
    }),
    'vangogh': SimpleNamespace(**{
        'type': 'photostyle',
        'model': 'models/photo_wct.pth',
        'style_image_path': 'styles/vangogh.jpg',
        'fast': True
    }),
    'davinci': SimpleNamespace(**{
        'type': 'photostyle',
        'model': 'models/photo_wct.pth',
        'style_image_path': 'styles/davinci.jpg',
        'fast': True
    }),
    'picasso': SimpleNamespace(**{
        'type': 'photostyle',
        'model': 'models/photo_wct.pth',
        'style_image_path': 'styles/picasso.jpg',
        'fast': True
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

    if opts.style != '':
        transform = transforms.Compose([transforms.Resize(new_size),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        style_image = Variable(transform(Image.open(opts.style).convert('RGB')).unsqueeze(0).cuda())
    else:
        style_image = None

    return (encode, style_encode, decode, new_size, style_image, style_dim)

def build_photostyle_model(args):
    p_wct = PhotoWCT()
    p_wct.load_state_dict(torch.load(args.model))
    p_wct.cuda(0)

    if args.fast:
        from photo_gif import GIFSmoothing
        p_pro = GIFSmoothing(r=35, eps=0.001)
    else:
        from photo_smooth import Propagator
        p_pro = Propagator()

    return (p_wct, p_pro, args.style_image_path)

models = {}
for key in all_opts:
    opts = all_opts[key]
    if opts.type == 'munit':
        models[key] = build_munit_model(opts)
    elif opts.type == 'photostyle':
        models[key] = build_photostyle_model(opts)


#################
# model inference
#################

def infer_munit(model, input_path, output_path):
    encode, style_encode, decode, new_size, style_image, style_dim = model

    with torch.no_grad():
        img_file = Image.open(input_path)
        original_size = (img_file.size[1], img_file.size[0])
        if min(original_size) < new_size:
            new_size = min(original_size)
        transform = transforms.Compose([transforms.Resize(new_size),
                                        transforms.ToTensor(),
                                        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        image = Variable(transform(img_file.convert('RGB')).unsqueeze(0).cuda())

        # Start testing
        content, _ = encode(image)

        style_rand = Variable(torch.randn(1, style_dim, 1, 1).cuda())
        if style_image is not None:
            _, style = style_encode(style_image)
        else:
            style = style_rand

        s = style[0].unsqueeze(0)
        outputs = decode(content, s)
        outputs = (outputs + 1) / 2.

        resized_data = transforms.Resize(original_size)(transforms.ToPILImage()(outputs.data[0].cpu()))
        resized_data.save(output_path)

def infer_photostyle(model, input_path, output_path):
    p_wct, p_pro, style_path = model

    process_stylization.stylization(
        stylization_module=p_wct,
        smoothing_module=p_pro,
        content_image_path=input_path,
        style_image_path=style_path,
        content_seg_path=[],
        style_seg_path=[],
        output_image_path=output_path,
        cuda=1,
        save_intermediate=False,
        no_post=False
    )


#########
# serving
#########

app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
CORS(app)

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
            elif opts.type == 'photostyle':
                infer_photostyle(model, input_path, output_path)

            return b64encode(open(output_path, 'rb').read())

app.run(host='0.0.0.0', port=5000)
