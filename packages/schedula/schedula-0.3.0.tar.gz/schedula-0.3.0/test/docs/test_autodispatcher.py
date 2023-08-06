import os
import unittest
import schedula as sh
try:
    from .util import TestApp, Struct
except SystemError:
    from test.docs.util import TestApp, Struct

app = None

directive = options = None

_warnings = []


def _setup(**kw):
    global options, directive, _warnings, app
    from schedula.ext.dispatcher import PLOT
    _warnings = []
    options = Struct(
        des=True,
        opt=PLOT,
        data=True,
        func=True,
        code=True,
        dsp=True,
        inherited_members=False,
        undoc_members=False,
        private_members=False,
        special_members=False,
        imported_members=False,
        show_inheritance=False,
        noindex=False,
        annotation=None,
        synopsis='',
        platform='',
        deprecated=False,
        members=[],
        member_order='alphabetic',
        exclude_members=set(),
    )
    from docutils.statemachine import ViewList
    directive = Struct(
        env=app.builder.env,
        genopt=options,
        result=ViewList(),
        warn=warnfunc,
        filename_set=set(),
        **kw
    )


def warnfunc(msg):
    _warnings.append(msg)


def assert_equal_items(test, items):
    global directive
    items = list(reversed(items))
    it = iter(directive.result)
    while items:
        item = items.pop()
        v = next(it)
        test.assertEqual(item, v, 'item %r not found in result or not in'
                                  ' the correct order' % item)
    del directive.result[:]


EXTRAS = os.environ.get('EXTRAS', 'all')


@unittest.skipIf(EXTRAS not in ('all', 'sphinx'), 'Not for extra %s.' % EXTRAS)
class TestDispatcherDirective(unittest.TestCase):
    def setUp(self):
        global app
        app = TestApp()
        app.builder.env.app = app
        app.builder.env.temp_data['docname'] = 'dummy'

    def tearDown(self):
        global app
        app.cleanup()

    def test_format_signature(self):
        _setup()

        def formatsig(name, obj, args, retann):
            global directive
            from schedula.ext.dispatcher.documenter import DispatcherDocumenter
            inst = DispatcherDocumenter(directive, name)
            inst.fullname = name
            inst.doc_as_attr = False  # for class objtype
            inst.object = obj
            inst.objpath = [name]
            inst.args = args
            inst.retann = retann
            res = inst.format_signature()
            return res

        # no signatures for dispatchers
        dsp = sh.Dispatcher()
        self.assertEqual(formatsig('dsp', dsp, None, None), '')

    def test_get_doc(self):
        _setup()

        def getdocl(obj, name, encoding=None):
            global directive
            from schedula.ext.dispatcher.documenter import DispatcherDocumenter
            inst = DispatcherDocumenter(directive, name)

            inst.objpath = [name]
            inst.object = obj
            ds = inst.get_doc(encoding)
            # for testing, concat them and strip the empty line at the end.
            res = sum(ds, [])[:-1]
            return res

        # objects without docstring
        dsp_local = sh.Dispatcher()
        self.assertEqual(getdocl(dsp_local, 'dsp_local'), [])

        dsp_local = sh.Dispatcher(description='Description')
        res = getdocl(dsp_local, 'dsp_local')
        self.assertEqual(res, ['Description'])

        dsp_local.__doc__ = 'First line\n\nOther\n  lines'
        res = getdocl(dsp_local, 'dsp_local')
        self.assertEqual(res, ['First line', '', 'Other', '  lines'])

    def test_docstring_property_processing(self):
        _setup()

        def genarate_docstring(name, **kw):
            global directive
            from schedula.ext.dispatcher.documenter import DispatcherDocumenter
            inst = DispatcherDocumenter(directive, name)
            inst.generate(**kw)
            results = list(directive.result)
            del directive.result[:]
            return results

        results = genarate_docstring(__name__ + '.dsp')
        assert '.. py:data:: dsp' in results
        assert '   :module: %s' % __name__ in results
        assert '   :annotation:  = Pippo' in results

    def test_code(self):
        import docutils.statemachine
        content_offset = 0
        content = docutils.statemachine.StringList(
            [" >>> from schedula import Dispatcher",
             " >>> s = Dispatcher(name='Dispatcher')",
             " >>> f = s.add_function('fun', lambda x: 0, ['a'], ['b'])"])
        content._offset = content_offset
        _setup(
            arguments=['dsp'],
            options={'opt': "graph_attr={'ratio': '1'}", 'code': True},
            content=content,
            content_offset=content_offset
        )

        def assert_result(self, items, name, **kw):
            global directive
            from schedula.ext.dispatcher.documenter import DispatcherDocumenter
            inst = DispatcherDocumenter(directive, name)
            inst.generate(**kw)
            assert len(_warnings) == 0, _warnings
            assert_equal_items(self, items)

        res = ['', '',
               '    >>> from schedula import Dispatcher',
               "    >>> s = Dispatcher(name='Dispatcher')",
               "    >>> f = s.add_function('fun', lambda x: 0, ['a'], ['b'])",
               '   ', '   ', '   ',
               '   .. dsp:: _build/_dispatchers/dispatcher-e6fae1119c5ef15c4426de01b7ad758f98e88d54.gv',
               '      :graphviz_dot: dot',
               '   ',
               "   .. csv-table:: **Dispatcher's data**",
               '   ',
               '      ":obj:`a <>`", ""',
               '      ":obj:`b <>`", ""',
               '   ',
               "   .. csv-table:: **Dispatcher's functions**",
               '   ',
               '      ":func:`fun <None.<lambda>>`", ""',
               '   ']
        assert_result(self, res, 's', more_content=content)

    def test_generate(self):
        _setup()

        def assert_result(self, items, name, **kw):
            global directive
            from schedula.ext.dispatcher.documenter import DispatcherDocumenter
            inst = DispatcherDocumenter(directive, name)
            inst.generate(**kw)
            assert len(_warnings) == 0, _warnings
            assert_equal_items(self, items)

        directive.env.ref_context['py:module'] = __name__

        res = [
            '',
            '.. py:data:: dsp',
            '   :module: %s' % __name__,
            '   :annotation:  = Pippo',
            '',
            '   Docstring 1',
            '   ',
            '   good',
            '   ',
            '   .. dsp:: _build/_dispatchers/dispatcher-73e25d64a2d3385b1a6fde2e07406deab3171ab2.gv',
            '      :graphviz_dot: dot',
            '   ',
            "   .. csv-table:: **Pippo's data**",
            '   ',
            '      ":obj:`a <>`", "Description of a"',
            '      ":obj:`b <>`", "Nice e."',
            '      ":obj:`c <>`", "Nice f."',
            '      ":obj:`d <>`", "Other args."',
            '      ":obj:`e <>`", "Nice arg."',
            '      ":obj:`sink <>`", "Sink node of the dispatcher that '
            'collects all unused outputs."',
            '      ":obj:`start <>`", "Starting node that identifies '
            'initial inputs of the workflow."',
            '   ',
            "   .. csv-table:: **Pippo's functions**",
            '   ',
            '      ":func:`fun1 <>`", "Fun1"',
            '      ":func:`fun2 <%s.fun2>`", "Fun2"' % __name__,
            '      ":func:`fun3 <%s.fun2>`", "Fun3"' % __name__,
            '   ']
        assert_result(self, res, 'dsp')

        res[1] = '.. py:data:: dsp_1'
        res[5] = '   Docstring 2'
        res[9] = '   .. dsp:: _build/_dispatchers/dispatcher-c4cdb95f7c323136c07b06e9cc9e97c054e65cd3.gv'
        assert_result(self, res, 'dsp_1')

        res[1] = '.. py:data:: dsp_2'
        res[5] = '   Docstring 3'
        res[9] = '   .. dsp:: _build/_dispatchers/dispatcher-626650ebb81b12cfd2764e7dde8087e834a31bd1.gv'
        assert_result(self, res, 'dsp_2')

    def test_build(self):
        app = TestApp()
        app.builder.env.app = app
        app.builder.env.temp_data['docname'] = 'dummy'
        app.build(True)
        s = 'while setting up extension'
        errors = [v for v in app._warning.content if s not in v and v != '\n']
        self.assertEqual(errors, [], '\n'.join(errors))


def fun2(e, my_args, *args):
    """
    Fun2

    error

    :param None e:
        Nice e.

        error

    :param my_args:
        Nice arg.

        error
    :type my_args: None

    :param args:
        Other args.

        error
    :type args: None

    :returns:
        Nice f.

        error
    :rtype: None
    """
    return


#: Docstring 1
#:
#: good
dsp = sh.Dispatcher(name='Pippo', description='Docstring 2\n\ngood')
dsp.add_data(data_id='a', description='Description of a\n\nerror')
dsp.add_function(function_id='fun1', description='Fun1\n\nerror')
dsp.add_function('fun2', fun2, ['b', 'e', 'd'], ['c'])
dsp.add_function('fun3', fun2, description='Fun3\n\nerror')

dsp_1 = dsp

dsp_2 = dsp
"""
Docstring 3

good
"""
