from cronably.actions.post_action.post_action import PostAction
from cronably.actions.pre_action.pre_actions import PreActions
from cronably.context.context import Context

ext_cronably = None



class Cronably(object):

    def __init__(self, **kwargs):
        global ext_cronably
        self.annotation_params = kwargs
        self.context = None
        self.pre_action = None
        self.post_action = None
        ext_cronably = self

    def __call__(self, original_func):
        decorator_self = self

        def execute(*args):
            decorator_self.pre_actions()
            decorator_self.execute(original_func)
            decorator_self.post_actions()
        return execute

    def pre_actions(self):
        global context
        if not self.annotation_params:
            self.annotation_params = {}
        self.pre_action = PreActions(self.annotation_params)
        self.post_action = PostAction(self.annotation_params)

    def post_actions(self):
        self.post_action.run()

    def execute(self, original_func):
        repetition = self.pre_action.repetition
        Context(self.post_action).execute(original_func, repetition)


def exist_job(name):
    context = ext_cronably.context
    if not context:
        context = Context(PostAction({}))
    return context.check_exist_job(name)

