"""
This is a backport of the Django-compatible template loader from jingo.

The current version of jingo isn't quite compatible with MDN, so this is a
half-attempt to make at least this much work.
"""
from django.conf import settings

try:
    from jingo import Loader as jingo_Loader
except ImportError, e:
    from django.template.loader import BaseLoader
    import jinja2

    class Template(jinja2.Template):

        def render(self, context={}):
            """Render's a template, context can be a Django Context or a
            dictionary.
            """
            from django.template import Origin

            # flatten the Django Context into a single dictionary.
            context_dict = {}
            if hasattr(context, 'dicts'):
                for d in context.dicts:
                    context_dict.update(d)
            else:
                context_dict = context

                # Django Debug Toolbar needs a RequestContext-like object in order
                # to inspect context.
                class FakeRequestContext:
                    dicts = [context]
                context = FakeRequestContext()

            # Used by debug_toolbar.
            if settings.TEMPLATE_DEBUG:
                from django.test import signals
                self.origin = Origin(self.filename)
                signals.template_rendered.send(sender=self, template=self,
                                               context=context)

            return super(Template, self).render(context_dict)

    class jingo_Loader(BaseLoader):

        is_usable = True

        def load_template(self, template_name, template_dirs=None):
            from jingo import env
            from django.template import TemplateDoesNotExist

            env.template_class = Template

            EXCLUDE_APPS = (
                'admin',
                'admindocs',
                'registration',
            )

            if hasattr(template_name, 'rsplit'):
                app = template_name.rsplit('/')[0]
                if app in getattr(settings, 'JINGO_EXCLUDE_APPS', EXCLUDE_APPS):
                    raise TemplateDoesNotExist(template_name)
            try:
                template = env.get_template(template_name)
                return template, template.filename
            except jinja2.TemplateNotFound:
                raise TemplateDoesNotExist(template_name)

