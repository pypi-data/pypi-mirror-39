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

from marshmallow import fields, Schema, post_load, pre_load

from .helpers import timestamp_to_date


# {{{ V3

class FileExtSchemaV3(Schema):

    @classmethod
    def dynschema(cls, data):
        """ Dynamically retrieve required schema
        :param data: data to unmarshall
        :returns: the required schema class
        """
        try:
            submitter = data["submitter"]
            if submitter == FileCli.submitter_type:
                return FileCliSchemaV3
            if submitter == FileKiosk.submitter_type:
                return FileKioskSchemaV3
            if submitter == FileProbeResult.submitter_type:
                return FileProbeResultSchemaV3
            if submitter == FileSuricata.submitter_type:
                return FileSuricataSchemaV3
            return cls
        except KeyError:
            return cls

    id = fields.UUID(attribute="external_id")
    status = fields.Integer(allow_none=True)
    name = fields.String()

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    file = fields.Nested('FileSchema')
    scan = fields.Nested('ScanSchema', allow_none=True, only=('id', 'date'))

    parent_file_sha256 = fields.Pluck(
            'FileSchema', 'sha256', attribute="parent", allow_none=True)

    submitter = fields.String()

    other_results = fields.Nested(
        'self', only=("id", "scan", "status"), many=True)

    probe_results = fields.Function(
            lambda fe, ctx: fe.get_probe_results(ctx.get('formatted', True)),
            lambda dct: dct)

    @post_load
    def make_object(self, data):
        return FileExt(**data)


class FileCliSchemaV3(FileExtSchemaV3):
    path = fields.String()


class FileKioskSchemaV3(FileCliSchemaV3):
    submitter_id = fields.String()


class FileProbeResultSchemaV3(FileExtSchemaV3):
    probe_parent = fields.Nested(
        'ProbeResultSchema',
        attribute="probe_result_parent",
        only=('type', 'name', 'status',)
    )


class FileSuricataSchemaV3(FileExtSchemaV3):
    context = fields.Dict()

# }}}


# {{{ V2

class FileExtSchemaV2(Schema):

    @classmethod
    def dynschema(cls, data):
        """ Dynamically retrieve required schema
        :param data: data to unmarshall
        :returns: the required schema class
        """
        try:
            submitter = data["submitter"]
            if submitter == FileCli.submitter_type:
                return FileCliSchemaV2
            if submitter == FileKiosk.submitter_type:
                return FileKioskSchemaV2
            if submitter == FileProbeResult.submitter_type:
                return FileProbeResultSchemaV2
            if submitter == FileSuricata.submitter_type:
                return FileSuricataSchemaV2
            return cls
        except KeyError:
            return cls

    id = fields.UUID(attribute="external_id")
    status = fields.Integer(allow_none=True)
    name = fields.String()

    probes_finished = fields.Integer()
    probes_total = fields.Integer()

    file = fields.Nested('FileSchema', load_only=True)
    file_infos = fields.Nested(
            'FileSchema', attribute="file", dump_only=True)
    file_sha256 = fields.Pluck(
            'FileSchema', 'sha256', dump_only=True, attribute="file")

    scan = fields.Nested('ScanSchemaV2', load_only=True, allow_none=True)
    scan_id = fields.Pluck(
            'ScanSchemaV2', 'id', attribute='scan', dump_only=True)
    scan_date = fields.Pluck(
            'ScanSchemaV2', 'date', attribute='scan', dump_only=True)

    parent_file_sha256 = fields.Pluck(
            'FileSchema', 'sha256', attribute="parent", allow_none=True)

    submitter = fields.String()

    other_results = fields.Nested(
        'self', many=True,
        only=("id", "scan", "scan_id", "scan_date", "file", "file_sha256",
              "status"))

    probe_results = fields.Function(
            lambda fe, ctx: fe.get_probe_results(ctx.get('formatted', True)),
            lambda dct: dct)

    @post_load
    def make_object(self, data):
        return FileExt(**data)

    @pre_load
    def merge_scan_fields(self, data):
        try:
            scanid = data.pop('scan_id', None)
            if scanid is None:
                del data['scan_date']
            else:
                data['scan'] = {'id': scanid}
                data['scan']['date'] = data.pop('scan_date')
        except KeyError:
            pass
        return data

    @pre_load
    def merge_file_fields(self, data):
        try:
            data['file'] = {'sha256': data.pop('file_sha256')}

            try:
                data['file']['size'] = data.pop('size')
            except KeyError:
                pass

            try:
                data['file'].update(data.pop('file_infos'))
            except KeyError:
                pass

        except KeyError:
            pass
        return data


class FileCliSchemaV2(FileExtSchemaV2):
    path = fields.String()

    @post_load
    def make_object(self, data):
        return FileCli(**data)


class FileKioskSchemaV2(FileCliSchemaV2):
    submitter_id = fields.String()

    @post_load
    def make_object(self, data):
        return FileKiosk(**data)


class FileProbeResultSchemaV2(FileExtSchemaV2):
    probe_parent = fields.Nested(
        'ProbeResultSchema',
        attribute="probe_result_parent",
        only=('type', 'name', 'status',)
    )

    @post_load
    def make_object(self, data):
        return FileProbeResult(**data)


class FileSuricataSchemaV2(FileExtSchemaV2):
    context = fields.Dict()

    @post_load
    def make_object(self, data):
        return FileSuricata(**data)

# }}}


# {{{ OBJECTS

class FileExt:
    submitter_type = "whatever"

    def __init__(
            self, external_id, *, status=None, name=None,
            probes_finished=None, probes_total=None,
            file=None, scan=None, parent=None,
            submitter=None,
            probe_results=None, other_results=None):
        self.external_id = str(external_id)
        self.name = name
        self.status = status

        self.probes_finished = probes_finished
        self.probes_total = probes_total

        self.scan = scan
        self.file = file
        self.parent = parent

        self.submitter = submitter
        self.probe_results = probe_results
        self.other_results = other_results

    @property
    def id(self):
        return self.external_id

    @property
    def pscan_date(self):
        return timestamp_to_date(self.scan.date)

    def get_probe_results(self, *args, **kwargs):
        return self.probe_results

    def __repr__(self):
        return "FileExt." + self.id

    def __str__(self):
        ret = "FileExt{"
        ret += "id: {}; ".format(self.id)
        ret += "status: {}; ".format(self.status)
        ret += "scan: {!r}; ".format(self.scan)
        if self.probes_total:
            ret += "probes progress: {}/{}; ".format(
                self.probes_finished, self.probes_total)
        if self.name:
            ret += "filename: {}; ".format(self.name)
        if self.file is not None:
            ret += "file: {!r}; ".format(self.file)
        if self.parent:
            ret += "parent: {}; ".format(self.parent)
        ret += "}"
        return ret

    def __eq__(self, other):
        return isinstance(other, FileExt) and self.id == other.id

    def __neq__(self, other):
        return not (self == other)


class FileCli(FileExt):
    submitter_type = "cli"

    def __init__(self, *args, path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path


class FileKiosk(FileCli):
    submitter_type = "kiosk"

    def __init__(self, *args, submitter_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.submitter_id = submitter_id


class FileProbeResult(FileExt):
    submitter_type = "probe_result"

    def __init__(self, *args, probe_parent=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.probe_parent = probe_parent


class FileSuricata(FileExt):
    submitter_type = "suricata"

    def __init__(self, *args, context=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = context

# }}}
