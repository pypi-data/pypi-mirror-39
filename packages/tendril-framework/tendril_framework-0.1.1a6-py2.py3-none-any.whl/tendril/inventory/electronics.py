# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Electronics Inventory module documentation (:mod:`inventory.electronics`)
=========================================================================
"""

import os
import csv

from tendril.utils.config import ELECTRONICS_INVENTORY_DATA
from tendril.utils.types.lengths import Length
from tendril.conventions.electronics import fpiswire_ident
from tendril.entityhub.transforms import ContextualReprNotRecognized

import acquire
from db.controller import get_inventorylocationcode

from tendril.utils import log
logger = log.get_logger(__name__, log.INFO)

inventory_locations = []


class InventoryLine(object):
    def __init__(self, ident, qty=None, parent=None, ctx=None):
        self._ident = ident
        self._qty = qty
        self._parent = parent
        self._ctx = ctx
        self._reservations = []

    @property
    def ident(self):
        return self._ident

    @property
    def avail_qty(self):
        try:
            if fpiswire_ident(self._ident):
                qty = self._qty
                if not isinstance(qty, Length):
                    qty = Length(str(self._qty) + 'm')
                return qty - self.reserved_qty
            else:
                return self._qty - self.reserved_qty
        except AttributeError:
            return self._qty - self.reserved_qty

    @property
    def reserved_qty(self):
        reserved = 0
        for reservation in self._reservations:
            reserved += reservation[0]
        return reserved

    def reserve_qty(self, value, earmark):
        try:
            if fpiswire_ident(self._ident) and not isinstance(value, Length):
                value = Length(str(value) + 'm')
        except AttributeError:
            pass
        if value > self.avail_qty:
            raise ValueError

        logger.debug("Reserving " + self.ident + " in " +
                     self._parent._dname + " for " + earmark +
                     " : " + str(value))
        self._reservations.append((value, earmark))

    @property
    def earmarks(self):
        em = []
        for reservation in self._reservations:
            em.append(reservation[1])
        return em

    def _reservation_gen(self):
        for reservation in self._reservations:
            yield reservation

    def get_reservation_gen(self):
        return self._reservation_gen()

    def __repr__(self):
        return self.ident + '\t' + str(self._qty) + '\t' + \
            str(self.reserved_qty)

    @property
    def context(self):
        return self._ctx


class InventoryLocation(object):
    def __init__(self, name, dname, reader):
        self._name = name
        self._dname = dname
        self._lines = []
        self._code = None
        self._get_code()

        self._reader = reader
        self._is_valid = False
        if reader is not None:
            self._get_data()

    def _get_code(self):
        self._code = get_inventorylocationcode(self._dname)

    def _get_data(self):
        self._is_valid = False
        try:
            self._load_from_reader()
            self._is_valid = True
        except self._reader.exc:
            pass

    @property
    def is_valid(self):
        # TODO Build in some kind of backoff here
        if not self._is_valid:
            self._get_data()
        return self._is_valid

    @property
    def name(self):
        return self._dname

    @property
    def tf(self):
        return self._reader.tf

    def _load_from_reader(self):
        try:
            for (ident, qty, ctx) in self._reader.tf_row_gen:
                self._lines.append(InventoryLine(ident, qty, self, ctx))
            self._reader.close()
        except ContextualReprNotRecognized:
            logger.error("Inventory has unrecognized components.")
            raise ContextualReprNotRecognized

    def get_ident_qty(self, ident):
        avail_qty = 0
        is_here = False
        for line in self._lines:
            if line.ident == ident:
                is_here = True
                avail_qty += line.avail_qty
        if is_here:
            logger.debug("Found " + ident + " in " + self._dname +
                         " : " + str(avail_qty))
            # if fpiswire_ident(ident):
            #     avail_qty = Length(str(avail_qty)+'m')
            return avail_qty
        else:
            return None

    def get_reserve_qty(self, ident):
        reserve_qty = 0
        is_here = False
        for line in self._lines:
            if line.ident == ident:
                is_here = True
                reserve_qty += line.reserved_qty
        if is_here:
            return reserve_qty
        else:
            return None

    def reserve_ident_qty(self, ident, qty, earmark):
        for line in self._lines:
            if line.ident == ident:
                if line.avail_qty > qty:
                    line.reserve_qty(qty, earmark)
                    return 0
                elif line.avail_qty > 0:
                    qty = qty - line.avail_qty
                    line.reserve_qty(line.avail_qty, earmark)
        if qty > 0:
            raise ValueError("Unexpected Overrequisition : " + ident)
        return qty

    @property
    def earmarks(self):
        earmarks = []
        for line in self._lines:
            for em in line.earmarks:
                if em not in earmarks:
                    earmarks.append(em)
        return earmarks

    def _reservation_gen(self):
        for line in self._lines:
            if line.reserved_qty > 0:
                yield (line.ident, line.get_reservation_gen())

    def get_reservation_gen(self):
        return self._reservation_gen()

    def commit_reservations(self):
        pass

    @property
    def lines(self):
        return self._lines

    def get_line_context(self, ident):
        for line in self._lines:
            if line.ident == ident:
                return line.context


def init_inventory_locations(regen=True):
    for idx, item in enumerate(ELECTRONICS_INVENTORY_DATA):
        logger.info("Acquiring Inventory Location : " + item['location'])
        retries = 1
        while retries:
            try:
                reader = acquire.get_reader(idx)
                inventory_locations.append(
                    InventoryLocation(item['sname'], item['location'], reader)
                )
                break
            except ContextualReprNotRecognized:
                if not regen:
                    raise
                retries -= 1
                logger.warning(
                    "Regenerating Transform for Inventory "
                    "Location {0}.".format(idx)
                )
                logger.warning(
                    "All inventory functions will be unreliable "
                    "until the transform is manually verified."
                )
                acquire.gen_canonical_transform(idx)


def get_total_availability(ident):
    total_avail = 0
    for location in inventory_locations:
        if not location.is_valid:
            continue
        lqty = location.get_ident_qty(ident)
        if lqty is not None:
            total_avail += lqty
    return total_avail


def get_total_reservations(ident):
    total_reserve = 0
    for location in inventory_locations:
        if not location.is_valid:
            continue
        lqty = location.get_reserve_qty(ident)
        if lqty is not None:
            total_reserve += lqty
    return total_reserve


def reserve_items(ident, qty, earmark, die_if_not=True):
    if qty <= 0:
        raise ValueError
    if fpiswire_ident(ident) and not isinstance(qty, Length):
        qty = Length(str(qty) + 'm')
    for location in inventory_locations:
        if not location.is_valid:
            continue
        lqty = location.get_ident_qty(ident)
        if lqty is not None:
            if lqty > qty:
                location.reserve_ident_qty(ident, qty, earmark)
                return 0
            elif lqty > 0:
                location.reserve_ident_qty(ident, lqty, earmark)
                qty -= lqty
        if qty == 0:
            return 0
    if qty > 0:
        logger.warning('Partial Reservation of ' + ident +
                       ' for ' + earmark + ' : Short by ' + str(qty))
        if die_if_not is True:
            raise ValueError("Insufficient Qty. "
                             "Call with die_if_not=False if handled downstream"
                             )
    return qty


def export_reservations(folderpath):
    earmarks = []
    for location in inventory_locations:
        for em in location.earmarks:
            if em not in earmarks:
                earmarks.append(em)
    for location in inventory_locations:
        dump_path = os.path.join(folderpath,
                                 'reserve-' + location._dname + '.csv')
        with open(dump_path, 'wb') as f:
            w = csv.writer(f)
            header = ['Ident'] + earmarks + ['Total', 'Remaining']
            w.writerow(header)
            for ident, emgen in location.get_reservation_gen():
                row = [ident] + [0] * (len(earmarks) + 2)
                total = 0
                for reservation in emgen:
                    row[earmarks.index(reservation[1]) + 1] += reservation[0]
                    total += reservation[0]
                for idx, hdr in enumerate(earmarks):
                    if row[idx + 1] == 0:
                        row[idx + 1] = ''
                row[header.index('Total')] = total
                row[header.index('Remaining')] = get_total_availability(ident)
                w.writerow(row)
        logger.info("Exported " + location._dname +
                    " Reservations to File : " + dump_path)

init_inventory_locations()


def get_inventory_location(idx):
    for loc in inventory_locations:
        if loc._code == int(idx):
            return loc
    raise ValueError


def get_recognized_repr(regen=False):
    global recognized_representations
    if regen or recognized_representations is None:
        rval = []
        for loc in inventory_locations:
            rval.extend(list(loc.tf.names))
        recognized_representations = rval
    return set(recognized_representations)

recognized_representations = None
get_recognized_repr()


def get_inventory_stage(ident):
    inv_loc_status = {}
    inv_loc_transform = {}
    for loc in inventory_locations:
        if not loc.is_valid:
            continue
        qty = loc.get_ident_qty(ident) or 0
        reserve = loc.get_reserve_qty(ident) or 0
        inv_loc_status[loc._code] = (loc.name, qty, reserve, qty - reserve)
        contextual_repr = loc.tf.get_contextual_repr(ident)
        inv_loc_transform[loc._code] = (loc.name, contextual_repr,
                                        loc.get_line_context(ident))
    inv_total_reservations = get_total_reservations(ident)
    inv_total_quantity = get_total_availability(ident)
    inv_total_availability = inv_total_quantity - inv_total_reservations
    from tendril.inventory.guidelines import electronics_qty
    inv_guideline = electronics_qty.get_guideline(ident)
    from tendril.entityhub.guidelines import QtyGuidelineTableRow
    inv_guideline = QtyGuidelineTableRow(ident, inv_guideline)

    inv_stage = {
        'loc_status': inv_loc_status,
        'total_reservations': inv_total_reservations,
        'total_quantity': inv_total_quantity,
        'total_availability': inv_total_availability,
    }
    return {'inv_status': inv_stage,
            'inv_transform': inv_loc_transform,
            'inv_guideline': inv_guideline}
