import asyncio
import bleach
import bs4
import logging
import os
import signal
import shutil
import tempfile


logger = logging.getLogger(__name__)


HTML_EXTENSIONS = ('.htm', '.html', '.xhtml')


class ConversionError(ValueError):
    """Error converting document.
    """


if hasattr(signal, 'SIGCHLD'):
    from tornado.process import Subprocess, CalledProcessError

    def check_call(cmd):
        proc = Subprocess(cmd)
        return proc.wait_for_exit()
else:
    import subprocess
    from subprocess import CalledProcessError

    # Windows doesn't have this, so tornado.process doesn't work
    # Use Popen with a thread pool
    def check_call(cmd):
        return asyncio.get_event_loop().run_in_executor(
            None,
            subprocess.check_call,
            cmd
        )


POSSIBLE_OUTPUT_NAMES = ['index.html', 'index.xhtml', 'index.htm']


async def to_html(body, content_type, filename):
    logger.info("Converting file %r, type %r", filename, content_type)

    if os.path.splitext(filename)[1].lower() not in HTML_EXTENSIONS:
        # Convert file to HTML using Calibre
        tmp = tempfile.mkdtemp(prefix='taguette_calibre_')
        try:
            input_filename = os.path.join(tmp, filename)
            with open(input_filename, 'wb') as fp:
                fp.write(body)
            output_dir = os.path.join(tmp, 'output')
            convert = 'ebook-convert'
            if os.environ.get('CALIBRE'):
                convert = os.path.join(os.environ['CALIBRE'], convert)
            cmd = [convert, input_filename, output_dir]
            logger.info("Running: %s", ' '.join(cmd))
            try:
                await check_call(cmd)
            except CalledProcessError as e:
                raise ConversionError("Calibre returned %d" % e.returncode)
            logger.info("ebook-convert successful")
            for output_name in POSSIBLE_OUTPUT_NAMES:
                output_filename = os.path.join(output_dir, output_name)
                if os.path.isfile(output_filename):
                    break
            else:
                raise RuntimeError("index.html not found in output dir: %r" %
                                   (os.listdir(output_dir),))
            with open(output_filename, 'rb') as fp:
                body = fp.read()
            # TODO: Store media files
        finally:
            shutil.rmtree(tmp)

    # Use beautifulsoup to remove head, script, style elements
    # (bleach can do that, but would keep the text inside them)
    soup = bs4.BeautifulSoup(body, 'html5lib')
    for tag in ['head', 'script', 'style']:
        for e in soup.find_all(tag):
            e.extract()
    # Update 'src' URLs
    for e in soup.find_all('img'):
        e.attrs['src'] = '/static/missing.png'
    # Update 'href' URLs
    for e in soup.find_all('a'):
        if 'href' not in e.attrs:
            continue
        href = e.attrs['href'].lower()
        if not href.startswith('http://') and not href.startswith('https://'):
            e.attrs['href'] = '#'
    # Back to string
    body = str(soup)
    del soup

    # Use bleach to sanitize the content
    body = bleach.clean(
        body,
        tags=['p', 'a', 'img',
              'h1', 'h2', 'h3', 'h4', 'h5',
              'strong', 'em', 'b', 'u',
              'ul', 'ol', 'li'],
        attributes={'a': ['href'], 'img': ['src', 'width', 'height']},
        strip=True,
    )

    body = body.strip()

    return body


async def to_html_chunks(body, content_type, filename):
    html = await to_html(body, content_type, filename)
    # TODO: Do chunks
    return html


async def calibre_from_html(html, extension):
    # Convert file using Calibre
    tmp = tempfile.mkdtemp(prefix='taguette_calibre_')
    try:
        input_filename = os.path.join(tmp, 'input.html')
        with open(input_filename, 'w') as fp:
            fp.write(html)
        output_filename = os.path.join(tmp, 'output.%s' % extension)
        convert = 'ebook-convert'
        if os.environ.get('CALIBRE'):
            convert = os.path.join(os.environ['CALIBRE'], convert)
        cmd = [convert, input_filename, output_filename,
               '--page-breaks-before=/']
        logger.info("Running: %s", ' '.join(cmd))
        try:
            await check_call(cmd)
        except CalledProcessError as e:
            raise ConversionError("Calibre returned %d" % e.returncode)
        logger.info("ebook-convert successful")
        if not os.path.isfile(output_filename):
            raise RuntimeError("output file does not exist")
    except Exception:
        shutil.rmtree(tmp)
        raise
    else:
        def reader():
            try:
                with open(output_filename, 'rb') as fp:
                    chunk = fp.read(4096)
                    yield chunk
                    while len(chunk) == 4096:
                        chunk = fp.read(4096)
                        if chunk:
                            yield chunk
            finally:
                shutil.rmtree(tmp)

        return reader()


def html_to_html(html):
    future = asyncio.get_event_loop().create_future()
    future.set_result([html])
    return future


_extensions = {
    'html': (html_to_html,
             'text/html; charset=utf-8'),
    'doc': (lambda html: calibre_from_html(html, 'docx'),
            'application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.document; charset=utf-8'),
    'docx': (lambda html: calibre_from_html(html, 'docx'),
             'application/vnd.openxmlformats-officedocument.'
             'wordprocessingml.document; charset=utf-8'),
    'pdf': (lambda html: calibre_from_html(html, 'pdf'),
            'application/pdf'),
}


def html_to(html, extension):
    func, mimetype = _extensions[extension]
    return mimetype, asyncio.ensure_future(func(html))
