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
        pars.add_argument("--size", type=float,
                          default=100, help="Box size (px)")
        pars.add_argument("--rows", type=int,
                          default=1, help="Number of rows")
        pars.add_argument("--columns", type=int,
                          default=1, help="Number of columns")

    def effect(self):
        """
        This cloning approach follows Nup.generate_nup.make_clones in
        extensions/layout_nup.py.
        """
        layername = 'bxmlayer'
        modelname = 'bxmmodel'
        size = self.options.size
        rows = self.options.rows
        columns = self.options.columns

        layer = self.svg.add(inkex.Layer.new(layername))
        source = inkex.Rectangle(x='0', y='0', width=str(size), height=str(
            size))

        for row in range (0, rows):
            for col in range (0, columns):
                if row == 0 and col == 0:
                    model = layer.add(source.copy())
                    model.set('id', modelname)
                    continue
                use = layer.add(inkex.Use())
                use.set('xlink:href', '#' + modelname)
                use.transform.add_translate(col * size, row * size)


if __name__ == '__main__':
    BoxMaster().run()
