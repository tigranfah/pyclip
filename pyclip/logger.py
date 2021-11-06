import logging


def movie_view_log(func):

    def inner_func(movie):
        logging.info("Playing movie {}.".format(movie.name))
        ret = func(movie)
        if ret:
            logging.info("Finished playing movie {}.".format(movie.name))
        else:
            logging.info("Interrupted movie {}.".format(movie.name))

    return inner_func


def pre_clip_message(message):
    def clip_func(func):
        def inner_func(self, *args, **kwargs):
            logging.info(f"Clip {self._info.name} {message}.")
            func(self, *args, **kwargs)
        return inner_func
    return clip_func


def post_clip_message(message):
    def clip_func(func):
        def inner_func(self, *args, **kwargs):
            func(self, *args, **kwargs)
            logging.info(f"Clip {self._info.name} {message}.")
        return inner_func
    return clip_func

# def post_clip_message(func, message):
#     def inner_func(self, *args, **kwargs):
#         logging.info(f"Clip {self._info.name} {message}.")
#         func(*args, **kwargs)
#     return inner_func
