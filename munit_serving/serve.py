import os
import tempfile
from flask import Flask, jsonify, request, send_file
from types import SimpleNamespace

from utils import get_config, pytorch03_to_pytorch04
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

opts = SimpleNamespace(**{
    'config': 'configs/mars2earth.yaml',
    'a2b': 1,
    'style': '', # style image path
    'checkpoint': 'gen_00510000.pt',
    'seed': 10
})


#######
# setup
#######

torch.manual_seed(opts.seed)
torch.cuda.manual_seed(opts.seed)

# Load experiment setting
config = get_config(opts.config)

# Setup model and data loader
config['vgg_model_path'] = '/tmp'
style_dim = config['gen']['style_dim']
trainer = MUNIT_Trainer(config)

try:
    state_dict = torch.load(opts.checkpoint)
    trainer.gen_a.load_state_dict(state_dict['a'])
    trainer.gen_b.load_state_dict(state_dict['b'])
except:
    state_dict = pytorch03_to_pytorch04(torch.load(opts.checkpoint), opts.trainer)
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
    if opts.a2b==1:
        new_size = config['new_size_a']
    else:
        new_size = config['new_size_b']


#########
# serving
#########

app = Flask(__name__)
app.config.from_object(__name__)

@app.errorhandler(Exception)
def unhandled_exception(exception):
    if str(exception) == '<Response [404]>' or 'Max retries exceeded with url' in str(exception):
        return jsonify({'error': 'unable to resolve image url'})
    elif 'cannot identify image file' in str(exception):
        return jsonify({'error': 'unable to read image file'})
    else:
        return jsonify({'error': str(exception)})

@app.route('/infer', methods=['POST'])
def infer():
    with tempfile.NamedTemporaryFile() as input_file:
        input_path = input_file.name
        if 'image' not in request.files:
            return jsonify({'error': 'missing image file'})
        input_file.write(request.files['image'].read())
        input_file.flush()

        with torch.no_grad():
            transform = transforms.Compose([transforms.Resize(new_size),
                                            transforms.ToTensor(),
                                            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
            image = Variable(transform(Image.open(input_path).convert('RGB')).unsqueeze(0).cuda())
            style_image = Variable(transform(Image.open(opts.style).convert('RGB')).unsqueeze(0).cuda()) if opts.style != '' else None

            # Start testing
            content, _ = encode(image)

            style_rand = Variable(torch.randn(1, style_dim, 1, 1).cuda())
            if opts.style != '':
                _, style = style_encode(style_image)
            else:
                style = style_rand

            s = style[0].unsqueeze(0)
            outputs = decode(content, s)
            outputs = (outputs + 1) / 2.

            with tempfile.NamedTemporaryFile() as output_file:
                output_path = output_file.name + '.jpg'
                vutils.save_image(outputs.data, output_path, padding=0, normalize=True)

                return send_file(output_path, attachment_filename='result.jpg')

app.run(host='0.0.0.0', port=5000)
