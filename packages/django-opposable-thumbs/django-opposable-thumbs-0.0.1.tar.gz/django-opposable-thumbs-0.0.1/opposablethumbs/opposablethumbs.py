import hashlib
import requests
import os.path
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse


class OpposableThumbs:
    def __init__(self, params):
        self.format = 'JPEG'
        self.size = None
        self.image = None
        self.processes = []
        self.use_cache = False
        self.cache_key = None
        self.cache_exists = False
        self.error = None

        # extract params into dict
        self.param_dict = {}
        for p in params.split('&'):
            key, value = p.split('=')
            self.param_dict[key.lower()] = value

        # get cache value
        if 'cache' in self.param_dict:
            self.cache = self.param_dict['cache'] == '1'

        # use cache if applicable
        if self.cache:
            self.cache_key = (hashlib.md5(params.encode('utf-8'))).hexdigest()
            self.cache_exists = os.path.isfile(self.get_cache_path())
            if self.cache_exists:
                return

        # at this point, the cache is not being used or the file does not
        # exist on disk so we're loading it from somewhere

        # define image source
        if 'domain' in self.param_dict and 'path' in self.param_dict:
            # use 'hidden' domain
            self.source = 'uri'
            self.target = '%s/%s' % ('http://whatever.com', self.param_dict['path'])
            return self.set_error('This feature is currently unavailable')
        elif 'file' in self.param_dict:
            # use local file
            self.source = 'file'
            self.target = self.param_dict['file']
            return self.set_error('This feature is currently unavailable')
        elif 'uri' in self.param_dict:
            self.source = 'uri'
            self.target = self.param_dict['uri']
            if not self.is_allowed_source():
                return self.set_error('Disallowed domain')
        else:
            return self.set_error('Invalid request')

        # define processes to perform on image
        if 'p' in self.param_dict:
            self.processes = self.param_dict['p'].split('|')
            self.processes = [p.split(',') for p in self.processes]

        # open image
        if self.source == 'file':
            pass
        elif self.source == 'uri':
            try:
                r = requests.get(self.target)
                self.image = Image.open(BytesIO(r.content))
            except:
                pass

        # error if broken
        if self.image is None:
            return self.set_error('Failed to open URI')

        # get meta information about the image
        self.format = self.image.format
        if 'format' in self.param_dict:
            self.format = self.param_dict['format'].upper()

        # perform processing on the image
        for p in self.processes:
            self.process(p)

        # save to disk (if applicable)
        if self.cache:
            self.image.save(self.get_cache_path(), self.format)

    def is_allowed_source(self):
        if len(settings.OPPOSABLE_THUMBS['ALLOWED_SOURCES']) > 0:
            allowed = False
            for s in settings.OPPOSABLE_THUMBS['ALLOWED_SOURCES']:
                if self.target.lower().startswith(s.lower()):
                    allowed = True
                    break

            if not allowed:
                return False

        return True

    def get_cache_path(self):
        return '%s%s' % (
            settings.OPPOSABLE_THUMBS['CACHE_DIR'],
            self.cache_key
        )

    def process(self, command):
        # autocontrast
        if command[0] == 'autocontrast':
            self.image = ImageOps.autocontrast(self.image)

        # blur
        if command[0] == 'blur':
            self.image = self.image.filter(ImageFilter.BLUR)

        # brightness
        if command[0] == 'brightness':
            try:
                self.image = ImageEnhance.Brightness(self.image).enhance(float(command[1]))
            except:
                self.set_error('Invalid brightness argument')

        # color
        if command[0] == 'color':
            try:
                self.image = ImageEnhance.Color(self.image).enhance(float(command[1]))
            except:
                self.set_error('Invalid color argument')

        # colorize
        if command[0] == 'colorize':
            try:
                self.image = ImageOps.colorize(
                    ImageOps.grayscale(self.image),
                    black='#%s' % command[1],
                    white='#%s' % command[2]
                )
            except:
                self.set_error('Invalid colorize arguments')

        # contour
        if command[0] == 'contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)

        # contrast
        if command[0] == 'contrast':
            try:
                self.image = ImageEnhance.Contrast(self.image).enhance(float(command[1]))
            except:
                self.set_error('Invalid contrast argument')

        # crop
        if command[0] == 'crop':
            try:
                self.image = self.image.crop((
                    int(command[1]),
                    int(command[2]),
                    int(command[3]),
                    int(command[4])
                ))
            except:
                self.set_error('Invalid crop arguments')

        # cropratio
        if command[0] == 'cropratio':
            try:
                # get sizes
                width = float(self.image.size[0])
                height = float(self.image.size[1])
                orig_ratio = width / height
                target_ratio = float(command[1])

                # crop
                if orig_ratio > target_ratio:
                    # same height, change width
                    target_width = int(round(height * target_ratio))
                    left = int(round((width / 2) - (target_width / 2)))
                    self.image = self.image.crop((
                        left,
                        0,
                        left + target_width,
                        int(height),
                    ))
                elif target_ratio > orig_ratio:
                    # same width, change height
                    target_height = int(round(width / target_ratio))
                    top = int(round((height / 2) - (target_height / 2)))
                    self.image = self.image.crop((
                        0,
                        top,
                        int(width),
                        top + target_height
                    ))
                else:
                    return self.image

            except:
                self.set_error('Invalid cropratio arguments')

        # emboss
        if command[0] == 'emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)

        # equalize
        if command[0] == 'equalize':
            self.image = ImageOps.equalize(self.image)

        # fliphoriz
        if command[0] == 'fliphoriz':
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

        # flipvert
        if command[0] == 'flipvert':
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

        # gblur
        if command[0] == 'gblur':
            try:
                self.image = self.image.filter(
                    ImageFilter.GaussianBlur(radius=int(command[1]))
                )
            except:
                self.set_error('Invalid gblur argument')

        # grayscale
        if command[0] == 'grayscale':
            self.image = ImageOps.grayscale(self.image)

        # invert
        if command[0] == 'invert':
            self.image = ImageOps.invert(self.image)

        # posterize
        if command[0] == 'posterize':
            try:
                self.image = ImageOps.posterize(self.image, int(command[1]))
            except:
                self.set_error('Invalid posterize argument')

        # resize
        if command[0] == 'resize':
            try:
                self.image = self.image.resize(
                    (int(command[1]), int(command[2])),
                    resample=Image.ANTIALIAS
                )
            except:
                self.set_error('Invalid resize arguments')

        # resizemin
        if command[0] == 'resizemin':
            try:
                # get orig size
                orig_width = float(self.image.size[0])
                orig_height = float(self.image.size[1])
                orig_ratio = orig_width / orig_height

                # get target size
                target_width = int(command[1])
                target_height = int(command[2])
                target_ratio = target_width / target_height

                # resize accordingly
                if orig_ratio > target_ratio:
                    target_width = int(round(target_height * orig_ratio))
                elif orig_ratio < target_ratio:
                    target_height = int(round(target_width / orig_ratio))

                self.image = self.image.resize(
                    (target_width, target_height),
                    resample=Image.ANTIALIAS
                )
            except:
                self.set_error('Invalid cropratio arguments')

        # resizepc
        if command[0] == 'resizepc':
            try:
                x, y = self.image.size
                self.image = self.image.resize(
                    (int(x * float(command[1])), int(y * float(command[2]))),
                    resample=Image.ANTIALIAS
                )
            except:
                self.set_error('Invalid resizepc arguments')

        # rotate
        if command[0] == 'rotate':
            try:
                self.image = self.image.rotate(int(command[1]))
            except:
                self.set_error('Invalid rotate argument')

        # sharpness
        if command[0] == 'sharpness':
            try:
                self.image = ImageEnhance \
                                .Sharpness(self.image) \
                                .enhance(float(command[1]))
            except:
                self.set_error('Invalid sharpness argument')

        # solarize
        if command[0] == 'solarize':
            try:
                self.image = ImageOps.solarize(self.image, int(command[1]))
            except:
                self.set_error('Invalid solarize argument')

    def set_error(self, error):
        self.error = error
        return None

    def response(self):
        # show error if one exists
        if self.error is not None:
            return HttpResponse(self.error)

        # init reponse object
        r = HttpResponse(content_type='image/%s' % self.format.lower())

        # fetch from appropriate source
        if self.cache_exists:
            with open(self.get_cache_path(), 'rb') as fp:
                r.write(fp.read())
        else:
            self.image.save(r, self.format)

        return r
