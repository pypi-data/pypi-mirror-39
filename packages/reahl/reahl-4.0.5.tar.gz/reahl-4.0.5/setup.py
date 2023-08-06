from setuptools import setup, Command
class InstallTestDependencies(Command):
    user_options = []
    def run(self):
        import sys
        import subprocess
        if self.distribution.tests_require: subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"]+self.distribution.tests_require)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='reahl',
    version='4.0.5',
    description='The Reahl web framework.',
    long_description='Reahl is a web application framework for Python programmers.\n\nWith Reahl, programming is done purely in Python, using concepts familiar from GUI programming---like reusable Widgets and Events. There\'s no need for a programmer to know several different languages (HTML, JavaScript, template languages, etc) or to keep up with the tricks of these trades. The abstractions presented by Reahl relieve the programmer from the burden of dealing with the annoying problems of the web: security, accessibility, progressive enhancement (or graceful degradation) and browser quirks.\n\nReahl consists of many different eggs that are not all needed all of the time. This package does not contain much itself, but is an entry point for installing a set of Reahl eggs:\n\nInstall Reahl by installing with extras, eg: pip install "reahl[declarative,sqlite,dev,doc]" to install everything needed to run Reahl on sqlite, the dev tools and documentation. (On Windows platforms, use easy_install instead of pip.)\n\nSee http://www.reahl.org/docs/4.0/tutorial/gettingstarted-install.d.html for installation instructions. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=[],
    py_modules=[],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=[],
    install_requires=[],
    setup_requires=['setuptools-git>=1.1,<1.1.999', 'pytest-runner'],
    tests_require=['pytest>=3.0'],
    test_suite='tests',
    entry_points={
        'reahl.eggs': [
            'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={'doc': ['reahl-doc>=4.0,<4.1'], 'sqlite': ['reahl-sqlitesupport>=4.0,<4.1'], 'all': ['reahl-component>=4.0,<4.1', 'reahl-web>=4.0,<4.1', 'reahl-mailutil>=4.0,<4.1', 'reahl-sqlalchemysupport>=4.0,<4.1', 'reahl-web-declarative>=4.0,<4.1', 'reahl-domain>=4.0,<4.1', 'reahl-domainui>=4.0,<4.1', 'reahl-postgresqlsupport>=4.0,<4.1', 'reahl-sqlitesupport>=4.0,<4.1', 'reahl-mysqlsupport>=4.0,<4.1', 'reahl-dev>=4.0,<4.1', 'reahl-webdev>=4.0,<4.1', 'reahl-stubble>=4.0,<4.1', 'reahl-tofu>=4.0,<4.1', 'reahl-doc>=4.0,<4.1'], 'mysql': ['reahl-mysqlsupport>=4.0,<4.1'], 'declarative': ['reahl-sqlalchemysupport>=4.0,<4.1', 'reahl-web-declarative>=4.0,<4.1', 'reahl-domain>=4.0,<4.1', 'reahl-domainui>=4.0,<4.1'], 'postgresql': ['reahl-postgresqlsupport>=4.0,<4.1'], 'dev': ['reahl-dev>=4.0,<4.1', 'reahl-webdev>=4.0,<4.1', 'reahl-stubble>=4.0,<4.1', 'reahl-tofu>=4.0,<4.1'], 'web': ['reahl-component>=4.0,<4.1', 'reahl-web>=4.0,<4.1', 'reahl-mailutil>=4.0,<4.1']},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
