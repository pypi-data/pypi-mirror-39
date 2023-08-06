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
    name='reahl-web-declarative',
    version='4.0.5',
    description='An implementation of Reahl persisted classes using Elixir.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nSome core elements of Reahl can be implemented for use with different persistence technologies. This is such an implementation based on SqlAlchemy/Elixir.\n\nSee http://www.reahl.org/docs/4.0/tutorial/gettingstarted-install.d.html for installation instructions. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.webdeclarative', 'reahl.webdeclarative_dev'],
    py_modules=[],
    include_package_data=True,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['reahl-sqlalchemysupport>=4.0,<4.1', 'reahl-web>=4.0,<4.1', 'reahl-component>=4.0,<4.1'],
    setup_requires=['setuptools-git>=1.1,<1.1.999', 'pytest-runner'],
    tests_require=['webob>=1.4,<1.4.999', 'pytest>=3.0', 'reahl-tofu>=4.0,<4.1', 'reahl-stubble>=4.0,<4.1', 'reahl-dev>=4.0,<4.1', 'reahl-webdev>=4.0,<4.1', 'reahl-postgresqlsupport>=4.0,<4.1'],
    test_suite='reahl.webdeclarative_dev',
    entry_points={
        'reahl.persistlist': [
            '0 = reahl.webdeclarative.webdeclarative:UserSession',
            '1 = reahl.webdeclarative.webdeclarative:SessionData',
            '2 = reahl.webdeclarative.webdeclarative:UserInput',
            '3 = reahl.webdeclarative.webdeclarative:PersistedException',
            '4 = reahl.webdeclarative.webdeclarative:PersistedFile'    ],
        'reahl.eggs': [
            'Egg = reahl.component.eggs:ReahlEgg'    ],
        'reahl.configspec': [
            'config = reahl.webdeclarative.webdeclarative:WebDeclarativeConfig'    ],
        'reahl.migratelist': [
            '0 = reahl.webdeclarative.migrations:RenameRegionToUi',
            '1 = reahl.webdeclarative.migrations:ElixirToDeclarativeWebDeclarativeChanges',
            '2 = reahl.webdeclarative.migrations:MergeWebUserSessionToUserSession',
            '3 = reahl.webdeclarative.migrations:RenameContentType',
            '4 = reahl.webdeclarative.migrations:AllowNullUserInputValue'    ],
        'reahl.scheduled_jobs': [
            'reahl.webdeclarative.webdeclarative:UserSession.remove_dead_sessions = reahl.webdeclarative.webdeclarative:UserSession.remove_dead_sessions'    ],
                 },
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
