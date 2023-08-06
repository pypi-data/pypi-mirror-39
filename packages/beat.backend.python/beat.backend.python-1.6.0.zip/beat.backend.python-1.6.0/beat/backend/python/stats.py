#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###############################################################################
#                                                                             #
# Copyright (c) 2017 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.backend.python module of the BEAT platform.   #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################

"""
=====
stats
=====

This module implements statistical related helper functions.
"""


def io_statistics(configuration, input_list=None, output_list=None):
    """Summarize current I/O statistics looking at data sources and sinks,
    inputs and outputs

    Parameters:

        configuration (dict): Executor configuration

        input_list (inputs.InputList): List of input to gather statistics from

        output_list (outputs.OutputList): List of outputs to gather statistics
            from


    Returns:

      dict: A dictionary summarizing current I/O statistics
    """

    network_time = 0.0

    # Data reading
    bytes_read = 0
    blocks_read = 0
    read_time = 0.0

    if input_list is not None:
        for input in input_list:
            size, duration = input.data_source.statistics()
            bytes_read += size
            read_time += duration
            blocks_read += input.nb_data_blocks_read

    # Data writing
    bytes_written = 0
    blocks_written = 0
    write_time = 0.0
    files = []

    if output_list is not None:
        for output in output_list:
            size, duration = output.data_sink.statistics()
            bytes_written += size
            write_time += duration
            blocks_written += output.nb_data_blocks_written

            if 'result' in configuration:
                hash = configuration['result']['path'].replace('/', '')
            else:
                hash = configuration['outputs'][output.name]['path'].replace(
                    '/', '')

            files.append(dict(
                hash=hash,
                size=size,
                blocks=output.nb_data_blocks_written,
            ))

    # Result
    return dict(
        volume=dict(read=bytes_read, write=bytes_written),
        blocks=dict(read=blocks_read, write=blocks_written),
        time=dict(read=read_time, write=write_time),
        network=dict(wait_time=network_time),
        files=files,
    )


# ----------------------------------------------------------


def update(statistics, additional_statistics):
    """Updates the content of statistics parameter with additional data. No new
    entries will be created. Only the values already available in statistics
    will be used.

    Parameters:

        statistics (dict): Original statistics

        additional_statistics (dict): Additional data to be added to the
            original statistics dict.
    """

    for k in statistics.keys():
        if k == 'files':
            continue

        for k2 in statistics[k].keys():
            statistics[k][k2] += additional_statistics[k][k2]

    if 'files' in statistics:
        statistics['files'].extend(additional_statistics.get('files', []))
    else:
        statistics['files'] = additional_statistics.get('files', [])
