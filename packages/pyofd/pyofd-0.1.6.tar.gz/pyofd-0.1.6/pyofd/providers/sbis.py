# -*- coding: utf-8 -*-

"""
pyofd.providers.sbis
SBIS OFD provider. Also handles Tensor Company
(c) Serge A. Levin, 2018
"""

from .base import Base
import pyofd
import json
from decimal import Decimal
import datetime


class ofdSbis(Base):
    providerName = 'SBIS'
    requiredFields = ('purchase_date', 'rn_kkt', 'fpd')
    urlTemplate = 'https://ofd.sbis.ru/service/'

    def validate(
            self,
            fpd=None,
            total=None,
            rn_kkt=None,
            fd=None,
            fn=None,
            inn=None,
            purchase_date=None,
    ):
        request_body = json.dumps({
            'id': 1,
            'jsonrpc': '2.0',
            'method':  'FiscalDocument.FindByFiscalSignAndDate',
            'protocol': 5,
            'params': {
                'FiscalSign': '{fpd:0>10}'.format(fpd=fpd),
                'KKTRegNum': '{rn_kkt:0>16}'.format(rn_kkt=rn_kkt),
                'DateTime': purchase_date.strftime('%Y-%m-%d')
            }
        }, separators=(',', ':'))
        request = self._build_request(self.urlTemplate, request_body)
        data = self._get_json_data(request)
        try:
            result_data = data['result']
        except KeyError:
            return None

        if result_data is None:
            return None


