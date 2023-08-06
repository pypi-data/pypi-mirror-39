import os
import sys
import pydoc
import inspect
import logging


def _module_header(module):
    return [
        '# {module_name}'.format(module_name=module.__name__),
        ''
    ]


def _class_header(class_, parent):
    return [
        '',
        '## Class **{class_name}**'.format(
            parent_name=parent.__name__,
            class_name=class_.__name__
        ),
        ''
    ]


def _functions_header(parent):
    return ['', '## Functions', '']


def _function_header(function_, parent):
    return [
        '',
        '### **{function_name}**'.format(
            function_name=function_.__name__
        ),
        ''
    ]


def _method_header(method, parent):
    if method.__name__ == '__init__':
        return ['', '### Constructor', '']

    return [
        '',
        '### **{function_name}**'.format(
            function_name=method.__name__
        ),
        ''
    ]


def _function_signature(function_, parent):
    args_specs = pydoc.inspect.getargspec(function_)
    args_signature = pydoc.inspect.formatargspec(*args_specs)
    return [
        '```python',
        '{parent_name}.{function_name}{args_signature}'.format(
            parent_name=parent.__name__,
            function_name=function_.__name__,
            args_signature=args_signature
        ),
        '```',
        ''
    ]


def _method_signature(method, parent):
    args, varags, varkw, defaults = pydoc.inspect.getargspec(method)
    args_signature = pydoc.inspect.formatargspec(args[1:], varags, varkw, defaults)

    if method.__name__ == '__init__':
        name = ""
    else:
        name = "." + method.__name__

    return [
        '```python',
        '{parent_name}{function_name}{args_signature}'.format(
            parent_name=parent.__name__,
            function_name=name,
            args_signature=args_signature
        ),
        '```',
        ''
    ]


def _separator():
    return [
        '',
        '***',
        ''
    ]


def _is_function_or_method(object_):
    return pydoc.inspect.isfunction(object_) or pydoc.inspect.ismethod(object_)


def _format_docstring(docstring):
    output = list()
    lines = docstring.split('\n')

    inside_caption = True

    caption = list()
    arguments = list()
    return_message = ""

    for line in lines:
        if line.startswith(':'):
            inside_caption = False
            _, arg, role = line.split(':')

            if arg == "return":
                return_message = "**Returns :** " + role
                continue
            else:
                arg = "`" + arg.replace("param ", "") + "`"
            arguments.append([arg, role])

        elif not inside_caption:
            arguments[-1][1] += " " + line

        if inside_caption:
            caption.append(line)

    caption = "\n".join(caption)
    output.append(caption)

    if arguments:
        output.append("")
        output.append("| Argument | Role |")
        output.append("| --- | --- |")

        for argument in arguments:
            output.append("| %s | %s |" % (argument[0], argument[1]))

    if return_message:
        output.append("")
        output.append(return_message)

    return output


def get_module(module_name):
    try:
        working_dir = os.getcwd()
        if working_dir not in sys.path:
            sys.path.append(working_dir)

        module = pydoc.safeimport(module_name)
        logging.info("Imported '%s'" % module_name)

        if module is None:
            logging.info("Module '%s' not found" % module_name)
            return

        return module

    except pydoc.ErrorDuringImport as e:
        logging.warning("Error while trying to import '%s' :" % module_name)
        logging.warning(e)


def make_output_filepath(module):
    filepath = module.__file__
    filepath, ext = os.path.splitext(filepath)

    if filepath.endswith('__init__'):
        filepath = os.path.join(os.path.dirname(os.path.dirname(filepath)), module.__name__)

    return filepath + ".md"


def get_markdown(module):
    logging.info("Generating markdown from %s" % module.__file__)
    output = _module_header(module)

    doc = pydoc.inspect.getdoc(module)
    if doc is not None:
        output.append(doc)

    output.extend(get_classes(module))

    functions = get_functions(module)

    if functions:
        output.extend(_functions_header(module))
        output.extend(functions)

    if hasattr(module, "DISCLAIMER"):
        output.extend([
            '',
            '---',
            '',
            module.DISCLAIMER
        ])

    return "\n".join([str(item) for item in output])


def _is_foreign(object_, parent):
    try:
        file_ = inspect.getsourcefile(object_)
    except TypeError:
        return True

    return file_ != parent.__file__


def get_functions(item):
    output = list()

    for function_name, function in pydoc.inspect.getmembers(item, _is_function_or_method):
        logging.info(" => generating Markdown for function : %s" % function_name)

        if function_name.startswith("_") or _is_foreign(function, parent=item):
            logging.info("    skipped")
            continue

        output.extend(_function_header(function, parent=item))
        output.extend(_function_signature(function, parent=item))

        docstring = pydoc.inspect.getdoc(function)
        if docstring is not None:
            output.extend(_format_docstring(docstring))

        logging.info("    ok")

    return output


def get_methods(class_):
    output = list()

    for method_name, method in pydoc.inspect.getmembers(class_, _is_function_or_method):
        logging.info(" -> generating Markdown for method : %s.%s" % (class_.__name__, method_name))

        if method_name.startswith("_") and method_name != '__init__':
            logging.info("    skipped")
            continue

        output.extend(_method_header(method, parent=class_))
        output.extend(_method_signature(method, parent=class_))

        docstring = pydoc.inspect.getdoc(method)
        if docstring is not None:
            output.extend(_format_docstring(docstring))

        logging.info("    ok")

    return output


def get_classes(item):
    output = list()

    for class_name, class_ in inspect.getmembers(item, inspect.isclass):
        logging.info(" => generating Markdown for class : %s" % class_name)

        if class_ is None or class_name.startswith("_") or _is_foreign(class_, parent=item):
            logging.info("    skipped")
            continue

        output.extend(_class_header(class_, parent=item))

        doc = pydoc.inspect.getdoc(class_)
        if doc is not None:
            output.append(doc)

        output.extend(get_methods(class_))
        output.extend(get_classes(class_))

        logging.info("    ok")

    return output
