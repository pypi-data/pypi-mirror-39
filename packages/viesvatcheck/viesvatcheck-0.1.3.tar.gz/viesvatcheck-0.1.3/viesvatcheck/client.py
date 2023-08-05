from typing import Tuple, Optional, Dict, Callable

import zeep
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from .exceptions import EXCEPTION_MAP, OtherError, NotEUMember
from .countries import is_eu_member

PROD_WSDL = "http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
TEST_WSDL = "http://ec.europa.eu/taxation_customs/vies/checkVatTestService.wsdl"

Response = Tuple[bool, Optional[Dict]]


def parse_country_code(country_code: str) -> str:
    country_code = country_code.upper()
    if not is_eu_member(country_code):
        raise NotEUMember

    """
    http://publications.europa.eu/code/pdf/370000en.htm
    The abbreviations to use are the ISO codes, except for Greece and the United Kingdom,
    for which EL and UK are recommended (instead of GR and GB).
    The former abbreviations were generally taken from the international code for automobiles and were used
    until the end of 2002.

    United Kingdom is fine but we have to remap Greece???
    """
    if country_code == 'GR':
        country_code = 'EL'

    return country_code


class Client(object):
    def __init__(self, wsdl: str = PROD_WSDL) -> None:
        self.zeep = zeep.CachingClient(wsdl=wsdl)

    def _request(self, method: Callable, **arguments) -> Response:
        try:
            response = method(**arguments)
            return response.valid, serialize_object(response, dict)
        except Fault as error:
            try:
                raise EXCEPTION_MAP[error.message]
            except KeyError:
                raise OtherError

    def check(self, country_code: str, vat_number: str) -> Response:
        country_code = parse_country_code(country_code)
        return self._request(
            self.zeep.service.checkVat,
            countryCode=country_code,
            vatNumber=vat_number
        )

    def check_approx(self,
                     country_code: str,
                     vat_number: str,
                     trader_name: Optional[str] = None,
                     trader_company_type: Optional[str] = None,  # tns1:traderCompanyType @TODO
                     trader_street: Optional[str] = None,
                     trader_postcode: Optional[str] = None,
                     trader_city: Optional[str] = None,
                     requester_country_code: Optional[str] = None,
                     requester_vat_number: Optional[str] = None) -> Response:

        country_code = parse_country_code(country_code)
        resp = self._request(
            self.zeep.service.checkVatApprox,
            countryCode=country_code,
            vatNumber=vat_number,
            traderName=trader_name,
            traderCompanyType=trader_company_type,
            traderStreet=trader_street,
            traderPostcode=trader_postcode,
            traderCity=trader_city,
            requesterCountryCode=requester_country_code,
            requesterVatNumber=requester_vat_number
        )
        print(resp)
        return resp
