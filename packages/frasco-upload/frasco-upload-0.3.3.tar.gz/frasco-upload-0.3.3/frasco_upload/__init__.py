from frasco import Feature, current_app, action
from .backends import upload_backends, StorageBackend
from werkzeug import secure_filename, FileStorage
from flask import send_from_directory
import uuid
import os
from .utils import *
from io import BytesIO
from tempfile import TemporaryFile, NamedTemporaryFile, gettempdir
from flask.wrappers import Request


def _get_file_stream(self, total_content_length, content_type, filename=None, content_length=None):
    if total_content_length > 1024 * 500:
        return TemporaryFile('wb+', dir=os.environ.get('FRASCO_UPLOAD_TMP_DIR'))
    return BytesIO()

Request._get_file_stream = _get_file_stream


class UploadFeature(Feature):
    name = 'upload'
    defaults = {"default_backend": "local",
                "backends": {},
                "upload_dir": "uploads",
                "upload_url": "/uploads",
                "upload_tmp_dir": None,
                "uuid_prefixes": True,
                "uuid_prefix_path_separator": False,
                "keep_filenames": True,
                "subfolders": False}

    def init_app(self, app):
        self.backends = {}
        app.add_template_global(url_for_upload)
        app.add_template_global(format_file_size)

        def send_uploaded_file(filename):
            return send_from_directory(self.options["upload_dir"], filename)
        app.add_url_rule(self.options["upload_url"] + "/<path:filename>",
                         endpoint="static_upload",
                         view_func=send_uploaded_file)

    def get_backend(self, name=None):
        if isinstance(name, StorageBackend):
            return name
        if name is None:
            name = self.options['default_backend']
        if name not in self.backends:
            backend = name
            options = self.options
            if name in self.options['backends']:
                options = dict(self.options, **self.options['backends'][name])
                backend = options.pop('backend') 
            if backend not in upload_backends:
                raise Exception("Upload backend '%s' does not exist" % backend)
            self.backends[name] = upload_backends[backend](options)
        return self.backends[name]

    def get_backend_from_filename(self, filename):
        if '://' in filename:
            return filename.split('://', 1)
        return None, filename

    @action(default_option='filename')
    def generate_filename(self, filename, uuid_prefix=None, keep_filename=None, subfolders=None,
                          backend=None):
        if uuid_prefix is None:
            uuid_prefix = self.options["uuid_prefixes"]
        if keep_filename is None:
            keep_filename = self.options["keep_filenames"]
        if subfolders is None:
            subfolders = self.options["subfolders"]

        if uuid_prefix and not keep_filename:
            _, ext = os.path.splitext(filename)
            filename = str(uuid.uuid4()) + ext
        else:
            filename = secure_filename(filename)
            if uuid_prefix:
                filename = str(uuid.uuid4()) + ("/" if self.options['uuid_prefix_path_separator'] else "-") + filename

        if subfolders:
            if uuid_prefix:
                parts = filename.split("-", 4)
                filename = os.path.join(os.path.join(*parts[:4]), filename)
            else:
                filename = os.path.join(os.path.join(*filename[:4]), filename)

        if backend:
            if backend is True:
                backend = self.options['default_backend']
            filename = backend + '://' + filename

        return filename

    def get_file_size(self, file):
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        return size

    @action(default_option='file')
    def save_uploaded_file_temporarly(self, file, filename=None):
        if filename:
            tmpfilename = os.path.join(self.options['upload_tmp_dir'] or gettempdir(), filename.replace('/', '-'))
        else:
            _, ext = os.path.splitext(file.filename)
            tmp = NamedTemporaryFile(delete=False, suffix=ext, dir=self.options['upload_tmp_dir'])
            tmp.close()
            tmpfilename = tmp.name
        file.save(tmpfilename)
        return tmpfilename

    def upload(self, pathname, *args, **kwargs):
        with open(pathname, 'rb') as f:
            return self.save(FileStorage(f, kwargs.get('name', os.path.basename(pathname))), *args, **kwargs)

    def save(self, file, filename=None, backend=None, **kwargs):
        if not isinstance(file, FileStorage):
            file = FileStorage(file)
        if not filename:
            filename = self.generate_filename(file.filename, backend=backend, **kwargs)
        r = filename
        if not backend or backend is True:
            backend, filename = self.get_backend_from_filename(filename)
        self.get_backend(backend).save(file, filename)
        return r

    def url_for(self, filename, backend=None, **kwargs):
        if not backend:
            backend, filename = self.get_backend_from_filename(filename)
        return self.get_backend(backend).url_for(filename, **kwargs)

    def delete(self, filename, backend=None, **kwargs):
        if not backend:
            backend, filename = self.get_backend_from_filename(filename)
        self.get_backend(backend).delete(filename, **kwargs)


def url_for_upload(filename, **kwargs):
    return current_app.features.upload.url_for(filename, **kwargs)


def format_file_size(size, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, suffix)
        size /= 1024.0
    return "%.1f%s%s" % (size, 'Y', suffix)


try:
    import frasco_forms.form
    import form
    frasco_forms.form.field_type_map.update({
        "upload": form.FileField})
except ImportError:
    pass
