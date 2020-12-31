from ovos_utils.skills.templates.video_collection import VideoCollectionSkill, \
    CPSMatchLevel, CPSMatchType
from mycroft.skills.core import intent_file_handler
from pyvod import Collection
from os.path import join, dirname, basename


class BlackMetalSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("TRVEKVLT")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.VIDEO,
                                CPSMatchType.MUSIC]

        path = join(dirname(__file__), "res", "trveKvlt.jsondb")
        self.default_image = join(dirname(__file__), "res", "trvekvlt_logo.png")
        # load video catalog
        self.media_collection = Collection("TrveKvlt", logo=self.default_image, db_path=path)

    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # matching
    def match_media_type(self, phrase, media_type):
        match = None
        score = 0

        if self.voc_match(phrase,
                          "video") or media_type == CPSMatchType.VIDEO:
            score += 0.01
            match = CPSMatchLevel.GENERIC

        if self.voc_match(phrase,
                          "music") or media_type == CPSMatchType.MUSIC:
            score += 0.1
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(phrase, "trve"):
            score += 0.1
            match = CPSMatchLevel.CATEGORY

        if self.voc_match(phrase, "black-metal"):
            score += 0.3
            match = CPSMatchLevel.TITLE

        return match, score

    def calc_final_score(self, phrase, base_score, match_level):
        score = base_score
        if self.voc_match(phrase, "black-metal"):
            score += 0.6
        return score


def create_skill():
    return BlackMetalSkill()
