from .__base__ import Base
from typing import Dict
from datetime import datetime


class Friends(Base):
    """ Object represents friend list and friends. """

    def _startup(self):
        self._register_files({
            "__friends": "friends/friends.json",
            "__received_friend_requests": "friends/received_friend_requests.json",
            "__rejected_friend_requests": "friends/rejected_friend_requests.json",
            "__sent_friend_requests": "friends/sent_friend_requests.json",
            "__removed_friends": "friends/removed_friends.json",
        })
        pass

    def describe(self) -> str:
        """
        Returns summary of friends list in time and counts requests and removing.

        :rtype: str
        :return:
        """
        def percent(part, sm) -> float:
            return round(100 * (part / sm), 2) if sm else sm

        def text_graph_by_year() -> str:
            bar_len = 20
            data = self.friends_by_year()
            b = ''
            for y in data:
                filled = int(round(bar_len * data[y] / float(len(self.friends))))

                b += f"{y}: {'#'*filled + '.' * (bar_len - filled)}  " \
                     f"{data[y]} ({round(percent(data[y], len(self.friends)), 1)}%)\n"
                pass
            return b

        s = len(self.friends) + len(self.received_requests) + len(self.rejected_requests) + len(self.sent_requests)
        return f"""Percentages without removed friends
Friends:\t\t{len(self.friends)} ({percent(len(self.friends), s)}%)
Requests:
\tReceived:\t{len(self.received_requests)} ({percent(len(self.received_requests), s)}%)
\tRejected:\t{len(self.rejected_requests)} ({percent(len(self.rejected_requests), s)}%)
\tSent:\t\t{len(self.sent_requests)} ({percent(len(self.sent_requests), s)}%)

Removed friends:\t{len(self.removed_friends)} ({percent(len(self.removed_friends), s + len(self.removed_friends))}%, with all states)

New friends in time:
{text_graph_by_year()}"""
        pass

    def friends_by_year(self) -> Dict[int, int]:
        """
        Returns dict where key is year and value count of friends added in the year.

        :rtype: Dict[int, int]
        :return:
        """
        # TODO: RemovedFriend.Timestamp is timestamp of remove or add friends?
        counter = {}
        for friend in self.friends:
            year = datetime.fromtimestamp(friend['timestamp']).year
            if year in counter:
                counter[year] += 1
                pass
            else:
                counter[year] = 1
                pass
            pass
        return counter

    @property
    def friends(self):
        return self.__getattribute__('__friends')['friends']

    @property
    def removed_friends(self):
        return self.__getattribute__('__removed_friends')['deleted_friends']

    @property
    def received_requests(self):
        return self.__getattribute__('__received_friend_requests')['received_requests']

    @property
    def rejected_requests(self):
        return self.__getattribute__('__rejected_friend_requests')['rejected_requests']

    @property
    def sent_requests(self):
        return self.__getattribute__('__sent_friend_requests')['sent_requests']

    def __str__(self):
        return f"Friends: {len(self.friends)}, Removed: {len(self.removed_friends)}, " \
               f"Requests Received/Rejected/Sent: " \
               f"{len(self.received_requests)}/" \
               f"{len(self.rejected_requests)}/" \
               f"{len(self.sent_requests)}"

    def __repr__(self):
        return f"<{str(self)}>"
        pass
