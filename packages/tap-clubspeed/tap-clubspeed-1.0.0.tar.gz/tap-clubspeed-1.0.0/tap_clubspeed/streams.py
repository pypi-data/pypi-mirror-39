import os
import json
import datetime
import pytz
import singer
from singer import metadata
from singer import utils
from singer.metrics import Point
from dateutil.parser import parse


logger = singer.get_logger()
KEY_PROPERTIES = ['id']


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def needs_parse_to_date(string):
    if isinstance(string, str):
        try: 
            parse(string)
            return True
        except ValueError:
            return False
    return False


class Stream():
    name = None
    replication_method = None
    replication_key = None
    stream = None
    key_properties = KEY_PROPERTIES


    def __init__(self, client=None):
        self.client = client


    def get_bookmark(self, state):
        return singer.get_bookmark(state, self.name, self.replication_key)


    def update_bookmark(self, state, value):
        current_bookmark = self.get_bookmark(state)
        if value and needs_parse_to_date(value) and needs_parse_to_date(current_bookmark):
            if utils.strptime_with_tz(value) > utils.strptime_with_tz(current_bookmark):
                singer.write_bookmark(state, self.name, self.replication_key, value)
        elif current_bookmark is None:
            singer.write_bookmark(state, self.name, self.replication_key, value)


    # This function returns boolean and checks if
    # book mark is old.
    def is_bookmark_old(self, state, value):
        current_bookmark = self.get_bookmark(state)
        if current_bookmark is None:
            return True
        if needs_parse_to_date(current_bookmark) and needs_parse_to_date(value):
            if utils.strptime_with_tz(value) >= utils.strptime_with_tz(current_bookmark):
                return True
        else:
            if int(value) >= int(current_bookmark):
                return True
        return False


    def load_schema(self):
        schema_file = "schemas/{}.json".format(self.name)
        with open(get_abs_path(schema_file)) as f:
            schema = json.load(f)
        return self._add_custom_fields(schema)


    def _add_custom_fields(self, schema): # pylint: disable=no-self-use
        return schema


    def load_metadata(self):
        schema = self.load_schema()
        mdata = metadata.new()

        mdata = metadata.write(mdata, (), 'table-key-properties', self.key_properties)
        mdata = metadata.write(mdata, (), 'forced-replication-method', self.replication_method)

        if self.replication_key:
            mdata = metadata.write(mdata, (), 'valid-replication-keys', [self.replication_key])

        for field_name in schema['properties'].keys():
            if field_name in self.key_properties or field_name == self.replication_key:
                mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'automatic')
            else:
                mdata = metadata.write(mdata, ('properties', field_name), 'inclusion', 'available')

        return metadata.to_list(mdata)


    def is_selected(self):
        return self.stream is not None


    # The main sync function.
    def sync(self, state):
        get_data = getattr(self.client, self.name)

        bookmark = self.get_bookmark(state)

        res = get_data(self.replication_key, bookmark)

        if self.replication_method == "INCREMENTAL":
            for item in res:
                try:
                    if self.is_bookmark_old(state, item[self.replication_key]):
                        self.update_bookmark(state, item[self.replication_key])
                        yield (self.stream, item)

                except KeyError:
                    logger.info('Bookmark doesn\'t exist: syncing row.')
                    yield (self.stream, item)
                    pass

                except Exception as e:
                    logger.error('Handled exception: {error}'.format(error=str(e)))
                    pass

        elif self.replication_method == "FULL_TABLE":
            for item in res:
                yield (self.stream, item)

        else:
            raise Exception('Replication key not defined for {stream}'.format(self.name))



class Booking(Stream):
    name = "booking"
    replication_method = "FULL_TABLE"
    key_properties = [ "onlineBookingsId" ]


class BookingAvailability(Stream):
    name = "booking_availability"
    replication_method = "FULL_TABLE"
    key_properties = ["heatId"]


class CheckDetails(Stream):
    name = "check_details"
    replication_method = "INCREMENTAL"
    replication_key = "createdDate"
    key_properties = [ "checkDetailId" ]


class Checks(Stream):
    name = "checks"
    replication_method = "INCREMENTAL"
    replication_key = "closedDate"
    key_properties = [ "checkId" ]


class CheckTotals(Stream):
    name = "check_totals"
    replication_method = "INCREMENTAL"
    replication_key = "closedDate"
    key_properties = [ "checkId" ]


class Customers(Stream):
    name = "customers"
    replication_method = "INCREMENTAL"
    replication_key = "lastVisited"
    key_properties = [ "customerId" ]


class DiscountTypes(Stream):
    name = "discount_types"
    replication_method = "FULL_TABLE"
    key_properties = ["discountId"]


class EventHeatDetails(Stream):
    name = "event_heat_details"
    replication_method = "INCREMENTAL"
    replication_key = "added" 
    key_properties = [ "eventId" ]


class EventHeatTypes(Stream):
    name = "event_heat_types"
    replication_method = "FULL_TABLE"
    key_properties = ["eventHeatTypeId"]


class EventReservationLinks(Stream): 
    name = "event_reservation_links"
    replication_method = "FULL_TABLE"
    key_properties = ["eventReservationLinkId"]


class EventReservations(Stream):
    name = "event_reservations"
    replication_method = "INCREMENTAL"
    replication_key = "startTime"
    key_properties = [ "eventReservationId" ]


class EventReservationTypes(Stream):
    name = "event_reservation_types"
    replication_method = "FULL_TABLE"
    key_properties = ["eventReservationTypeId"]


class EventRounds(Stream):
    name = "event_rounds"
    replication_method = "FULL_TABLE"
    key_properties = ["eventRoundId"]


class Events(Stream):
    name = "events"
    replication_method = "INCREMENTAL"
    replication_key = "eventScheduledTime"
    key_properties = [ "eventId" ]


class EventStatuses(Stream):
    name = "event_statuses"
    replication_method = "FULL_TABLE"
    key_properties = ["eventStatusId"]


class EventTasks(Stream):
    name = "event_tasks"
    replication_method = "INCREMENTAL"
    replication_key = "completedAt"
    key_properties = [ "eventTaskId" ]


class EventTaskTypes(Stream):
    name = "event_task_types"
    replication_method = "FULL_TABLE"
    key_properties = [ "eventTaskId" ]


class EventTypes(Stream):
    name = "event_types"
    replication_method = "FULL_TABLE"
    key_properties = [ "eventTypeId" ]


class GiftCardHistory(Stream):
    name = "gift_card_history"
    replication_method = "INCREMENTAL"
    replication_key = "transactionDate"
    key_properties = [ "giftCardHistoryId" ]


class HeatMain(Stream):
    name = "heat_main"
    replication_method = "INCREMENTAL"
    replication_key = "finish"
    key_properties = [ "heatId" ]


#
# This table uses heat_main's bookmark as it's bookmark,
# but to allow this to work, we give the replication_key
# an intentional "None".
#

class HeatMainDetails(Stream):
    name = "heat_main_details"
    replication_method = "INCREMENTAL"
    replication_key = "None"
    key_properties = [ "heatId" ]


class HeatTypes(Stream):
    name = "heat_types"
    replication_method = "FULL_TABLE"
    key_properties = ["heatTypesId"]


class Memberships(Stream):
    name = "memberships"
    replication_method = "INCREMENTAL"
    replication_key = "changed"
    key_properties = [ "membershipTypeId" ]


class MembershipTypes(Stream):
    name = "membership_types"
    replication_method = "FULL_TABLE"
    key_properties = ["membershipTypeId"]


class Payments(Stream):
    name = "payments"
    replication_method = "INCREMENTAL"
    replication_key = "payDate"
    key_properties = [ "paymentId" ]


class PaymentsVoided(Stream):
    name = "payments_voided"
    replication_method = "INCREMENTAL"
    replication_key = "voidDate"
    key_properties = [ "paymentId" ]


class ProductClasses(Stream):
    name = "product_classes"
    replication_method = "FULL_TABLE"
    key_properties = ["productClassId"]


class Products(Stream):
    name = "products"
    replication_method = "FULL_TABLE"
    key_properties = ["productId"]


class Reservations(Stream):
    name = "reservations"
    replication_method = "INCREMENTAL"
    replication_key = "createdAt"
    key_properties = [ "onlineBookingReservationsId" ]


class Sources(Stream):
    name = "sources"
    replication_method = "FULL_TABLE"
    key_properties = ["sourceId"]


class Taxes(Stream):
    name = "taxes"
    replication_method = "FULL_TABLE"
    key_properties = ["taxId"]


class Users(Stream):
    name = "users"
    replication_method = "FULL_TABLE"
    key_properties = ["userId"]



STREAMS = {
    "booking": Booking,
    "booking_availability": BookingAvailability,
    "check_details": CheckDetails,
    "checks": Checks,
    "customers": Customers,
    "discount_types": DiscountTypes,
    "event_heat_details": EventHeatDetails,
    "event_heat_types": EventHeatTypes,
    "event_reservation_links": EventReservationLinks,
    "event_reservations": EventReservations,
    "event_reservation_types": EventReservationTypes,
    "event_rounds": EventRounds,
    "events": Events,
    "event_statuses": EventStatuses,
    "event_tasks": EventTasks,
    "event_task_types": EventTaskTypes,
    "event_types": EventTypes,
    "gift_card_history": GiftCardHistory,
    "heat_main": HeatMain,
    "heat_main_details": HeatMainDetails,
    "heat_types": HeatTypes,
    "memberships": Memberships,
    "membership_types": MembershipTypes,
    "payments": Payments,
    "payments_voided": PaymentsVoided,
    "product_classes": ProductClasses,
    "products": Products,
    "reservations": Reservations,
    "sources": Sources,
    "taxes": Taxes,
    "users": Users
}
