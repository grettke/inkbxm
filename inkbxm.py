#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2021 Grant Rettke <grant@wisdomandwonder.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
import inkex


class BoxMaster(inkex.EffectExtension):

    def add_arguments(self, p):
        # The INX file is the authoritative source of this information:
        # keep that current /then/ update it here.
        p.add_argument("--units", type=str, default="px",
                       help="Unit of Measurement: px, pt, mm, cm, or in.")
        p.add_argument("--side", type=float, default=100,
                       help="Side length.")
        p.add_argument("--rows", type=int, default=1, help="Number of rows.")
        p.add_argument("--columns", type=int, default=1,
                       help="Number of columns.")
        p.add_argument("--spacing", type=float, default=0,
                       help="Spacing distance.")
        p.add_argument("--grouptype", type=str, default="newgroup",
                       help="Group element type.")
        p.add_argument("--tab", type=str, help="Ignored.")

    def effect(self):

        groupbase_name = self.svg.get_unique_id('bxm:')
        model_name = self.svg.get_unique_id('bxm.model:')

        user_side = self.options.side
        side = self.svg.unittouu(str(user_side) + self.options.units)
        side_str = str(side)
        rows = self.options.rows
        columns = self.options.columns
        spacing = self.options.spacing
        groupbase_type = self.options.grouptype
        groupbase = 'Undefined'

        if groupbase_type == 'newgroup':
            groupbase = self.svg.get_current_layer().add(
                inkex.Group.new(groupbase_name))
        elif groupbase_type == 'newrootlayer':
            groupbase = self.svg.add(
                inkex.Layer.new(groupbase_name))
        elif groupbase_type == 'newsublayer':
            groupbase = self.svg.get_current_layer().add(
                inkex.Layer.new(groupbase_name))
        elif groupbase_type == 'currentlayer':
            groupbase = self.svg.get_current_layer()
        else:
            inkex.utils.debug("I'm sorry it looks like I might have a bug: " +
                              "I don't know how to handle a " +
                              "groupbase_type of '" + groupbase_type + "'. " +
                              "You can also still try to use another group "
                              "type. " +
                              "Please see README and file an issue report. " +
                              "I appreciate your help!")
            return

        source = inkex.Rectangle(x='0', y='0', width=side_str,
                                 height=side_str)
        source.style = {'stroke': '#000000', 'stroke-opacity': '1',
                        'stroke-width': self.svg.unittouu('1px'),
                        'fill': 'none'}

        model = groupbase.add(source.copy())
        model.set('id', model_name)

        for row_index in range(0, rows):
            row_y_translation = row_index * side
            if not row_index == 0:
                row_y_translation = row_y_translation + (spacing * row_index)
            for column_index in range(0, columns):
                if row_index == 0 and column_index == 0:
                    continue
                use = groupbase.add(inkex.Use())
                use.set('id', self.svg.get_unique_id('bxm.clone:'))
                use.set('xlink:href', '#' + model_name)
                column_x_translation = column_index * side
                if not column_index == 0:
                    column_x_translation = column_x_translation + (spacing *
                                                                   column_index)
                use.transform.add_translate(column_x_translation,
                                            row_y_translation)


if __name__ == '__main__':
    BoxMaster().run()
