from setuptools import setup

setup(
    name="django-server-side-piwik",
    version="1.1.1",
    author="David Burke",
    author_email="david@burkesoftware.com",
    description=("Send analytics data to piwik using celery"),
    license="BSD",
    keywords="django piwik",
    url="https://gitlab.com/burke-software/django-server-side-piwik",
    packages=['server_side_piwik'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.3',
    install_requires=[
        'celery>=4.1.0',
        'django-ipware',
        'piwikapi>=0.3',
    ]
)

