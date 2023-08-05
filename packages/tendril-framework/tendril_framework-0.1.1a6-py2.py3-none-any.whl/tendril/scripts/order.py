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
This file is part of tendril
See the COPYING, README, and INSTALL files for more information
"""

import re
import csv
import os

import tendril.boms.electronics
import tendril.boms.outputbase

import tendril.inventory.electronics
import tendril.conventions.electronics
import tendril.sourcing.electronics

from tendril.entityhub import projects
from tendril.gedaif import projfile

from tendril.utils.terminal import TendrilProgressBar
import tendril.inventory.guidelines

from tendril.utils.config import INSTANCE_ROOT
from tendril.utils.files import yml as yaml

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

if __name__ == '__main__':

    bomlist = []

    orderfolder = os.path.join(INSTANCE_ROOT, 'scratch',
                               'sourcing', 'current')
    orderfile = os.path.join(orderfolder, 'order.yaml')

    with open(orderfile, 'r') as f:
        data = yaml.load(f)

    LOAD_PRESHORT = False
    LOAD_EXTERNAL_REQ = False
    EXTERNAL_REQ_IMMEDIATE = True
    external_req_file = None
    USE_STOCK = True
    IS_INDICATIVE = False
    indication_context = None
    PRIORITIZE = False
    PRELIMINARY = False
    IMMEDIATE_EARMARKS = []

    if 'preshort' in data.keys():
        LOAD_PRESHORT = data['preshort']
    if 'use_stock' in data.keys():
        USE_STOCK = data['use_stock']
    if 'is_indicative' in data.keys():
        IS_INDICATIVE = data['is_indicative']
        indication_context = data['context']
    if 'orderref' in data.keys():
        orderref = data['orderref']
    else:
        # TODO
        orderref = ''
    if 'prioritize' in data.keys():
        PRIORITIZE = data['prioritize']
        IMMEDIATE_EARMARKS = data['immediate']
    if 'preliminary' in data.keys():
        PRELIMINARY = data['preliminary']

    # Define base transforms for external data
    base_tf_0 = tendril.inventory.electronics.inventory_locations[0]._reader.tf  # noqa
    base_tf_1 = tendril.inventory.electronics.inventory_locations[1]._reader.tf  # noqa
    base_tf_2 = tendril.inventory.electronics.inventory_locations[2]._reader.tf  # noqa

    if LOAD_PRESHORT is True:
        # Load Preshort File
        if os.path.exists(os.path.join(orderfolder, 'preshort.csv')):
            with open(os.path.join(orderfolder, 'preshort.csv'), 'r') as f:
                logger.debug('Creating PRESHORT Bom')
                obom_descriptor = tendril.boms.outputbase.OutputElnBomDescriptor(  # noqa
                    'PRESHORT', os.path.join(INSTANCE_ROOT, 'scratch'),
                    'PRESHORT', None
                )
                obom = tendril.boms.outputbase.OutputBom(obom_descriptor)
                rex_qty = re.compile(ur'^-(?P<qty>[\d]+)\s+(qty)?$')
                reader = csv.reader(f)
                for line in reader:
                    line = [elem.strip() for elem in line]
                    if line[0] == 'Device':
                        header = line
                        continue
                    cident = line[0].strip()
                    try:
                        qty = int(rex_qty.match(line[1].strip()).group('qty'))
                    except AttributeError:
                        print line, line[1]
                        raise
                    if base_tf_0.has_contextual_repr(cident):
                        device, value, footprint = tendril.conventions.electronics.parse_ident(base_tf_0.get_canonical_repr(cident))  # noqa
                    elif base_tf_1.has_contextual_repr(cident):
                        device, value, footprint = tendril.conventions.electronics.parse_ident(base_tf_1.get_canonical_repr(cident))  # noqa
                    elif base_tf_2.has_contextual_repr(cident):
                        device, value, footprint = tendril.conventions.electronics.parse_ident(base_tf_2.get_canonical_repr(cident))  # noqa
                    else:
                        logger.info('NOT HANDLED : {0}'.format(line[0]))
                        continue

                    item = tendril.boms.electronics.EntityElnComp()
                    item.define('Undef', device, value, footprint)
                    logger.debug(
                        "Inserting : {0:4} {1}".format(
                            str(qty), str(item.ident)
                        )
                    )
                    for i in range(qty + 1):
                        obom.insert_component(item)

                logger.info('Inserting PRESHORT Bom')
                IMMEDIATE_EARMARKS.append(obom.descriptor.configname)
                bomlist.append(obom)

    if 'external' in data.keys():
        for exf in data['external']:
            external_req_file = os.path.join(orderfolder, exf['file'])
            if exf['priority'] == 'normal':
                EXTERNAL_REQ_IMMEDIATE = False
            elif exf['priority'] == 'immediate':
                EXTERNAL_REQ_IMMEDIATE = True
            else:
                EXTERNAL_REQ_IMMEDIATE = True
                logger.warning("External Req File Priority Not Recognized. "
                               "Assuming Immediate")

            if os.path.exists(external_req_file):
                logger.info(
                    "Loading External Req File : " + external_req_file
                )
                with open(external_req_file, 'r') as f:
                    header = []
                    reader = csv.reader(f)
                    for line in reader:
                        line = [elem.strip() for elem in line]
                        if line[0] == 'Device':
                            header = line
                            break

                    logger.info('Inserting External Boms')
                    oboms = []
                    for head in header[1:]:
                        logger.debug('Creating Bom : ' + head)
                        obom_descriptor = tendril.boms.outputbase.OutputElnBomDescriptor(  # noqa
                            head, os.path.join(INSTANCE_ROOT, 'scratch'),
                            head, None
                        )
                        obom = tendril.boms.outputbase.OutputBom(
                            obom_descriptor
                        )
                        oboms.append(obom)

                    for line in reader:
                        line = [elem.strip() for elem in line]
                        if line[0] == '':
                            continue
                        if line[0] == 'END':
                            break
                        if not base_tf_0.has_contextual_repr(line[0]):
                            print line[0] + ' Possibly not recognized'
                        device, value, footprint = tendril.conventions.electronics.parse_ident(base_tf_0.get_canonical_repr(line[0]))  # noqa
                        # print base_tf.get_canonical_repr(line[0])
                        item = tendril.boms.electronics.EntityElnComp()
                        item.define('Undef', device, value, footprint)
                        for idx, col in enumerate(line[1:]):
                            num = int(col)
                            if num > 0:
                                for i in range(num):
                                    oboms[idx].insert_component(item)

                    for obom in oboms:
                        logger.info(
                            'Inserting External Bom : ' +
                            obom.descriptor.configname
                        )
                        if EXTERNAL_REQ_IMMEDIATE is True:
                            IMMEDIATE_EARMARKS.append(
                                obom.descriptor.configname
                            )
                        bomlist.append(obom)

    # Generate Tendril Requisitions
    if isinstance(data['cards'], dict):
        logger.info('Generating Card BOMs')
        for k, v in data['cards'].iteritems():
            try:
                bom = tendril.boms.electronics.import_pcb(projects.cards[k])
            except KeyError:
                if not PRELIMINARY:
                    raise
                logger.warning("Card not found. Not adding : " + k)
                continue
            obom = bom.create_output_bom(k)
            obom.multiply(v)
            logger.info(
                'Inserting Card Bom : ' + obom.descriptor.configname +
                ' x' + str(obom.descriptor.multiplier)
            )
            bomlist.append(obom)

    cobom = tendril.boms.outputbase.CompositeOutputBom(bomlist)
    if PRIORITIZE is True:
        immediate_idxs = cobom.get_subset_idxs(IMMEDIATE_EARMARKS)
    else:
        immediate_idxs = range(len(cobom.descriptors))

    with open(os.path.join(orderfolder, 'cobom.csv'), 'w') as f:
        logger.info(
            'Exporting Composite Output BOM to File : ' +
            os.linesep + os.path.join(orderfolder, 'cobom.csv')
        )
        cobom.dump(f)

    orders_path = os.path.join(orderfolder, 'purchase-orders')
    if not os.path.exists(orders_path):
        os.makedirs(orders_path)

    reservations_path = os.path.join(orderfolder, 'reservations')
    if not os.path.exists(reservations_path):
        os.makedirs(reservations_path)

    unsourced = []
    deferred = []
    nlines = len(cobom.lines)
    pb = TendrilProgressBar(max=nlines)

    # TODO Heavily refactor

    for pbidx, line in enumerate(cobom.lines):
        if logger.getEffectiveLevel() >= log.INFO or \
                (PRIORITIZE is False and USE_STOCK is False):
            percentage = (float(pbidx) / nlines) * 100.00
            pb.next(note=line.ident)
            # "\n{0:>7.4f}% {1:<40} Qty:{2:<4}\n"
            # "Constructing Shortage File, Reservations, and Preparing Orders".format(  # noqa
            #     percentage, line.ident, line.quantity
            shortage = 0
        if USE_STOCK is True:
            if PRIORITIZE is False:
                for idx, descriptor in enumerate(cobom.descriptors):
                    earmark = descriptor.configname + \
                        ' x' + str(descriptor.multiplier)
                    avail = tendril.inventory.electronics.get_total_availability(line.ident)  # noqa
                    if line.columns[idx] == 0:
                        continue
                    if avail > line.columns[idx]:
                        tendril.inventory.electronics.reserve_items(line.ident, line.columns[idx], earmark)  # noqa
                    elif avail > 0:
                        tendril.inventory.electronics.reserve_items(line.ident, avail, earmark)  # noqa
                        pshort = line.columns[idx] - avail
                        shortage += pshort
                        logger.debug(
                            'Adding Partial Qty of ' + line.ident +
                            ' for ' + earmark +
                            ' to shortage : ' + str(pshort)
                        )
                    else:
                        shortage += line.columns[idx]
                        logger.debug(
                            'Adding Full Qty of ' + line.ident +
                            ' for ' + earmark +
                            ' to shortage : ' + str(line.columns[idx])
                        )
            else:
                avail = tendril.inventory.electronics.get_total_availability(line.ident)  # noqa
                if avail >= line.subset_qty(immediate_idxs):
                    if avail < line.quantity:
                        deferred.append((line.ident, line.quantity - avail))
                    logger.debug(
                        'Availability surpasses priority requirement. '
                        'Rejecting for order : ' + line.ident
                    )
                    shortage = 0
                else:
                    logger.debug(
                        'Availability falls short of priority requirement. '
                        'Accepting for order : ' + line.ident
                    )
                    # Reserve for immediate
                    for idx, descriptor in enumerate(cobom.descriptors):
                        if idx in immediate_idxs:
                            earmark = descriptor.configname + \
                                ' x' + str(descriptor.multiplier)
                            avail = tendril.inventory.electronics.get_total_availability(line.ident)  # noqa
                            if line.columns[idx] == 0:
                                continue
                            if avail > line.columns[idx]:
                                tendril.inventory.electronics.reserve_items(line.ident, line.columns[idx], earmark)  # noqa
                            elif avail > 0:
                                tendril.inventory.electronics.reserve_items(line.ident, avail, earmark)  # noqa
                                pshort = line.columns[idx] - avail
                                shortage += pshort
                                logger.debug(
                                    'Adding Partial Qty of ' + line.ident +
                                    ' for ' + earmark +
                                    ' to shortage : ' + str(pshort)
                                )
                            else:
                                shortage += line.columns[idx]
                                logger.debug(
                                    'Adding Full Qty of ' + line.ident +
                                    ' for ' + earmark +
                                    ' to shortage : ' + str(line.columns[idx])
                                )
                    # Reserve for the rest
                    for idx, descriptor in enumerate(cobom.descriptors):
                        if idx not in immediate_idxs:
                            earmark = descriptor.configname + \
                                ' x' + str(descriptor.multiplier)
                            avail = tendril.inventory.electronics.get_total_availability(line.ident)  # noqa
                            if line.columns[idx] == 0:
                                continue
                            if avail > line.columns[idx]:
                                tendril.inventory.electronics.reserve_items(line.ident, line.columns[idx], earmark)  # noqa
                            elif avail > 0:
                                tendril.inventory.electronics.reserve_items(line.ident, avail, earmark)  # noqa
                                pshort = line.columns[idx] - avail
                                shortage += pshort
                                logger.debug(
                                    'Adding Partial Qty of ' + line.ident +
                                    ' for ' + earmark +
                                    ' to shortage : ' + str(pshort)
                                )
                            else:
                                shortage += line.columns[idx]
                                logger.debug(
                                    'Adding Full Qty of ' + line.ident +
                                    ' for ' + earmark +
                                    ' to shortage : ' + str(line.columns[idx])
                                )
        else:
            if PRIORITIZE is False:
                shortage = line.quantity
            else:
                if line.subset_qty(immediate_idxs) > 0:
                    logger.debug(
                        "Accepting for priority inclusion : " + line.ident
                    )
                    shortage = line.quantity
                else:
                    logger.debug(
                        "Rejecting for priority inclusion : " + line.ident
                    )
                    shortage = 0
        if shortage > 0:
            result = tendril.sourcing.electronics.order.add(line.ident, line.quantity, shortage, orderref)  # noqa
            if result is False:
                unsourced.append((line.ident, shortage))

    if len(unsourced) > 0:
        logger.warning("Unable to source the following components: ")
        for elem in unsourced:
            logger.warning("{0:<40}{1:>5}".format(elem[0], elem[1]))
    if len(deferred) > 0:
        logger.warning("Deferred sourcing of the following components: ")
        for elem in deferred:
            logger.warning("{0:<40}{1:>5}".format(elem[0], elem[1]))

    tendril.sourcing.electronics.order.collapse()
    tendril.sourcing.electronics.order.rebalance()
    tendril.sourcing.electronics.order.generate_orders(orders_path)
    tendril.sourcing.electronics.order.dump_to_file(os.path.join(orderfolder, 'shortage.csv'), include_others=True)  # noqa
    tendril.inventory.electronics.export_reservations(reservations_path)

    if IS_INDICATIVE:
        logger.info('Generating Indicative Pricing Files')
        logger.debug('Loading Ident Pricing Information')
        pricing = {}
        if USE_STOCK:
            logger.warning(
                "Possibly Incorrect Analysis : "
                "Using Stock for Indicative Pricing Calculation"
            )
        with open(os.path.join(orderfolder, 'shortage.csv'), 'r') as f:
            reader = csv.reader(f)
            headers = None
            for row in reader:
                if row[0] == 'Ident':
                    headers = row
                    break
            for row in reader:
                if row[0] is not '':
                    if row[0] not in pricing.keys():
                        try:
                            pricing[row[0]] = (
                                row[headers.index('Vendor')],
                                row[headers.index('Vendor Part No')],
                                row[headers.index('Manufacturer')],
                                row[headers.index('Manufacturer Part No')],
                                row[headers.index('Description')],
                                row[headers.index('Used Break Qty')],
                                row[headers.index('Effective Unit Price')]
                            )
                        except IndexError:
                            pricing[row[0]] = None
        summaryf = open(os.path.join(orderfolder, 'costing-summary.csv'), 'w')
        summaryw = csv.writer(summaryf)
        summaryw.writerow(
            ["Card", "Total BOM Lines", "Uncosted BOM Lines", "Quantity",
             "Indicative Unit Cost", "Indicative Line Cost"]
        )
        all_uncosted_idents = []
        for k, v in sorted(data['cards'].iteritems()):
            logger.info('Creating Indicative Pricing for Card : ' + k)
            bom = tendril.boms.electronics.import_pcb(projects.cards[k])
            obom = bom.create_output_bom(k)
            gpf = projfile.GedaProjectFile(obom.descriptor.cardfolder)
            ipfolder = gpf.configsfile.indicative_pricing_folder
            if not os.path.exists(ipfolder):
                os.makedirs(ipfolder)
            for configuration in gpf.configsfile.configdata['configurations']:
                if configuration['configname'] == k:
                    desc = configuration['desc']
            if desc is None:
                desc = ''
            ipfile = os.path.join(
                ipfolder,
                obom.descriptor.configname + '~' + indication_context + '.csv'
            )
            totalcost = 0
            uncosted_idents = []
            total_lines = 0
            with open(ipfile, 'w') as f:
                writer = csv.writer(f)
                headers = ['Ident',
                           'Vendor', 'Vendor Part No',
                           'Manufacturer', 'Manufacturer Part No',
                           'Description',
                           'Used Break Qty', 'Effective Unit Price',
                           'Quantity', 'Line Price']
                writer.writerow(headers)
                for line in obom.lines:
                    total_lines += 1
                    if pricing[line.ident][0].strip() != '':
                        try:
                            writer.writerow(
                                [line.ident] + list(pricing[line.ident]) +
                                [line.quantity, line.quantity * float(pricing[line.ident][-1])]  # noqa
                            )
                        except ValueError:
                            print pricing[line.ident][-1]
                            raise ValueError
                        totalcost += line.quantity * float(pricing[line.ident][-1])  # noqa
                    else:
                        writer.writerow(
                            [line.ident] +
                            [None] * (len(headers) - 3) +
                            [line.quantity] +
                            [None]
                        )
                        uncosted_idents.append([line.ident])

                summaryw.writerow(
                    [k, total_lines, len(uncosted_idents), v,
                     totalcost, totalcost * v, desc]
                )
                logger.info(
                    'Indicative Pricing for Card ' + k +
                    ' Written to File : ' + os.linesep + ipfile
                )
                for ident in uncosted_idents:
                    if ident not in all_uncosted_idents:
                        all_uncosted_idents.append(ident)
        summaryw.writerow([])
        summaryw.writerow([])
        summaryw.writerow(["Uncosted Idents : "])
        for ident in sorted(all_uncosted_idents):
            summaryw.writerow(ident)
        summaryf.close()
        logger.info(
            'Indicative Pricing Summary Written to File : ' +
            os.linesep + os.path.join(orderfolder, 'costing-summary.csv')
        )
