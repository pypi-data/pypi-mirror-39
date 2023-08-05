import Orange
from Orange.widgets.tests.base import WidgetTest
from orangecontrib.spectroscopy.widgets.owintegrate import OWIntegrate, PREPROCESSORS


class TestOWIntegrate(WidgetTest):

    def setUp(self):
        self.widget = self.create_widget(OWIntegrate)

    def test_load_unload(self):
        self.send_signal("Data", Orange.data.Table("iris.tab"))
        self.send_signal("Data", None)

    def test_allint_indv(self):
        data = Orange.data.Table("peach_juice.dpt")
        for i,p in enumerate(PREPROCESSORS):
            self.widget = self.create_widget(OWIntegrate)
            self.send_signal("Data", data)
            self.widget.add_preprocessor(i)
            # direct calls the preview so that exceptions do not get lost in Qt
            self.widget.show_preview()

    def test_allint_indv_empty(self):
        data = Orange.data.Table("peach_juice.dpt")[:0]
        for i, p in enumerate(PREPROCESSORS):
            self.widget = self.create_widget(OWIntegrate)
            self.send_signal("Data", data)
            self.widget.add_preprocessor(i)
            self.widget.show_preview()  # direct call
        # no attributes
        data = Orange.data.Table("peach_juice.dpt")
        data = Orange.data.Table(Orange.data.Domain([],
                class_vars=data.domain.class_vars,
                metas=data.domain.metas), data)
        for i, p in enumerate(PREPROCESSORS):
            self.widget = self.create_widget(OWIntegrate)
            self.send_signal("Data", data)
            self.widget.add_preprocessor(i)
            self.widget.show_preview()  # direct call
