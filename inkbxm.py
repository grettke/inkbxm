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

    def add_arguments(self, pars):
        pars.add_argument("--units", default="px",
                          help="Units: px, pt, mm, cm, or in.")
        pars.add_argument("--side", type=float, default=100,
                          help="Side length.")
        pars.add_argument("--rows", type=int, default=1, help="Number of rows")
        pars.add_argument("--columns", type=int, default=1,
                          help="Number of columns")
        pars.add_argument("--spacing", type=float, default=0,
                          help="Spacing distance.")
        pars.add_argument("--tab", help="Ignored.")

    def effect(self):
        layer_name = self.svg.get_unique_id('bxm:')
        model_name = self.svg.get_unique_id('bxm.model:')

        user_side = self.options.side
        side = self.svg.unittouu(str(user_side) + self.options.units)
        side_str = str(side)
        rows = self.options.rows
        columns = self.options.columns
        spacing = self.options.spacing

        layer = self.svg.add(inkex.Layer.new(layer_name))
        source = inkex.Rectangle(x='0', y='0', width=side_str,
                                 height=side_str)
        source.style = {'stroke': '#000000', 'stroke-opacity': '1',
                        'stroke-width': self.svg.unittouu('1px'), 'fill': 'none'}

        model = layer.add(source.copy())
        model.set('id', model_name)

        for row_index in range(0, rows):
            row_y_translation = row_index * side
            if not row_index == 0:
                row_y_translation = row_y_translation + (spacing * row_index)
            for column_index in range(0, columns):
                if row_index == 0 and column_index == 0:
                    continue
                use = layer.add(inkex.Use())
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
