# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['starlette_apispec']

package_data = \
{'': ['*']}

install_requires = \
['apispec>=0.39.0,<0.40.0', 'starlette>=0.8.8']

setup_kwargs = {
    'name': 'starlette-apispec',
    'version': '0.1.3',
    'description': 'APISpec support for starlette',
    'long_description': '==================\nStarlette APISpec\n==================\n\n    Easy APISpec integration for Starlette\n\n.. image:: https://img.shields.io/travis/Woile/starlette-apispec.svg?style=flat-square\n    :alt: Travis\n    :target: https://travis-ci.org/Woile/starlette-apispec\n\n.. image:: https://img.shields.io/codecov/c/github/Woile/starlette-apispec.svg?style=flat-square\n    :alt: Codecov\n    :target: https://codecov.io/gh/Woile/starlette-apispec\n\n.. image:: https://img.shields.io/pypi/v/starlette-apispec.svg?style=flat-square\n    :alt: PyPI\n    :target: https://pypi.org/project/starlette-apispec/\n\n.. image:: https://img.shields.io/pypi/pyversions/starlette-apispec.svg?style=flat-square\n    :alt: PyPI - Python Version\n    :target: https://pypi.org/project/starlette-apispec/\n\n.. contents::\n    :depth: 2\n\n.. code-block:: python\n\n    from apispec import APISpec\n    from starlette.applications import Starlette\n    from starlette_apispec import APISpecSchemaGenerator\n\n    app = Starlette()\n    app.schema_generator = APISpecSchemaGenerator(\n        APISpec(\n            title="Example API",\n            version="1.0",\n            openapi_version="3.0.0",\n            info={"description": "explanation of the api purpose"},\n            plugins=["apispec.ext.marshmallow"],\n        )\n    )\n\nInstallation\n============\n\n::\n\n    pip install -U starlette-apispec\n\nAlternatively you can do\n\n::\n\n    poetry add starlette-apispec\n\nAbout\n-----\n\nThis library helps you easily document your REST API built with starlette.\n\n`Starlette <https://www.starlette.io/>`_ is a is a lightweight ASGI framework/toolkit,\nwhich is ideal for building high performance asyncio services.\n\n`APISpec <https://apispec.readthedocs.io/en/stable/>`_ supports the `OpenApi Specification <https://github.com/OAI/OpenAPI-Specification>`_\nand it has some useful plugins like `marshmallow <https://marshmallow.readthedocs.io/en/3.0/>`_ support.\n\nVersion supported: :code:`0.39.0`\n\n\nUsage\n=====\n\n\nThis example includes `marshmallow <https://marshmallow.readthedocs.io/en/3.0/>`_ integration\n\n.. code-block:: python\n\n    from apispec import APISpec\n\n    from marshmallow import Schema, fields\n\n    from starlette.applications import Starlette\n    from starlette.endpoints import HTTPEndpoint\n    from starlette.schemas import OpenAPIResponse\n    from starlette_apispec import APISpecSchemaGenerator\n\n\n    class UserSchema(Schema):\n        username = fields.Str(required=True)\n\n\n    app = Starlette()\n    app.schema_generator = APISpecSchemaGenerator(\n        APISpec(\n            title="Example API",\n            version="1.0",\n            openapi_version="3.0.0",\n            info={"description": "explanation of the api purpose"},\n            plugins=["apispec.ext.marshmallow"],\n        )\n    )\n    app.schema_generator.spec.definition("User", schema=UserSchema)\n\n\n    @app.route("/users", methods=["GET", "HEAD"])\n    def list_users(request):\n        """\n        responses:\n        200:\n            description: A list of users.\n            schema: UserSchema\n            examples:\n            [{"username": "tom"}, {"username": "lucy"}]\n        """\n        raise NotImplementedError()\n\n\n    @app.route("/users", methods=["POST"])\n    def create_user(request):\n        """\n        responses:\n        200:\n            description: A user.\n            schema: UserSchema\n            examples:\n            {"username": "tom"}\n        """\n        raise NotImplementedError()\n\n\n    @app.route("/orgs")\n    class OrganisationsEndpoint(HTTPEndpoint):\n        def get(self, request):\n            """\n            responses:\n            200:\n                description: A list of organisations.\n                examples:\n                [{"name": "Foo Corp."}, {"name": "Acme Ltd."}]\n            """\n            raise NotImplementedError()\n\n        def post(self, request):\n            """\n            responses:\n            200:\n                description: An organisation.\n                examples:\n                {"name": "Foo Corp."}\n            """\n            raise NotImplementedError()\n\n\n    @app.route("/schema", methods=["GET"], include_in_schema=False)\n    def schema(request):\n        return OpenAPIResponse(app.schema)\n\nMore documentation\n==================\n\nThis package is basically a proxy, so if you wonder how to do something,\nhere are the sources you need:\n\n`Starlette documentation <https://www.starlette.io/>`_\n\n`APISpec Documentation <https://apispec.readthedocs.io/en/stable/>`_\n\n\nTesting\n=======\n\n1. Clone the repo\n2. Install dependencies\n\n::\n\n    poetry install\n\n3. Run tests\n\n::\n\n    poetry run pytest -s --cov-report term-missing --cov=starlette_apispec tests/\n\n\nContributing\n============\n\n**PRs are welcome!**\n',
    'author': 'Santiago Fraire Willemoes',
    'author_email': 'santiwilly@gmail.com',
    'url': 'https://github.com/Woile/starlette-apispec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
