#!/usr/bin/env python
# encoding: utf-8

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
Docstring for controller.py
"""

from sqlalchemy.orm.exc import NoResultFound

from tendril.utils.db import with_db

from model import SerialNumberSeries
from model import SerialNumber
from model import SerialNumberAssociation

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class SeriesNotFound(Exception):
    pass


class SerialNoNotFound(Exception):
    pass


@with_db
def get_series_obj(series=None, session=None):
    if series is None:
        return session.query(SerialNumberSeries).all()
    try:
        return session.query(SerialNumberSeries).filter_by(series=series).one()
    except NoResultFound:
        raise SeriesNotFound('Series {0} is not defined.'.format(series))


@with_db
def create_series_obj(series=None, start_seed=None,
                      description=None, session=None):
    if not series or not isinstance(series, str):
        raise ValueError('series should be a string, got : ' +
                         repr(series))
    if not start_seed or not isinstance(series, str):
        raise ValueError('start_seed should be a string, got : ' +
                         repr(start_seed))
    sobj = SerialNumberSeries(series=series,
                              last_seed=start_seed,
                              description=description)
    session.add(sobj)
    session.flush()
    return sobj


@with_db
def get_all_serialnos(session=None):
    return session.query(SerialNumber).all()


@with_db
def get_serialnos_by_efield(efield=None, session=None):
    return session.query(SerialNumber).filter_by(efield=efield).all()


@with_db
def get_serialnos_by_series(series=None, session=None):
    if not series or not isinstance(series, str):
        raise ValueError('series should be a string, got : ' + repr(series))
    return session.query(SerialNumber).filter(
        SerialNumber.sno.like('{0}%'.format(series))).all()


@with_db
def get_serialno_object(sno=None, session=None):
    if sno is None:
        raise AttributeError("sno cannot be None")
    try:
        return session.query(SerialNumber).filter_by(sno=sno).one()
    except NoResultFound:
        raise SerialNoNotFound("Serial No {0} not defined.".format(sno))


@with_db
def register_serialno(sno=None, efield=None, session=None):
    sobj = SerialNumber(sno=sno, efield=efield)
    session.add(sobj)
    session.flush()
    return sobj


@with_db
def delete_serialno(sno=None, session=None):
    if sno is None:
        raise AttributeError("sno cannot be None")
    if not isinstance(sno, SerialNumber):
        sno = get_serialno_object(sno=sno, session=session)
    session.delete(sno)
    session.flush()


@with_db
def link_serialno(child=None, parent=None,
                  association_type=None, session=None):

    if not isinstance(child, SerialNumber):
        child = get_serialno_object(sno=child, session=session)
    if not isinstance(parent, SerialNumber):
        parent = get_serialno_object(sno=parent, session=session)

    try:
        existing = session.query(SerialNumberAssociation).filter_by(
            child_id=child.id, parent_id=parent.id).one()
        session.delete(existing)
        session.flush()
    except NoResultFound:
        pass

    assoc_object = SerialNumberAssociation(child_id=child.id, child=child,
                                           parent_id=parent.id, parent=parent,
                                           association_type=association_type)
    session.add(assoc_object)
    session.flush()
    return assoc_object


@with_db
def get_child_snos(serialno=None, child_efield=None, child_series=None,
                   session=None):

    if serialno is None:
        raise ValueError("serialno cannot be None")
    if not isinstance(serialno, SerialNumber):
        serialno = get_serialno_object(sno=serialno, session=session)

    q = session.query(SerialNumberAssociation).filter_by(
        parent_id=serialno.id
    )
    q = q.join(SerialNumberAssociation.child)

    if child_efield is not None:
        q = q.filter(SerialNumber.efield == child_efield)

    if child_series is not None:
        q = q.filter(SerialNumber.sno.like(child_series+'%'))

    return [x.child.sno for x in q.all()]
