import random
from abc import abstractproperty, abstractmethod

from robosanta.stackexchange import sede


class PostPicker:
    """
    Abstract class to pick a random post from a list of post ids,
    taken from the Post Link column of a SEDE query.
    """

    @abstractproperty
    def name(self):
        """
        Short name to represent the query, in slug format.
        Used for for caching and logging. Should be unique.

        :return: short name
        """
        raise NotImplementedError

    @abstractproperty
    def url(self):
        """
        SEDE URL to fetch

        :return: a SEDE URL with a Post Link column
        """
        raise NotImplementedError

    @abstractmethod
    def accept(self, post_id):
        """
        Tests whether or not the specified post id should be included in a list.

        :param post_id: the post id to be tested
        :return: (post, accept), where accept = if and only if the post should be included
        """
        raise NotImplementedError

    def pick(self):
        cols, rows = sede.fetch_table(self.name, self.url)

        answer_id_index = cols['Post Link']['index']
        post_ids = [row[answer_id_index]['id'] for row in rows]

        random.shuffle(post_ids)

        for post_id in post_ids:
            post, accept = self.accept(post_id)
            if accept:
                return post

        return None
