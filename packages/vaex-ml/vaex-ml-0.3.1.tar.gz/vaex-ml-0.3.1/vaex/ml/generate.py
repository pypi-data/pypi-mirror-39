import os
import re
import sys
import traitlets
from . import generate
from collections import defaultdict

# registry = {}
registry = []



def register(cls):
    registry.append(cls)
    # registry[(cls.__module__, cls.__name__)] = cls
    return cls

def camel_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_vaex_ml():
    from jinja2 import Template
    import vaex.ml.transformations
    import vaex.ml.cluster
    import vaex.ml.lightgbm
    import vaex.ml.xgboost
    import vaex.ml.linear_model
    try:
        import vaex.ml.incubator.annoy
    except:
        pass
    try:
        import vaex.ml.incubator.pygbm
    except:
        pass

    docstring_args_template = Template("""
{% for arg in args %}
:param {{ arg.name }}: {{ arg.help }}{% endfor %}
""")

    template_method = Template("""

from {{ module }} import *
import traitlets

def {{ method_name }}(self, {{ signature }}):
    obj = {{ module }}.{{ class_name }}({{ args }})
    obj.fit(self{{ extra_fit }})
    return obj

import vaex.dataset
vaex.dataset.Dataset.ml._add({{ method_name }}={{ method_name }})

def __init__(self, {{ full_signature }}):
    \"\"\"
    {{ docstring_args }}
    \"\"\"
    given_kwargs = {key:value for key, value in dict({{ full_args }}).items() if value is not traitlets.Undefined}

    super({{ module }}.{{ class_name }}, self).__init__(**given_kwargs)

{{ class_name }}.__init__ = __init__
{{ class_name }}.__signature__ = __init__
del __init__
    """)
    filename = os.path.join(os.path.dirname(__file__), "generated.py")
    snippets = defaultdict(list) # module name -> list of snippets
    # with open(filename, "w") as f:
    for cls in generate.registry:
        traits = {key: value for key, value in cls.class_traits().items()
                    if 'output' not in value.metadata}
        traits_nodefault = {key: value for key, value in traits.items()
                            if value.default_value is traitlets.Undefined}
        import IPython
        IPython
        traits_default = {key: value for key, value in traits.items()
                            if key not in traits_nodefault}
        signature_list = ["{name}".format(name=name, value=value.default_value)
                            for name, value in traits_nodefault.items()]
        signature_list.extend(["{name}={value!r}".format(name=name, value=value.default_value)
                                for name, value in traits_default.items()])
        signature = ", ".join(signature_list)
        args = ", ".join(["{name}={name}".format(name=name, value=value)
                            for name, value in traits.items()])

        signature_list = ["{name}={value!r}".format(name=name, value=value.default_value)
                            for name, value in traits.items()]
        full_signature = ", ".join(signature_list)
        full_args = args

        method_name = camel_to_underscore(cls.__name__)
        module = cls.__module__
        class_name = cls.__name__

        doctraits = {name: trait for name, trait in traits.items() if 'help' in trait.metadata}
        args = [{'name': name, 'help': trait.metadata['help']} for name, trait in doctraits.items()]

        kwargs = dict(locals())
        docstring_args = docstring_args_template.render(**kwargs)

        kwargs = dict(locals())
        code = template_method.render(**kwargs)
        snippets[cls.__module__].append(code)
    for module_name, snippets in snippets.items():
        path = sys.modules[module_name].__file__
        basepath, dot, ext = path.rpartition('.')
        dirname, basename = os.path.dirname(basepath), os.path.basename(basepath)
        gen_path = os.path.join(dirname, 'autogen', basename + '.py')
        print(gen_path)
        with open(gen_path, "w") as f:
            f.write('\n'.join(snippets))


def main(argv=sys.argv):
    generate_vaex_ml()


if __name__ == '__main__':
    main()
