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
    name='reahl-commands',
    version='4.0.5',
    description='The component framework of Reahl.',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nReahl-commands contains useful commandline commands for reahl components.\n\nSee http://www.reahl.org/docs/4.0/tutorial/gettingstarted-install.d.html for installation instructions. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['reahl', 'reahl.commands'],
    py_modules=[],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['six'],
    setup_requires=['setuptools-git>=1.1,<1.1.999', 'pytest-runner'],
    tests_require=['pytest>=3.0', 'reahl-tofu>=4.0,<4.1', 'reahl-stubble>=4.0,<4.1'],
    test_suite='tests',
    entry_points={
        'reahl.component.commands': [
            'CreateDBUser = reahl.commands.prodshell:CreateDBUser',
            'DropDBUser = reahl.commands.prodshell:DropDBUser',
            'CreateDB = reahl.commands.prodshell:CreateDB',
            'DropDB = reahl.commands.prodshell:DropDB',
            'BackupDB = reahl.commands.prodshell:BackupDB',
            'RestoreDB = reahl.commands.prodshell:RestoreDB',
            'BackupAllDB = reahl.commands.prodshell:BackupAllDB',
            'RestoreAllDB = reahl.commands.prodshell:RestoreAllDB',
            'SizeDB = reahl.commands.prodshell:SizeDB',
            'RunJobs = reahl.commands.prodshell:RunJobs',
            'CreateDBTables = reahl.commands.prodshell:CreateDBTables',
            'DropDBTables = reahl.commands.prodshell:DropDBTables',
            'MigrateDB = reahl.commands.prodshell:MigrateDB',
            'DiffDB = reahl.commands.prodshell:DiffDB',
            'ListConfig = reahl.commands.prodshell:ListConfig',
            'CheckConfig = reahl.commands.prodshell:CheckConfig',
            'ListDependencies = reahl.commands.prodshell:ListDependencies',
            'ExportStaticFiles = reahl.commands.prodshell:ExportStaticFiles',
            'ComponentInfo = reahl.commands.prodshell:ComponentInfo'    ],
        'reahl.eggs': [
            'Egg = reahl.component.eggs:ReahlEgg'    ],
        'reahl.migratelist': [
            '0 = reahl.commands.migrations:ReahlCommandsReahlSchemaInitialise'    ],
                 },
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
