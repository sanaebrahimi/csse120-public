import abc
import datetime
from typing import List

import TermInfo
from Constants import *  # All constants, and only constants, are in ALL_CAPS.
from Session import Session, RegularClassSession, ReviewSession, \
    EveningExamSession, InClassExamSession, CapstoneProjectSession


class ScheduleDay(abc.ABC):
    """ Data associated with a single day in the Schedule. """

    def __init__(self, date: datetime.date, session: Session = None,
                 message: str = None):
        self.date = date
        self.session = session
        self.message = message

    def __repr__(self):
        return "{}/{} {}".format(self.date.month, self.date.day, self.session)

    def date_as_string(self):
        return self.date.strftime('%B') + " " + str(self.date.day)

    @abc.abstractmethod
    def make_html(self) -> str:
        """ Returns the HTML for this ScheduleDay. """
        # Subclasses must implement this method.

    def make_html_for_topics(self):
        # Most of the following HTML should be in the templates, not here.
        if len(self.session.topics) == 1:
            html = '<div class="session-topics one-topic">\n'
        else:
            html = '<div class="session-topics">\n'

        html += "      <ul>\n"
        if len(self.session.topics) == 1:
            html += '        <li><span class="tight">'
            html += self.session.topics[0].topic
            html += "</span></li>\n"
            html += "      </ul>\n"
        else:
            current_level = 0
            for k in range(len(self.session.topics)):
                topic = self.session.topics[k]

                # Down a level:
                if current_level == 1 and topic.level == 2:
                    html += '\n          <ul class="XXX">\n'
                elif current_level == 2 and topic.level == 3:
                    html += '\n            <ul class="YYY">\n'

                # Up a level:
                if current_level == 2 and topic.level == 1:
                    html += "</li>\n          </ul>\n        </li>\n"
                elif current_level == 3 and topic.level == 2:
                    html += "</li>\n          </ul>\n        </li>\n"

                # Same level:
                elif current_level == topic.level:
                    html += "</li>\n"

                current_level = topic.level

                # Now do the item:
                if current_level == 1:
                    html += '        <li><span class="tight">'
                    html += topic.topic
                elif current_level == 2:
                    html += '            <li><span class="tight">'
                    html += topic.topic
                elif current_level == 3:
                    html += '              <li"><span class="tight">'
                    html += topic.topic
                html += "</span>"

            html += "</li>\n"
            if current_level >= 3:
                html += "            </ul>\n        </li>\n"
            if current_level >= 2:
                html += "          </ul>\n        </li>\n"
            if current_level >= 1:
                html += "      </ul>\n"
        html += "    </div>"

        return html


class BeforeClassesStartDay(ScheduleDay):
    def __init__(self, date: datetime.date):
        super().__init__(date, message="No class")
        with open(SCHEDULE_NO_CLASS_TEMPLATE, "r") as file_handle:
            self.template = file_handle.read()

    def make_html(self) -> str:
        return self.template.replace(
            "DATE", self.date_as_string())


class BreakDay(ScheduleDay):
    def __init__(self, date: datetime.date, term: str):
        super().__init__(date)
        self.term = term
        with open(SCHEDULE_BREAK_TEMPLATE, "r") as file_handle:
            self.template = file_handle.read()

    def make_html(self) -> str:
        return self.template.replace(
            "TERM", self.term).replace(
            "DATE", self.date_as_string())


class SessionDay(ScheduleDay):
    def __init__(self, date: datetime.date, session: Session):
        super().__init__(date, session)
        with open(SCHEDULE_SESSSION_TEMPLATE, "r") as file_handle:
            self.template = file_handle.read()
        self.template.replace("    SESSIONS", "SESSIONS")

    def make_html(self) -> str:
        if self.session.session_number < 10:
            two_digit_number = "0{}".format(self.session.session_number)
        else:
            two_digit_number = "{}".format(self.session.session_number)

        return self.template.replace(
            "SESSION_NUMBER", str(self.session.session_number)).replace(
            "SESSION_DATE", self.date.strftime("%B %d")).replace(
            "SESSION_FOLDER_NUMBER", two_digit_number).replace(
            "SESSION_TITLE", self.session.session_title).replace(
            "SESSION_TOPICS", self.make_html_for_topics())


class RegularClassSessionDay(SessionDay):
    pass


class ReviewSessionDay(SessionDay):
    pass


class EveningExamSessionDay(SessionDay):
    def __init__(self, date: datetime.date, session: EveningExamSession):
        super().__init__(date, session)


class InClassExamSessionDay(SessionDay):
    pass


class CapstoneProjectSessionDay(SessionDay):
    pass


class Schedule:
    def __init__(self, term_info: TermInfo, sessions: List[Session]):
        self.term_info = term_info
        self.sessions = sessions
        with open(SCHEDULE_TEMPLATE, "r") as file_handle:
            self.template = file_handle.read()
        self.template = self.template.replace("  SESSIONS", "SESSIONS")

        with open(SCHEDULE_NO_CLASS_TEMPLATE, "r") as file_handle:
            self.no_class_template = file_handle.read()
        with open(SCHEDULE_BREAK_TEMPLATE, "r") as file_handle:
            self.break_template = file_handle.read()

        self.schedule_days = self.make_schedule_days()

    def make_schedule_days(self) -> List[ScheduleDay]:
        # Start on a Monday:
        if self.term_info.first_day_of_term.weekday() == 3:  # Fall session
            date = self.term_info.first_day_of_term - datetime.timedelta(3)
        else:
            date = self.term_info.first_day_of_term
        session_index = 0  # For indexing through the Sessions
        schedule_days = []  # From Monday of Week 1 to Friday of Week 10

        while True:
            # Go through each date from the start of term to end of term.
            # Done when we get to the last date of the term.
            if date > self.term_info.last_day_of_tenth_week:
                break

            # Deal only with dates that are on class days-of-week.
            if date.weekday() in self.term_info.class_meeting_days_of_week:
                if date < self.term_info.first_day_of_term:
                    schedule_days.append(BeforeClassesStartDay(date))
                elif self.term_info.start_date_of_break <= date \
                        <= self.term_info.end_date_of_break:
                    schedule_days.append(BreakDay(date, self.term_info.term))
                else:  # CONSIDER: Can make the following more elegant.
                    session = self.sessions[session_index]

                    if isinstance(session, RegularClassSession):
                        day_type = RegularClassSessionDay
                    elif isinstance(session, ReviewSession):
                        day_type = ReviewSessionDay
                    elif isinstance(session, EveningExamSession):
                        day_type = EveningExamSessionDay
                    elif isinstance(session, InClassExamSession):
                        day_type = InClassExamSessionDay
                    elif isinstance(session, CapstoneProjectSession):
                        day_type = CapstoneProjectSessionDay
                    else:
                        raise ValueError("Unknown session type")

                    schedule_days.append(day_type(date, session))
                    session_index = session_index + 1

            date = date + datetime.timedelta(1)

        return schedule_days

    def make_html(self) -> str:
        days_of_week = self.term_info.class_meeting_days_of_week
        template = self.template.replace(
            "DAY-OF-WEEK-1", DAYS_OF_WEEK[days_of_week[0]]).replace(
            "DAY-OF-WEEK-2", DAYS_OF_WEEK[days_of_week[1]]).replace(
            "DAY-OF-WEEK-3", DAYS_OF_WEEK[days_of_week[2]])

        html = ""
        for day in self.schedule_days:
            html += day.make_html()
        html = template.replace("SESSIONS", html)
        return html