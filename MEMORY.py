

class Memory(object):

    def __init__(self, question):
        self.question = question
        self.name = []
        self.info = []
        self.answer = []


    def getLast(self):

        memoData = self.answer[-1]
        return memoData
