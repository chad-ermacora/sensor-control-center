from guizero import App, Window, Text


class MainApplication:
    def __init__(self):
        self.app = App(title="KootNet Sensors - PC Control Center",
                       width=405,
                       height=295,
                       layout="grid")

        self.test_text = Text(self.app,
                              text="Main App Variance",
                              color='green',
                              grid=[1, 1],
                              align="left")


class AboutWindow:
    def __init__(self, app):
        self.window_app_about = Window(app,
                                       title="About KootNet Sensors - PC Control Center",
                                       width=610,
                                       height=325,
                                       layout="grid",
                                       visible=True)
        self.test_text = Text(self.window_app_about,
                              text="about Text",
                              color='green',
                              grid=[1, 1],
                              align="left")


def change_text(textbox, text):
    textbox.value = text


new_app = MainApplication()
new_about_window = AboutWindow(new_app.app)
change_text(new_app.test_text, "test444444444")
new_app.app.display()

# class Test1:
#     def __init__(self):
#         self.var1 = "test1: var1"
#         self.var2 = "test1: var2"
#
#
# class Test2:
#     def __init__(self):
#         self.var1 = "test2: var1"
#         self.var2 = "test2: var2"
#
#
# class Test3:
#     def __init__(self):
#         self.var1 = "test3: var1"
#         self.var2 = "test3: var2"
#
#
# def print_test(test):
#     print(test.var1)
#     print(test.var2)
#
#
# def mod_var1(test):
#     test.var1 = "Changed"
#
#
# def mod_var2(test):
#     test.var2 = "Changed2"
#
#
# test_1 = Test1()
# test_2 = Test2()
# test_3 = Test3()
#
# print_test(test_1)
# print_test(test_2)
# print_test(test_3)
#
# mod_var1(test_1)
# print_test(test_1)
# print_test(test_2)
# print_test(test_3)
# mod_var2(test_3)
#
# print_test(test_1)
# print_test(test_2)
# print_test(test_3)
