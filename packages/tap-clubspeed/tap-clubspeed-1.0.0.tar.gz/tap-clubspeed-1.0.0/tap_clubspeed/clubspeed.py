
import requests
import logging

logger = logging.getLogger()


class IgnoreHttpException(Exception):
    pass


class Clubspeed(object):


    def __init__(self, subdomain=None, private_key=None, session=None):
        """ Simple Python wrapper for the Clubspeed API. Only supports GET. """
        self.protocol = 'https'
        self.domain = 'clubspeedtiming.com'
        self.subdomain = subdomain
        self.api_prefix = 'api/index.php/'
        self.private_key = private_key
        self._new_heats = []
        self._url_template = "{protocol}://{subdomain}.{domain}/{api_prefix}{path}.json?key={private_key}"
        self._limit = 100
        self._test = False


    def _get(self, url, **kwargs):
        logger.info("Hitting endpoint {url}".format(url=url))
        response = requests.get(url)
        if response.status_code == 500:
            raise IgnoreHttpException("http status is 500.")
        response.raise_for_status()
        return response.json()


    def _construct_endpoint(self, path):
        return self._url_template.format(protocol=self.protocol, 
                                         subdomain=self.subdomain, 
                                         domain=self.domain, 
                                         api_prefix=self.api_prefix,
                                         path=path,
                                         private_key=self.private_key)


    def _set_page_in_endpoint(self, endpoint, page=0):
        if "&page=" not in endpoint:
            endpoint += "&page=0&limit={limit}".format(limit=self._limit)
        else:
            array = endpoint.split('&')
            index = 0
            while index < len(array):
                if "page=" in array[index]:
                    array[index] = "page=" + str(page)
                index += 1
            endpoint = '&'.join(array)
        return endpoint


    def _add_filter(self, endpoint, api_version, column_name, bookmark):
        if column_name is None:
            return endpoint
        if bookmark is None:
            if api_version == 'V2':
                endpoint += '&where={{"{column_name}":{{"$isnot":"null"}}}}&order={column_name} ASC'.format(column_name=column_name)
            else:
                endpoint += '&filter={column_name} IS NOT NULL&order={column_name} ASC'.format(column_name=column_name)
            return endpoint
        if api_version == 'V2':
            endpoint += '&where={{"{column_name}":{{"$gt":"{bookmark}"}}}}&order={column_name} ASC'.format(column_name=column_name, bookmark=bookmark)
        else:
            endpoint += '&filter={column_name} > {bookmark}&order={column_name} ASC'.format(column_name=column_name, bookmark=bookmark)
        return endpoint


    def _get_response(self, endpoint, key=None):
        length = 1
        page = 0
        while length > 0:
            endpoint = self._set_page_in_endpoint(endpoint, page)
            try:
                res = self._get(endpoint)
                res = res[key] if key is not None else res
                length = len(res)
                logger.info('Endpoint returned {length} rows.'.format(length=length))
                for item in res:
                    if 'heatMain' in endpoint and 'heatId' in item:
                        self._new_heats.append(item['heatId'])
                    yield item
            except IgnoreHttpException:
                logger.info('Encountered 500, will ignore.')
                pass
            if self._test and page >= 2:
                break
            page += 1


    def is_authorized(self):
        endpoint = self._construct_endpoint('payments')
        return self._get(endpoint)


    def booking(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('booking')
        endpoint = self._add_filter(endpoint, 'V1', column_name, bookmark)
        return self._get_response(endpoint, 'bookings')


    def booking_availability(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('bookingAvailability')
        endpoint = self._add_filter(endpoint, 'V1', column_name, bookmark)
        return self._get_response(endpoint, 'bookings')


    def check_details(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('checkDetails')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint, 'checkDetails')


    def checks(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('checks')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint, 'checks')


    def check_totals(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('checkTotals')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def customers(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('customers')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def discount_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('discountType')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_heat_details(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventHeatDetails')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_heat_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventHeatTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_reservation_links(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventReservationLinks')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_reservations(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventReservations')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_reservation_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventReservationTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_rounds(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventRounds')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def events(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('events')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_statuses(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventStatuses')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_tasks(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventTasks')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_task_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventTaskTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def event_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('eventTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def gift_card_history(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('giftCardHistory')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    # Note: This function pulls `heat_details` from the API, but since
    # the API doesn't have a `last_edited_at` field, we use `heat_main.finish`
    # to determine when to pull `heat_details`.
    def heat_main_details(self, column_name=None, bookmark=None):
        endpoints = []
        idx = 0
        query = ''
        endpoint_base = self._construct_endpoint('heatDetails')

        # Using `heat_id`s, create array of endpoints for `heat_details`
        for heat_id in self._new_heats:
            query += '{{"heatId":{heat_id}}}'.format(heat_id=heat_id)
            if (idx is not 0 and idx % 30 == 0) or idx == len(self._new_heats) - 1:
                endpoint = endpoint_base + '&where={{"$or":[{query}]}}&order={column_name} ASC'.format(query=query, column_name='heatId')
                endpoints.append(endpoint)
                query = ''
            else:
                query += ','
            idx += 1

        # Yield all results from endpoints.
        for endpoint in endpoints:
            gtr = self._get_response(endpoint)
            for item in gtr:
                yield item


    def heat_main(self, column_name=None, bookmark=None):
        self._new_heats = []
        endpoint = self._construct_endpoint('heatMain')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def heat_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('heatTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def memberships(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('memberships')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def membership_types(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('membershipTypes')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def payments(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('payments')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def payments_voided(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('payments')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def product_classes(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('productClasses')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def products(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('products')
        endpoint = self._add_filter(endpoint, 'V1', column_name, bookmark)
        return self._get_response(endpoint, 'products')


    def reservations(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('reservations')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint, 'reservations')


    def sources(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('sources')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)


    def taxes(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('taxes')
        endpoint = self._add_filter(endpoint, 'V1', column_name, bookmark)
        return self._get_response(endpoint, 'taxes')


    def users(self, column_name=None, bookmark=None):
        endpoint = self._construct_endpoint('users')
        endpoint = self._add_filter(endpoint, 'V2', column_name, bookmark)
        return self._get_response(endpoint)





