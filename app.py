from typing import List, Iterator, NamedTuple, Optional, Set, Tuple
from flask import Flask, render_template, request
app = Flask(__name__)


class PackageInfo(NamedTuple):
    """
    Representation of paragraph in package dependency file based on:
        https://www.debian.org/doc/debian-policy/ch-controlfields.html

    Some fields have been ommitted, but can be added under
    """
    name: str
    status: str
    priority: str
    section: str
    installed_size: str
    maintainer: str
    architecture: str
    version: str
    description: str
    dependencies: Set[Tuple[str]]
    paragraph: str

    def __str__(self):
        """ Retursn pretty string representation """
        discard = ('description', 'dependencies', 'maintainer', 'version', 'paragraph')
        attrs = ', '.join('%s=%r' % (k, v) for k, v in self._asdict().items() if k not in discard)
        repr = '%s(%s)' % (self.__class__.__name__, attrs)
        return repr

    @staticmethod
    def _parse_paragraph(paragraph: str) -> dict:
        """ Parses a paragraph from file to dict """
        parsed = {}
        lines = paragraph.replace('\n ', ' ').replace('\n\t', ' ').splitlines()
        for line in lines:
            field, sep, value = line.partition(':')
            parsed[field.strip()] = value.strip()

        return parsed

    @staticmethod
    def _parse_depends(depends: Optional[str]) -> set:
        """ Parses Depends field from paragraph to set of tuples """
        dependencies = set()
        if not isinstance(depends, str):
            return dependencies

        for dependency in depends.replace(' ','').split(','):
            packages = []
            for alternative in dependency.split('|'):
                # drop version
                package, sep, version = alternative.partition('(')
                packages.append(package)

            dependencies.add(tuple(packages))

        return dependencies

    @classmethod
    def from_paragraph(cls, paragraph: str):
        """ Alternative constructor: Create PackageInfo object from paragraph"""
        parsed = cls._parse_paragraph(paragraph)
        dependencies = cls._parse_depends(parsed.get('Depends'))
        instance = cls(
            name=parsed.get('Package', ''),
            status=parsed.get('Status', ''),
            priority=parsed.get('Priority', ''),
            section=parsed.get('Section', ''),
            installed_size=parsed.get('Installed-Size', ''),
            maintainer=parsed.get('Maintainer', ''),
            architecture=parsed.get('Architecture', ''),
            version=parsed.get('Version', ''),
            description=parsed.get('Description', ''),
            dependencies=dependencies,
            paragraph=paragraph
        )
        return instance


def _read_dpkg_file(dpkg_path: str = '/var/lib/dpkg/status') -> List[str]:
    """ Reads dpkg file and returns list of paragraphs"""
    try:
        with open(dpkg_path, 'r') as dpkg_file:
            data = dpkg_file.read()
    except OSError:
        raise

    # split by paragraph
    paragraphs = data.split('\n\n')
    return paragraphs


def _parse_dpkg_content(paragraphs: List[str]) -> Iterator[PackageInfo]:
    """ Parses content of dpkg file and yields an PackageInfo object """
    for paragraph in paragraphs:
        package_info = PackageInfo.from_paragraph(paragraph)

        # skip packages without name
        if not package_info.name:
            continue

        yield PackageInfo.from_paragraph(paragraph)


def get_all_packages(dpkg_path: str = '/var/lib/dpkg/status') -> List[PackageInfo]:
    """ Returns all packages from dpkg file as PackageInfo objects """
    paragraphs = _read_dpkg_file(dpkg_path)
    packages = list(_parse_dpkg_content(paragraphs))
    return packages


def get_package(name: str, dpkg_path: str = '/var/lib/dpkg/status') -> Optional[PackageInfo]:
    """ Returns package with name if found, otherwise None"""
    paragraphs = _read_dpkg_file(dpkg_path)
    mapped = {package.name: package for package in _parse_dpkg_content(paragraphs)}
    match = mapped.get(name)
    return match


def get_package_and_reverse_dependencies(name: str, dpkg_path: str = '/var/lib/dpkg/status') -> Tuple[Optional[PackageInfo], Set[str]]:
    """
    Returns package and its reverse dependencies if found,
    otherwise None and empty set
    """
    reverse_dependencies = set()
    paragraphs = _read_dpkg_file(dpkg_path)
    packages = list(_parse_dpkg_content(paragraphs))
    mapped = {package.name: package for package in packages}
    match = mapped.get(name)

    if match is None:
        return None, reverse_dependencies

    for package in packages:
        dependencies = []
        for dependency in package.dependencies:
            dependencies.extend(list(dependency))

        if name in dependencies:
            reverse_dependencies.add(package.name)

    return match, reverse_dependencies


@app.route('/', methods=['GET'])
def index():
    try:
        packages = get_all_packages()
    except Exception as e:
        return "Failed to get packages. Reason: %s" % str(e)

    packages.sort(key=lambda x: x.name)
    amount = len(packages)
    return render_template('index.html', packages=packages, row_amount=amount)


@app.route('/<package_name>', methods=['GET'])
def detail(package_name):
    package, rev_deps = get_package_and_reverse_dependencies(package_name)
    return render_template('detail.html', query_name=package_name, package=package, reverse_dependencies=rev_deps)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
