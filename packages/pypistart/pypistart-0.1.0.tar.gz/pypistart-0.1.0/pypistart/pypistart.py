from jinja2 import Environment, PackageLoader, select_autoescape
import os


TEMPLATES_DIR = os.path.abspath('templates')


class PyPiStarter(object):

    def __init__(self, package_name, package_root, author_name, author_email):
        self.package_name = package_name
        self.package_root = package_root
        self.author_name = author_name
        self.author_email = author_email
        self.env = Environment(
            loader=PackageLoader('pypistart', TEMPLATES_DIR),
            autoescape=select_autoescape(['html', 'xml']),
        )
        return

    def _write_file(self, contents, dest):
        if contents is None:
            contents = ''
        if dest is None:
            raise Exception('dest is None')
        with open(dest, 'w') as f:
            f.write(contents)
        return

    def _init_package_dir(self, parent_dir, package_name):
        package_dir = os.path.join(parent_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        self._write_file('', os.path.join(package_dir, '__init__.py'))
        self._write_file('', os.path.join(package_dir, '{}.py'.format(package_name)))
        return package_dir

    def _get_rendered_template(self, template):
        template = self.env.get_template(template)
        contents = template.render()
        if contents:
            # jinja2 removes leading and ending whitespace; we want a \n at the end because it is pretty
            contents += '\n'
        return contents

    def _readme(self):
        template = self.env.get_template('readme.txt')
        contents = template.render(package_name=self.package_name)
        return contents

    def _setup(self):
        template = self.env.get_template('setup_py.txt')
        contents = template.render(
            package_name=self.package_name,
            author_name=self.author_name,
            author_email=self.author_email
        )
        return contents

    def start(self):
        # make sure the dest dir exists
        os.makedirs(self.package_root, exist_ok=True)
        # do the simple files (template, dest)
        simple_files = [
            ('license.txt', 'LICENSE'),
            ('manifest.txt', 'MANIFEST.in'),
            ('changes.txt', 'CHANGES.txt'),
            ('gitignore.txt', '.gitignore')
        ]
        for template, dest in simple_files:
            contents = self._get_rendered_template(template)
            self._write_file(contents, os.path.join(self.package_root, dest))
        # do the customizable files
        customizable_files = [
            (self._readme, 'README'),
            (self._setup, 'setup.py')
        ]
        for file_func, dest in customizable_files:
            contents = file_func()
            self._write_file(contents, os.path.join(self.package_root, dest))
        # do the src dir
        src_dir = self._init_package_dir(self.package_root, self.package_name)
        # do the tests dir
        tests_dir = self._init_package_dir(src_dir, 'tests')
        return

    def __repr__(self):
        return '<PyPiStarter(name={})>'.format(self.package_name)


def parse_args():

    # parse args
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--package-name', action='store', required=True, help='Name of your new project')
    parser.add_argument('-o', '--output-dir', action='store', required=True, help='Where to create your new project')
    parser.add_argument('-a', '--author-name', action='store', required=False, default='tbd', help='Name of project author')
    parser.add_argument('-e', '--author-email', action='store', required=False, default='tbd@tbd.com', help='Email of project author')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    PackageStarter = PyPackageStarter(
        package_name=args.package_name,
        package_root=args.output_dir,
        author_name=author_name,
        author_emai=author_emai
    )
    PackageStarter.start()

    return


if __name__ == '__main__':
    main()
