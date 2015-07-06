# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Université Catholique de Louvain.
#
# This file is part of INGInious.
#
# INGInious is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INGInious is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with INGInious.  If not, see <http://www.gnu.org/licenses/>.
import web

from frontend.base import renderer
from frontend.pages.course_admin.utils import make_csv, get_course_and_check_rights
from frontend.user_data import UserData


class CourseStudentListPage(object):
    """ Course administration page: list of registered students """

    def GET(self, courseid):
        """ GET request """
        course, _ = get_course_and_check_rights(courseid)
        return self.page(course)

    def submission_url_generator(self, course, username):
        """ Generates a submission url """
        return "/admin/" + course.get_id() + "/submissions?dl=student&username=" + username

    def page(self, course, error="", post=False):
        """ Get all data and display the page """
        users = course.get_registered_users()
        user_data = dict([(username, dict([
            ("username", username), ("total_tasks", 0), ("task_grades", {"answer": 0, "match": 0}),
            ("task_succeeded", 0), ("task_tried", 0), ("total_tries", 0),
            ("url", self.submission_url_generator(course, username))])) for username in users])

        for (username, user) in UserData.get_course_data_for_users(course.get_id(), users).iteritems():
            user_data[username].update(user)

        user_data = sorted(user_data.values(), key=lambda x: x["username"])

        if "csv" in web.input():
            return make_csv(user_data)

        return renderer.course_admin.student_list(course, user_data, error, post)
