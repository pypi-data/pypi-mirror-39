import falcon
from falcon.response import Response
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

__all__ = ['FalconTemplate']


class FalconTemplateNotFound(Exception):
    pass


class FalconTemplate:
    """
        Args:
            path (str): Name of an directory where HTML files defined.

        Attributes:
            _env (jinja2.Environment): Jinja component which shared
            variables like configuration and etc.

            template_path (str): Name of folder where all
            HTML files are defined.

            loader (jinja2.FileSystemLoader): Jinja2 class which loaded
            HTML template from filesystem.
    """

    BASE_FOLDER = 'templates'

    def __init__(self, path: str = None):
        self.template_path = path or self.BASE_FOLDER
        self.loader = FileSystemLoader(self.template_path)
        self._env = Environment(loader=self.loader)

    @staticmethod
    def __get_response(objects: tuple):
        """Retrieve falcon's Response object
            Args:
                objects (tuple): An list with falcon.Request,
                falcon.Response, and other arguments.

            Returns:
                An falcon.Response object if it there
                otherwise False.
        """
        for response in objects:
            if isinstance(response, Response):
                return response
        return False

    def _make_template(self, template: str, context: dict):
        """Makes a jinja template, and rendered passed context

            Args:
                template (str): Name of HTML file which will be rendered.

                context (dict): An dictionary with
                a response context.

            Returns:
                A string representation of HTML content
        """
        try:
            template = self._env.get_template(template)
        except TemplateNotFound:
            raise FalconTemplateNotFound(
                'Template {} not found '
                'in {} folder'.format(template, self.template_path)
            )
        return template.render(**context)

    def render(self, template: str):
        """Decorator which renders HTML content

            Args:
                template (str): HTML file for which will
                be rendered HTML content
        """
        def render_template(func):
            def wrapper(*args, **kwargs):

                response = self.__get_response(args)
                func(*args, **kwargs)

                response.content_type = falcon.MEDIA_HTML
                response.status = falcon.HTTP_200
                response.body = self._make_template(
                    template, response.context
                )
            return wrapper
        return render_template
