from .__base__ import Base
from typing import List, Union
from os.path import join
from glob import glob
from click import progressbar


class Threads(Base):
    """ Object represents threads. """
    __analysis = None
    threads = []

    def _startup(self):
        g = glob(join(self._path, 'messages/*/message.json'))
        if self._verbose:
            with progressbar(g, length=len(g), label="Loading data") as bar:
                for x in bar:
                    self.threads.append(Thread(**self.parse_file(x)))
                    pass
                pass
            pass
        else:
            for x in g:
                self.threads.append(Thread(**self.parse_file(x)))
                pass
            pass
        pass

    @property
    def analysis(self):
        """
        Returns Analysis object of threads.

        :rtype: Analysis
        :return:
        """
        if self.__analysis:
            return self.__analysis

        self.__analysis = Analysis()

        for t in self.threads:
            assert isinstance(t, Thread)
            self.__analysis.call_duration += t.analysis.call_duration
            self.__analysis.audio_files += t.analysis.audio_files
            self.__analysis.sticker += t.analysis.sticker
            self.__analysis.photos += t.analysis.photos
            self.__analysis.videos += t.analysis.videos
            self.__analysis.calls += t.analysis.calls
            self.__analysis.files += t.analysis.files
            self.__analysis.share += t.analysis.share
            self.__analysis.texts += t.analysis.texts
            self.__analysis.plan += t.analysis.plan
            self.__analysis.gifs += t.analysis.gifs
            pass
        return self.__analysis
    pass

    def find_thread_by_name(self, name: str):
        """
        Returns thread by name.

        :param name:
        :rtype: Union[Thread, bool]
        :return:
        """
        for t in self.threads:
            assert isinstance(t, Thread)  # For PyCharm

            if t.title == name:
                return t
            pass
        return False

    def find_threads_by_participant(self, name: str):
        """
        Returns threads by name of participant.

        :param name:
        :rtype: List[Thread]
        :return:
        """
        threads = []
        for t in self.threads:
            assert isinstance(t, Thread)  # For PyCharm

            if t.participants and name in t.participants:
                threads.append(t)
                pass
            pass

        return threads

    def describe(self) -> str:
        """
        Returns summary of threads.

        :rtype: str
        :return:
        """
        d = self.analysis.call_duration
        return f"""Threads: {len(self.threads)}

Text messages:  {self.analysis.texts}
Stickers:       {self.analysis.sticker}
Photos:         {self.analysis.photos}
Videos:         {self.analysis.videos}
Gifs:           {self.analysis.gifs}
Audios:         {self.analysis.audio_files}
Shares:         {self.analysis.share}
Plans:          {self.analysis.plan}
Calls:          {self.analysis.calls}
Calls duration: {d}s => ~{d // 60}m => ~{d // (60 * 60)}h
"""
        pass


class Thread:
    """ Object represents single thread """
    __analysis = None

    def __init__(self, messages: list, title: str, status, is_still_participant: bool, thread_type, thread_path,
                 participants=None):
        """
        :param list messages:
        :param str title:
        :param status:
        :param bool is_still_participant:
        :param thread_type:
        :param thread_path:
        :param participants:
        """
        self.title = title
        self.status = status
        self.is_still_participant = is_still_participant
        self.thread_type = thread_type
        self.participants = participants
        self.thread_path = thread_path

        self.messages: List[Message] = []

        def d2o(x):
            """
            Helper function for map, transform dict to object Message

            :rtype: Message
            :return:
            """
            return Message(**x)

        self.messages = list(map(d2o, messages))
        pass

    @property
    def analysis(self):
        """
        Returns Analysis object of threads.

        :rtype: Analysis
        :return:
        """
        if self.__analysis:
            return self.__analysis

        self.__analysis = Analysis()
        problem_messages = 0

        for m in self.messages:
            # assert m is Message
            if m.plan:
                self.__analysis.plan += 1
                pass
            elif m.gifs:
                self.__analysis.gifs += 1
                pass
            elif m.files:
                self.__analysis.files += 1
                pass
            elif m.share:
                self.__analysis.share += 1
                pass
            elif m.photos:
                self.__analysis.photos += 1
                pass
            elif m.videos:
                self.__analysis.videos += 1
                pass
            elif m.sticker:
                self.__analysis.sticker += 1
                pass
            elif m.audio_files:
                self.__analysis.audio_files += 1
                pass
            elif m.call_duration:
                self.__analysis.calls += 1
                self.__analysis.call_duration += m.call_duration
                pass
            elif m.content:
                self.__analysis.texts += 1
                pass
            elif m.reactions:
                # print("reaction:", m)
                pass
            else:
                problem_messages += 1
                pass

        if problem_messages and False:  # TODO: verbose mod?
            print("Ignored items: ", problem_messages, f"({self.title})")
        return self.__analysis

    def describe(self) -> str:
        """
        Returns summary of thread.

        :rtype: str
        :return:
        """
        d = self.analysis.call_duration
        return f"""Text messages:  {self.analysis.texts}
Stickers:       {self.analysis.sticker}
Photos:         {self.analysis.photos}
Videos:         {self.analysis.videos}
Gifs:           {self.analysis.gifs}
Audios:         {self.analysis.audio_files}
Shares:         {self.analysis.share}
Plans:          {self.analysis.plan}
Calls:          {self.analysis.calls}
Calls duration: {d}s => ~{d // 60}m => ~{d // (60 * 60)}h
        """
        pass

    def __repr__(self):
        return f"{self.title}: {len(self.messages)} messages"
    pass


class Message:
    """ Object represents single message. """
    def __init__(self, sender_name, timestamp, content=None, type: str = 'Generic', sticker=None, photos=None,
                 reactions=None, gifs=None, call_duration=None, share=None, files=None, videos=None, audio_files=None,
                 plan=None):
        """
        :param sender_name:
        :param timestamp:
        :param content:
        :param str type:
        :param sticker:
        :param photos:
        :param reactions:
        :param gifs:
        :param call_duration:
        :param share:
        :param files:
        :param videos:
        :param audio_files:
        :param plan:
        """
        self.sender_name = sender_name
        self.timestamp = timestamp
        self.content = content
        self.type = type
        self.sticker = sticker
        self.photos = photos
        self.reactions = reactions
        self.gifs = gifs
        self.call_duration = call_duration
        self.share = share
        self.files = files
        self.videos = videos
        self.audio_files = audio_files
        self.plan = plan
        pass

    def __repr__(self):
        return f"From: {self.sender_name}, type: {self.type}"
    pass


class Analysis:
    """ Object for universal analysis of thread or threads. """
    def __init__(self):
        self.plan = 0
        self.gifs = 0
        self.texts = 0
        self.files = 0
        self.share = 0
        self.photos = 0
        self.videos = 0
        self.sticker = 0
        self.audio_files = 0
        self.call_duration = 0
        self.calls = 0
        pass
    pass
