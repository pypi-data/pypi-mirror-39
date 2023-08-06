#
# Copyright (c) 2013-2018 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

from marshmallow import Schema, fields

from .artifact import ArtifactSchema
from .file import FileSchema
from .fileext import (
        FileCliSchemaV3 as FileCliSchema,
        FileExtSchemaV3 as FileExtSchema,
        FileKioskSchemaV3 as FileKioskSchema,
        FileProbeResultSchemaV3 as FileProbeResultSchema,
        FileSuricataSchemaV3 as FileSuricataSchema,
)
from .scan import ScanSchema
from .srcode import (
        SRScanSchemaV3 as SRScanSchema,
        ScanRetrievalCodeSchemaV3 as ScanRetrievalCodeSchema,
)
from .tag import TagSchema


__all__ = (
    'ArtifactSchema',
    'FileCliSchema',
    'FileExtSchema',
    'FileKioskSchema',
    'FileProbeResultSchema',
    'FileResultSchema',
    'FileSchema',
    'FileSuricataSchema',
    'Paginated',
    'ScanRetrievalCodeSchema',
    'ScanSchema',
    'SRScanSchema',
    'TagSchema',
)


class Paginated(type):
    def __new__(_, enclosed, **extra):
        class Page(Schema):
            offset = fields.Integer()
            limit = fields.Integer()
            total = fields.Integer()
            items = fields.Nested(enclosed, many=True, **extra)
            # NOTE: APIv3 no longer use the 'data' field

        return Page


class FileResultSchema(Paginated(
        FileExtSchema,
        exclude=('probe_results', 'files_infos', 'other_results'))):
    file_infos = fields.Nested(FileSchema)
