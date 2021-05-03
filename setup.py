import setuptools

setuptools.setup(
	name="immuneportal_django_app",
	version="0.0.1",
	description="Custom output viewer and django app for immuneportal_django_app",
	packages=setuptools.find_packages(),
	install_requires=[
		'django>=1.11.16',
		'cclib',
		'numpy',
		'matplotlib',
		'periodictable',
		'scipy',
		'dash',
		'pandas',
		'logomaker'

	],
	entry_points="""
[airavata.output_view_providers]
irneo-pred-link = immuneportal_django_app.output_views:IrneoPredLink
irneo-seq = immuneportal_django_app.output_views:irneoSeq
[airavata.djangoapp]
immuneportal_django_app = immuneportal_django_app.apps:ImmunePortalAppConfig
""",
)
