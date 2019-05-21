class Memory(object):
    """Use to create a memory record of the conversation"""

    def __init__(self, question):
        self.question = question
        self.name = []
        self.info = []
        self.answer = []


    def getLast(self):
        """Use to get the last answer given by the chatbot"""

        memoData = self.answer[-1]
        return memoData

    def getInfo(self):

        memoData = self.info[-1]
        return memoData
