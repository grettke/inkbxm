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
from inkex import EffectExtension, Group, Layer, Rectangle, Use, utils

#
# Create a grid of cloned boxes.
#
class BoxMaster(EffectExtension):

    def add_arguments(self, p):
        # The INX file is the authoritative source of this information:
        # keep *that* current /then/ update it _here_.
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
        # Shorten references.
        s = self.svg
        o = self.options

        # Object ID prefix to uniquely namespace and consistently name
        # extension created objects.
        prf = 'bxm'

        # Inkex GroupBase objects define any group elements. This extension
        # uses those groups to store objects it creates. To avoid confusion
        # between different group objects though naming the reference with its
        # base type. Also forward declaring it for sake of the reader.
        gbase_name = s.get_unique_id(prf + ':')
        gbase = None

        # The "Model" box object serves as the source for creating all new
        # boxes. The prefix makes it stand out.
        model_name = s.get_unique_id(prf + '.model:')

        # User specifies units for conversion to user-inits:
        # *this is a feature*.
        side = s.unittouu(str(o.side) + o.units)

        # Many objects are created so apply a grouping strategy. It comes
        # down to either: use or create—an object or layer. They are listed
        # in order with an emphasis on brand-new groupings.
        if o.grouptype == 'newgroup':
            # Create a new group and add there.
            gbase = s.get_current_layer().add(
                Group.new(gbase_name))
        elif o.grouptype == 'newrootlayer':
            # Create a new root layer and add there.
            gbase = s.add(
                Layer.new(gbase_name))
        elif o.grouptype == 'newsublayer':
            # Create a new sub-layer and add there.
            gbase = s.get_current_layer().add(
                Layer.new(gbase_name))
        elif o.grouptype == 'currentlayer':
            # Add objects to /this/ layer.
            gbase = s.get_current_layer()
        else:
            # Don't support that group type so ask for help.
            utils.debug("I'm sorry it looks like I might have a bug: " +
                        "I don't know how to handle a " +
                        "o.grouptype of '" + o.grouptype + "'. " +
                        "You can also still try to use another group "
                        "type. " +
                        "Please see README and file an issue report. " +
                        "I appreciate your help!")
            return

        # Model object configuration.
        source = Rectangle(x='0', y='0', width=str(side), height=str(side))
        # TODO: Address stroke-width unit
        source.style = {'stroke': '#000000', 'stroke-opacity': '1',
                        'stroke-width': s.unittouu('1px'),
                        'fill': 'none'}
        # A "Model" object is created by copy of a source object.
        # Reason why? Unknown.
        # Determined by researching built-in extensions.
        model = gbase.add(source.copy())
        model.set('id', model_name)

        # Rows go left to right starting at 0.
        # Columns go top to bottom starting at 0.
        for row_idx in range(0, o.rows):
            row_y_shift = row_idx * side
            # Don't add space above the first row.
            if not row_idx == 0:
                row_y_shift = row_y_shift + (o.spacing * row_idx)
            for column_idx in range(0, o.columns):
                if row_idx == 0 and column_idx == 0:
                    continue
                # A Use element links itself to another element. Readers know
                # this as a Clone in both common-use and Inkscape terminolog:
                # specifically Edit -> Clone -> Create Clone. Although this
                # is in the class documentation, like other code: built-in
                # extensions were researched to verify usage.
                use = gbase.add(Use())
                # Clones need distinct names.
                use.set('id', s.get_unique_id(prf + '.clone:'))
                use.set('xlink:href', '#' + model_name)
                column_x_shift = column_idx * side
                # Don't add space betfore the first column.
                if not column_idx == 0:
                    column_x_shift = column_x_shift + (o.spacing * column_idx)
                use.transform.add_translate(column_x_shift, row_y_shift)


if __name__ == '__main__':
    BoxMaster().run()
